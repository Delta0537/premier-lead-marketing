# GTM Script Failing to Load - Fix Steps

## 🚨 The Problem

Your browser console shows:
```
Loading failed for the <script> with source "https://www.googletagmanager.com/gtm.js?id=GTM-WGDC6CQS"
```

This means the GTM script URL is not accessible.

---

## ✅ Step-by-Step Fix

### Step 1: Test the GTM Script URL Directly

**Open this URL in your browser (in a NEW tab):**
```
https://www.googletagmanager.com/gtm.js?id=GTM-WGDC6CQS
```

**What should happen:**
- ✅ **If you see JavaScript code** (minified code starting with `(function(){` or similar) = Container exists!
- ❌ **If you see "404 Not Found" or blank page** = Container ID is wrong or container doesn't exist

**What do you see?** ⬅️ **DO THIS FIRST**

---

### Step 2: Verify Container ID in GTM

1. Go to: https://tagmanager.google.com
2. Make sure you're logged into the CORRECT Google account (cleanslate0537@gmail.com)
3. Click on container: **www.premierleadmarketing.ai**
4. Look at the TOP of the page - you should see: **GTM-WGDC6CQS**
5. **Copy it exactly** - is it exactly `GTM-WGDC6CQS`?

**Common mistakes:**
- Extra spaces: `GTM- WGDC6CQS` ❌
- Wrong characters: `GTM-WGD6CCQS` ❌ (missing 'C')
- Case sensitive: `gtm-wgdc6cqs` ❌ (should be uppercase)

---

### Step 3: Check Container Status

In GTM, go to **Versions** (left sidebar):

**Do you see:**
- ✅ Green banner saying "Version X is Live"?
- ✅ "Published" date?

**If you DON'T see "Live":**
1. Click **Workspace** (left sidebar)
2. Click **Submit** (top right)
3. Click **Publish**
4. Wait 30 seconds
5. Test the script URL again (Step 1)

---

### Step 4: Verify You're in the Right Account

**Make sure:**
- You're logged into GTM with: **cleanslate0537@gmail.com**
- The container is in the **Premier Lead Marketing** account
- You're NOT looking at a different Google account's containers

---

### Step 5: Try Creating a New Container (If Above Fails)

If the script URL returns 404, the container might not exist or be inaccessible.

**Option A: Create New Container**
1. Go to GTM
2. Click **Create Container**
3. Container Name: `premierleadmarketing.ai`
4. Target Platform: **Web**
5. Click **Create**
6. Copy the NEW container ID (will be different)
7. Update `index.html` with the new ID

**Option B: Re-verify Container ID**
- Double-check the container ID by copying it directly from GTM
- Don't type it manually - copy/paste it

---

## 🎯 Most Likely Issues (In Order)

### 1. Container ID Typo
**Symptom:** Script URL returns 404
**Fix:** Copy container ID directly from GTM (don't type it)

### 2. Container Not Published
**Symptom:** Container exists but script URL returns error
**Fix:** Go to Workspace → Submit → Publish

### 3. Wrong Google Account
**Symptom:** Can't find container in GTM
**Fix:** Log out, log back in with correct account

### 4. Container Doesn't Exist
**Symptom:** Script URL returns 404, container not in GTM
**Fix:** Create new container, get new ID, update code

---

## ✅ Quick Test Checklist

1. [ ] Open script URL directly: https://www.googletagmanager.com/gtm.js?id=GTM-WGDC6CQS
2. [ ] Do you see JavaScript code? (Not 404)
3. [ ] Container ID matches exactly in GTM
4. [ ] Container shows "Version X is Live"
5. [ ] Logged into correct Google account
6. [ ] Tested in incognito window (no extensions)

---

## 💡 Next Steps After Fix

Once the script URL loads correctly:

1. **Refresh your website:** `premierleadmarketing.ai`
2. **Open Console:** Press `F12`
3. **Type:** `dataLayer`
4. **Press Enter**
5. **Should see:** `Array(1) [{gtm.start: ..., event: "gtm.js"}]`

If you see the array → **GTM is working!** ✅

---

## 🚨 Critical: Test Script URL First!

**Before doing anything else, test this URL:**
```
https://www.googletagmanager.com/gtm.js?id=GTM-WGDC6CQS
```

**Tell me:**
- ✅ Do you see JavaScript code?
- ❌ Or do you see an error/404?

This will tell us exactly what's wrong! 🔍
