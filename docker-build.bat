@echo off
REM Build and test Docker image locally before deploying to Render

echo Building Resume ATS Docker Image...
echo ======================================

docker build -t resume-ats-service:latest .

if %ERRORLEVEL% EQU 0 (
    echo Build successful!
    echo.
    echo To run locally:
    echo   docker run -p 8002:8002 --env-file .env resume-ats-service:latest
    echo.
    echo To test:
    echo   curl http://localhost:8002/health
    echo.
    echo To push to Render:
    echo   1. Push code to GitHub
    echo   2. Connect repository in Render Dashboard
    echo   3. Render will build and deploy automatically
) else (
    echo Build failed!
    exit /b 1
)
