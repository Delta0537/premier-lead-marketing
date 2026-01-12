# Components Directory

This directory contains reusable React components for the Premier Lead Marketing website.

## GoogleTagManager Component

### Setup Instructions

1. **Install Required Package:**
   ```bash
   npm install @next/third-parties
   ```

2. **Configure Environment Variable:**
   - Copy `.env.local.example` to `.env.local`
   - Replace `GTM-XXXXXXX` with your actual GTM Container ID
   - Get your GTM ID from: https://tagmanager.google.com

3. **Add to Root Layout:**
   
   ```tsx
   // app/layout.tsx
   import GoogleTagManager from '@/components/GoogleTagManager';
   
   export default function RootLayout({
     children,
   }: {
     children: React.ReactNode;
   }) {
     return (
       <html lang="en">
         <body>
           <GoogleTagManager />
           {children}
         </body>
       </html>
     );
   }
   ```

4. **Verify Installation:**
   - Deploy to production (GTM doesn't work in localhost by default)
   - Or enable GTM Preview mode
   - Check browser console for GTM initialization
   - Use GTM Preview mode to verify tags are firing

### Usage

**Basic Usage:**
```tsx
import GoogleTagManager from '@/components/GoogleTagManager';

export default function Layout({ children }) {
  return (
    <>
      <GoogleTagManager />
      {children}
    </>
  );
}
```

**With Custom GTM ID:**
```tsx
<GoogleTagManager gtmId="GTM-CUSTOM123" />
```

### Features

- ✅ Automatic GTM initialization
- ✅ Noscript fallback for accessibility
- ✅ Environment variable configuration
- ✅ TypeScript types included
- ✅ Development mode warnings
- ✅ Client-side only rendering (prevents SSR issues)

### Troubleshooting

**GTM not loading:**
- Verify `NEXT_PUBLIC_GTM_ID` is set in `.env.local`
- Check GTM ID format (should be `GTM-XXXXXXX`)
- Ensure `.env.local` is not committed to git
- Restart Next.js dev server after changing env variables

**GTM not tracking:**
- GTM requires production deployment or Preview mode
- Check browser console for errors
- Verify GTM container is published (not draft)
- Use GTM Preview mode to debug

**Hydration errors:**
- Component only renders on client side (prevents SSR issues)
- This is expected behavior

### Related Files

- `.env.local.example` - Environment variable template
- `app/layout.tsx` - Where to import the component
- `.cursorrules` - Coding standards this component follows
