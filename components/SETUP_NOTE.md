# ⚠️ IMPORTANT NOTE

## Current Website Status

Your Premier Lead Marketing website is currently:
- **Pure HTML/CSS/JavaScript** (static site)
- Deployed on Vercel
- Located in: `C:\ideas\Digital Marketing\Premier Lead Marketing\website\`

## GoogleTagManager Component

The `GoogleTagManager.tsx` component I created is for **Next.js 14** (React).

### Two Options:

#### Option 1: Use Current HTML Site (Quick Fix)

Add GTM directly to your `index.html`:

```html
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXXX');</script>
<!-- End Google Tag Manager -->

<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXXX"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
```

Replace `GTM-XXXXXXX` with your actual GTM ID.

#### Option 2: Migrate to Next.js (Future)

When you're ready to upgrade to Next.js:
1. The `GoogleTagManager.tsx` component is ready to use
2. Follow the setup instructions in `components/README.md`
3. Install Next.js dependencies: `npm install next react react-dom @next/third-parties`

---

**For now, use Option 1 (HTML) to get tracking working immediately!**
