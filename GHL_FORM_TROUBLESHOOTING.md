# 🔧 GHL Form Embed Troubleshooting

## The Problem
The form isn't showing up because we need the **external website embed code**, not the inline embed code.

---

## ✅ Solution: Get the Correct Embed Code

### Step 1: Go to GHL Form Builder
1. Go to: https://app.gohighlevel.com
2. Navigate to: **Forms** → **Form Builder**
3. Open your form (Form 1)

### Step 2: Get External Embed Code
1. Click **"Integrate"** button (top right)
2. You'll see tabs:
   - **Embed Code** (this is for GHL pages - WRONG)
   - **Share** (this might have the external embed)
   - **API** (for developers)

3. Look for: **"Embed on External Website"** or **"Copy Embed Code for Your Website"**

### Step 3: The Correct Code Format
For external websites, GHL usually provides code like:

```html
<script src="https://lighterleads.com/forms/embed.js"></script>
<script>
  LighterLeads.create({
    formId: "9LDTj4dmDdTj3ONVJc3Q",
    domain: "link.msgsndr.com"
  });
</script>
```

OR sometimes:

```html
<iframe src="https://YOUR-GHL-DOMAIN.com/widget/form/9LDTj4dmDdTj3ONVJc3Q" 
        width="100%" 
        height="963" 
        frameborder="0">
</iframe>
```

---

## 🔍 Alternative: Check Your GHL Domain

Your GHL form might use a custom domain. Check:

1. **GHL Settings** → **Domains**
2. Look for your custom domain (might be something like `premierleadmarketing.gohighlevel.com` or custom)
3. Use that domain instead of `link.msgsndr.com`

---

## 📋 Quick Fix Options

### Option 1: Use GHL Share Link (Temporary)
If you can't find the embed code, you could:
1. In GHL Form → Click **"Share"**
2. Get the share link
3. Use that as a button link temporarily
4. Form opens in popup/separate page

### Option 2: Create Form on GHL Page
1. Create a page in GHL
2. Embed form on that page
3. Link to that GHL page from your website

### Option 3: Get Correct Embed Code
**This is the best solution** - get the proper external embed code from GHL support or documentation.

---

## ❓ What We Need From You

Please check GHL and tell me:
1. What does the **"Integrate"** button show?
2. Are there multiple embed options?
3. Do you see "External Website" or "Your Website" option?
4. What's your GHL domain/subdomain?

Then we can use the correct code! 🔧
