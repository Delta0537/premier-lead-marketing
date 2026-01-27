# Missed Call Revenue Engine - Implementation Guide
## Premier Lead Marketing - Complete Setup

**Strategy Source:** AI Marketing Website SEO & Case Study  
**Implementation Date:** January 2026  
**Tech Stack:** Next.js 14 + GoHighLevel + GTM + Vercel

---

## 🎯 OVERVIEW: The Assembly Line Approach

This strategy treats AI tools as specialized employees:

1. **Claude (Me)** = Architect/Strategist
2. **Cursor** = Builder/Developer
3. **ChatGPT (GHL Native)** = Sales Agent

**Goal:** Automate lead capture and follow-up to recover 80% of missed opportunities.

---

## 📋 PHASE 1: THE ARCHITECT → THE BUILDER

### Step 1: Configure Cursor for SEO/AEO-Optimized Code

**File Created:** `C:\ideas\Digital Marketing\Premier Lead Marketing\website\.cursorrules`

**What it does:**
- Tells Cursor how to code so you don't have to constantly correct it
- Enforces SEO best practices automatically
- Ensures all pages are optimized for AI search engines (ChatGPT, Perplexity, Google AI)
- Mandates proper Schema.org structured data
- Implements tracking on all CTAs

**How to use it:**

1. **Copy the `.cursorrules` file** to your website project root:
   ```
   C:\ideas\Digital Marketing\Premier Lead Marketing\website\.cursorrules
   ```

2. **Restart Cursor** (File → Exit, then reopen)

3. **Verify it's working:**
   - Open Cursor
   - Hit Cmd+I (Mac) or Ctrl+I (Windows) for Composer
   - Type: "Build a service page for Local SEO"
   - Cursor should automatically include metadata, Schema.org, and tracking

---

### Step 2: The "Composer" Workflow (Building with Cursor)

**Cursor Composer Mode** is your power tool. Use it for all site features.

#### How to Use Composer:

**Open Composer:**
- Mac: `Cmd + I`
- Windows: `Ctrl + I`

**Paste Strategic Prompts:**

Instead of saying "build a contact form", use this mega-prompt format:

```
Build a contact form for Premier Lead Marketing with these requirements:

FUNCTIONALITY:
- Server Action for form handling (no API route)
- Zod validation for all fields
- Connect to GHL webhook: [WEBHOOK_URL]
- Fire GTM event "form_submit" on success
- Show loading spinner during submission
- Display success/error toast notifications

FIELDS:
- First Name (required)
- Last Name (required)
- Business Name (required)
- Phone (required, US format)
- Email (required)
- Industry (dropdown)
- Message (textarea)
- Honeypot field (hidden, spam protection)

DESIGN:
- Match existing site design (dark theme, cyan accents)
- Mobile-first, responsive
- Proper focus states for accessibility
- Error messages inline under fields

TRACKING:
- data-event="form_submit"
- data-category="contact"
- Track field completion rates

Following .cursorrules standards.
```

#### If Cursor Gets Stuck:

**Option 1: Switch Model**
- Click model dropdown in Cursor
- Select `claude-3.5-sonnet` (if available)

**Option 2: Refine with Claude**
- Copy Cursor's output
- Paste into Claude (me) with prompt:
  ```
  Refactor this code to ensure:
  1. JSON-LD schema nests Service inside LocalBusiness properly
  2. generateMetadata uses answer-first descriptions
  3. All CTA buttons have proper tracking attributes
  
  [PASTE CODE HERE]
  ```

---

## 📋 PHASE 2: THE SALES ENGINE (GoHighLevel Native AI)

### What is "Conversation AI"?

GHL's native ChatGPT integration. It responds to missed calls via SMS automatically.

**Key Feature:** "Autopilot" mode replies WITHOUT your approval = instant response.

---

### Step 1: Enable Conversation AI in GHL

1. **Login to GoHighLevel**

2. **Navigate to:**
   - Settings → Conversation AI
   - (Or: Settings → AI → Conversation AI)

3. **Enable Conversation AI:**
   - Toggle: **ON**

4. **Set Mode:**
   - Select: **"Autopilot"**
   - ⚠️ Important: Autopilot allows instant replies without your approval

5. **Set Response Delay:**
   - Recommended: **12 seconds** (looks natural, not instant-bot)

---

### Step 2: Configure Bot Persona

**In the "Bot Training" or "Instructions" field, paste this:**

```
Name: Sarah

Role: Senior Booking Assistant for Premier Lead Marketing

Goal: Acknowledge missed calls, validate the lead's need, and book a discovery call

Context: You are responding to a text message because the lead called and we missed it. They may be frustrated or in a hurry.

Tone: Professional, empathetic, and efficient. Always sound human.

Rules:
1. NEVER mention you are an AI or bot
2. Keep ALL responses under 160 characters (to look like real SMS)
3. If they ask about price, say: "We build custom AI packages starting around $1k/mo, but I need to see if your systems are ready for it. Can we chat for 15 mins?"
4. If they say "Yes" to booking, send calendar link: [YOUR_CALENDLY_LINK]
5. If they're rude or aggressive, stay calm: "I understand you're busy. Just want to help if I can."
6. If they ask for Andrew directly, say: "He's with a client right now, but I can get you on his calendar. What time works?"

Opening Message (will be configured in workflow):
"Hi! This is Sarah with Premier Lead Marketing. I saw we just missed your call—so sorry about that! How can I help?"

Knowledge Base:
- We offer: AI Missed Call Text Back, GoHighLevel Automation, Local SEO, Google Business Profile optimization, Website Development, and Lead Generation
- We help: Local businesses in Mobile, AL recover lost revenue and automate marketing
- Our clients: Attorneys, contractors, real estate agents, medical practices
- Location: Mobile, Alabama
- Phone: (251) 367-6948
- Email: andrew@premierleadmarketing.ai
- Website: premierleadmarketing.ai
- Owner: Andrew Knight
- Tagline: "Strategic Digital Dominance"

Typical lead pain points:
- "I'm losing calls because I'm busy with clients"
- "My Google Business Profile isn't showing up"
- "I need more leads but don't have time for marketing"
- "My website doesn't generate leads"
- "I'm spending too much on ads with no results"

What NOT to say:
- Don't promise specific rankings ("I'll get you to #1 on Google")
- Don't quote prices without a discovery call
- Don't bad-mouth competitors
- Don't use marketing jargon (CRM, CTA, funnel, etc.)
- Don't make it obvious you're reading from a script

Escalation:
- If they ask technical questions beyond your knowledge: "Great question! Andrew will cover that in detail on your call. He's the expert on [topic]."
- If they're hostile: "I apologize for any frustration. Would you prefer I have Andrew call you directly?"
```

---

### Step 3: Create the "Missed Call Auto-Text" Workflow

**This is the magic that makes it all work.**

#### Create Workflow:

1. **Go to:** Automation → Workflows
2. **Click:** + Create Workflow
3. **Name:** "PLM - Missed Call Auto-Text"
4. **Click:** Create

#### Configure Trigger:

**Trigger Type:** Call Status

**Settings:**
- Select: **"Missed Call"** or **"No Answer"**
- Also select: **"Busy"** and **"Voicemail"** (if available)
- Filter by phone number (optional): Your GHL tracking number

**Save Trigger**

#### Add Actions (In This Order):

**ACTION 1: Wait**
- **Type:** Wait
- **Duration:** 0.2 Minutes (12 seconds)
- **Why:** Feels natural, not instant-bot

**ACTION 2: Send SMS**
- **Type:** SMS
- **Message:**
  ```
  Hi! This is Sarah from Premier Lead Marketing. Saw we just missed you—so sorry! I'm tied up with a client, but how can I help?
  ```
- **From:** Your GHL phone number

**ACTION 3: Enable Conversation AI**
- **Type:** Conversation AI
- **Action:** Turn ON for this contact
- **Bot:** Select your "Sarah" bot (configured in Step 2)
- **Duration:** Keep enabled for 24 hours (or until conversation ends)

**ACTION 4: Create Task (Optional)**
- **Type:** Task
- **Description:** "Missed call from {{contact.first_name}} - AI engaged"
- **Assigned to:** You (Andrew Knight)
- **Due:** Today

**ACTION 5: Internal Notification (Optional)**
- **Type:** Email or SMS
- **To:** andrew@premierleadmarketing.ai (or your personal phone)
- **Subject:** "Missed Call - AI Responding"
- **Message:**
  ```
  Missed call from: {{contact.full_name}}
  Phone: {{contact.phone}}
  AI has engaged. Monitor conversation in GHL.
  ```

#### Activate Workflow:

- **Toggle:** Set to **ACTIVE** (top right)
- **Test:** Have someone call your GHL number, let it go to voicemail, wait for text

---

### Step 4: Test the Missed Call Engine

**Run a live test:**

1. **Call your GHL tracking number** from a different phone
2. **Let it ring** until it goes to voicemail
3. **Wait 12 seconds**
4. **You should receive SMS** from "Sarah"
5. **Reply with:** "I need help with my website"
6. **Verify:** Conversation AI responds automatically
7. **Check GHL:** Contact should be created, conversation logged, task created

**If it doesn't work:**
- Verify Conversation AI is in "Autopilot" mode
- Check workflow is ACTIVE
- Verify trigger phone number matches
- Check GHL phone settings (SMS must be enabled)

---

## 📋 PHASE 3: THE FEEDBACK LOOP (Tracking & Analytics)

### Goal: Connect Vercel site → GHL → Prove ROI

---

### Step 1: Create GTM Component for Next.js

**Ask Cursor to build this:**

```
Create a client component GoogleTagManager.tsx using @next/third-parties

Requirements:
- Accept GTM ID from environment variable (NEXT_PUBLIC_GTM_ID)
- Use @next/third-parties/google package
- Include noscript fallback
- Should be imported in root layout.tsx
- Add TypeScript types
- Include comments explaining usage

Following .cursorrules standards.
```

**Cursor will generate:**
- `components/GoogleTagManager.tsx` (Client Component)
- Proper TypeScript types
- Environment variable handling
- Usage instructions

**Then add to your `.env.local`:**
```
NEXT_PUBLIC_GTM_ID=GTM-XXXXXXX
```

*(Get GTM ID from Google Tag Manager)*

---

### Step 2: Connect GHL Forms to Website

You have 2 options:

#### Option A: GHL Form Embed (Easier, Slower)

**Pros:**
- No coding required
- Updates automatically in GHL

**Cons:**
- Loads slower (iframe)
- Less control over design
- Can't fire custom GTM events easily

**How:**
1. Create form in GHL
2. Get embed code
3. Paste in your Next.js page (in a Client Component)

#### Option B: Custom Form → GHL Webhook (Recommended)

**Pros:**
- 300% faster load time (better SEO)
- Full design control
- Fire GTM events on submit
- Better mobile experience

**Cons:**
- Requires coding (but Cursor does it for you)

**How:**

**Get GHL Webhook URL:**
1. In GHL: Automation → Webhooks
2. Click: + Create Webhook
3. Name: "Website Contact Form"
4. Copy: Webhook URL

**Ask Cursor:**
```
Build a custom contact form that submits to this GHL webhook:
[PASTE_WEBHOOK_URL]

Requirements:
- Server Action for submission
- Send data as JSON to webhook
- Include all form fields
- Fire GTM event "form_submit" with data layer push
- Show loading state during submission
- Display success/error messages
- Handle network errors gracefully
- Match website design (dark theme, cyan accents)

Fields: First Name, Last Name, Business Name, Phone, Email, Industry, Message

Following .cursorrules standards.
```

**Cursor will build:**
- Form component with validation
- Server Action that posts to GHL webhook
- GTM event tracking
- Loading/error states
- Proper TypeScript types

---

### Step 3: Set Up Conversion Tracking

**In GTM, create these tags:**

**Tag 1: Form Submission**
- **Tag Type:** Custom HTML
- **Trigger:** Custom Event = `form_submit`
- **HTML:**
  ```html
  <script>
    dataLayer.push({
      'event': 'conversion',
      'conversion_type': 'form_submit',
      'conversion_value': 500
    });
  </script>
  ```

**Tag 2: Phone Click**
- **Tag Type:** Custom HTML
- **Trigger:** Click = element matches `a[href^="tel:"]`
- **HTML:**
  ```html
  <script>
    dataLayer.push({
      'event': 'conversion',
      'conversion_type': 'phone_click'
    });
  </script>
  ```

**Tag 3: Calendar Booking**
- **Tag Type:** Custom HTML  
- **Trigger:** Custom Event = `calendar_book`
- **HTML:**
  ```html
  <script>
    dataLayer.push({
      'event': 'conversion',
      'conversion_type': 'calendar_book',
      'conversion_value': 1000
    });
  </script>
  ```

---

### Step 4: Measure Success (The Efficiency Proof)

**Track these metrics:**

**In GHL:**
- Missed calls recovered (%)
- Response time (should be ~12 seconds)
- Conversations → Appointments booked (%)
- AI conversation → Human takeover rate

**In GTM/GA4:**
- Form submission rate
- Phone click rate
- Calendar booking rate
- Traffic → Lead conversion rate

**Calculate ROI:**
```
Missed Calls Before AI: 10/week = 40/month
Recovery Rate with AI: 80% = 32 recovered
Booking Rate: 25% = 8 appointments
Close Rate: 30% = 2.4 new clients
Avg Client Value: $500/month × 12 months = $6,000
Monthly Revenue from AI: 2.4 × $6,000 = $14,400

Cost of System: ~$300/month (GHL + development amortized)
ROI: 4,700%
```

---

## 🚀 IMPLEMENTATION CHECKLIST

### Phase 1: Cursor Setup
- [ ] Copy `.cursorrules` to website root directory
- [ ] Restart Cursor
- [ ] Test Composer with simple prompt
- [ ] Verify SEO metadata is auto-generated

### Phase 2: GHL Conversation AI
- [ ] Enable Conversation AI in GHL
- [ ] Set mode to "Autopilot"
- [ ] Paste "Sarah" bot persona/training
- [ ] Create "Missed Call Auto-Text" workflow
- [ ] Configure trigger (Call Status = Missed)
- [ ] Add actions (Wait → SMS → Enable AI)
- [ ] Activate workflow
- [ ] **TEST with real phone call**

### Phase 3: Tracking & Forms
- [ ] Get GTM ID from Google Tag Manager
- [ ] Ask Cursor to build GTM component
- [ ] Add GTM_ID to environment variables
- [ ] Get GHL webhook URL
- [ ] Ask Cursor to build custom form → webhook
- [ ] Set up GTM conversion tags
- [ ] Test form submission end-to-end
- [ ] Verify lead appears in GHL

### Phase 4: Monitor & Optimize
- [ ] Check AI conversations daily (first week)
- [ ] Review missed call recovery rate
- [ ] Adjust bot responses based on real conversations
- [ ] Track conversion rates (form, phone, calendar)
- [ ] Calculate ROI monthly

---

## 🆘 TROUBLESHOOTING

### "Conversation AI isn't responding"
- Verify "Autopilot" mode is ON
- Check bot training is saved
- Ensure workflow is ACTIVE
- Test trigger (make sure missed call fires it)
- Check GHL SMS credits (need credits to send)

### "Cursor isn't following .cursorrules"
- Restart Cursor completely
- Verify .cursorrules is in project ROOT (not subdirectory)
- Use Composer mode (Cmd/Ctrl + I), not inline autocomplete
- Check Cursor settings → Rules → Enabled

### "GHL webhook not receiving form data"
- Test webhook URL in Postman first
- Check Server Action is POSTing correct JSON format
- Verify webhook is active in GHL
- Check GHL webhook logs for errors
- Ensure CORS isn't blocking (GHL should allow all origins)

### "GTM events not firing"
- Check GTM container is published (not draft)
- Use GTM Preview mode to debug
- Verify dataLayer.push() syntax
- Check browser console for errors
- Ensure GTM_ID environment variable is correct

---

## 📊 SUCCESS METRICS (90 Days)

### Week 1-2: Setup & Testing
- All systems operational
- AI responding to 100% of missed calls
- Forms submitting to GHL correctly

### Week 3-4: Optimization
- AI conversation quality improving
- Response templates refined based on real interactions
- Conversion tracking validated

### Month 2: Momentum
- 80%+ missed call recovery rate
- 15-25% booking rate from AI conversations
- 3-5 new clients from recovered calls

### Month 3: Proof
- ROI calculated and documented
- Case study created from real data
- System runs on autopilot with minimal intervention

---

## 💡 PRO TIPS

### For Cursor:
- Always use Composer mode for complex features
- Reference .cursorrules in your prompts: "Following .cursorrules standards"
- Use claude-3.5-sonnet model if available (better at architecture)

### For Conversation AI:
- Monitor first 20 conversations closely
- Refine bot responses based on real questions
- Add common objections to Knowledge Base
- Keep responses SHORT (under 160 chars)

### For Forms:
- Custom form > GHL embed (for performance)
- Fire GTM events BEFORE webhook call (in case webhook fails)
- Include honeypot field to reduce spam

### For Tracking:
- Set up weekly reports in GTM/GA4
- Compare before/after AI implementation
- Document success stories for marketing

---

## 🎯 NEXT ACTIONS

**TODAY:**
1. Copy `.cursorrules` to website project
2. Enable Conversation AI in GHL
3. Create "Sarah" bot persona

**THIS WEEK:**
1. Build missed call workflow
2. Test with real phone calls
3. Ask Cursor to build GTM component

**THIS MONTH:**
1. Build custom form → GHL webhook
2. Set up conversion tracking
3. Monitor and optimize AI responses

---

**This is your competitive advantage. Most agencies talk about AI - you're actually using it to scale.** 🚀
