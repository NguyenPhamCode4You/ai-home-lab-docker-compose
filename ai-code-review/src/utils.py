"""
Utility functions for code review processing
"""

import os
from typing import Dict, Any
from datetime import datetime


def load_guidelines(custom_guidelines: str = None) -> str:
    """Load code review guidelines from file or use custom guidelines"""
    if custom_guidelines:
        return custom_guidelines
    
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
        if len(description) > 300:
            description = description[:297] + "..."
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
            # Auto-truncate diff if > 300 characters
            if len(diff_content) > 300:
                # Try to keep complete lines when truncating
                lines = diff_content.split('\n')
                truncated_lines = []
                char_count = 0
                
                for line in lines:
                    if char_count + len(line) + 1 <= 300:  # +1 for newline
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
