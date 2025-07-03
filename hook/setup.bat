@echo off
echo 🚀 Setting up GitLab to Azure DevOps Sync Server...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9 or later.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Create virtual environment
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat
echo ✅ Virtual environment activated

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo ⚙️  Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please edit .env file with your configuration before running the server
)

REM Create work directory
if not exist "sync_workspace" mkdir sync_workspace

echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file with your GitLab and Azure DevOps configuration
echo 2. Run the server with: python server.py
echo 3. Configure GitLab webhook to point to: http://your-server:5000/webhook/gitlab
echo.
echo For Docker deployment:
echo 1. Edit .env file with your configuration
echo 2. Run: docker-compose up -d
echo.
pause
