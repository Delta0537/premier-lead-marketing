# Barrett Realty Website

Professional real estate website for Barrett Realty in Mobile, Alabama.

## Setup Instructions

### Required Images

Before deploying, add these images to this folder:

1. **logo.png** - Barrett Realty logo (the BR logo on navy blue background)
2. **owner-photo.jpg** - Photo of the owner for the About page

### Deployment to Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Run: `vercel` in this directory
3. Follow the prompts to deploy

### Local Development

Run a local server:
```bash
npx serve .
```

Then open http://localhost:3000

## Customization

### Contact Information
Update phone numbers and addresses in:
- `index.html` (contact section and footer)
- `about.html` (footer)

### Colors
Primary colors are defined in `styles.css` root variables:
- `--primary: #4a6fa5` - Navy blue (matches logo)
- `--accent: #c9a961` - Gold accent

### Content
- Property listings can be updated in the Properties section of `index.html`
- Testimonials can be edited in the Testimonials section
- About page content is in `about.html`

## Features

- Responsive design (mobile-first)
- Smooth scrolling navigation
- Contact form with validation
- Property listing cards
- Testimonials section
- Call-to-action sections
- SEO optimized meta tags

## Built by Premier Lead Marketing
