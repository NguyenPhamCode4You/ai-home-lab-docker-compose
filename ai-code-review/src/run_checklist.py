#!/usr/bin/env python3
"""
AI Code Review Tool for GitLab - Checklist Review
This script automates checklist-based code review by fetching merge request changes from GitLab,
analyzing them with Ollama AI using structured checklist guidelines, and posting the review as comments.
"""

import sys
import argparse

from config import load_config
from code_reviewer import CodeReviewer


def main():
    """Main entry point for checklist-based code review"""
    parser = argparse.ArgumentParser(description='AI Code Review Tool for GitLab - Checklist Review')
    parser.add_argument('mr_input', help='Merge Request ID or Project_ID/MR_ID format')
    parser.add_argument('--config', help='Path to .env config file', default='.env')
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = load_config()
        
        # Create reviewer instance
        reviewer = CodeReviewer(config)
        
        # Perform checklist-based review
        success = reviewer.checklist_merge_request(args.mr_input)
        
        sys.exit(0 if success else 1)
        
    except ValueError as e:
        print(f"❌ Configuration Error: {str(e)}")
        print("Please check your .env file and ensure all required variables are set.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Checklist review cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()