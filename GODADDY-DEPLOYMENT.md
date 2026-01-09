# 🚀 Deploy to GoDaddy - Premier Lead Marketing

## Quick Overview
You need to upload 3 files to your GoDaddy hosting:
- `index.html`
- `styles.css`
- `script.js`

---

## Step-by-Step Instructions

### Step 1: Access GoDaddy File Manager

**Option A: Using cPanel (Recommended)**
1. Log into your GoDaddy account: https://www.godaddy.com
2. Go to **My Products** → **Web Hosting**
3. Click **Manage** next to your premierleadmarketing.at hosting
4. Click **cPanel Admin**
5. Find and click **File Manager**

**Option B: Using GoDaddy's File Manager**
1. Log into your GoDaddy account
2. Go to **My Products** → **Web Hosting**
3. Click **Manage**
4. Click **File Manager** under Files

---

### Step 2: Navigate to the Right Folder

In File Manager, go to:
- **public_html** (this is where your website files go)

If premierleadmarketing.at is an addon domain, it might be in:
- **public_html/premierleadmarketing.at**

---

### Step 3: Clean Up Old Files (if any)

In the `public_html` folder:
1. Look for any old `index.html`, `index.php`, or placeholder files
2. **Delete or rename them** (right-click → Delete or Rename)
3. Keep: `.htaccess` file if it exists (important!)

---

### Step 4: Upload Your Website Files

**Files to Upload** (from this folder):
```
✅ index.html
✅ styles.css
✅ script.js
```

**How to Upload:**
1. Click the **Upload** button in File Manager
2. Select all 3 files from your computer:
   - Navigate to: `C:\ideas\Digital Marketing\Premier Lead Marketing\website\`
   - Select: `index.html`, `styles.css`, `script.js`
3. Click **Open** to upload
4. Wait for upload to complete (should be instant - they're small files)

---

### Step 5: Set File Permissions (if needed)

Usually automatic, but if you get errors:
1. Right-click each file
2. Select **Change Permissions**
3. Set to **644** (or check: Read for Owner, Group, World)
4. Click **Save**

---

### Step 6: Test Your Website

Open your browser and go to:
```
https://premierleadmarketing.at
```

Or:
```
http://premierleadmarketing.at
```

**You should see your new website!** 🎉

---

## 🔧 Troubleshooting

### Problem: Site still shows old page or GoDaddy placeholder
**Solution:**
1. Clear browser cache (Ctrl + Shift + Delete)
2. Try incognito/private browsing
3. Wait 5-10 minutes for DNS/cache to update
4. Make sure you deleted old `index.html` or `index.php` files

### Problem: CSS/styling not working
**Solution:**
1. Check that all 3 files are in the **same folder**
2. File names are case-sensitive: must be exactly `styles.css` and `script.js`
3. Re-upload if needed

### Problem: "403 Forbidden" or "404 Not Found"
**Solution:**
1. Check file permissions (should be 644)
2. Make sure files are in `public_html` not a subfolder
3. Contact GoDaddy support if issue persists

### Problem: Images missing (infinity logo)
**Solution:**
- The infinity logo is SVG (code-based), so no image files needed
- If you want to add images later, upload them to `public_html` too

---

## 📱 After Deployment Checklist

Once live, test these:
- [ ] Homepage loads correctly
- [ ] Navigation links work
- [ ] Form displays properly
- [ ] Webinar banner shows correctly
- [ ] Mobile view works (test on phone)
- [ ] All buttons/links work
- [ ] Contact form submission (you'll need to connect to email/GHL)

---

## 🔐 SSL Certificate (HTTPS)

GoDaddy usually includes free SSL. To enable:
1. In GoDaddy hosting panel
2. Go to **SSL Certificates**
3. If not active, click **Set Up** or **Manage**
4. Follow prompts to activate

Your site should be accessible via:
```
https://premierleadmarketing.at
```

---

## 📧 Connect Form to Email/GHL

The contact form currently logs to console. To make it work:

**Option 1: Use Formspree (Easiest)**
1. Go to https://formspree.io
2. Create free account
3. Get your form endpoint
4. Update `script.js` line 70 with your endpoint

**Option 2: Connect to GoHighLevel**
1. Get your GHL webhook URL
2. Update `script.js` line 70 with webhook URL
3. Forms will send directly to GHL

I can help with either setup!

---

## 🎨 Future Updates

To update your website later:
1. Edit files on your computer
2. Re-upload the changed files via GoDaddy File Manager
3. Clear cache and refresh browser

---

## 📞 Need Help?

**GoDaddy Support:**
- Phone: 1-480-505-8877
- Live Chat: Available in your account dashboard

**Questions for me:**
- Form not working? I can help connect it
- Want to customize? Just ask!
- Analytics setup? I can add Google Analytics

---

## ✅ You're All Set!

Your Premier Lead Marketing website is ready to dominate! 🚀

Files are located at:
```
C:\ideas\Digital Marketing\Premier Lead Marketing\website\
```

Upload to GoDaddy and you're live! 🎉

