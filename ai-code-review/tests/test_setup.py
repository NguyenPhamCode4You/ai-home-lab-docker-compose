#!/usr/bin/env python3
"""
Test script to verify the AI Code Review Tool setup
"""

import os
import sys
import requests
from dotenv import load_dotenv


def test_env_file():
    """Test if .env file exists and contains required variables"""
    print("Testing .env file...")
    
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    if not os.path.exists(env_path):
        print("❌ .env file not found")
        return False
    
    load_dotenv(env_path)
    
    required_vars = ['GITLAB_URL', 'GITLAB_PAT', 'OLLAMA_URL', 'OLLAMA_MODEL']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ .env file configured correctly")
    return True


def test_gitlab_connection():
    """Test GitLab API connection"""
    print("Testing GitLab connection...")
    
    gitlab_url = os.getenv('GITLAB_URL')
    gitlab_pat = os.getenv('GITLAB_PAT')
    
    if not gitlab_url or not gitlab_pat:
        print("❌ GitLab configuration missing")
        return False
    
    try:
        headers = {'Authorization': f'Bearer {gitlab_pat}'}
        url = f"{gitlab_url.rstrip('/')}/api/v4/user"
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ GitLab connection successful - User: {user_data.get('name', 'Unknown')}")
            return True
        else:
            print(f"❌ GitLab API error: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ GitLab connection failed: {str(e)}")
        return False


def test_ollama_connection():
    """Test Ollama API connection"""
    print("Testing Ollama connection...")
    
    ollama_url = os.getenv('OLLAMA_URL')
    ollama_model = os.getenv('OLLAMA_MODEL')
    
    if not ollama_url or not ollama_model:
        print("❌ Ollama configuration missing")
        return False
    
    try:
        # Test if Ollama is running
        url = f"{ollama_url.rstrip('/')}/api/tags"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            models = response.json().get('models', [])
            model_names = [model['name'] for model in models]
            
            if ollama_model in model_names:
                print(f"✅ Ollama connection successful - Model '{ollama_model}' available")
                return True
            else:
                print(f"❌ Model '{ollama_model}' not found. Available models: {', '.join(model_names)}")
                print(f"Run: ollama pull {ollama_model}")
                return False
        else:
            print(f"❌ Ollama API error: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama connection failed: {str(e)}")
        print("Make sure Ollama is running: ollama serve")
        return False


def test_dependencies():
    """Test if required Python packages are installed"""
    print("Testing Python dependencies...")
    
    required_packages = ['requests', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages installed")
    return True


def main():
    """Run all tests"""
    print("🔍 AI Code Review Tool - Setup Test")
    print("=" * 50)
    
    tests = [
        test_dependencies,
        test_env_file,
        test_gitlab_connection,
        test_ollama_connection
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with error: {str(e)}")
            results.append(False)
        print()
    
    print("=" * 50)
    if all(results):
        print("🎉 All tests passed! The AI Code Review Tool is ready to use.")
        print("\nUsage: python run.py <merge_request_id>")
    else:
        print("❌ Some tests failed. Please fix the issues above before using the tool.")
        sys.exit(1)


if __name__ == '__main__':
    main()
