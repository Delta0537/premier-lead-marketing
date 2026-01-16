# Docker API Environment Debug Guide

## Problem Summary

You're experiencing connection issues between your Python `ai_ops_manager.py` script and Docker-hosted services (n8n and GHL). The "connection refused" error indicates the script cannot reach the APIs.

## Root Causes

Based on the screenshots, there are several potential issues:

### 1. Environment Variables Not Persisted
When you set environment variables in Windows, they need to be:
- Set as **User** or **System** environment variables (not just session variables)
- Terminal must be **closed and reopened** after setting them
- Your Python script must load them (either from system or from a `.env` file)

### 2. Docker Desktop MCP Configuration is Separate
The API key you enter in Docker Desktop's n8n MCP Toolkit is **separate** from your system environment variables. They serve different purposes:
- **System env vars**: Used by scripts running directly on your machine
- **Docker MCP config**: Used by the Docker MCP Toolkit internally

### 3. Network Connectivity
- `localhost:5678` - Works when n8n runs directly on your machine
- `host.docker.internal:5678` - Works from inside Docker containers
- If running Python directly (not in Docker), use `localhost:5678`

## Solutions

### Option A: Quick Fix - Run the Setup Script

1. Open PowerShell as Administrator
2. Navigate to your project directory
3. Run:
   ```powershell
   powershell -ExecutionPolicy Bypass -File setup_api_env.ps1
   ```
4. Follow the prompts to enter your API keys
5. **Close and reopen** your terminal
6. Run `python ai_ops_manager.py`

### Option B: Manual Environment Variable Setup

#### Windows (PowerShell as Admin):
```powershell
# Set n8n variables
[System.Environment]::SetEnvironmentVariable('N8N_API_KEY', 'eyJhbGci...your-full-key', 'User')
[System.Environment]::SetEnvironmentVariable('N8N_API_URL', 'http://localhost:5678', 'User')

# Set GHL variables
[System.Environment]::SetEnvironmentVariable('GHL_API_KEY', 'your-ghl-key', 'User')
[System.Environment]::SetEnvironmentVariable('GHL_LOCATION_ID', 'your-location-id', 'User')
```

#### Windows (Command Prompt):
```batch
setx N8N_API_KEY "eyJhbGci...your-full-key"
setx N8N_API_URL "http://localhost:5678"
setx GHL_API_KEY "your-ghl-key"
setx GHL_LOCATION_ID "your-location-id"
```

**IMPORTANT:** Close and reopen your terminal after running these commands!

### Option C: Use a .env File

Create a `.env` file in the same directory as `ai_ops_manager.py`:

```env
# n8n Configuration
N8N_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...your-full-key
N8N_API_URL=http://localhost:5678

# GHL Configuration
GHL_API_KEY=your-ghl-api-key
GHL_LOCATION_ID=your-location-id
GHL_BASE_URL=https://services.leadconnectorhq.com
```

Then make sure your `ai_ops_manager.py` loads it:
```python
from dotenv import load_dotenv
load_dotenv()  # Add this at the top of your script

import os
n8n_key = os.environ.get('N8N_API_KEY')
```

## Debugging Steps

### Step 1: Run the Debug Script
```bash
python debug_docker_api.py
```

This will check:
- Environment variables are set
- Network connectivity to n8n
- API authentication
- Docker status

### Step 2: Verify n8n is Running
```bash
# Check if n8n is accessible
curl http://localhost:5678/healthz

# If using Docker, check container status
docker ps | grep n8n
```

### Step 3: Test API Key Validity
```bash
# Test n8n API (replace with your key)
curl -H "X-N8N-API-KEY: your-api-key" http://localhost:5678/api/v1/workflows
```

### Step 4: Check Python Environment
```python
import os
print("N8N_API_KEY:", os.environ.get('N8N_API_KEY', 'NOT SET'))
print("N8N_API_URL:", os.environ.get('N8N_API_URL', 'NOT SET'))
print("GHL_API_KEY:", os.environ.get('GHL_API_KEY', 'NOT SET'))
```

## Docker Desktop MCP Toolkit Configuration

For the Docker Desktop n8n MCP Toolkit specifically:

1. Open **Docker Desktop**
2. Go to **My Servers** → **n8n**
3. Click **Configuration** tab
4. Set:
   - `n8n_api_url`: `http://host.docker.internal:5678`
   - `n8n_api_key`: Your n8n API key (the full JWT token)
5. Click **Save**

Note: This configuration is for Docker's internal use. Your Python script running on Windows still needs the system environment variables set separately.

## Common Issues

### "Connection Refused" Error
- n8n is not running
- Wrong URL (use `localhost` for direct Python, `host.docker.internal` for Docker containers)
- Firewall blocking port 5678

### "401 Unauthorized" Error
- API key is invalid or expired
- API key not being sent in request headers
- Wrong header name (should be `X-N8N-API-KEY` for n8n)

### "Environment Variable Not Found"
- Variable not set as User/System variable
- Terminal not reopened after setting
- Script not loading `.env` file

### Keys Work in Browser but Not in Script
- Browser uses cookies/session, script uses API key
- Different authentication mechanisms
- Make sure you're using the API key, not session token

## File Overview

| File | Purpose |
|------|---------|
| `debug_docker_api.py` | Diagnostic script - run this first |
| `setup_api_env.ps1` | PowerShell setup script (recommended) |
| `setup_api_env.bat` | Batch file setup script (alternative) |
| `.env.template` | Template for environment variables |

## Need More Help?

1. Run `python debug_docker_api.py` and share the output
2. Check Docker Desktop logs for n8n container
3. Verify your API keys are valid by testing in n8n's UI
