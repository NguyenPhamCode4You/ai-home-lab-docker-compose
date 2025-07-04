#!/usr/bin/env python3
"""
AI Code Review Tool for GitLab
This script automates code review by fetching merge request changes from GitLab,
analyzing them with Ollama AI, and posting the review as comments.

This file is maintained for backward compatibility.
The code has been split into multiple modules for better maintainability.
"""

# Import the main function from the new modular structure
from main import main

# Keep the old main entry point for backward compatibility
if __name__ == '__main__':
    main()
