"""
Configuration management for AI Code Review Tool
"""

import os
from typing import Dict
from dotenv import load_dotenv


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
