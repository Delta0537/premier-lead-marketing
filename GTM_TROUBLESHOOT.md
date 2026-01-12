# GTM Troubleshooting - Container Not Loading

## 🔍 Quick Diagnosis Steps

### Step 1: Verify Container ID
**Your Container ID should be:** `GTM-WGDC6CQS`

1. Go to: https://tagmanager.google.com
2. Click on your container: `www.premierleadmarketing.ai`
3. Look at the top - you should see: **GTM-WGDC6CQS**
4. **Confirm it matches exactly** (no typos, same capitalization)

---

### Step 2: Test GTM Script URL Directly

**Open this URL in your browser:**
```
https://www.googletagmanager.com/gtm.js?id=GTM-WGDC6CQS
```

**What should happen:**
- ✅ **If working:** You'll see JavaScript code (looks like minified code)
- ❌ **If broken:** You'll see an error page or "404 Not Found"

**If you see 404:**
- Container ID might be wrong
- Container might not be published
- Container might be in a different account

---

### Step 3: Check Container Status

1. Go to: https://tagmanager.google.com
2. Click: **Versions** (left sidebar)
3. Look for: **"Version 3 is Live"** (green banner)
4. If you DON'T see "Live" → Container isn't published!

**To publish:**
1. Click **Workspace** (left sidebar)
2. Click **Submit** (top right)
3. Click **Publish**
4. Wait 30 seconds
5. Refresh your website

---

### Step 4: Verify Code in index.html

**Open:** `C:\ideas\Digital Marketing\Premier Lead Marketing\website\index.html`

**Look for line 37 (should be exactly this):**
```javascript
})(window,document,'script','dataLayer','GTM-WGDC6CQS');</script>
```

**Check:**
- ✅ Container ID: `GTM-WGDC6CQS` (no spaces, exact match)
- ✅ No typos in the URL
- ✅ Code is inside `<head>` tag (before `</head>`)

---

### Step 5: Check Browser Console

1. Go to: https://premierleadmarketing.ai
2. Press `F12` (open Developer Tools)
3. Click **Console** tab
4. Look for errors

**Common Errors:**

**Error 1: `ERR_NAME_NOT_RESOLVED`**
- Means: Can't find the domain
- Fix: Check internet connection, try different browser

**Error 2: `ERR_BLOCKED_BY_CLIENT`**
- Means: Ad blocker is blocking it
- Fix: Test in incognito window (no extensions)

**Error 3: `404 Not Found` or `Container not found`**
- Means: Container ID is wrong or container doesn't exist
- Fix: Double-check container ID in GTM

**Error 4: `net::ERR_FAILED`**
- Means: Network error or container not accessible
- Fix: Try accessing the script URL directly (Step 2)

---

## 🎯 Most Likely Issues

### Issue 1: Container Not Published
**Symptom:** Script URL returns 404
**Fix:** Go to GTM → Workspace → Submit → Publish

### Issue 2: Wrong Container ID
**Symptom:** Script URL returns 404
**Fix:** Copy container ID directly from GTM (top of container page)

### Issue 3: Container in Wrong Account
**Symptom:** Can't find container in GTM
**Fix:** Make sure you're logged into the correct Google account

### Issue 4: Ad Blocker
**Symptom:** `ERR_BLOCKED_BY_CLIENT`
**Fix:** Test in incognito window

---

## ✅ Verification Checklist

- [ ] Container ID matches: `GTM-WGDC6CQS`
- [ ] Container shows "Version X is Live" in GTM
- [ ] Script URL works: https://www.googletagmanager.com/gtm.js?id=GTM-WGDC6CQS
- [ ] Code in index.html has correct ID
- [ ] Tested in incognito window (no ad blockers)
- [ ] Console shows `dataLayer` exists (type `dataLayer` in console)

---

## 🚨 If Still Not Working

**Try this:**

1. **Copy the GTM code directly from GTM:**
   - Go to GTM
   - Click your container
   - Click **Admin** (left sidebar)
   - Click **Install Google Tag Manager**
   - Copy the code EXACTLY as shown
   - Replace the code in your `index.html`

2. **Create a simple test page:**
   - Create a new file: `test-gtm.html`
   - Paste ONLY the GTM code from GTM
   - Open it in browser
   - Check console - does it work?

3. **Check if container is public:**
   - Some GTM containers can be private/restricted
   - Make sure your container is set to "Public" (default)

---

## 💡 Quick Test

**Paste this in your browser address bar:**
```
javascript:alert(window.dataLayer ? 'GTM Loaded!' : 'GTM Not Loaded')
```

**Then press Enter:**
- ✅ If you see "GTM Loaded!" → GTM is working!
- ❌ If you see "GTM Not Loaded" → GTM isn't loading

---

**Tell me what you find from these steps!** 🔍
