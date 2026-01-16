# ============================================
# Docker API Environment Setup Script (PowerShell)
# For n8n and GHL API Configuration
# Run as: powershell -ExecutionPolicy Bypass -File setup_api_env.ps1
# ============================================

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Docker API Environment Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Function to set environment variable for User scope
function Set-EnvVar {
    param($Name, $Value)
    [System.Environment]::SetEnvironmentVariable($Name, $Value, [System.EnvironmentVariableTarget]::User)
    # Also set for current session
    Set-Item -Path "Env:$Name" -Value $Value
    Write-Host "  [OK] $Name set successfully" -ForegroundColor Green
}

# Prompt for n8n API Key
Write-Host "Enter your n8n API Key" -ForegroundColor Yellow
Write-Host "(Copy from n8n: Settings > API > Create API Key)" -ForegroundColor Gray
$n8n_key = Read-Host "n8n API Key"

if ([string]::IsNullOrWhiteSpace($n8n_key)) {
    Write-Host "  [!] Warning: n8n API Key is empty" -ForegroundColor Red
} else {
    Set-EnvVar -Name "N8N_API_KEY" -Value $n8n_key
}

# Set n8n URL
Write-Host ""
Write-Host "Which n8n URL should be used?" -ForegroundColor Yellow
Write-Host "  1. http://localhost:5678 (default - n8n running directly)"
Write-Host "  2. http://host.docker.internal:5678 (for Docker containers)"
Write-Host "  3. Custom URL"
$url_choice = Read-Host "Choose (1/2/3)"

switch ($url_choice) {
    "2" { $n8n_url = "http://host.docker.internal:5678" }
    "3" { $n8n_url = Read-Host "Enter custom URL" }
    default { $n8n_url = "http://localhost:5678" }
}
Set-EnvVar -Name "N8N_API_URL" -Value $n8n_url

# Prompt for GHL API Key
Write-Host ""
Write-Host "Enter your GHL (GoHighLevel) API Key" -ForegroundColor Yellow
Write-Host "(From GHL: Settings > Business Profile > API Keys)" -ForegroundColor Gray
$ghl_key = Read-Host "GHL API Key"

if ([string]::IsNullOrWhiteSpace($ghl_key)) {
    Write-Host "  [!] Warning: GHL API Key is empty" -ForegroundColor Red
} else {
    Set-EnvVar -Name "GHL_API_KEY" -Value $ghl_key
}

# Prompt for GHL Location ID
Write-Host ""
Write-Host "Enter your GHL Location ID (optional, press Enter to skip)" -ForegroundColor Yellow
$ghl_location = Read-Host "GHL Location ID"

if (-not [string]::IsNullOrWhiteSpace($ghl_location)) {
    Set-EnvVar -Name "GHL_LOCATION_ID" -Value $ghl_location
}

# Set GHL Base URL
Set-EnvVar -Name "GHL_BASE_URL" -Value "https://services.leadconnectorhq.com"

# Verify settings
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Verification" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Test n8n connectivity
Write-Host "Testing n8n connectivity..." -ForegroundColor Yellow
try {
    $headers = @{}
    if ($n8n_key) {
        $headers["X-N8N-API-KEY"] = $n8n_key
    }
    $response = Invoke-WebRequest -Uri "$n8n_url/healthz" -TimeoutSec 5 -ErrorAction Stop
    Write-Host "  [OK] n8n is reachable at $n8n_url" -ForegroundColor Green
} catch {
    Write-Host "  [!] Cannot reach n8n at $n8n_url" -ForegroundColor Red
    Write-Host "      Error: $($_.Exception.Message)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Troubleshooting:" -ForegroundColor Yellow
    Write-Host "    - Make sure n8n is running"
    Write-Host "    - Check if port 5678 is not blocked by firewall"
    Write-Host "    - Try: docker ps (to see if n8n container is running)"
}

# Test GHL connectivity
if ($ghl_key) {
    Write-Host ""
    Write-Host "Testing GHL connectivity..." -ForegroundColor Yellow
    try {
        $headers = @{
            "Authorization" = "Bearer $ghl_key"
            "Version" = "2021-07-28"
        }
        $response = Invoke-WebRequest -Uri "https://services.leadconnectorhq.com/locations/" -Headers $headers -TimeoutSec 10 -ErrorAction Stop
        Write-Host "  [OK] GHL API key is valid" -ForegroundColor Green
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        if ($statusCode -eq 401) {
            Write-Host "  [!] GHL API key is invalid or expired" -ForegroundColor Red
            Write-Host "      Generate a new key in GHL Settings" -ForegroundColor Gray
        } elseif ($statusCode -eq 403) {
            Write-Host "  [!] GHL API key lacks required permissions" -ForegroundColor Red
        } else {
            Write-Host "  [!] GHL API error: $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

# Summary
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Environment variables have been set for your user account." -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. Close ALL terminals and PowerShell windows"
Write-Host "  2. Open a NEW terminal"
Write-Host "  3. Run your script: python ai_ops_manager.py"
Write-Host ""
Write-Host "If you're using Docker Desktop MCP Toolkit:" -ForegroundColor Yellow
Write-Host "  - Open Docker Desktop"
Write-Host "  - Go to: My Servers > n8n > Configuration"
Write-Host "  - Paste the same API key in the 'n8n_api_key' field"
Write-Host "  - Click Save"
Write-Host ""

# Create .env file option
Write-Host "Would you like to create a .env file as backup? (y/n)" -ForegroundColor Yellow
$create_env = Read-Host "Choice"

if ($create_env -eq "y") {
    $env_content = @"
# n8n Configuration
N8N_API_KEY=$n8n_key
N8N_API_URL=$n8n_url

# GHL Configuration
GHL_API_KEY=$ghl_key
GHL_LOCATION_ID=$ghl_location
GHL_BASE_URL=https://services.leadconnectorhq.com
"@
    $env_content | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "  [OK] .env file created in current directory" -ForegroundColor Green
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
