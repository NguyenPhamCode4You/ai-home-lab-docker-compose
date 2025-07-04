"""
AI Code Review Tool for GitLab

A modular tool for automated code review using GitLab API and Ollama AI.
"""

from .config import load_config
from .gitlab_api import GitLabAPI
from .ollama_api import OllamaAPI
from .code_reviewer import CodeReviewer
from .utils import (
    load_guidelines,
    extract_project_and_mr,
    format_changes_for_review,
    get_user_info,
    get_current_timestamp
)

__version__ = "1.0.0"
__all__ = [
    "load_config",
    "GitLabAPI", 
    "OllamaAPI",
    "CodeReviewer",
    "load_guidelines",
    "extract_project_and_mr",
    "format_changes_for_review",
    "get_user_info",
    "get_current_timestamp"
]
