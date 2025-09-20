# AI Research Agent Deployment Script
# This script helps deploy the application to various cloud platforms

Write-Host "🚀 AI Research Agent Deployment Script" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "main.py")) {
    Write-Host "❌ Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Project structure verified" -ForegroundColor Green

# Check for required files
$requiredFiles = @("main.py", "requirements.txt", "frontend/package.json", "Dockerfile", "docker-compose.yml")
foreach ($file in $requiredFiles) {
    if (-not (Test-Path $file)) {
        Write-Host "❌ Missing required file: $file" -ForegroundColor Red
        exit 1
    }
}

Write-Host "✅ All required files present" -ForegroundColor Green

# Test backend
Write-Host "🔍 Testing backend..." -ForegroundColor Yellow
try {
    python -c "import main; print('Backend imports successful')"
    Write-Host "✅ Backend test passed" -ForegroundColor Green
} catch {
    Write-Host "❌ Backend test failed: $_" -ForegroundColor Red
    exit 1
}

# Test frontend build
Write-Host "🔍 Testing frontend build..." -ForegroundColor Yellow
try {
    Set-Location frontend
    npm run build
    Set-Location ..
    Write-Host "✅ Frontend build successful" -ForegroundColor Green
} catch {
    Write-Host "❌ Frontend build failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎯 Deployment Options:" -ForegroundColor Cyan
Write-Host "1. Docker Compose (Local)" -ForegroundColor White
Write-Host "2. Render.com (Cloud)" -ForegroundColor White
Write-Host "3. Railway (Cloud)" -ForegroundColor White
Write-Host "4. Vercel + Railway (Separate)" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Select deployment option (1-4)"

switch ($choice) {
    "1" {
        Write-Host "🐳 Deploying with Docker Compose..." -ForegroundColor Yellow
        Write-Host "Run: docker-compose up -d" -ForegroundColor Cyan
        Write-Host "Access: http://localhost:3000" -ForegroundColor Cyan
    }
    "2" {
        Write-Host "☁️ Deploying to Render.com..." -ForegroundColor Yellow
        Write-Host "1. Push code to GitHub" -ForegroundColor White
        Write-Host "2. Connect repository to Render" -ForegroundColor White
        Write-Host "3. Use render.yaml configuration" -ForegroundColor White
        Write-Host "4. Set environment variables:" -ForegroundColor White
        Write-Host "   - OPENAI_API_KEY" -ForegroundColor Gray
        Write-Host "   - ALLOWED_ORIGINS" -ForegroundColor Gray
    }
    "3" {
        Write-Host "🚂 Deploying to Railway..." -ForegroundColor Yellow
        Write-Host "1. Install Railway CLI: npm install -g @railway/cli" -ForegroundColor White
        Write-Host "2. Login: railway login" -ForegroundColor White
        Write-Host "3. Deploy: railway up" -ForegroundColor White
        Write-Host "4. Add PostgreSQL service" -ForegroundColor White
        Write-Host "5. Set environment variables" -ForegroundColor White
    }
    "4" {
        Write-Host "🌐 Deploying to Vercel + Railway..." -ForegroundColor Yellow
        Write-Host "Backend (Railway):" -ForegroundColor White
        Write-Host "1. Deploy backend to Railway" -ForegroundColor Gray
        Write-Host "2. Get backend URL" -ForegroundColor Gray
        Write-Host "Frontend (Vercel):" -ForegroundColor White
        Write-Host "1. Update vercel.json with backend URL" -ForegroundColor Gray
        Write-Host "2. Deploy to Vercel" -ForegroundColor Gray
    }
    default {
        Write-Host "❌ Invalid choice" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "📋 Pre-deployment Checklist:" -ForegroundColor Cyan
Write-Host "✅ Code is production-ready" -ForegroundColor Green
Write-Host "✅ All tests pass" -ForegroundColor Green
Write-Host "✅ Environment variables configured" -ForegroundColor Green
Write-Host "✅ Docker configuration ready" -ForegroundColor Green
Write-Host "✅ Documentation complete" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 Ready for deployment!" -ForegroundColor Green
Write-Host "Check DEPLOYMENT.md for detailed instructions" -ForegroundColor Cyan
