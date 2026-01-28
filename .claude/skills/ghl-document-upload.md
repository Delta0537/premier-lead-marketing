# GHL Document Upload Skill

## Purpose
Upload standardized PLM documents (Proposals, Competitive Analyses) to GoHighLevel for consistent client deliverables.

---

## Standard Document Templates

### 1. Competitive Analysis Template
**Standard Example:** Hampton Law Wins Analysis (First Customer)
**Location:**
- Final PDF: `Business_Operations/PLM_Core/Competitive Analysis & Stageic Plans/Hampton_Law_Competitive_Analysis_ver2.pdf`
- Editable: `Client_Work/Competitive_Analysis_Reports/Templates/Hampton_Law_Analysis_CLEAN.md`

**Required Sections:**
1. Executive Summary with Critical Issues
2. Investment Summary (pricing, what's included)
3. Website Technical Issues Table
4. Google Business Profile Issues
5. Current Marketing Scorecard (1-10 scale)
6. Local Competitor Analysis
7. First 14 Days Action Plan
8. Expected ROI & Timeline
9. Next Steps

### 2. Proposal Template
**Location:** `Business_Operations/PLM_Core/Templates/Proposal_Template.md`
**Final PDF Example:** `Business_Operations/PLM_Core/Competitive Analysis & Stageic Plans/Hampton_Law_Strategic_Proposal_ver2.pdf`

**Required Sections:**
1. The Opportunity (summary)
2. Current Situation
3. The Strategy (deliverables)
4. Expected Results (timeline)
5. Investment (pricing)
6. Why Premier Lead Marketing
7. How We Work Together
8. Client Success Stories
9. FAQs
10. Next Steps & Special Offer

---

## PLM Brand Standards

### Header Format
```
∞ PLM - Strategic Digital Dominance

[DOCUMENT TITLE]

PREPARED FOR:
[Client Name]
[Business Name]
[Location] • [Industry]
[Date]

Premier Lead Marketing, LLC
(251) 367-6948 • andrew@premierleadmarketing.ai
```

### Footer Format
```
∞ PLM - Strategic Digital Dominance
(251) 367-6948
andrew@premierleadmarketing.ai
premierleadmarketing.ai

Thank you for considering Premier Lead Marketing as your digital growth partner.
```

### Color Scheme
- Primary: Deep Blue (#1a365d)
- Accent: Gold/Orange (#d69e2e)
- Text: Dark Gray (#2d3748)
- Background: White (#ffffff)

### Typography
- Headers: Bold, clean sans-serif
- Body: Professional, readable
- Tables: Clear borders, alternating rows

---

## Upload Process to GHL

### Method 1: Media Storage
1. GHL → Media Storage
2. Create folder: "Client Documents" or "Templates"
3. Upload PDF versions of templates
4. Use in emails/automations as attachments

### Method 2: Custom Values for Links
1. GHL → Settings → Custom Values
2. Create values:
   - `{{custom_values.proposal_template_link}}`
   - `{{custom_values.competitive_analysis_link}}`
3. Link to Google Drive or hosted PDFs

### Method 3: Email Templates
1. GHL → Marketing → Emails → Templates
2. Create "Proposal Delivery" template
3. Attach PDF or include download link
4. Use merge fields for personalization

---

## Creating New Client Documents

### Step 1: Copy Template
```bash
# For Competitive Analysis
Copy: Templates/Hampton_Law_Analysis_CLEAN.md
To: Client_Work/Competitive_Analysis_Reports/[CLIENT_NAME]_Analysis.md

# For Proposal
Copy: Templates/Proposal_Template.md
To: Client_Work/Proposals/[CLIENT_NAME]_Proposal.md
```

### Step 2: Replace Placeholders
Replace all bracketed placeholders:
- `[CLIENT_NAME]` → Client's name
- `[BUSINESS_NAME]` → Business name
- `[CITY, STATE]` → Location
- `[INDUSTRY]` → Industry type
- `[PRICE]` → Monthly price
- `[COMPETITOR_X]` → Competitor names
- All metrics, scores, and findings

### Step 3: Generate PDF
- Use Word/Google Docs to format
- Export as PDF
- Save to: `Client_Work/Competitive_Analysis_Reports/Final/[CLIENT_NAME]_Analysis.pdf`

### Step 4: Upload to GHL
- Upload PDF to Media Storage
- Link in email template
- Send to client

---

## SOP: Document Consistency Checklist

Before sending ANY client document:

### Branding ✓
- [ ] PLM logo/header present
- [ ] Correct phone number: (251) 367-6948
- [ ] Correct email: andrew@premierleadmarketing.ai
- [ ] "Strategic Digital Dominance ∞" tagline
- [ ] Professional footer

### Content ✓
- [ ] All placeholders replaced
- [ ] Pricing accurate
- [ ] Competitor data current
- [ ] Metrics make sense
- [ ] No typos or errors

### Format ✓
- [ ] Tables properly formatted
- [ ] Consistent fonts
- [ ] Proper headings hierarchy
- [ ] Page breaks appropriate
- [ ] PDF quality check

### Delivery ✓
- [ ] Client name correct
- [ ] Date current
- [ ] Attached to email
- [ ] Follow-up scheduled

---

## Files Reference

| Document Type | Template Location | Example |
|---------------|-------------------|---------|
| Competitive Analysis | `Templates/Competitive_Analysis_Template.md` | Hampton Law Analysis |
| Proposal | `Templates/Proposal_Template.md` | Hampton Law Proposal |
| Final PDFs | `Competitive Analysis & Stageic Plans/` | `Hampton_Law_*_ver2.pdf` |

---

## Usage Commands

- `/upload-doc competitive [client]` - Create competitive analysis for client
- `/upload-doc proposal [client]` - Create proposal for client
- `/upload-doc template` - Show available templates
- `/upload-doc checklist` - Run consistency checklist
