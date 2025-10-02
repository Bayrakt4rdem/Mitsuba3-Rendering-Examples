# Launch Mitsuba 3 Render Studio GUI
# Quick launcher script for Windows PowerShell

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Mitsuba 3 Render Studio - GUI Launcher" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Get script directory and project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

# Check virtual environment
$VenvPath = Join-Path $ProjectRoot "mitsuba_venv\Scripts\Activate.ps1"
if (-Not (Test-Path $VenvPath)) {
    Write-Host "Error: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please create it first: python -m venv mitsuba_venv" -ForegroundColor Yellow
    Write-Host "Then install dependencies: pip install -r requirements.txt" -ForegroundColor Yellow
    pause
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& $VenvPath

# Check dependencies
Write-Host "Checking dependencies..." -ForegroundColor Green

$missingDeps = @()

python -c "import mitsuba" 2>$null
if ($LASTEXITCODE -ne 0) { $missingDeps += "mitsuba" }

python -c "import PyQt6" 2>$null
if ($LASTEXITCODE -ne 0) { $missingDeps += "PyQt6" }

python -c "import loguru" 2>$null
if ($LASTEXITCODE -ne 0) { $missingDeps += "loguru" }

if ($missingDeps.Count -gt 0) {
    Write-Host ""
    Write-Host "Missing dependencies detected!" -ForegroundColor Yellow
    Write-Host "Installing: $($missingDeps -join ', ')" -ForegroundColor Yellow
    Write-Host ""
    pip install -r "$ProjectRoot\requirements.txt"
    Write-Host ""
}

# Launch GUI
Write-Host ""
Write-Host "Launching Mitsuba 3 Render Studio..." -ForegroundColor Cyan
Write-Host ""

# Change to project root to ensure correct path
Set-Location $ProjectRoot
python launch_gui.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "GUI exited with error code: $LASTEXITCODE" -ForegroundColor Red
    pause
}
