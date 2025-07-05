"""
GitLab API client for handling merge request operations
"""

import requests
from typing import Dict, Any


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
