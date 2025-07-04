"""
Test script for AI Code Review FastAPI Server
"""

import requests
import json
from typing import Dict, Any


def test_health_check(base_url: str = "http://localhost:8000") -> bool:
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{base_url}/health")
        response.raise_for_status()
        
        result = response.json()
        print("✅ Health check passed:")
        print(f"   Status: {result['status']}")
        print(f"   Message: {result['message']}")
        return True
        
    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        return False


def test_review_generation(
    project_id: str,
    mr_id: str, 
    should_post: bool = False,
    base_url: str = "http://localhost:8000"
) -> Dict[str, Any]:
    """Test the review generation endpoint"""
    try:
        params = {
            "project_id": project_id,
            "mr_id": mr_id,
            "post_review_to_gitlab": should_post
        }
        
        print(f"🔍 Testing review generation for MR {project_id}/{mr_id}")
        print(f"   Should post to GitLab: {should_post}")
        
        response = requests.get(f"{base_url}/review", params=params)
        response.raise_for_status()
        
        result = response.json()
        
        print("✅ Review generation successful:")
        print(f"   Success: {result['success']}")
        print(f"   Posted to GitLab: {result['post_review_to_gitlab']}")
        print(f"   Message: {result['message']}")
        
        if result.get('merge_request_url'):
            print(f"   MR URL: {result['merge_request_url']}")
        
        # Print first 200 characters of review content
        if result.get('review_content'):
            preview = result['review_content'][:200] + "..." if len(result['review_content']) > 200 else result['review_content']
            print(f"   Review preview: {preview}")
        
        return result
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        try:
            error_detail = e.response.json()
            print(f"   Detail: {error_detail.get('detail', 'No detail available')}")
        except:
            pass
        return {"success": False, "error": str(e)}
        
    except Exception as e:
        print(f"❌ Request failed: {str(e)}")
        return {"success": False, "error": str(e)}


def main():
    """Main test function"""
    print("🧪 AI Code Review API Test Script")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Health check
    print("\n1. Testing health check...")
    health_ok = test_health_check(base_url)
    
    if not health_ok:
        print("❌ Health check failed. Make sure the server is running!")
        return
    
    # Test 2: Get user input for MR details
    print("\n2. Testing review generation...")
    print("Please provide merge request details:")
    
    project_id = input("Enter GitLab project ID: ").strip()
    if not project_id:
        print("❌ Project ID is required")
        return
    
    mr_id = input("Enter merge request ID: ").strip()
    if not mr_id:
        print("❌ Merge request ID is required")
        return
    
    should_post = input("Should post comment to GitLab? (y/N): ").strip().lower() == 'y'
    
    # Test review generation
    result = test_review_generation(project_id, mr_id, should_post, base_url)
    
    if result.get('success'):
        print("\n✅ All tests passed!")
        
        # Option to save review content to file
        if result.get('review_content'):
            save_file = input("\nSave review to file? (y/N): ").strip().lower() == 'y'
            if save_file:
                filename = f"review_{project_id}_{mr_id}.md"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(result['review_content'])
                print(f"📄 Review saved to {filename}")
    else:
        print("\n❌ Tests failed!")


if __name__ == "__main__":
    main()
