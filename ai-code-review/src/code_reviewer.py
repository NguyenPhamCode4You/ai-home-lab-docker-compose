"""
Main code reviewer orchestrator
"""

import asyncio
import os
import requests
from typing import Dict

from gitlab_api import GitLabAPI
from ollama_api import OllamaAPI
from utils import (
    load_guidelines, 
    extract_project_and_mr, 
    format_changes_for_review, 
    get_user_info, 
    get_current_timestamp
)


class CodeReviewer:
    """Main code review orchestrator"""
    
    def __init__(self, config: Dict[str, str]):
        self.gitlab = GitLabAPI(config['GITLAB_URL'], config['GITLAB_PAT'])
        self.ollama = OllamaAPI(config['OLLAMA_URL'], config['OLLAMA_MODEL'], int(config['OLLAMA_NUM_CTX']))
        self.reviewer_name = config.get('REVIEWER_NAME', 'AI Code Reviewer')
        self.reviewer_email = config.get('REVIEWER_EMAIL', 'ai-reviewer@example.com')
        self.default_guidelines = load_guidelines()
        self.checklist_guidelines = self._load_checklist_guidelines()
    
    def _load_checklist_guidelines(self) -> str:
        """Load checklist guidelines from file"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            guidelines_path = os.path.join(current_dir, "checklist_guidelines.txt")
            
            with open(guidelines_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"❌ Checklist guidelines file not found: {guidelines_path}")
            return ""
        except Exception as e:
            print(f"❌ Error loading checklist guidelines: {str(e)}")
            return ""
    
    def _perform_review(self, mr_input: str, guidelines: str, review_type: str = "review") -> bool:
        """Core method to perform review with specified guidelines and type"""
        try:
            # Parse input
            project_id, mr_iid = extract_project_and_mr(mr_input)
            print(f"Starting {review_type} for MR {mr_iid} in project {project_id}...")
            
            # Get MR data
            print("Fetching merge request details...")
            mr_data = self.gitlab.get_merge_request(project_id, mr_iid)
            
            # Get MR changes
            print("Fetching merge request changes...")
            changes_data = self.gitlab.get_merge_request_changes(project_id, mr_iid)
            
            # Extract user info
            user_info = get_user_info(mr_data)
            print(f"Author: {user_info['author']['name']} ({user_info['author']['email']})")
            if user_info['reviewer']:
                print(f"Reviewer: {user_info['reviewer']['name']} ({user_info['reviewer']['email']})")
            else:
                print("No reviewer assigned")
            
            # Format changes for AI review
            print("Preparing code for AI review...")
            formatted_changes = format_changes_for_review(changes_data)
            
            # Get AI review
            print(f"Generating AI {review_type}...")
            ai_review = self._run_async_review(formatted_changes, guidelines)
            
            # Format final review comment
            review_icon = "📋" if review_type == "checklist" else "🤖"
            review_title = f"## {review_icon} AI Code {'Checklist' if review_type == 'checklist' else 'Check'} by {self.reviewer_name}\n\n"
            
            review_comment = review_title
            review_comment += f"**Reviewed by:** {self.reviewer_name} ({self.reviewer_email})\n"
            review_comment += f"**Review Date:** {get_current_timestamp()}\n"
            review_comment += f"**Review Type:** {'Checklist Review' if review_type == 'checklist' else 'Standard Review'}\n\n"
            review_comment += ai_review
            review_comment += "\n\n---\n*This review was generated automatically by AI. Please use your judgment and verify the suggestions.*"
            
            print(f"✅ {review_type.capitalize()} completed successfully!")
            return True
            
        except requests.exceptions.RequestException as e:
            print(f"❌ GitLab API Error: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return False
    
    def review_merge_request(self, mr_input: str, custom_guidelines: str = None) -> bool:
        """Main method to review a merge request with standard guidelines"""
        # Use custom guidelines if provided, otherwise use default
        guidelines = custom_guidelines if custom_guidelines else self.default_guidelines
        return self._perform_review(mr_input, guidelines, "review")
    
    def checklist_merge_request(self, mr_input: str) -> bool:
        """Main method to review a merge request using checklist guidelines"""
        if not self.checklist_guidelines:
            print("❌ Checklist guidelines not available")
            return False
        
        return self._perform_review(mr_input, self.checklist_guidelines, "checklist")
    
    def _run_async_review(self, content: str, guidelines: str) -> str:
        """Helper method to run the async review generation"""
        return asyncio.run(self.ollama.generate_review(content, guidelines))