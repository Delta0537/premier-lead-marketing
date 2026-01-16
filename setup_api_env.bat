@echo off
REM ============================================
REM Docker API Environment Setup Script
REM For n8n and GHL API Configuration
REM ============================================

echo.
echo ============================================
echo  Docker API Environment Setup
echo ============================================
echo.

REM Prompt for n8n API Key
echo Enter your n8n API Key (from n8n Settings ^> API):
set /p N8N_API_KEY="> "

REM Prompt for GHL API Key
echo.
echo Enter your GHL API Key:
set /p GHL_API_KEY="> "

REM Prompt for GHL Location ID (optional)
echo.
echo Enter your GHL Location ID (or press Enter to skip):
set /p GHL_LOCATION_ID="> "

REM Set environment variables permanently for current user
echo.
echo Setting environment variables...

setx N8N_API_KEY "%N8N_API_KEY%"
setx N8N_API_URL "http://localhost:5678"
setx GHL_API_KEY "%GHL_API_KEY%"

if not "%GHL_LOCATION_ID%"=="" (
    setx GHL_LOCATION_ID "%GHL_LOCATION_ID%"
)

echo.
echo ============================================
echo  Environment variables have been set!
echo ============================================
echo.
echo IMPORTANT: You must close and reopen your
echo terminal/PowerShell for changes to take effect.
echo.
echo Variables set:
echo   N8N_API_KEY = %N8N_API_KEY:~0,20%...
echo   N8N_API_URL = http://localhost:5678
echo   GHL_API_KEY = %GHL_API_KEY:~0,20%...
if not "%GHL_LOCATION_ID%"=="" echo   GHL_LOCATION_ID = %GHL_LOCATION_ID%
echo.
echo Next steps:
echo   1. Close this terminal
echo   2. Open a NEW terminal
echo   3. Run: python ai_ops_manager.py
echo.
pause
