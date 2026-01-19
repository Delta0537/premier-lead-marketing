# Premier Lead Marketing - Email Signature Templates

Professional email signature templates and assets for Premier Lead Marketing team members.

## Quick Start

### Option 1: Use HTML Templates Directly
1. Open any `.html` file in this folder in a browser
2. Select and copy the signature content
3. Paste into your email client's signature settings

### Option 2: Create in Canva (Recommended for Customization)
See detailed Canva instructions below.

---

## Available Templates

| Template | Description | Best For |
|----------|-------------|----------|
| `signature-professional.html` | Logo + full contact info + CTA | Standard business use |
| `signature-executive.html` | Minimal, elegant design | C-suite executives |
| `signature-full-featured.html` | Photo + social icons + stats | Marketing outreach |
| `signature-compact.html` | Single line, mobile-friendly | Quick replies |
| `signature-dark-theme.html` | Dark background variant | Dark mode users |

---

## Brand Assets Included

### Logos (`/logos/`)
- `plm-logo-full-color.svg` - Full logo for light backgrounds
- `plm-logo-dark-bg.svg` - Logo optimized for dark backgrounds
- `plm-icon-only.svg` - Infinity symbol icon only
- `plm-logo-horizontal.svg` - Wide horizontal layout
- `plm-logo-stacked.svg` - Compact stacked layout

### Social Icons (`/icons/`)
- `linkedin.svg`
- `facebook.svg`
- `instagram.svg`
- `twitter-x.svg`
- `email.svg`
- `website.svg`
- `phone.svg`

---

## Brand Guidelines

### Colors
| Color | Hex Code | Usage |
|-------|----------|-------|
| Primary Blue | `#3b82f6` | Main brand color, links |
| Primary Light | `#60a5fa` | Hover states, accents |
| Teal/Growth | `#14b8a6` | Secondary accent, gradients |
| Dark Blue | `#2563eb` | Buttons, emphasis |
| Text Primary | `#1e293b` | Main text (dark) |
| Text Secondary | `#64748b` | Secondary info |
| Text Muted | `#94a3b8` | Captions, taglines |

### Typography
- **Primary Font:** Inter (Google Fonts)
- **Display Font:** Orbitron (for "PLM" text)
- **Fallback:** Arial, Helvetica, sans-serif

### Gradient
```css
background: linear-gradient(90deg, #3b82f6, #14b8a6);
```

---

## Creating Signatures in Canva

### Step 1: Set Up Your Canvas
1. Go to [canva.com](https://canva.com) and log in
2. Click **Create a design** → **Custom size**
3. Set dimensions: **600 x 200 pixels** (for most signatures)
4. Name your design: "PLM Email Signature - [Your Name]"

### Step 2: Upload Brand Assets
1. Click **Uploads** in the left sidebar
2. Upload these files from the `/logos/` folder:
   - `plm-logo-stacked.svg` or `plm-icon-only.svg`
3. Upload icons from `/icons/` folder as needed

### Step 3: Design Your Signature

**Layout Structure:**
```
┌──────────────────────────────────────────────────┐
│  [LOGO]  │  Name                                 │
│          │  Title                                │
│          │  email@premierleadmarketing.com       │
│          │  premierleadmarketing.ai              │
│          │  [Social Icons]                       │
└──────────────────────────────────────────────────┘
```

**Design Tips:**
1. Use the **vertical divider line** (3px, color #3b82f6) between logo and text
2. Keep font sizes:
   - Name: 18-20px, Bold
   - Title: 13-14px, Medium
   - Contact: 12px, Regular
3. Use Inter font (search in Canva fonts)
4. Align text left, logo center

### Step 4: Add Text Elements
1. **Name:** Bold, #1e293b
2. **Title:** Medium weight, #3b82f6
3. **Email/Website:** Regular, #64748b
4. **Tagline:** Italic, #94a3b8, 11px

### Step 5: Add CTA Button (Optional)
1. Add a rectangle shape
2. Set background: Use gradient colors or solid #3b82f6
3. Add text: "Book Your Free Marketing Audit"
4. Text color: #ffffff, 13px, Bold

### Step 6: Export
1. Click **Share** → **Download**
2. Select **PNG** format
3. Check "Transparent background" if using on dark emails
4. Download

### Step 7: Add to Email Client
- **Gmail:** Settings → See all settings → General → Signature
- **Outlook:** File → Options → Mail → Signatures
- **Apple Mail:** Preferences → Signatures

---

## Customization for Team Members

Replace these placeholders in any template:

| Placeholder | Replace With |
|-------------|--------------|
| `Andrew Knight` | Team member name |
| `Co-Founder & COO` | Job title |
| `andrew@premierleadmarketing.com` | Email address |
| `andrew-knight.jpg` | Team member photo URL |

---

## Hosting Images

For the HTML signatures to work, images need to be hosted online. Options:

1. **Upload to your website:**
   - Upload files to `premierleadmarketing.ai/email-signatures/`
   - Update image URLs in HTML templates

2. **Use Canva:**
   - Export signature as single image
   - Use Canva's sharing link

3. **Use an image hosting service:**
   - Cloudinary, Imgur, or similar
   - Replace `src` URLs in templates

---

## File Structure

```
email-signatures/
├── README.md                    # This file
├── signature-professional.html  # Standard professional template
├── signature-executive.html     # Minimal executive template
├── signature-full-featured.html # Full template with photo & socials
├── signature-compact.html       # Mobile-friendly compact version
├── signature-dark-theme.html    # Dark mode variant
├── logos/
│   ├── plm-logo-full-color.svg
│   ├── plm-logo-dark-bg.svg
│   ├── plm-icon-only.svg
│   ├── plm-logo-horizontal.svg
│   └── plm-logo-stacked.svg
└── icons/
    ├── linkedin.svg
    ├── facebook.svg
    ├── instagram.svg
    ├── twitter-x.svg
    ├── email.svg
    ├── website.svg
    └── phone.svg
```

---

## Support

For questions or additional customization, contact the marketing team.

**Company:** Premier Lead Marketing, LLC
**Website:** [premierleadmarketing.ai](https://premierleadmarketing.ai)
**Email:** andrew@premierleadmarketing.com
