@echo off
echo Starting AI Code Review FastAPI Server...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist .env (
    echo Warning: .env file not found!
    echo Please create a .env file with the following variables:
    echo GITLAB_URL=your_gitlab_url
    echo GITLAB_PAT=your_personal_access_token
    echo OLLAMA_URL=your_ollama_url
    echo OLLAMA_MODEL=your_model_name
    echo REVIEWER_NAME=AI Code Reviewer
    echo REVIEWER_EMAIL=ai-reviewer@example.com
    echo OLLAMA_NUM_CTX=6122
    echo.
    pause
    exit /b 1
)

echo.
echo Starting server on http://localhost:8000
echo API Documentation will be available at http://localhost:8000/docs
echo.

REM Start the server
python server.py
