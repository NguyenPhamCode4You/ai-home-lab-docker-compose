#!/usr/bin/env python3
"""
AI Code Review Tool for GitLab
This script automates code review by fetching merge request changes from GitLab,
analyzing them with Ollama AI, and posting the review as comments.
"""

import os
import sys
import argparse
import requests
import json
import asyncio
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
import httpx


class GitLabAPI:
    """Handle GitLab API interactions"""
    
    def __init__(self, gitlab_url: str, access_token: str):
        self.gitlab_url = gitlab_url.rstrip('/')
        self.access_token = access_token
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    
    def get_merge_request(self, project_id: str, mr_iid: str) -> Dict[str, Any]:
        """Get merge request details"""
        url = f"{self.gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_merge_request_changes(self, project_id: str, mr_iid: str) -> Dict[str, Any]:
        """Get merge request changes/diffs"""
        url = f"{self.gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/changes"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def post_merge_request_note(self, project_id: str, mr_iid: str, note: str) -> Dict[str, Any]:
        """Post a note/comment to merge request"""
        url = f"{self.gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/notes"
        data = {'body': note}
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Get user details by ID"""
        url = f"{self.gitlab_url}/api/v4/users/{user_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()


class OllamaAPI:
    """Handle Ollama AI interactions"""
    
    def __init__(self, ollama_url: str, model: str, num_ctx: int = 6122):
        self.ollama_url = ollama_url.rstrip('/')
        self.model = model
        self.num_ctx = num_ctx  # Configurable context window
        self.max_content_tokens = int(self.num_ctx * 0.8)  # Reserve 20% for response and overhead
    
    async def stream(self, prompt: str):
        if not self.ollama_url or not self.model:
            raise ValueError("URL and model must be set before using the assistant.")
        async with httpx.AsyncClient(timeout=httpx.Timeout(80.0)) as client:
            async with client.stream("POST", f"{self.ollama_url}/api/generate", json={"model": self.model, "prompt": prompt, "options": {"num_ctx": self.num_ctx}}) as response:
                async for chunk in response.aiter_bytes():
                    if (len(chunk) > 1000):
                        continue
                    try:
                        response = json.loads(chunk).get("response", "")
                        yield response
                    except Exception as e:
                        print(f"Error decoding chunk: {e}")
                        continue
    
    async def generate_review(self, content: str, guidelines: str) -> str:
        """Generate a complete review by collecting all streaming chunks"""
        # Prepare content with guidelines, truncating if necessary
        prepared_prompt = self._prepare_content_for_review(content, guidelines)
        
        output = ''
        print("🤖 AI is generating review...")
        
        async for chunk in self.stream(prepared_prompt):
            if chunk:
                output += chunk
                print(chunk, end='', flush=True)  # Print chunk to console in real-time
        
        print("\n🤖 Review generation completed!")
        return output
    
    def _prepare_content_for_review(self, content: str, guidelines: str) -> str:
        """Prepare content for review, truncating if necessary to fit context window"""
        guidelines_tokens = self._estimate_tokens(guidelines)
        content_tokens = self._estimate_tokens(content)
        total_tokens = guidelines_tokens + content_tokens
        
        if total_tokens <= self.max_content_tokens:
            # Content fits, return as-is with guidelines at the end
            return f"{content}\n\n{guidelines}"
        
        # Content too large, need to truncate
        available_content_tokens = self.max_content_tokens - guidelines_tokens
        target_char_count = available_content_tokens * 4  # Convert back to characters
        
        if target_char_count <= 0:
            raise ValueError("Guidelines are too long to fit in context window")
        
        # Truncate content and add indication of truncation
        truncated_content = content[:target_char_count]
        
        # Try to truncate at a reasonable boundary (end of line)
        last_newline = truncated_content.rfind('\n')
        if last_newline > target_char_count * 0.8:  # If we can find a newline in the last 20%
            truncated_content = truncated_content[:last_newline]
        
        print(f"⚠️  Content truncated due to context window limits. Original: {content_tokens} tokens, Truncated: {self._estimate_tokens(truncated_content)} tokens")
        
        # Add truncation notice and guidelines
        result = f"{truncated_content}\n\n[... Content truncated due to length ...]\n\n{guidelines}"
        return result
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate the number of tokens in a text string"""
        # Rough estimate: 4 characters per token on average
        return len(text) // 4


class CodeReviewer:
    """Main code review orchestrator"""
    
    def __init__(self, config: Dict[str, str]):
        self.gitlab = GitLabAPI(config['GITLAB_URL'], config['GITLAB_PAT'])
        self.ollama = OllamaAPI(config['OLLAMA_URL'], config['OLLAMA_MODEL'], int(config['OLLAMA_NUM_CTX']))
        self.reviewer_name = config.get('REVIEWER_NAME', 'AI Code Reviewer')
        self.reviewer_email = config.get('REVIEWER_EMAIL', 'ai-reviewer@example.com')
        self.guidelines = self._load_guidelines()
    
    def _load_guidelines(self) -> str:
        """Load code review guidelines from file"""
        guidelines_path = os.path.join(os.path.dirname(__file__), 'review_guidelines.txt')
        try:
            with open(guidelines_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return "Please review this code for quality, bugs, and best practices."
    
    def _extract_project_and_mr(self, mr_input: str) -> tuple[str, str]:
        """Extract project ID and MR IID from input"""
        if '/' in mr_input:
            # Format: project_id/mr_iid
            parts = mr_input.split('/')
            if len(parts) == 2:
                return parts[0], parts[1]
        
        # Assume it's just MR IID and ask for project ID
        project_id = input("Please enter the project ID: ").strip()
        return project_id, mr_input
    
    def _format_changes_for_review(self, changes: Dict[str, Any]) -> str:
        """Format the changes data for AI review"""
        review_text = "# Code Changes for Review\n\n"
        
        # Add MR basic info
        mr_info = changes
        review_text += f"**Title:** {mr_info.get('title', 'N/A')}\n"
        review_text += f"**Description:** {mr_info.get('description', 'N/A')}\n"
        review_text += f"**Source Branch:** {mr_info.get('source_branch', 'N/A')}\n"
        review_text += f"**Target Branch:** {mr_info.get('target_branch', 'N/A')}\n\n"
        
        # Add file changes
        review_text += "## Changed Files\n\n"
        for change in changes.get('changes', []):
            file_path = change.get('new_path', change.get('old_path', 'unknown'))
            review_text += f"### File: {file_path}\n\n"
            
            if change.get('diff'):
                review_text += "```diff\n"
                review_text += change['diff']
                review_text += "\n```\n\n"
        
        return review_text
    
    def _get_user_info(self, mr_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract user information from MR data"""
        user_info = {}
        
        # Author info
        author = mr_data.get('author', {})
        user_info['author'] = {
            'username': author.get('username', 'unknown'),
            'email': author.get('email', 'unknown'),
            'name': author.get('name', 'unknown')
        }
        
        # Assignee info (reviewer)
        assignee = mr_data.get('assignee')
        if assignee:
            user_info['reviewer'] = {
                'username': assignee.get('username', 'unknown'),
                'email': assignee.get('email', 'unknown'),
                'name': assignee.get('name', 'unknown')
            }
        else:
            user_info['reviewer'] = None
        
        return user_info
    
    def review_merge_request(self, mr_input: str) -> bool:
        """Main method to review a merge request"""
        try:
            # Parse input
            project_id, mr_iid = self._extract_project_and_mr(mr_input)
            print(f"Reviewing MR {mr_iid} in project {project_id}...")
            
            # Get MR data
            print("Fetching merge request details...")
            mr_data = self.gitlab.get_merge_request(project_id, mr_iid)
            
            # Get MR changes
            print("Fetching merge request changes...")
            changes_data = self.gitlab.get_merge_request_changes(project_id, mr_iid)
            
            # Extract user info
            user_info = self._get_user_info(mr_data)
            print(f"Author: {user_info['author']['name']} ({user_info['author']['email']})")
            if user_info['reviewer']:
                print(f"Reviewer: {user_info['reviewer']['name']} ({user_info['reviewer']['email']})")
            else:
                print("No reviewer assigned")
            
            # Format changes for AI review
            print("Preparing code for AI review...")
            formatted_changes = self._format_changes_for_review(changes_data)
            
            # Get AI review (guidelines will be added automatically with content length check)
            print("Generating AI review...")
            ai_review = self._run_async_review(formatted_changes, self.guidelines)
            
            # Format final review comment
            review_comment = f"## 🤖 AI Code Review by {self.reviewer_name}\n\n"
            review_comment += f"**Reviewed by:** {self.reviewer_name} ({self.reviewer_email})\n"
            review_comment += f"**Review Date:** {self._get_current_timestamp()}\n\n"
            review_comment += ai_review
            review_comment += "\n\n---\n*This review was generated automatically by AI. Please use your judgment and verify the suggestions.*"
            
            # Post review
            print("Posting review to GitLab...")
            self.gitlab.post_merge_request_note(project_id, mr_iid, review_comment)
            
            print("✅ Code review completed successfully!")
            print(f"Review posted to: {self.gitlab.gitlab_url}/merge_requests/{mr_iid}")
            
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ GitLab API Error: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def _run_async_review(self, content: str, guidelines: str) -> str:
        """Helper method to run the async review generation"""
        return asyncio.run(self.ollama.generate_review(content, guidelines))
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp for review"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    


def load_config() -> Dict[str, str]:
    """Load configuration from .env file"""
    # Load .env file
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(env_path)
    
    # Required config
    required_vars = ['GITLAB_URL', 'GITLAB_PAT', 'OLLAMA_URL', 'OLLAMA_MODEL']
    config = {}
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            raise ValueError(f"Missing required environment variable: {var}")
        config[var] = value
    
    # Optional config
    config['REVIEWER_NAME'] = os.getenv('REVIEWER_NAME', 'AI Code Reviewer')
    config['REVIEWER_EMAIL'] = os.getenv('REVIEWER_EMAIL', 'ai-reviewer@example.com')
    config['OLLAMA_NUM_CTX'] = os.getenv('OLLAMA_NUM_CTX', '6122')  # Default context window
    
    return config


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='AI Code Review Tool for GitLab')
    parser.add_argument('mr_input', help='Merge Request ID or Project_ID/MR_ID format')
    parser.add_argument('--config', help='Path to .env config file', default='.env')
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = load_config()
        
        # Create reviewer instance
        reviewer = CodeReviewer(config)
        
        # Perform review
        success = reviewer.review_merge_request(args.mr_input)
        
        sys.exit(0 if success else 1)
        
    except ValueError as e:
        print(f"❌ Configuration Error: {str(e)}")
        print("Please check your .env file and ensure all required variables are set.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Review cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
