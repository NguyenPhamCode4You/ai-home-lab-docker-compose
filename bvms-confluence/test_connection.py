#!/usr/bin/env python3
"""
Test script to verify Confluence connection and basic functionality.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_confluence_connection():
    """Test the connection to Confluence API."""
    confluence_url = os.getenv('CONFLUENCE_URL')
    token = os.getenv('CONFLUENCE_TOKEN')
    username = os.getenv('CONFLUENCE_USERNAME')
    space_key = os.getenv('CONFLUENCE_SPACE_KEY')
    
    if not all([confluence_url, token, username, space_key]):
        print("❌ Missing configuration. Please check your .env file.")
        return False
    
    print(f"Testing connection to: {confluence_url}")
    print(f"Username: {username}")
    print(f"Space: {space_key}")
    
    # Test API connection
    api_url = f"{confluence_url}/wiki/rest/api/space/{space_key}"
    
    try:
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
    """Test fetching a few pages from the space."""
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
    """Run all tests."""
    print("Confluence Exporter - Connection Test")
    print("=" * 40)
    
    # Test connection
    if not test_confluence_connection():
        return 1
    
    print()
    
    # Test page fetching
    if not test_page_fetch():
        return 1
    
    print()
    print("✅ All tests passed! You can now run the main exporter.")
    return 0

if __name__ == "__main__":
    exit(main())
