# Postman Flow Complete Deployment Script
# Updates Flow variables and deploys via MCP Router

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "POSTMAN FLOW DEPLOYMENT - COMPLETE SETUP" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check for Postman API Key
Write-Host "[1/3] Checking Postman API Key..." -ForegroundColor Yellow
$postmanKey = $env:POSTMAN_API_KEY
if (-not $postmanKey) {
    Write-Host "  ⚠️  POSTMAN_API_KEY not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Set it with:" -ForegroundColor Yellow
    Write-Host "    `$env:POSTMAN_API_KEY='your-api-key'" -ForegroundColor White
    Write-Host ""
    Write-Host "  Get your key from: https://postman.com/settings/me/api-keys" -ForegroundColor Cyan
    Write-Host ""
    $continue = Read-Host "  Continue anyway? (y/n)"
    if ($continue -ne 'y') {
        exit 1
    }
} else {
    Write-Host "  ✅ Postman API Key found" -ForegroundColor Green
}

# Step 2: Update Flow Variables
Write-Host ""
Write-Host "[2/3] Updating Postman Flow Variables..." -ForegroundColor Yellow
Write-Host "  Flow ID: 69755954010ddb0014f502dc" -ForegroundColor White
Write-Host "  Variables: GHL_API_KEY, GHL_LOCATION_ID" -ForegroundColor White
Write-Host ""

try {
    python update_postman_flow_vars.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Flow variables updated successfully!" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Flow variable update had issues" -ForegroundColor Yellow
        Write-Host "  You may need to update manually in Postman UI" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ❌ Error updating flow variables: $_" -ForegroundColor Red
    Write-Host "  You can update manually in Postman UI" -ForegroundColor Yellow
}

# Step 3: Test MCP Router Deployment
Write-Host ""
Write-Host "[3/3] Testing MCP Router Deployment..." -ForegroundColor Yellow

try {
    python deploy_postman_flow_mcp.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ MCP Router deployment test successful!" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  MCP Router test had issues" -ForegroundColor Yellow
        Write-Host "  This is okay if webhook endpoint isn't implemented yet" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ⚠️  MCP Router test failed: $_" -ForegroundColor Yellow
    Write-Host "  This is okay - you can test the flow directly in Postman" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "DEPLOYMENT SUMMARY" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✅ Next Steps:" -ForegroundColor Green
Write-Host "  1. Open Postman and navigate to Flow: 69755954010ddb0014f502dc" -ForegroundColor White
Write-Host "  2. Click 'Run' to test the flow" -ForegroundColor White
Write-Host "  3. Verify variables are updated correctly" -ForegroundColor White
Write-Host "  4. Test with a real contact if applicable" -ForegroundColor White
Write-Host ""
Write-Host "📚 Documentation: POSTMAN_FLOW_DEPLOYMENT_GUIDE.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
