# Open Postman Flow for Manual Variable Update
# This script opens your Flow in the browser with clear instructions

$FlowID = "69755954010ddb0014f502dc"
$FlowURL = "https://postman.com/flows/$FlowID"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "POSTMAN FLOW VARIABLE UPDATE HELPER" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Opening your Flow in the browser..." -ForegroundColor Yellow
Start-Process $FlowURL

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "STEP-BY-STEP INSTRUCTIONS" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

Write-Host "1. In the Postman Flow that just opened:" -ForegroundColor White
Write-Host "   - Look for a 'Configuration' or 'Settings' panel" -ForegroundColor Gray
Write-Host "   - Usually in the right sidebar or top menu" -ForegroundColor Gray
Write-Host ""

Write-Host "2. Find and update these variables:" -ForegroundColor White
Write-Host ""

Write-Host "   Variable 1: GHL_API_KEY" -ForegroundColor Yellow
Write-Host "   - Variable ID: vq0LPMl6" -ForegroundColor Gray
Write-Host "   - Type: Secret (make sure it's Secret, not String!)" -ForegroundColor Gray
Write-Host "   - Value: pit-81ca6da4-c48f-4d4d-887e-a6d35bca70a5" -ForegroundColor Gray
Write-Host ""

Write-Host "   Variable 2: GHL_LOCATION_ID" -ForegroundColor Yellow
Write-Host "   - Variable ID: qDnQBK2f" -ForegroundColor Gray
Write-Host "   - Type: String" -ForegroundColor Gray
Write-Host "   - Value: 4X72lI7IBpK9tJOdKwOf" -ForegroundColor Gray
Write-Host ""

Write-Host "3. Click 'Save' or 'Update' to save your changes" -ForegroundColor White
Write-Host ""

Write-Host "4. Test the Flow:" -ForegroundColor White
Write-Host "   - Click 'Run' on your Flow" -ForegroundColor Gray
Write-Host "   - Verify it executes successfully" -ForegroundColor Gray
Write-Host ""

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "QUICK COPY VALUES:" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "GHL_API_KEY:" -ForegroundColor Yellow
Write-Host "pit-81ca6da4-c48f-4d4d-887e-a6d35bca70a5" -ForegroundColor White
Write-Host ""
Write-Host "GHL_LOCATION_ID:" -ForegroundColor Yellow
Write-Host "4X72lI7IBpK9tJOdKwOf" -ForegroundColor White
Write-Host ""

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "TROUBLESHOOTING" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Can't find Configuration panel?" -ForegroundColor Yellow
Write-Host "  - Try clicking on individual Action blocks" -ForegroundColor Gray
Write-Host "  - Look for a Settings/Config icon" -ForegroundColor Gray
Write-Host "  - Check the Flow menu in the top bar" -ForegroundColor Gray
Write-Host ""
Write-Host "Need more help?" -ForegroundColor Yellow
Write-Host "  - See: MANUAL_POSTMAN_FLOW_UPDATE.md" -ForegroundColor Gray
Write-Host ""

# Copy values to clipboard for easy pasting
$clipboard = @"
GHL_API_KEY: pit-81ca6da4-c48f-4d4d-887e-a6d35bca70a5
GHL_LOCATION_ID: 4X72lI7IBpK9tJOdKwOf
"@
Set-Clipboard -Value $clipboard
Write-Host "[INFO] Values copied to clipboard for easy pasting!" -ForegroundColor Green
Write-Host ""
