# TestGenie Enterprise - PowerShell Startup Script

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "    TestGenie Enterprise Startup Script" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Activate virtual environment
Write-Host "[1/4] Activating virtual environment..." -ForegroundColor Green
try {
    & .\venv\Scripts\Activate.ps1
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Failed to activate virtual environment" -ForegroundColor Red
    Write-Host "Please run: python -m venv venv" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 2: Check dependencies
Write-Host "[2/4] Checking dependencies..." -ForegroundColor Green
try {
    python -c "import flask" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installing required dependencies..." -ForegroundColor Yellow
        pip install -r requirements_basic.txt
    }
    Write-Host "✅ Dependencies verified" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Dependency check failed" -ForegroundColor Red
}

# Step 3: Setup directories
Write-Host "[3/4] Setting up directories..." -ForegroundColor Green
if (!(Test-Path "uploads")) {
    New-Item -ItemType Directory -Name "uploads" | Out-Null
}
Write-Host "✅ Directories ready" -ForegroundColor Green

# Step 4: Start application
Write-Host "[4/4] Starting TestGenie Enterprise..." -ForegroundColor Green
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   TestGenie Enterprise is starting..." -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   Open your browser and go to:" -ForegroundColor White
Write-Host "   http://localhost:5000" -ForegroundColor Green
Write-Host ""
Write-Host "   API Endpoints:" -ForegroundColor White
Write-Host "   - Health Check: " -NoNewline -ForegroundColor White
Write-Host "http://localhost:5000/api/health" -ForegroundColor Blue
Write-Host "   - System Status: " -NoNewline -ForegroundColor White
Write-Host "http://localhost:5000/api/status" -ForegroundColor Blue
Write-Host "   - File Upload: " -NoNewline -ForegroundColor White
Write-Host "http://localhost:5000/api/upload" -ForegroundColor Blue
Write-Host "   - Generate Tests: " -NoNewline -ForegroundColor White
Write-Host "http://localhost:5000/api/generate-test-cases" -ForegroundColor Blue
Write-Host ""
Write-Host "   Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Start the Python application
python simple_app.py
