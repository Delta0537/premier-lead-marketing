# Postman Flow Deployment Guide
## Deploy GHL Integration Flow via Postman and MCP Router

This guide walks you through deploying your Postman Flow with updated environment variables and integrating it with the MCP Router.

---

## 📋 Prerequisites

1. **Postman API Key**
   - Get from: https://postman.com/settings/me/api-keys
   - Required to update Flow configuration variables

2. **MCP Router Access**
   - URL: `https://mcp-router-production.up.railway.app`
   - API Key (if required): Set in `MCP_API_KEY` environment variable

3. **Flow Information**
   - Flow ID: `69755954010ddb0014f502dc`
   - Variables to update:
     - `GHL_API_KEY`: `pit-81ca6da4-c48f-4d4d-887e-a6d35bca70a5` (secret)
     - `GHL_LOCATION_ID`: `4X72lI7IBpK9tJOdKwOf` (string)

---

## 🚀 Step 1: Set Environment Variables

### Set Postman API Key

**PowerShell (Current Session):**
```powershell
$env:POSTMAN_API_KEY='your-postman-api-key-here'
```

**PowerShell (Permanent):**
```powershell
[System.Environment]::SetEnvironmentVariable('POSTMAN_API_KEY', 'your-postman-api-key-here', 'User')
```

**Verify:**
```powershell
$env:POSTMAN_API_KEY
```

### Set MCP Router API Key (Optional)

```powershell
$env:MCP_API_KEY='your-mcp-api-key-here'
```

---

## 🔧 Step 2: Update Postman Flow Variables

Run the update script:

```powershell
cd C:\Users\dezel\DigitalMarketing
python update_postman_flow_vars.py
```

**Expected Output:**
```
============================================================
POSTMAN FLOW CONFIGURATION VARIABLE UPDATER
============================================================

Flow ID: 69755954010ddb0014f502dc
Variables to update: 2

Attempting to update variables by ID...
✅ Successfully updated variables by ID!
```

**If API update fails**, you can update manually:
1. Go to: https://postman.com/flows/69755954010ddb0014f502dc
2. Open the Flow
3. Click on the Configuration panel
4. Update:
   - `GHL_API_KEY`: `pit-81ca6da4-c48f-4d4d-887e-a6d35bca70a5` (set as secret)
   - `GHL_LOCATION_ID`: `4X72lI7IBpK9tJOdKwOf` (set as string)

---

## 🌐 Step 3: Deploy via MCP Router

### Option A: Test Deployment

```powershell
python deploy_postman_flow_mcp.py
```

This will:
1. Check MCP Router health
2. Test the Postman Flow integration
3. Verify the flow can be triggered

### Option B: Manual Testing in Postman

1. Open Postman
2. Navigate to your Flow: `69755954010ddb0014f502dc`
3. Click "Run" to test the flow
4. Verify the variables are updated correctly

---

## 🔗 Step 4: Integrate with MCP Router

### If Webhook Endpoint Doesn't Exist

The MCP Router may need a webhook handler for Postman Flows. The code is provided in `deploy_postman_flow_mcp.py` in the `create_mcp_router_webhook_handler()` function.

**To add to MCP Router:**

1. Open `MCP_Router/main.py`
2. Add the webhook handler code
3. Deploy the updated MCP Router

### Alternative: Direct Postman Flow Execution

If MCP Router integration isn't needed, you can:
1. Run the Flow directly in Postman
2. Set up a Postman Monitor to run it on a schedule
3. Use Postman's API to trigger the flow programmatically

---

## ✅ Verification Checklist

- [ ] Postman API key is set
- [ ] Flow variables updated successfully
- [ ] MCP Router is accessible
- [ ] Flow runs successfully in Postman
- [ ] GHL API credentials are working
- [ ] Test contact receives messages (if applicable)

---

## 🐛 Troubleshooting

### Issue: "POSTMAN_API_KEY not found"

**Solution:**
```powershell
$env:POSTMAN_API_KEY='your-key'
python update_postman_flow_vars.py
```

### Issue: "Flow ID not found" or "404 Error"

**Solution:**
1. Verify the Flow ID is correct: `69755954010ddb0014f502dc`
2. Check you have access to the Flow in Postman
3. Verify your API key has permission to modify the Flow

### Issue: "MCP Router not available"

**Solution:**
1. Check MCP Router deployment status
2. Verify the URL: `https://mcp-router-production.up.railway.app`
3. Check Railway deployment logs

### Issue: "Variables not updating"

**Solution:**
1. Try manual update in Postman UI
2. Check variable IDs match:
   - `GHL_API_KEY`: `vq0LPMl6`
   - `GHL_LOCATION_ID`: `qDnQBK2f`
3. Verify variable types (secret vs string)

---

## 📚 Additional Resources

- **Postman API Docs:** https://www.postman.com/postman/workspace/postman-public-workspace/documentation
- **Postman Flows Docs:** https://learning.postman.com/docs/postman-flows/
- **MCP Router:** See `MCP_Router/README.md`

---

## 🎯 Next Steps

1. **Test the Flow** - Run it in Postman to verify everything works
2. **Set up Monitoring** - Configure Postman Monitor for scheduled runs
3. **Integrate with PLM** - Connect the Flow to your PLM Lead Assistant
4. **Monitor Performance** - Track Flow execution and success rates

---

## 📝 Notes

- Flow ID: `69755954010ddb0014f502dc`
- Variable IDs:
  - `GHL_API_KEY`: `vq0LPMl6`
  - `GHL_LOCATION_ID`: `qDnQBK2f`
- MCP Router URL: `https://mcp-router-production.up.railway.app`

---

**Ready to deploy? Run:**
```powershell
python update_postman_flow_vars.py
python deploy_postman_flow_mcp.py
```
