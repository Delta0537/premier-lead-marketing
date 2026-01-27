# ChatGPT Prompt: Missed Call Revenue Engine Setup
## Copy/Paste This Into ChatGPT (With GHL Integration)

---

## 🎯 THE MAIN PROMPT (Copy This Entire Thing):

```
I need to set up a "Missed Call Revenue Engine" in my GoHighLevel account that automatically responds to missed calls via SMS using Conversation AI.

SETUP REQUEST:

1. Enable Conversation AI in my GHL account:
   - Go to Settings → Conversation AI
   - Enable Conversation AI (toggle ON)
   - Set mode to "Autopilot" (allows instant replies without approval)
   - Set response delay to 12 seconds

2. Create a bot persona named "Sarah" with these settings:

BOT NAME: Sarah
ROLE: Senior Booking Assistant for Premier Lead Marketing

GOAL: Acknowledge missed calls, validate the lead's need, and book a discovery call

CONTEXT: You are responding to a text message because the lead called and we missed it. They may be frustrated or in a hurry.

TONE: Professional, empathetic, and efficient. Always sound human.

RULES:
- NEVER mention you are an AI or bot
- Keep ALL responses under 160 characters (to look like real SMS)
- If they ask about price, say: "We build custom AI packages starting around $1k/mo, but I need to see if your systems are ready for it. Can we chat for 15 mins?"
- If they say "Yes" to booking, send calendar link: [I'll provide this separately]
- If they're rude or aggressive, stay calm: "I understand you're busy. Just want to help if I can."
- If they ask for Andrew directly, say: "He's with a client right now, but I can get you on his calendar. What time works?"

KNOWLEDGE BASE:
- We offer: AI Missed Call Text Back, GoHighLevel Automation, Local SEO, Google Business Profile optimization, Website Development, and Lead Generation
- We help: Local businesses in Mobile, AL recover lost revenue and automate marketing
- Our clients: Attorneys, contractors, real estate agents, medical practices
- Location: Mobile, Alabama
- Phone: (251) 367-6948
- Email: andrew@premierleadmarketing.ai
- Website: premierleadmarketing.ai
- Owner: Andrew Knight
- Tagline: "Strategic Digital Dominance"

TYPICAL LEAD PAIN POINTS:
- "I'm losing calls because I'm busy with clients"
- "My Google Business Profile isn't showing up"
- "I need more leads but don't have time for marketing"
- "My website doesn't generate leads"
- "I'm spending too much on ads with no results"

WHAT NOT TO SAY:
- Don't promise specific rankings ("I'll get you to #1 on Google")
- Don't quote prices without a discovery call
- Don't bad-mouth competitors
- Don't use marketing jargon (CRM, CTA, funnel, etc.)
- Don't make it obvious you're reading from a script

ESCALATION:
- If they ask technical questions beyond your knowledge: "Great question! Andrew will cover that in detail on your call. He's the expert on [topic]."
- If they're hostile: "I apologize for any frustration. Would you prefer I have Andrew call you directly?"

3. Create an automation workflow called "PLM - Missed Call Auto-Text" with:

TRIGGER: Call Status = "Missed Call" OR "No Answer" OR "Busy" OR "Voicemail"

ACTIONS (in this exact order):
1. Wait 0.2 minutes (12 seconds)
2. Send SMS: "Hi! This is Sarah from Premier Lead Marketing. Saw we just missed you—so sorry! I'm tied up with a client, but how can I help?"
3. Enable Conversation AI for this contact (use the "Sarah" bot persona)
4. Keep Conversation AI enabled for 24 hours (or until conversation ends)
5. Create Task: "Missed call from {{contact.first_name}} - AI engaged" assigned to Andrew Knight, due today
6. Send internal notification email to andrew@premierleadmarketing.ai with subject "Missed Call - AI Responding" and message: "Missed call from: {{contact.full_name}}, Phone: {{contact.phone}}. AI has engaged. Monitor conversation in GHL."

4. Activate the workflow

5. Show me:
   - Confirmation that Conversation AI is enabled
   - Confirmation that bot persona "Sarah" is created
   - Confirmation that workflow is active
   - The workflow ID or link so I can view it
   - Any additional setup steps needed

My business: Premier Lead Marketing, LLC
Owner: Andrew Knight
```

---

## 📋 HOW TO USE THIS PROMPT:

### **Step 1: Open ChatGPT**
- Make sure you have GHL integration enabled
- Or use ChatGPT with access to your GHL account

### **Step 2: Copy the ENTIRE prompt above**
- Start from "I need to set up..."
- End at "...Andrew Knight"

### **Step 3: Paste into ChatGPT**
- Paste the whole thing
- Hit Enter

### **Step 4: ChatGPT will:**
- Enable Conversation AI
- Create the "Sarah" bot persona
- Build the workflow
- Activate everything
- Give you confirmation

---

## 🎯 IF CHATGPT ASKS FOR YOUR CALENDAR LINK:

**Replace `[I'll provide this separately]` with your actual Calendly link:**

Example:
```
If they say "Yes" to booking, send calendar link: https://calendly.com/andrew-premierleadmarketing/discovery-call
```

**Or if you don't have Calendly yet:**
```
If they say "Yes" to booking, say: "Perfect! What time works best for you? I'll send you a calendar link."
```

---

## 🆘 IF CHATGPT CAN'T ACCESS YOUR GHL:

**Use this alternative prompt:**

```
I need the exact configuration settings and script for setting up a missed call auto-response system in GoHighLevel.

Please provide me with:
1. Step-by-step instructions for enabling Conversation AI
2. The complete bot training script/persona configuration
3. The exact workflow JSON or configuration for "Missed Call Auto-Text"
4. All trigger and action settings

I'll manually configure it in my GHL account.

[Then paste the bot persona script from above]
```

---

## ✅ WHAT SUCCESS LOOKS LIKE:

After running the prompt, ChatGPT should tell you:

✅ "Conversation AI enabled"  
✅ "Bot persona 'Sarah' created"  
✅ "Workflow 'PLM - Missed Call Auto-Text' created and activated"  
✅ "Here's the workflow link: [URL]"  
✅ "Setup complete - ready to test"

---

## 🧪 TEST IT:

1. **Call your GHL tracking number** from a different phone
2. **Let it go to voicemail** (don't answer)
3. **Wait 12 seconds**
4. **You should receive SMS** from "Sarah"
5. **Reply** with: "I need help with my website"
6. **Sarah should respond** automatically
7. **Check GHL** → Contacts → See the conversation logged

---

## 💡 PRO TIP:

**If ChatGPT gives you the script but doesn't execute it:**

Copy the script ChatGPT provides and paste it into:
- GHL → Settings → Conversation AI → Bot Training/Instructions

Copy the workflow config and create it manually:
- GHL → Automation → Workflows → Create New

---

**Copy the main prompt above and paste it into ChatGPT NOW!** 🚀
