# Supabase Setup Guide

## 🚀 Quick Start

You now have Supabase integrated into your lovabel-dev project! Here's how to get it fully connected with your GitHub account 'Delta0537'.

## 📋 What's Already Set Up

✅ **Supabase CLI** - Available via `npx supabase`  
✅ **Supabase Client** - JavaScript library installed  
✅ **Project Structure** - Configuration files created  
✅ **Helper Functions** - Ready-to-use auth and database functions  

## 🔧 Next Steps

### 1. Connect to Your Supabase Account

Since you mentioned you have Supabase connected through GitHub 'Delta0537':

```bash
# Login to Supabase (this will open a browser)
npm run supabase:login
# or
npx supabase login
```

### 2. Link to Your Existing Project

If you already have a Supabase project:

```bash
# List your projects
npx supabase projects list

# Link to existing project
npx supabase link --project-ref YOUR_PROJECT_REF
```

### 3. Get Your Project Credentials

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Select your project
3. Go to **Settings** → **API**
4. Copy your:
   - **Project URL**
   - **anon/public key**

### 4. Update Environment Variables

Edit `.env.local` with your actual credentials:

```env
# Replace with your actual Supabase project values
NEXT_PUBLIC_SUPABASE_URL=https://your-project-ref.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-actual-anon-key-here
```

### 5. Update JavaScript Configuration

Edit `script.js` and replace the placeholder values:

```javascript
const SUPABASE_URL = 'https://your-project-ref.supabase.co'
const SUPABASE_ANON_KEY = 'your-actual-anon-key-here'
```

## 🛠️ Available Commands

```bash
# Start local Supabase (includes database, auth, storage)
npm run supabase:start

# Stop local Supabase
npm run supabase:stop

# Check status
npm run supabase:status

# Open Supabase Studio (database GUI)
npm run supabase:studio

# Reset local database
npm run supabase:reset
```

## 📝 Usage Examples

### Authentication

```javascript
// Sign up a new user
const { data, error } = await SupabaseHelpers.signUp(
  'user@example.com', 
  'password123',
  { name: 'John Doe' }
);

// Sign in
const { data, error } = await SupabaseHelpers.signIn(
  'user@example.com', 
  'password123'
);

// Get current user
const { user, error } = await SupabaseHelpers.getCurrentUser();

// Sign out
const { error } = await SupabaseHelpers.signOut();
```

### Database Operations

```javascript
// Insert data
const { data, error } = await SupabaseHelpers.insertData('profiles', {
  name: 'John Doe',
  email: 'john@example.com'
});

// Fetch data
const { data, error } = await SupabaseHelpers.fetchData('profiles');
```

### Listen to Auth Changes

```javascript
SupabaseHelpers.onAuthStateChange((event, session) => {
  if (event === 'SIGNED_IN') {
    console.log('User signed in:', session.user);
  } else if (event === 'SIGNED_OUT') {
    console.log('User signed out');
  }
});
```

## 🔗 Integration with GitHub

Since you have GitHub 'Delta0537' connected:

1. **GitHub OAuth**: You can enable GitHub authentication in your Supabase dashboard
2. **GitHub Integration**: Supabase can automatically deploy database changes via GitHub Actions
3. **Repository Sync**: Your database schema can be version controlled

## 📚 Next Steps

1. **Create Tables**: Use Supabase Studio to create your database tables
2. **Set Up Auth**: Configure authentication providers (email, GitHub, Google, etc.)
3. **Add RLS**: Set up Row Level Security for data protection
4. **Deploy**: Connect to Vercel or your preferred hosting platform

## 🆘 Need Help?

- [Supabase Documentation](https://supabase.com/docs)
- [JavaScript Client Docs](https://supabase.com/docs/reference/javascript)
- [Authentication Guide](https://supabase.com/docs/guides/auth)

## 🔧 Troubleshooting

**CLI not working?**
```bash
# Try installing globally (may not work)
npm install -g supabase

# Or always use npx
npx supabase --help
```

**Connection issues?**
- Check your `.env.local` file
- Verify your project URL and keys in Supabase dashboard
- Make sure your project is not paused

**Local development:**
```bash
# Start local Supabase stack
npm run supabase:start

# This will give you local URLs:
# API URL: http://127.0.0.1:54321
# Studio URL: http://127.0.0.1:54323
```