#!/usr/bin/env python3
"""
GitLab to Azure DevOps Sync Server

This server listens for GitLab webhook events (merge requests, commits)
and automatically syncs the code to an Azure DevOps repository to trigger
build and test pipelines.
"""

import os
import json
import subprocess
import tempfile
import shutil
import logging
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('gitlab_sync.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class GitLabAzureSync:
    def __init__(self):
        # GitLab configuration
        self.gitlab_url = os.getenv('GITLAB_URL')
        self.gitlab_token = os.getenv('GITLAB_ACCESS_TOKEN')
        self.gitlab_project_id = os.getenv('GITLAB_PROJECT_ID')
        
        # Azure DevOps configuration
        self.azure_devops_url = os.getenv('AZURE_DEVOPS_URL')
        self.azure_devops_token = os.getenv('AZURE_DEVOPS_TOKEN')
        self.azure_devops_project = os.getenv('AZURE_DEVOPS_PROJECT')
        self.azure_devops_repo = os.getenv('AZURE_DEVOPS_REPO')
        
        # Local configuration
        self.work_dir = os.getenv('WORK_DIR', './sync_workspace')
        self.webhook_secret = os.getenv('GITLAB_WEBHOOK_SECRET')
        
        # Validate required environment variables
        self._validate_config()
        
        # Ensure work directory exists
        Path(self.work_dir).mkdir(parents=True, exist_ok=True)
    
    def _validate_config(self):
        """Validate that all required environment variables are set"""
        required_vars = [
            'GITLAB_URL', 'GITLAB_ACCESS_TOKEN', 'GITLAB_PROJECT_ID',
            'AZURE_DEVOPS_URL', 'AZURE_DEVOPS_TOKEN', 'AZURE_DEVOPS_PROJECT', 'AZURE_DEVOPS_REPO'
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    def verify_webhook_signature(self, payload, signature):
        """Verify GitLab webhook signature (if secret is configured)"""
        if not self.webhook_secret:
            return True
        
        import hmac
        import hashlib
        
        expected_signature = hmac.new(
            self.webhook_secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(f"sha256={expected_signature}", signature)
    
    def get_gitlab_headers(self):
        """Get headers for GitLab API requests"""
        return {
            'Authorization': f'Bearer {self.gitlab_token}',
            'Content-Type': 'application/json'
        }
    
    def get_commit_details(self, commit_sha):
        """Get commit details from GitLab API"""
        url = f"{self.gitlab_url}/api/v4/projects/{self.gitlab_project_id}/repository/commits/{commit_sha}"
        
        try:
            response = requests.get(url, headers=self.get_gitlab_headers())
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get commit details: {e}")
            return None
    
    def download_gitlab_archive(self, ref):
        """Download archive from GitLab for a specific ref (branch/commit)"""
        url = f"{self.gitlab_url}/api/v4/projects/{self.gitlab_project_id}/repository/archive.zip"
        params = {'sha': ref}
        
        try:
            response = requests.get(url, headers=self.get_gitlab_headers(), params=params, stream=True)
            response.raise_for_status()
            
            # Save to temporary file
            temp_file = os.path.join(self.work_dir, f"gitlab_archive_{ref[:8]}.zip")
            with open(temp_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return temp_file
        except requests.RequestException as e:
            logger.error(f"Failed to download GitLab archive: {e}")
            return None
    
    def extract_archive(self, archive_path, extract_to):
        """Extract zip archive to specified directory"""
        import zipfile
        
        try:
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
            
            # Find the extracted directory (GitLab archives have a project name prefix)
            extracted_dirs = [d for d in os.listdir(extract_to) if os.path.isdir(os.path.join(extract_to, d))]
            if extracted_dirs:
                return os.path.join(extract_to, extracted_dirs[0])
            return extract_to
        except Exception as e:
            logger.error(f"Failed to extract archive: {e}")
            return None
    
    def run_command(self, command, cwd=None):
        """Run shell command and return result"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout, result.stderr
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {command}")
            logger.error(f"Error: {e.stderr}")
            return None, e.stderr
    
    def setup_azure_devops_repo(self, repo_dir):
        """Setup Azure DevOps remote and configure git"""
        azure_remote_url = f"{self.azure_devops_url}/{self.azure_devops_project}/_git/{self.azure_devops_repo}"
        
        # Configure git credentials
        git_config_commands = [
            f'git config user.email "gitlab-sync@automation.local"',
            f'git config user.name "GitLab Sync Bot"',
            f'git remote remove azure 2>nul || true',
            f'git remote add azure https://{self.azure_devops_token}@{azure_remote_url.replace("https://", "")}'
        ]
        
        for command in git_config_commands:
            stdout, stderr = self.run_command(command, cwd=repo_dir)
            if stdout is None and "remove azure" not in command:
                logger.error(f"Git config failed: {command}")
                return False
        
        return True
    
    def push_to_azure_devops(self, repo_dir, branch_name, commit_message):
        """Push code to Azure DevOps repository"""
        try:
            # Add all files
            stdout, stderr = self.run_command("git add .", cwd=repo_dir)
            if stdout is None:
                return False
            
            # Commit changes
            commit_cmd = f'git commit -m "{commit_message}"'
            stdout, stderr = self.run_command(commit_cmd, cwd=repo_dir)
            
            # Push to Azure DevOps
            push_cmd = f"git push azure {branch_name}"
            stdout, stderr = self.run_command(push_cmd, cwd=repo_dir)
            if stdout is None:
                return False
            
            logger.info(f"Successfully pushed to Azure DevOps: {branch_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to push to Azure DevOps: {e}")
            return False
    
    def sync_gitlab_to_azure(self, ref, commit_message, branch_name="main"):
        """Main sync function: download from GitLab and push to Azure DevOps"""
        logger.info(f"Starting sync for ref: {ref}")
        
        # Create temporary directory for this sync operation
        sync_dir = os.path.join(self.work_dir, f"sync_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        try:
            # Download archive from GitLab
            logger.info("Downloading GitLab archive...")
            archive_path = self.download_gitlab_archive(ref)
            if not archive_path:
                return False
            
            # Extract archive
            logger.info("Extracting archive...")
            extracted_dir = self.extract_archive(archive_path, sync_dir)
            if not extracted_dir:
                return False
            
            # Initialize git repo if needed
            if not os.path.exists(os.path.join(extracted_dir, '.git')):
                stdout, stderr = self.run_command("git init", cwd=extracted_dir)
                if stdout is None:
                    return False
            
            # Setup Azure DevOps remote
            logger.info("Setting up Azure DevOps remote...")
            if not self.setup_azure_devops_repo(extracted_dir):
                return False
            
            # Push to Azure DevOps
            logger.info("Pushing to Azure DevOps...")
            success = self.push_to_azure_devops(extracted_dir, branch_name, commit_message)
            
            # Cleanup
            os.remove(archive_path)
            
            return success
            
        except Exception as e:
            logger.error(f"Sync operation failed: {e}")
            return False
        finally:
            # Cleanup sync directory
            if os.path.exists(sync_dir):
                shutil.rmtree(sync_dir, ignore_errors=True)

# Initialize the sync handler
sync_handler = GitLabAzureSync()

@app.route('/webhook/gitlab', methods=['POST'])
def gitlab_webhook():
    """Handle GitLab webhook events"""
    try:
        # Verify webhook signature if configured
        signature = request.headers.get('X-Gitlab-Token')
        if sync_handler.webhook_secret and signature != sync_handler.webhook_secret:
            logger.warning("Invalid webhook signature")
            return jsonify({'error': 'Invalid signature'}), 401
        
        # Parse webhook data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400
        
        event_type = request.headers.get('X-Gitlab-Event')
        logger.info(f"Received GitLab webhook: {event_type}")
        
        # Handle different event types
        if event_type == 'Push Hook':
            return handle_push_event(data)
        elif event_type == 'Merge Request Hook':
            return handle_merge_request_event(data)
        else:
            logger.info(f"Ignoring event type: {event_type}")
            return jsonify({'message': f'Event {event_type} ignored'}), 200
            
    except Exception as e:
        logger.error(f"Webhook handling error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

def handle_push_event(data):
    """Handle GitLab push events"""
    try:
        ref = data.get('ref', '').replace('refs/heads/', '')
        commits = data.get('commits', [])
        
        if not commits:
            return jsonify({'message': 'No commits in push event'}), 200
        
        # Get the latest commit
        latest_commit = commits[-1]
        commit_sha = latest_commit.get('id')
        commit_message = latest_commit.get('message', 'GitLab sync commit')
        
        logger.info(f"Processing push to branch: {ref}, commit: {commit_sha[:8]}")
        
        # Sync to Azure DevOps
        success = sync_handler.sync_gitlab_to_azure(
            ref=commit_sha,
            commit_message=f"GitLab sync: {commit_message}",
            branch_name=ref
        )
        
        if success:
            return jsonify({'message': 'Successfully synced to Azure DevOps'}), 200
        else:
            return jsonify({'error': 'Failed to sync to Azure DevOps'}), 500
            
    except Exception as e:
        logger.error(f"Push event handling error: {e}")
        return jsonify({'error': 'Failed to process push event'}), 500

def handle_merge_request_event(data):
    """Handle GitLab merge request events"""
    try:
        mr_action = data.get('object_attributes', {}).get('action')
        
        # Only process merged merge requests
        if mr_action != 'merge':
            logger.info(f"Ignoring MR action: {mr_action}")
            return jsonify({'message': f'MR action {mr_action} ignored'}), 200
        
        target_branch = data.get('object_attributes', {}).get('target_branch')
        source_branch = data.get('object_attributes', {}).get('source_branch')
        title = data.get('object_attributes', {}).get('title', 'Merge request')
        
        logger.info(f"Processing merged MR: {source_branch} -> {target_branch}")
        
        # Sync the target branch to Azure DevOps
        success = sync_handler.sync_gitlab_to_azure(
            ref=target_branch,
            commit_message=f"GitLab MR merged: {title}",
            branch_name=target_branch
        )
        
        if success:
            return jsonify({'message': 'Successfully synced MR to Azure DevOps'}), 200
        else:
            return jsonify({'error': 'Failed to sync MR to Azure DevOps'}), 500
            
    except Exception as e:
        logger.error(f"MR event handling error: {e}")
        return jsonify({'error': 'Failed to process MR event'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }), 200

@app.route('/sync/manual', methods=['POST'])
def manual_sync():
    """Manual sync endpoint for testing"""
    try:
        data = request.get_json()
        ref = data.get('ref', 'main')
        message = data.get('message', 'Manual sync')
        branch = data.get('branch', 'main')
        
        success = sync_handler.sync_gitlab_to_azure(
            ref=ref,
            commit_message=message,
            branch_name=branch
        )
        
        if success:
            return jsonify({'message': 'Manual sync completed successfully'}), 200
        else:
            return jsonify({'error': 'Manual sync failed'}), 500
            
    except Exception as e:
        logger.error(f"Manual sync error: {e}")
        return jsonify({'error': 'Manual sync failed'}), 500

if __name__ == '__main__':
    # Validate configuration on startup
    try:
        sync_handler._validate_config()
        logger.info("GitLab to Azure DevOps sync server starting...")
        logger.info(f"Work directory: {sync_handler.work_dir}")
        
        # Start the Flask server
        port = int(os.getenv('PORT', 5000))
        host = os.getenv('HOST', '0.0.0.0')
        
        app.run(host=host, port=port, debug=False)
        
    except Exception as e:
        logger.error(f"Server startup failed: {e}")
        exit(1)