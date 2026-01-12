# 🚂 Deploy to Railway - Premier Lead Marketing

## Quick Deploy Steps

### Option 1: Deploy from GitHub (Recommended)

1. **Push your code to GitHub** (if not already):
   ```powershell
   git add .
   git commit -m "Add Railway configuration"
   git push
   ```

2. **Go to Railway Dashboard**:
   - Visit: https://railway.app
   - Sign in (use GitHub)

3. **Create New Project**:
   - Click **"New Project"**
   - Select **"Deploy from GitHub repo"**
   - Choose your repository: `premier-lead-marketing` (or your repo name)
   - Railway will auto-detect the project

4. **Configure Deployment**:
   - Railway will detect the `nixpacks.toml` or `package.json`
   - It will automatically use `serve` to host your static files
   - No additional configuration needed!

5. **Get Your URL**:
   - Railway will generate a URL like: `https://your-project.railway.app`
   - You can add a custom domain in Settings → Domains

### Option 2: Deploy from Local Directory

1. **Install Railway CLI**:
   ```powershell
   npm install -g @railway/cli
   ```

2. **Login to Railway**:
   ```powershell
   railway login
   ```

3. **Initialize and Deploy**:
   ```powershell
   cd "Premier Lead Marketing\website"
   railway init
   railway up
   ```

4. **Get Your URL**:
   - Railway CLI will show your deployment URL
   - Or check the Railway dashboard

---

## 🔧 Configuration Files Created

✅ **package.json** - Defines start command for Railway  
✅ **nixpacks.toml** - Railway build configuration  
✅ **railway.json** - Railway deployment settings (optional)

---

## 🌐 Custom Domain Setup

1. In Railway Dashboard → Your Project → **Settings**
2. Go to **Domains** tab
3. Click **"Add Domain"**
4. Enter your domain: `premierleadmarketing.com`
5. Railway will provide DNS records
6. Update DNS in your domain provider (GoDaddy, etc.)

### DNS Records Example:
- **CNAME**: `www` → `your-project.railway.app`
- **A Record**: `@` → Railway's IP (provided by Railway)

---

## ✅ What Happens on Deploy

- Railway detects your static HTML site
- Uses `serve` to host your files
- Automatically sets up HTTPS
- Provides a public URL
- Auto-deploys on every git push (if connected to GitHub)

---

## 🔄 Making Updates

### If deployed from GitHub:
1. Make changes locally
2. Commit and push:
   ```powershell
   git add .
   git commit -m "Update website"
   git push
   ```
3. Railway automatically deploys!

### If deployed from CLI:
1. Make changes locally
2. Run:
   ```powershell
   railway up
   ```

---

## 📊 Your Live URLs

After deployment, you'll have:
- **Railway URL**: `https://your-project.railway.app`
- **Custom Domain** (after DNS setup): `https://premierleadmarketing.com`

---

## 🆘 Troubleshooting

### "Build failed"
- Make sure all files are in the repository
- Check that `package.json` is present
- Railway needs at least one config file

### "Service not starting"
- Check Railway logs in the dashboard
- Ensure `serve` is being used (via nixpacks.toml)
- Port should be set via `$PORT` environment variable (Railway handles this)

### Custom domain not working
- Wait 5-60 minutes for DNS propagation
- Verify DNS records are correct
- Check Railway dashboard for domain status

---

## 💰 Railway Pricing

- **Hobby Plan**: $5/month (includes $5 credit)
- **Pro Plan**: $20/month (includes $20 credit)
- **Free Trial**: Try it free for a period

For a static site, the Hobby plan is usually sufficient.

---

## 🎉 You're Live!

Your Premier Lead Marketing site is now on Railway!

**Built with ♾️ - Strategic Digital Dominance**
