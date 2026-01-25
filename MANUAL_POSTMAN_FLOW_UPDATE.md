# Manual Postman Flow Variable Update Guide

## ⚠️ Important Note

Postman Flows may not have a public API endpoint for updating configuration variables programmatically. You'll need to update them manually in the Postman UI.

---

## 📝 Step-by-Step Manual Update

### Step 1: Open Your Flow

1. Go to: **https://postman.com/flows/69755954010ddb0014f502dc**
   - Or open Postman → Navigate to Flows → Find Flow ID `69755954010ddb0014f502dc`

### Step 2: Access Configuration Panel

1. Click on your Flow to open it
2. Look for the **Configuration** or **Settings** panel
   - Usually found in the right sidebar or in Flow settings
   - May be labeled as "Configuration Variables" or "Flow Variables"

### Step 3: Update Variables

Update these two variables:

#### Variable 1: `GHL_API_KEY`
- **Variable ID:** `vq0LPMl6`
- **Name:** `GHL_API_KEY`
- **Type:** `Secret` (make sure it's set as Secret, not String)
- **Value:** `pit-81ca6da4-c48f-4d4d-887e-a6d35bca70a5`

#### Variable 2: `GHL_LOCATION_ID`
- **Variable ID:** `qDnQBK2f`
- **Name:** `GHL_LOCATION_ID`
- **Type:** `String`
- **Value:** `4X72lI7IBpK9tJOdKwOf`

### Step 4: Save Changes

1. Click **Save** or **Update** to save your changes
2. Verify the values are correct

### Step 5: Test the Flow

1. Click **Run** on your Flow
2. Verify it executes successfully
3. Check that the GHL API calls work correctly

---

## 🔍 Finding Configuration Variables in Postman

If you can't find the Configuration panel:

1. **Look for a Settings/Config icon** in the Flow editor
2. **Check the Flow properties** - right-click on the Flow canvas
3. **Look in the Flow menu** - top menu bar in Postman
4. **Check Action blocks** - some configurations might be in individual action blocks

---

## ✅ Verification Checklist

- [ ] `GHL_API_KEY` is set to: `pit-81ca6da4-c48f-4d4d-887e-a6d35bca70a5`
- [ ] `GHL_API_KEY` type is: `Secret` (not String)
- [ ] `GHL_LOCATION_ID` is set to: `4X72lI7IBpK9tJOdKwOf`
- [ ] `GHL_LOCATION_ID` type is: `String`
- [ ] Flow runs successfully
- [ ] GHL API calls work (if your Flow makes API calls)

---

## 🆘 Troubleshooting

### Can't Find Configuration Panel?

- Try clicking on individual **Action blocks** in your Flow
- Some variables might be set at the **Action level** rather than Flow level
- Check if variables are in **Environment** instead of Flow Configuration

### Variables Not Updating?

- Make sure you're editing the **correct Flow** (ID: `69755954010ddb0014f502dc`)
- Verify you have **permissions** to edit the Flow
- Try **refreshing** the Postman app
- Check if variables are **locked** or **read-only**

### Flow Still Not Working?

- Verify your **Postman API key** is valid
- Check that **GHL API credentials** are correct
- Review **Flow execution logs** for error messages
- Test GHL API directly to verify credentials work

---

## 📚 Alternative: Using Postman Collections API

If your Flow uses a Collection, you might be able to update Collection variables instead:

```powershell
# This would update Collection variables (not Flow configurations)
# You'd need to find your Collection ID first
```

---

**Note:** Postman Flows are relatively new, and the API for managing them may still be evolving. Manual updates in the UI are currently the most reliable method.
