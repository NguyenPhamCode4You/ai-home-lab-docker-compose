#!/usr/bin/env python3
"""
READ-ONLY Confluence Connection Test

⚠️  SAFETY NOTICE: This script is READ-ONLY ⚠️
- This script ONLY reads data from Confluence for testing
- It does NOT write, modify, or delete any content in Confluence
- It only tests connectivity and displays basic information
- Your Confluence space remains completely unchanged

Test script to verify Confluence connection and basic functionality.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_confluence_connection():
    """Test the READ-ONLY connection to Confluence API."""
    confluence_url = os.getenv('CONFLUENCE_URL')
    token = os.getenv('CONFLUENCE_TOKEN')
    username = os.getenv('CONFLUENCE_USERNAME')
    space_key = os.getenv('CONFLUENCE_SPACE_KEY')
    
    if not all([confluence_url, token, username, space_key]):
        print("❌ Missing configuration. Please check your .env file.")
        return False
    
    print("🔒 READ-ONLY Connection Test")
    print(f"Testing connection to: {confluence_url}")
    print(f"Username: {username}")
    print(f"Space: {space_key}")
    print("(This test will NOT modify any data)")
    print()
    
    # Test API connection with READ-ONLY request
    api_url = f"{confluence_url}/wiki/rest/api/space/{space_key}"
    
    try:
        # Only GET request for safety
        response = requests.get(
            api_url,
            auth=(username, token),
            timeout=10
        )
        
        if response.status_code == 200:
            space_info = response.json()
            print(f"✅ Connection successful!")
            print(f"Space Name: {space_info.get('name', 'N/A')}")
            print(f"Space Key: {space_info.get('key', 'N/A')}")
            return True
        else:
            print(f"❌ Connection failed. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {str(e)}")
        return False

def test_page_fetch():
    """Test fetching a few pages from the space (READ-ONLY)."""
    confluence_url = os.getenv('CONFLUENCE_URL')
    token = os.getenv('CONFLUENCE_TOKEN')
    username = os.getenv('CONFLUENCE_USERNAME')
    space_key = os.getenv('CONFLUENCE_SPACE_KEY')
    
    api_url = f"{confluence_url}/wiki/rest/api/content"
    params = {
        'spaceKey': space_key,
        'limit': 5,
        'expand': 'body.storage'
    }
    
    try:
        # Only GET request for safety
        response = requests.get(
            api_url,
            auth=(username, token),
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            pages = data.get('results', [])
            
            print(f"✅ Successfully fetched {len(pages)} pages")
            for page in pages:
                print(f"  - {page['title']} (ID: {page['id']})")
            return True
        else:
            print(f"❌ Failed to fetch pages. Status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching pages: {str(e)}")
        return False

def main():
    """Run all READ-ONLY tests."""
    print("🔒 Confluence Exporter - READ-ONLY Connection Test")
    print("=" * 50)
    print("⚠️  This test will NOT modify your Confluence space")
    print("   - Only reads data for testing connectivity")
    print("   - Your Confluence data remains unchanged")
    print("=" * 50)
    print()
    
    # Test connection
    if not test_confluence_connection():
        return 1
    
    print()
    
    # Test page fetching
    if not test_page_fetch():
        return 1
    
    print()
    print("✅ All READ-ONLY tests passed! You can now run the main exporter.")
    print("🔒 Remember: The exporters are READ-ONLY and won't modify your Confluence space.")
    return 0

if __name__ == "__main__":
    exit(main())
