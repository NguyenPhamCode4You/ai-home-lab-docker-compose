import asyncio

from .agents.Task import Task
from .agents.CodeReviewer import CodeReviewer
from .agents.models.Ollama import Ollama
from .agents.tools.GitLabAPI import GitLabAPI

class GitlabCodeReviewer():
    def __init__(self,
            llm_code_reviewer: CodeReviewer = None,
            gitlab_url: str = None,
            gitlab_access_token: str = None,
            reviewer_name: str = "AI Code Reviewer",
            reviewer_email: str = "ai-code-reviewer@c4y.com"
        ):
            self.llm_code_reviewer = llm_code_reviewer or CodeReviewer()
            self.gitlab_api = GitLabAPI(gitlab_url, gitlab_access_token)
            self.reviewer_name = reviewer_name
            self.reviewer_email = reviewer_email

    async def stream(self, context: str = None, question: str = None, conversation_history: list = None):
        """Main method to review a merge request"""

        project_config_string = await Task(
            llm_model=self.llm_code_reviewer.llm_model if self.llm_code_reviewer else Ollama(),
            instruction_template="What is the gitlab project id and merge request id? Return only the result in format project_id/merge_request_id, example is 30/180. User: {question}.",
        ).run(context=context, question=question, conversation_history=conversation_history)
        
        project_id, mr_iid = extract_project_and_mr(project_config_string)
        yield (f"Reviewing MR {mr_iid} in project {project_id}...")
        
        # Get MR data
        yield("Fetching merge request details...")
        mr_data = self.gitlab_api.get_merge_request(project_id, mr_iid)
        
        # Get MR changes
        yield("Fetching merge request changes...")
        changes_data = self.gitlab_api.get_merge_request_changes(project_id, mr_iid)
        
        # Extract user info
        user_info = get_user_info(mr_data)
        yield(f"Author: {user_info['author']['name']} ({user_info['author']['email']})")
        if user_info['reviewer']:
            yield(f"Reviewer: {user_info['reviewer']['name']} ({user_info['reviewer']['email']})")
        else:
            yield("No reviewer assigned")
        
        # Format changes for AI review
        yield("Preparing code for AI review...")
        formatted_changes = format_changes_for_review(changes_data)

        review_comment = ""
        
        # Format final review comment
        review_comment = f"## 🤖 AI Code Review by {self.reviewer_name}\n\n"
        review_comment += f"**Reviewed by:** {self.reviewer_name} ({self.reviewer_email})\n"
        review_comment += f"**Review Date:** {get_current_timestamp()}\n\n"
        yield("🤖 Generating AI review...")

        async for text_chunk in self.llm_code_reviewer.stream(context=formatted_changes, question=question, conversation_history=conversation_history):
            review_comment += text_chunk
            yield text_chunk

        review_comment += "\n\n---\n*This review was generated automatically by AI. Please use your judgment and verify the suggestions.*"

"""
Utility functions for code review processing
"""

import os
from typing import Dict, Any
from datetime import datetime


def load_guidelines() -> str:
    """Load code review guidelines from file"""
    guidelines_path = os.path.join(os.path.dirname(__file__), 'review_guidelines.txt')
    try:
        with open(guidelines_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "Please review this code for quality, bugs, and best practices."


def extract_project_and_mr(mr_input: str) -> tuple[str, str]:
    """Extract project ID and MR IID from input"""
    if '/' in mr_input:
        # Format: project_id/mr_iid
        parts = mr_input.split('/')
        if len(parts) == 2:
            return parts[0], parts[1]
    
    # Assume it's just MR IID and ask for project ID
    project_id = input("Please enter the project ID: ").strip()
    return project_id, mr_input


def format_changes_for_review(changes: Dict[str, Any]) -> str:
    """Format the changes data for AI review with optimized content"""
    review_text = "# Code Changes for Review\n\n"
    
    # Add essential MR info only
    title = changes.get('title', 'N/A')
    description = changes.get('description', '')
    
    review_text += f"**Title:** {title}\n"
    if description and description.strip() and description != 'N/A':
        # Truncate description if too long
        if len(description) > 200:
            description = description[:197] + "..."
        review_text += f"**Description:** {description}\n"
    review_text += f"**Branch:** {changes.get('source_branch', 'N/A')} → {changes.get('target_branch', 'N/A')}\n\n"
    
    # Add file changes with optimizations
    file_changes = changes.get('changes', [])
    if not file_changes:
        return review_text + "No file changes found.\n"
    
    review_text += f"## Files Changed ({len(file_changes)})\n\n"
    
    for change in file_changes:
        file_path = change.get('new_path', change.get('old_path', 'unknown'))
        file_name = file_path.split('/')[-1] if '/' in file_path else file_path
        
        # Include file extension for context
        review_text += f"### {file_name} ({file_path})\n"
        
        diff_content = change.get('diff', '')
        if diff_content:
            # Auto-truncate diff if > 200 characters
            if len(diff_content) > 200:
                # Try to keep complete lines when truncating
                lines = diff_content.split('\n')
                truncated_lines = []
                char_count = 0
                
                for line in lines:
                    if char_count + len(line) + 1 <= 200:  # +1 for newline
                        truncated_lines.append(line)
                        char_count += len(line) + 1
                    else:
                        break
                
                diff_content = '\n'.join(truncated_lines)
                if len(lines) > len(truncated_lines):
                    diff_content += f"\n... ({len(lines) - len(truncated_lines)} more lines truncated)"
            
            review_text += f"```diff\n{diff_content}\n```\n\n"
        else:
            review_text += "*No diff content available*\n\n"
    
    return review_text


def get_user_info(mr_data: Dict[str, Any]) -> Dict[str, Any]:
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


def get_current_timestamp() -> str:
    """Get current timestamp for review"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
