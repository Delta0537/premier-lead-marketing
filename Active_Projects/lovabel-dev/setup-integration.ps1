# GHL + n8n + Supabase Integration Setup Script
# Run this script to set up your automation environment

Write-Host "🚀 Setting up GHL + n8n + Supabase Integration..." -ForegroundColor Green

# Check if Docker is running
Write-Host "📋 Checking Docker status..." -ForegroundColor Yellow
try {
    $dockerInfo = docker info 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker is running" -ForegroundColor Green
    } else {
        Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Docker is not installed or not running." -ForegroundColor Red
    exit 1
}

# Create .env file from template
Write-Host "📋 Setting up environment variables..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.n8n" ".env"
    Write-Host "⚠️  Created .env file from template. Please edit it with your actual API keys!" -ForegroundColor Yellow
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

# Pull Docker images
Write-Host "📋 Pulling Docker images..." -ForegroundColor Yellow
docker-compose pull

# Start the services
Write-Host "🚀 Starting services..." -ForegroundColor Green
docker-compose up -d

# Wait for services to start
Write-Host "⏳ Waiting for services to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check service status
Write-Host "📋 Checking service status..." -ForegroundColor Yellow
$services = @("n8n", "redis")
foreach ($service in $services) {
    $status = docker-compose ps -q $service
    if ($status) {
        Write-Host "✅ $service is running" -ForegroundColor Green
    } else {
        Write-Host "❌ $service failed to start" -ForegroundColor Red
    }
}

# Display access information
Write-Host ""
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host "📊 n8n Dashboard: http://localhost:5678" -ForegroundColor Cyan
Write-Host "🗄️  Redis: localhost:6379" -ForegroundColor Cyan
Write-Host "🌐 Your Lovable Site: http://localhost:3333" -ForegroundColor Cyan
Write-Host "🗃️  Supabase Dashboard: https://supabase.com/dashboard/project/kixghhmqnnnkhiuminoe" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔐 Default n8n login:" -ForegroundColor Yellow
Write-Host "   Username: admin" -ForegroundColor White
Write-Host "   Password: (check your .env file)" -ForegroundColor White
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Edit the .env file with your GHL API keys" -ForegroundColor White
Write-Host "2. Run the Supabase schema: supabase-ghl-schema.sql" -ForegroundColor White
Write-Host "3. Configure GHL webhooks to point to: http://localhost:5678/webhook/ghl" -ForegroundColor White
Write-Host "4. Import the GHL workflow in n8n dashboard" -ForegroundColor White
Write-Host ""
Write-Host "🛠️  Commands:" -ForegroundColor Yellow
Write-Host "   Stop services: docker-compose down" -ForegroundColor White
Write-Host "   View logs: docker-compose logs -f" -ForegroundColor White
Write-Host "   Restart: docker-compose restart" -ForegroundColor White
Write-Host ""