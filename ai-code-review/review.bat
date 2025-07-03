@echo off
setlocal

if "%1"=="" (
    echo Usage: review.bat ^<merge_request_id^>
    echo Example: review.bat 123
    echo Example: review.bat project_id/123
    exit /b 1
)

echo Starting AI Code Review for MR: %1
echo.

python run.py %1

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Review failed. Check the error messages above.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Review completed successfully!
pause
