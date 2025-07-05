"""
Main code reviewer orchestrator
"""

import asyncio
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
    
    def review_merge_request(self, mr_input: str, custom_guidelines: str = None) -> bool:
        """Main method to review a merge request"""
        try:
            # Use custom guidelines if provided, otherwise use default
            guidelines = custom_guidelines if custom_guidelines else self.default_guidelines
            
            # Parse input
            project_id, mr_iid = extract_project_and_mr(mr_input)
            print(f"Reviewing MR {mr_iid} in project {project_id}...")
            
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
            
            # Get AI review (guidelines will be added automatically with content length check)
            print("Generating AI review...")
            ai_review = self._run_async_review(formatted_changes, guidelines)
            
            # Format final review comment
            review_comment = f"## 🤖 AI Code Review by {self.reviewer_name}\n\n"
            review_comment += f"**Reviewed by:** {self.reviewer_name} ({self.reviewer_email})\n"
            review_comment += f"**Review Date:** {get_current_timestamp()}\n\n"
            review_comment += ai_review
            review_comment += "\n\n---\n*This review was generated automatically by AI. Please use your judgment and verify the suggestions.*"
            
            # # Post review
            # print("Posting review to GitLab...")
            # self.gitlab.post_merge_request_note(project_id, mr_iid, review_comment)
            
            # print("✅ Code review completed successfully!")
            # print(f"Review posted to: {self.gitlab.gitlab_url}/merge_requests/{mr_iid}")
            
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
