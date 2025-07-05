#!/usr/bin/env python3
"""
AI Code Review Tool for GitLab
This script automates code review by fetching merge request changes from GitLab,
analyzing them with Ollama AI, and posting the review as comments.
"""

import sys
import argparse

from config import load_config
from code_reviewer import CodeReviewer


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='AI Code Review Tool for GitLab')
    parser.add_argument('mr_input', help='Merge Request ID or Project_ID/MR_ID format')
    parser.add_argument('--config', help='Path to .env config file', default='.env')
    parser.add_argument('--guidelines', help='Custom review guidelines text', default=None)
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = load_config()
        
        # Create reviewer instance
        reviewer = CodeReviewer(config)
        
        # Perform review with custom guidelines if provided
        success = reviewer.review_merge_request(args.mr_input, args.guidelines)
        
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
