@echo off
echo Setting up AI Code Review Tool...
echo.

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Edit the .env file with your GitLab URL and Personal Access Token
echo 2. Ensure Ollama is running with a suitable model
echo 3. Run: python run.py ^<merge_request_id^>
echo.
pause
