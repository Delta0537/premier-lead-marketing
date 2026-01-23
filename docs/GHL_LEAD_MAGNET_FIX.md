# GoHighLevel Lead Magnet Fix Instructions

## The Problem

Your subdomain `checklist.premierleadmarketing.ai` is returning a 404 error because:

- ✅ DNS is correctly pointing to GoHighLevel
- ✅ Subdomain is connected in GHL
- ❌ **The funnel "TikTok Lead Form - Marketing Audit" has NO pages**

When GHL receives traffic but the funnel is empty, it returns a 404.

---

## Solution: Add a Page to the Funnel

### Option A: Import Existing Page (Recommended)

1. **Log into GoHighLevel** → go to `app.gohighlevel.com`

2. **Navigate to Sites → Funnels**

3. **Find and open "TikTok Lead Form - Marketing Audit"** funnel

4. **Click "+ Add New Step" or "Import"**

5. **Import your existing "Free Marketing Audit Checklist - 47 Points" page** from:
   - "GHL_Lead_Magnet_Landing_Page" funnel, OR
   - "GHL_Lead_Magnet_Page" funnel

6. **Publish the funnel** (ensure the step is set as the default/first step)

7. **Test**: Visit `https://checklist.premierleadmarketing.ai`

---

### Option B: Reassign Domain to Different Funnel

If you want to use a funnel that already has pages:

1. **Go to Settings → Domains** in GoHighLevel

2. **Find `checklist.premierleadmarketing.ai`**

3. **Change the connected funnel** from "TikTok Lead Form - Marketing Audit" to one that has pages:
   - "GHL_Lead_Magnet_Landing_Page"
   - "GHL_Lead_Magnet_Page"
   - Or any other funnel with your checklist page

4. **Save and test**

---

### Option C: Create New Page from Scratch

1. Open "TikTok Lead Form - Marketing Audit" funnel

2. Click "+ Add New Step"

3. Choose "Blank Page" or use a template

4. Design your page with:
   - **Headline**: "Is Your Marketing Costing You $100K+ Per Year?"
   - **Subheadline**: "Get our free 47-point audit checklist..."
   - **Form fields**: First Name, Last Name, Email, Phone, Business Name, Industry
   - **CTA**: "Get Your Free Checklist"
   - **Background**: #000000 (black) to match premierleadmarketing.ai

5. **Style to match** the screenshot you provided (dark theme)

6. Publish and test

---

## After Fixing: Add TikTok Tracking

Once the page is live, add these tracking elements:

### TikTok Pixel (Add to Page Header)

```html
<script>
!function (w, d, t) {
  w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];
  ttq.methods=["page","track","identify","instances","debug","on","off","once","ready","alias","group","enableCookie","disableCookie"];
  ttq.setAndDefer=function(t,e){t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}};
  for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);
  ttq.instance=function(t){for(var e=ttq._i[t]||[],n=0;n<ttq.methods.length;n++)ttq.setAndDefer(e,ttq.methods[n]);return e};
  ttq.load=function(e,n){var i="https://analytics.tiktok.com/i18n/pixel/events.js";ttq._i=ttq._i||{},ttq._i[e]=[],ttq._i[e]._u=i,ttq._i[e]._s=e,ttq._i[e]._p=n||"page",ttq._i[e]._o=ttq._o||{},ttq._t=ttq._t||{},ttq._t[e]=+new Date,ttq._o[e]=n||{};var o=document.createElement("script");o.type="text/javascript",o.async=!0,o.src=i+"?sdkid="+e+"&lib="+t;var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(o,a)};

  ttq.load('YOUR_TIKTOK_PIXEL_ID');  // Replace with your actual TikTok Pixel ID
  ttq.page();
}(window, document, 'ttq');
</script>
```

### Form Submission Tracking (Add to Form Success Action)

```javascript
ttq.track('SubmitForm', {
  content_name: 'Marketing Audit Checklist',
  content_category: 'Lead Magnet'
});
```

### TikTok Ad URL Structure

Use this URL format in your TikTok ads:

```
https://checklist.premierleadmarketing.ai?utm_source=tiktok&utm_medium=paid&utm_campaign={{campaign.name}}&ttclid={{click_id}}
```

---

## Quick Verification Checklist

After making changes:

- [ ] Visit `https://checklist.premierleadmarketing.ai` - should load without 404
- [ ] Form appears correctly with all fields
- [ ] Submit a test lead
- [ ] Check GHL contacts to verify lead came through
- [ ] Verify automation/workflow triggers if configured

---

## Why I (Claude) Can't Fix This Directly

GoHighLevel's API does NOT support:
- Adding pages to funnels
- Changing domain-to-funnel connections
- Modifying funnel structure

These actions **require manual configuration** through the GoHighLevel web interface.

---

## Need More Help?

Use the Claude prompt in `CLAUDE_PROMPT_FOR_GHL.md` to get step-by-step guidance for specific GHL tasks.
