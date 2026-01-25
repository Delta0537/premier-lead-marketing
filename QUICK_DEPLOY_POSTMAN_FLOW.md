# Quick Deploy Postman Flow

## 🚀 One-Command Deployment

```powershell
.\deploy_postman_flow_complete.ps1
```

This script will:
1. ✅ Check for Postman API key
2. ✅ Update Flow variables (GHL_API_KEY, GHL_LOCATION_ID)
3. ✅ Test MCP Router connection

---

## 📝 Manual Steps (If Script Fails)

### 1. Set Postman API Key

```powershell
$env:POSTMAN_API_KEY='your-api-key-here'
```

Get key from: https://postman.com/settings/me/api-keys

### 2. Update Flow Variables

```powershell
python update_postman_flow_vars.py
```

**Or manually in Postman:**
- Go to: https://postman.com/flows/69755954010ddb0014f502dc
- Open Configuration panel
- Update:
  - `GHL_API_KEY`: `pit-81ca6da4-c48f-4d4d-887e-a6d35bca70a5` (secret)
  - `GHL_LOCATION_ID`: `4X72lI7IBpK9tJOdKwOf` (string)

### 3. Test Flow

1. Open Postman
2. Navigate to Flow: `69755954010ddb0014f502dc`
3. Click "Run"
4. Verify it works

---

## 🔑 Flow Information

- **Flow ID:** `69755954010ddb0014f502dc`
- **Variable IDs:**
  - `GHL_API_KEY`: `vq0LPMl6`
  - `GHL_LOCATION_ID`: `qDnQBK2f`

---

## ✅ Success Indicators

- ✅ Script completes without errors
- ✅ Flow variables show updated values in Postman
- ✅ Flow runs successfully when tested
- ✅ GHL API calls work (if flow makes API calls)

---

**Full guide:** See `POSTMAN_FLOW_DEPLOYMENT_GUIDE.md`
