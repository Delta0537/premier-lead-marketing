-- Supabase Schema for GHL Integration
-- Run these commands in your Supabase SQL Editor

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Leads table for storing GHL contacts
CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ghl_contact_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(50),
    company VARCHAR(255),
    source VARCHAR(100) DEFAULT 'GHL',
    status VARCHAR(50) DEFAULT 'new',
    tags TEXT[],
    custom_fields JSONB,
    ghl_location_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Opportunities table for GHL pipeline data
CREATE TABLE IF NOT EXISTS opportunities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ghl_opportunity_id VARCHAR(255) UNIQUE NOT NULL,
    lead_id UUID REFERENCES leads(id),
    pipeline_id VARCHAR(255),
    stage_id VARCHAR(255),
    title VARCHAR(255),
    value DECIMAL(10, 2),
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(50),
    source VARCHAR(100) DEFAULT 'GHL',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Activity logs for tracking all GHL webhook events
CREATE TABLE IF NOT EXISTS activity_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB,
    lead_id UUID REFERENCES leads(id),
    opportunity_id UUID REFERENCES opportunities(id),
    source VARCHAR(50) DEFAULT 'n8n',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- GHL API credentials and settings
CREATE TABLE IF NOT EXISTS ghl_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    location_id VARCHAR(255) UNIQUE NOT NULL,
    location_name VARCHAR(255),
    api_key_encrypted TEXT,
    webhook_url VARCHAR(500),
    active BOOLEAN DEFAULT true,
    last_sync TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Automation workflows tracking
CREATE TABLE IF NOT EXISTS automation_workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    trigger_type VARCHAR(100),
    trigger_conditions JSONB,
    actions JSONB,
    active BOOLEAN DEFAULT true,
    execution_count INTEGER DEFAULT 0,
    last_executed TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_leads_ghl_contact_id ON leads(ghl_contact_id);
CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads(created_at);

CREATE INDEX IF NOT EXISTS idx_opportunities_ghl_id ON opportunities(ghl_opportunity_id);
CREATE INDEX IF NOT EXISTS idx_opportunities_lead_id ON opportunities(lead_id);
CREATE INDEX IF NOT EXISTS idx_opportunities_status ON opportunities(status);

CREATE INDEX IF NOT EXISTS idx_activity_logs_event_type ON activity_logs(event_type);
CREATE INDEX IF NOT EXISTS idx_activity_logs_created_at ON activity_logs(created_at);
CREATE INDEX IF NOT EXISTS idx_activity_logs_lead_id ON activity_logs(lead_id);

-- Create updated_at triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_leads_updated_at BEFORE UPDATE ON leads
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_opportunities_updated_at BEFORE UPDATE ON opportunities
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ghl_settings_updated_at BEFORE UPDATE ON ghl_settings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_automation_workflows_updated_at BEFORE UPDATE ON automation_workflows
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Row Level Security (RLS) policies
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE opportunities ENABLE ROW LEVEL SECURITY;
ALTER TABLE activity_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE ghl_settings ENABLE ROW LEVEL SECURITY;
ALTER TABLE automation_workflows ENABLE ROW LEVEL SECURITY;

-- Policy for authenticated users (adjust based on your auth requirements)
CREATE POLICY "Allow authenticated users to read leads" ON leads
    FOR SELECT USING (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated users to insert leads" ON leads
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated users to update leads" ON leads
    FOR UPDATE USING (auth.role() = 'authenticated');

-- Similar policies for other tables
CREATE POLICY "Allow authenticated users full access to opportunities" ON opportunities
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated users full access to activity_logs" ON activity_logs
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated users full access to ghl_settings" ON ghl_settings
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow authenticated users full access to automation_workflows" ON automation_workflows
    FOR ALL USING (auth.role() = 'authenticated');

-- Create views for common queries
CREATE OR REPLACE VIEW leads_with_activity AS
SELECT 
    l.*,
    COUNT(al.id) as activity_count,
    MAX(al.created_at) as last_activity
FROM leads l
LEFT JOIN activity_logs al ON l.id = al.lead_id
GROUP BY l.id;

CREATE OR REPLACE VIEW opportunity_pipeline AS
SELECT 
    o.*,
    l.first_name,
    l.last_name,
    l.email,
    l.phone
FROM opportunities o
JOIN leads l ON o.lead_id = l.id;

-- Sample data for testing
INSERT INTO ghl_settings (location_id, location_name, webhook_url) 
VALUES ('default', 'Premier Lead Marketing', 'http://localhost:5678/webhook/ghl')
ON CONFLICT (location_id) DO NOTHING;