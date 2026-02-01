# GHL Webhook Configuration Guide

## 🔗 Setting Up GHL Webhooks for n8n Integration

### Step 1: Access GHL Settings
1. Log into your GHL account
2. Go to **Settings** → **Integrations** → **Webhooks**
3. Click **"Add Webhook"**

### Step 2: Configure Webhook Endpoints

#### Contact Creation Webhook
- **Event Type**: `ContactCreate`
- **URL**: `http://localhost:5678/webhook/ghl-lead-webhook`
- **Method**: `POST`
- **Headers**: 
  ```
  Content-Type: application/json
  X-Webhook-Secret: your_webhook_secret_key
  ```

#### Opportunity Webhooks
- **Event Type**: `OpportunityCreate`
- **URL**: `http://localhost:5678/webhook/ghl-opportunity-webhook`
- **Method**: `POST`

#### Additional Useful Webhooks
- `ContactUpdate` → `http://localhost:5678/webhook/ghl-contact-update`
- `OpportunityStageUpdate` → `http://localhost:5678/webhook/ghl-stage-update`
- `TaskCompleted` → `http://localhost:5678/webhook/ghl-task-complete`
- `AppointmentCreate` → `http://localhost:5678/webhook/ghl-appointment`

### Step 3: Production Setup (When Ready)

For production deployment, replace `localhost` with your actual domain:
- **Webhook URL**: `https://yourdomain.com/webhook/ghl-lead-webhook`
- **SSL Required**: Yes
- **Authentication**: Use webhook secrets for validation

### Step 4: Testing Webhooks

#### Test Data Structure
GHL sends data in this format:
```json
{
  "type": "ContactCreate",
  "locationId": "your-location-id",
  "id": "contact-id-123",
  "email": "test@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "phone": "+1234567890",
  "tags": ["lead", "website"],
  "customFields": {
    "source": "landing-page"
  },
  "dateAdded": "2026-02-01T12:00:00Z"
}
```

### Step 5: n8n Webhook URLs

Once your n8n is running, these are your webhook endpoints:

| Purpose | Endpoint | Description |
|---------|----------|-------------|
| Lead Capture | `/webhook/ghl-lead-webhook` | New contacts from GHL |
| Opportunity Updates | `/webhook/ghl-opportunity-webhook` | Pipeline changes |
| Contact Updates | `/webhook/ghl-contact-update` | Contact modifications |
| Appointment Booking | `/webhook/ghl-appointment` | New appointments |
| Task Completion | `/webhook/ghl-task-complete` | Task status updates |

### Step 6: Security Configuration

#### Webhook Secret Validation
Add this to your n8n workflow:
```javascript
// Validate webhook secret
const receivedSecret = $request.headers['x-webhook-secret'];
const expectedSecret = $env.GHL_WEBHOOK_SECRET;

if (receivedSecret !== expectedSecret) {
  throw new Error('Invalid webhook secret');
}
```

#### IP Whitelist (Optional)
Add GHL's webhook IPs to your firewall if using production server.

### Step 7: Troubleshooting

#### Common Issues:
1. **Webhook not firing**: Check GHL webhook logs
2. **n8n not receiving**: Verify URL and port accessibility
3. **Data not saving**: Check Supabase connection and schema
4. **Authentication errors**: Verify API keys and secrets

#### Debug Steps:
1. Check n8n execution logs
2. Verify Docker containers are running: `docker-compose ps`
3. Test webhook manually with curl:
```bash
curl -X POST http://localhost:5678/webhook/ghl-lead-webhook \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Secret: your_secret" \
  -d '{"type":"ContactCreate","email":"test@example.com"}'
```

### Step 8: Advanced Automations

Once basic webhooks work, you can add:
- **Email sequences** triggered by lead status
- **SMS notifications** for high-value opportunities  
- **Slack alerts** for urgent leads
- **Google Sheets sync** for reporting
- **Zapier integrations** for additional tools

## 🚀 Quick Start Commands

1. **Start the integration**:
   ```bash
   .\setup-integration.ps1
   ```

2. **Check service status**:
   ```bash
   docker-compose ps
   ```

3. **View n8n logs**:
   ```bash
   docker-compose logs -f n8n
   ```

4. **Stop services**:
   ```bash
   docker-compose down
   ```

Your GHL → n8n → Supabase pipeline will automatically:
✅ Capture leads from GHL
✅ Store them in your Supabase database  
✅ Log all activity for tracking
✅ Enable real-time automation workflows
✅ Connect to your Lovable frontend dashboard