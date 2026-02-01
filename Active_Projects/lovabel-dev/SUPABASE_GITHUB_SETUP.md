# Supabase Setup for Delta0537 (GitHub OAuth)

## 🔐 Your Account Details
- **GitHub**: Delta0537
- **Email**: cleanslate0537@gmail.com  
- **Authentication**: GitHub OAuth + Microsoft 2FA
- **No password needed** - uses GitHub OAuth flow

## 🚀 Quick Setup Steps

### 1. Get Your Project Credentials

Since you're already logged into Supabase, get your project details:

1. Go to [Supabase Dashboard](https://supabase.com/dashboard)
2. Select your project (or create a new one)
3. Go to **Settings** → **API**
4. Copy these values:

```env
# Your Project URL (replace YOUR_PROJECT_REF)
NEXT_PUBLIC_SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co

# Your anon/public key
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 2. Update Configuration Files

Replace the placeholder values in these files:

**`.env.local`** - Update the production URLs:
```env
# Change these lines:
# NEXT_PUBLIC_SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
# NEXT_PUBLIC_SUPABASE_ANON_KEY=YOUR_ACTUAL_ANON_KEY
```

**`script.js`** - Update for production:
```javascript
// Change these values when deploying:
const SUPABASE_URL = 'https://YOUR_PROJECT_REF.supabase.co'
const SUPABASE_ANON_KEY = 'YOUR_ACTUAL_ANON_KEY'
```

### 3. CLI Authentication

To use the Supabase CLI, you need to complete the login:

```bash
# This will open a browser for GitHub OAuth
npx supabase login
```

**Follow these steps:**
1. Command opens browser
2. Login with GitHub (Delta0537)
3. Authorize Supabase CLI
4. Complete Microsoft 2FA if prompted
5. Return to terminal

### 4. Link to Your Project

After CLI login:

```bash
# List your projects
npx supabase projects list

# Link to existing project
npx supabase link --project-ref YOUR_PROJECT_REF

# Or create a new project
npx supabase projects create your-project-name
```

## 🛠️ Local Development

For local development, you can use the local Supabase instance:

```bash
# Start local Supabase (includes auth, database, storage)
npm run supabase:start

# This gives you:
# - API URL: http://127.0.0.1:54321
# - Studio: http://127.0.0.1:54323
# - Inbucket (emails): http://127.0.0.1:54324
```

## 🔧 GitHub Integration Features

Since you're using GitHub OAuth, you can enable:

### GitHub Authentication in Your App
```javascript
// Enable GitHub OAuth for your users
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: 'github'
})
```

### GitHub Integration Settings
In your Supabase Dashboard:
1. **Authentication** → **Providers** → **GitHub**
2. Add your GitHub App credentials
3. Configure redirect URLs

## 📋 Production Checklist

When deploying to production:

- [ ] Update `.env.local` with production Supabase URL
- [ ] Update `script.js` with production credentials
- [ ] Configure GitHub OAuth provider in Supabase
- [ ] Set up proper redirect URLs
- [ ] Enable Row Level Security (RLS)
- [ ] Configure email templates
- [ ] Set up database backups

## 🔍 Finding Your Project Details

**Method 1: Supabase Dashboard**
1. Go to https://supabase.com/dashboard
2. Click on your project
3. Settings → API
4. Copy Project URL and anon key

**Method 2: CLI (after login)**
```bash
npx supabase projects list
npx supabase projects api-keys --project-ref YOUR_REF
```

## 🆘 Troubleshooting

**CLI Login Issues:**
- Make sure you're using the same browser where you're logged into GitHub
- Clear browser cache if authentication fails
- Try incognito/private browsing mode

**2FA Issues:**
- Have your Microsoft Authenticator app ready
- Make sure your phone's time is synced
- Try generating a new 2FA code

**Project Not Found:**
- Verify you're logged into the correct GitHub account (Delta0537)
- Check if the project was created under a different organization
- Try refreshing the Supabase dashboard

## 🎯 Next Steps

1. **Complete CLI login** (browser will open)
2. **Get your project credentials** from dashboard
3. **Update configuration files** with real values
4. **Test the demo page** (`supabase-demo.html`)
5. **Start building** your lovabel-dev features!

Your Supabase integration is ready for GitHub OAuth authentication! 🚀