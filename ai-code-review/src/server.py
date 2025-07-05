"""
FastAPI server for AI Code Review Tool
"""

import asyncio
import logging
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

from code_reviewer import CodeReviewer
from config import load_config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Code Review API",
    description="API for generating AI-powered code reviews for GitLab merge requests",
    version="1.0.0"
)

# Global code reviewer instance
code_reviewer = None

# Response models
class ReviewResponse(BaseModel):
    success: bool
    review_content: Optional[str] = None
    post_review_to_gitlab: bool = False
    message: str
    merge_request_url: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    message: str

@app.on_event("startup")
async def startup_event():
    """Initialize the code reviewer on startup"""
    global code_reviewer
    try:
        config = load_config()
        code_reviewer = CodeReviewer(config)
        logger.info("✅ Code reviewer initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize code reviewer: {str(e)}")
        raise

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="AI Code Review API is running"
    )

@app.get("/review", response_model=ReviewResponse)
async def review_merge_request(
    project_id: str = Query(..., description="GitLab project ID"),
    mr_id: str = Query(..., description="Merge request ID/IID"),
    post_review_to_gitlab: bool = Query(False, description="Whether to post the review as a comment to GitLab")
):
    """
    Generate AI code review for a GitLab merge request
    
    Args:
        project_id: GitLab project ID
        mr_id: Merge request ID/IID
        post_review_to_gitlab: If True, posts the review as a comment to GitLab
    
    Returns:
        ReviewResponse with the generated review content and status
    """
    if not code_reviewer:
        raise HTTPException(status_code=500, detail="Code reviewer not initialized")
    
    try:
        # Construct MR input string
        mr_input = f"{project_id}/{mr_id}"
        
        logger.info(f"🔍 Starting review for MR {mr_input}")
        
        # Parse input and get MR data
        from utils import extract_project_and_mr
        parsed_project_id, mr_iid = extract_project_and_mr(mr_input)
        
        logger.info(f"📥 Fetching MR data for project {parsed_project_id}, MR {mr_iid}")
        
        # Get MR data
        mr_data = code_reviewer.gitlab.get_merge_request(parsed_project_id, mr_iid)
        
        # Get MR changes
        logger.info("📄 Fetching merge request changes...")
        changes_data = code_reviewer.gitlab.get_merge_request_changes(parsed_project_id, mr_iid)
        
        # Extract user info
        from utils import get_user_info, format_changes_for_review, get_current_timestamp
        user_info = get_user_info(mr_data)
        
        logger.info(f"👤 Author: {user_info['author']['name']} ({user_info['author']['email']})")
        if user_info['reviewer']:
            logger.info(f"👨‍💼 Reviewer: {user_info['reviewer']['name']} ({user_info['reviewer']['email']})")
        
        # Format changes for AI review
        logger.info("🤖 Preparing code for AI review...")
        formatted_changes = format_changes_for_review(changes_data)
        
        # Generate AI review
        logger.info("🧠 Generating AI review...")
        ai_review = await code_reviewer.ollama.generate_review(formatted_changes, code_reviewer.guidelines)
        
        # Format final review comment
        review_content = f"## 🤖 AI Code Review by {code_reviewer.reviewer_name}\n\n"
        review_content += f"**Reviewed by:** {code_reviewer.reviewer_name} ({code_reviewer.reviewer_email})\n"
        review_content += f"**Review Date:** {get_current_timestamp()}\n\n"
        review_content += ai_review
        review_content += "\n\n---\n*This review was generated automatically by AI. Please use your judgment and verify the suggestions.*"
        
        posted_to_gitlab = False
        merge_request_url = f"{code_reviewer.gitlab.gitlab_url}/-/merge_requests/{mr_iid}"
        
        # Post review if requested
        if post_review_to_gitlab:
            logger.info("📝 Posting review to GitLab...")
            code_reviewer.gitlab.post_merge_request_note(parsed_project_id, mr_iid, review_content)
            posted_to_gitlab = True
            logger.info("✅ Review posted to GitLab successfully!")
        
        return ReviewResponse(
            success=True,
            review_content=review_content,
            post_review_to_gitlab=posted_to_gitlab,
            message="Code review generated successfully" + (" and posted to GitLab" if posted_to_gitlab else ""),
            merge_request_url=merge_request_url
        )
        
    except ValueError as e:
        logger.error(f"❌ Input validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        logger.error(f"❌ Error during review: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate review: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Code Review API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "review": "/review",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
