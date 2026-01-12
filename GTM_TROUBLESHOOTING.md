# GTM Troubleshooting - Console Errors

## 🚨 ERRORS YOU'RE SEEING:

**Error 1:** `Failed to load resource: net::ERR_NAME_NOT_RESOLVED` for `gtm.js:1`  
**Error 2:** `Failed to load resource: net::ERR_NAME_NOT_RESOLVED` for `gtag/js?id=DUMMY:1`

---

## 🔍 WHAT THESE ERRORS MEAN:

1. **GTM container might not be published** (most common)
2. **Network/DNS issue** (less likely)
3. **GTM ID mismatch** (check code vs GTM)

---

## ✅ FIX STEPS:

### **Step 1: Verify Container is Published**

1. Go to: https://tagmanager.google.com
2. Click on: `www.premierleadmarketing.ai` (GTM-WGDC6CQS)
3. **Look at top right corner:**
   - ✅ If it says **"Published"** → Container is live
   - ❌ If it says **"Not Published"** → Need to publish

4. **If NOT Published:**
   - Click **"Submit"** button (blue, top right)
   - Click **"Publish"**
   - Version name: `Initial Setup`
   - Click **"Publish"**

### **Step 2: Verify GTM ID in Code Matches**

**Your code should have:**
- Container ID: `GTM-WGDC6CQS`
- In `<head>`: Script with `GTM-WGDC6CQS`
- In `<body>`: Noscript with `GTM-WGDC6CQS`

**Verify:**
1. Open `index.html` in Cursor
2. Search for: `GTM-WGDC6CQS`
3. Should appear twice (head and body sections)

### **Step 3: Wait & Refresh**

1. **After publishing:** Wait 1-2 minutes
2. **Hard refresh:** `Ctrl + F5` on your website
3. **Check console again:** Should see no errors

### **Step 4: Test Again**

1. Go to: https://premierleadmarketing.ai
2. Open Console (F12)
3. Look for:
   - ✅ No red errors
   - ✅ GTM script loads successfully
   - ✅ Container ID: `GTM-WGDC6CQS`

---

## 🎯 MOST LIKELY FIX:

**The container is NOT published yet!**

Go to GTM → Click your container → Click "Submit" → "Publish"

**Then refresh your website!**

---

## 💡 IF STILL NOT WORKING:

**Check Network Tab:**
1. Open DevTools (F12)
2. Click **"Network"** tab
3. Refresh page
4. Look for `gtm.js` request
5. Check if it's:
   - ✅ 200 (success) = Working!
   - ❌ 404 = Container not published
   - ❌ ERR_NAME_NOT_RESOLVED = DNS/network issue

---

**Go publish your GTM container now!** 🚀
