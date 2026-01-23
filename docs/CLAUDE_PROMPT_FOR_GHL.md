# Claude Prompt for GoHighLevel Configuration

Copy and paste this prompt to get Claude to help you with GoHighLevel configuration step-by-step.

---

## THE PROMPT (Copy Everything Below This Line)

---

I need help configuring my GoHighLevel (GHL) account. I'm a marketing agency owner and I have a lead magnet landing page that needs to work on a subdomain.

**My Current Situation:**
- Main website: `premierleadmarketing.ai` (runs on Vercel)
- Lead magnet subdomain: `checklist.premierleadmarketing.ai` (runs on GoHighLevel)
- Problem: The subdomain returns a 404 error

**What I've Verified:**
- DNS is correctly configured and pointing to GoHighLevel
- The subdomain is connected in GHL Settings → Domains
- The subdomain is linked to a funnel called "TikTok Lead Form - Marketing Audit"
- **THE ISSUE**: The funnel is EMPTY - it has no pages in it

**What I Need Help With:**

1. **Walk me through adding a page to my funnel step-by-step**
   - I want to either import my existing "Free Marketing Audit Checklist - 47 Points" page from another funnel
   - OR create a new page from scratch with this content:
     - Headline: "Is Your Marketing Costing You $100K+ Per Year?"
     - Subheadline: "Get our free 47-point audit checklist and discover exactly what's broken in your marketing (and how to fix it)."
     - Benefits list with checkmarks
     - Form with fields: First Name, Last Name, Email, Phone, Business Name, Industry dropdown
     - Dark background (#000000) to match my main site
     - PLM branding

2. **After the page is created, help me:**
   - Set up TikTok pixel tracking
   - Configure form submission actions (add to contact list, trigger automation)
   - Set up proper UTM parameter tracking for ad attribution

3. **Give me exact click-by-click instructions** as if you're looking over my shoulder. Tell me:
   - Exactly what to click
   - What each button looks like
   - What I should see at each step
   - What to type/select

**My GoHighLevel Account:**
- I have admin access to my GHL agency account
- I'm using the web interface at app.gohighlevel.com
- I can share screenshots if needed

**Design Reference:**
The lead magnet page should look like this (dark theme):
- PLM logo at top
- Large cyan/teal headline text
- White body text
- Dark (#1a1a1a or #000000) background
- Form on the right side with dark input fields
- Benefits checkmarks in green/cyan

Please start by giving me the exact steps to add a page to my "TikTok Lead Form - Marketing Audit" funnel. Be specific about what I'll see in the GHL interface.

---

## END OF PROMPT

---

## Additional Prompts for Specific Tasks

### For Setting Up TikTok Pixel:

```
I have my lead magnet page live in GoHighLevel. Now I need to add TikTok pixel tracking.

My TikTok Pixel ID is: [YOUR_PIXEL_ID]

Walk me through:
1. Where to paste the TikTok pixel code in GHL page settings
2. How to set up form submission tracking (SubmitForm event)
3. How to test that the pixel is firing correctly

Give me exact click paths like: Settings → Tracking Code → Header → [paste here]
```

### For Setting Up Form Automations:

```
My GHL lead magnet form is working. Now I need to set up what happens after someone submits:

1. Add them to a specific contact list/tag
2. Send an immediate email with the checklist PDF
3. Add them to a nurture sequence
4. Send me a Slack notification of new leads

Walk me through setting this up in GHL Automations/Workflows.
```

### For Connecting Domain to Different Funnel:

```
I want to change which funnel my subdomain points to in GoHighLevel.

Current setup:
- Subdomain: checklist.premierleadmarketing.ai
- Currently connected to: "TikTok Lead Form - Marketing Audit" (empty funnel)
- Want to connect to: "GHL_Lead_Magnet_Landing_Page" (has pages)

Walk me through changing this in GHL Settings → Domains step by step.
```

### For Debugging 404 Errors:

```
My GHL subdomain is giving a 404 error. I've verified:
- DNS is pointing to GHL
- Domain is added in GHL Settings → Domains
- Domain is connected to a funnel

What else could cause this? Walk me through:
1. Checking if the funnel has a published page
2. Verifying the funnel step is set as default
3. Checking SSL certificate status
4. Any other common 404 causes in GHL
```

---

## Tips for Getting Better Help from Claude

1. **Share screenshots** when possible - Claude can analyze them
2. **Be specific** about what you see on screen vs what you expect
3. **Copy error messages** exactly as they appear
4. **Mention your GHL plan** (Agency, SaaS mode, etc.) as features vary
5. **Ask for alternatives** if a step doesn't match what you see (GHL updates their UI frequently)
