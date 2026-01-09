# Deploy to Vercel - Premier Lead Marketing

## 🚀 Quick Deploy (3 Steps)

### Step 1: Create GitHub Repository

1. Go to **https://github.com/new**
2. Repository name: `premier-lead-marketing`
3. Description: "Premier Lead Marketing - Strategic Digital Dominance"
4. **Keep it PUBLIC** (required for free Vercel)
5. **DO NOT** check "Add a README file"
6. Click **"Create repository"**

### Step 2: Push Your Code

Copy and run these commands (replace YOUR_USERNAME with your GitHub username):

```powershell
git remote add origin https://github.com/YOUR_USERNAME/premier-lead-marketing.git
git push -u origin main
```

**Example:**
```powershell
git remote add origin https://github.com/andrewknight/premier-lead-marketing.git
git push -u origin main
```

### Step 3: Deploy on Vercel

1. Go to **https://vercel.com**
2. Click **"Sign Up"** or **"Log In"** (use GitHub to sign in)
3. Click **"Add New..."** → **"Project"**
4. Click **"Import"** next to your `premier-lead-marketing` repository
5. Vercel will auto-detect it's a static site
6. Click **"Deploy"**
7. **DONE!** 🎉

Your site will be live at: `https://premier-lead-marketing.vercel.app`

---

## 🌐 Connect Your Custom Domain

After deployment:

1. In Vercel Dashboard → Click your project
2. Go to **Settings** → **Domains**
3. Click **"Add"**
4. Enter: `premierleadmarketing.at`
5. Vercel will give you DNS records

### Update DNS in GoDaddy:

1. Log into GoDaddy
2. Go to your domain → **DNS Management**
3. Add the records Vercel provides (usually):
   - **A Record**: `@` → `76.76.21.21`
   - **CNAME**: `www` → `cname.vercel-dns.com`

**DNS takes 5-60 minutes to propagate.**

---

## ✅ What Happens Next

✅ Your site is LIVE instantly  
✅ Free SSL certificate (HTTPS)  
✅ Global CDN (super fast)  
✅ **Auto-deploy**: Every time you push to GitHub, Vercel rebuilds your site!  

---

## 🔄 Making Updates

To update your website:

1. Edit your files locally
2. Commit changes:
   ```powershell
   git add .
   git commit -m "Update website content"
   git push
   ```
3. Vercel automatically deploys the update!

---

## 📊 Your Live URLs

- **Vercel URL**: `https://premier-lead-marketing.vercel.app`
- **Custom Domain** (after DNS): `https://premierleadmarketing.at`

---

## 🆘 Troubleshooting

### "Repository not found"
- Make sure the repository is PUBLIC
- Check you're using the correct GitHub username

### "Permission denied"
- You may need to authenticate with GitHub
- Try: `git remote set-url origin https://YOUR_USERNAME@github.com/YOUR_USERNAME/premier-lead-marketing.git`

### DNS not working
- Wait 30-60 minutes for propagation
- Clear browser cache (Ctrl+Shift+R)
- Check DNS records are correct in GoDaddy

---

## 🎉 You're Live!

Share your site:
- `https://premier-lead-marketing.vercel.app` (works immediately)
- `https://premierleadmarketing.at` (works after DNS)

**Built with ♾️ - Strategic Digital Dominance**
