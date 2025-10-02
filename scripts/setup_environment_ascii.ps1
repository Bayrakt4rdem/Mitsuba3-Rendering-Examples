# Mitsuba 3 Render Studio - Automated Setup Script
# This script sets up everything you need to run the GUI

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Mitsuba 3 Render Studio - Automated Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Step 1: Check Python
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Python not found!" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from: https://www.python.org/downloads/" -ForegroundColor Yellow
    pause
    exit 1
}
Write-Host "  Found: $pythonVersion" -ForegroundColor Green
Write-Host ""

# Step 2: Create virtual environment
Write-Host "[2/5] Creating virtual environment..." -ForegroundColor Yellow
$VenvPath = Join-Path $ScriptDir "mitsuba_venv"

if (Test-Path $VenvPath) {
    Write-Host "  Virtual environment already exists." -ForegroundColor Yellow
    $response = Read-Host "  Delete and recreate? (y/n)"
    if ($response -eq 'y') {
        Write-Host "  Removing old environment..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force $VenvPath
        Write-Host "  Creating fresh environment..." -ForegroundColor Yellow
        python -m venv mitsuba_venv
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Error: Failed to create virtual environment!" -ForegroundColor Red
            pause
            exit 1
        }
        Write-Host "  Virtual environment created" -ForegroundColor Green
    } else {
        Write-Host "  Using existing environment" -ForegroundColor Green
    }
} else {
    python -m venv mitsuba_venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to create virtual environment!" -ForegroundColor Red
        pause
        exit 1
    }
    Write-Host "  Virtual environment created" -ForegroundColor Green
}
Write-Host ""

# Step 3: Activate virtual environment
Write-Host "[3/5] Activating virtual environment..." -ForegroundColor Yellow
$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"

if (-Not (Test-Path $ActivateScript)) {
    Write-Host "Error: Activation script not found!" -ForegroundColor Red
    pause
    exit 1
}

# Check execution policy
$executionPolicy = Get-ExecutionPolicy
if ($executionPolicy -eq "Restricted") {
    Write-Host "  WARNING: Execution policy is Restricted. Changing to RemoteSigned..." -ForegroundColor Yellow
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
}

& $ActivateScript
Write-Host "  Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Step 4: Upgrade pip
Write-Host "[4/5] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "  pip upgraded" -ForegroundColor Green
} else {
    Write-Host "  pip upgrade failed (continuing anyway)" -ForegroundColor Yellow
}
Write-Host ""

# Step 5: Install dependencies
Write-Host "[5/5] Installing dependencies..." -ForegroundColor Yellow
Write-Host "  This may take a few minutes..." -ForegroundColor Cyan
Write-Host ""

# Install with progress
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Error: Dependency installation failed!" -ForegroundColor Red
    Write-Host "Try running manually:" -ForegroundColor Yellow
    Write-Host "  .\mitsuba_venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  pip install -r requirements.txt" -ForegroundColor White
    pause
    exit 1
}

Write-Host ""
    Write-Host "  All dependencies installed" -ForegroundColor Green
    Write-Host ""# Verify installation
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Verifying Installation" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check Mitsuba
Write-Host "Checking mitsuba..." -ForegroundColor Yellow
python -c "import mitsuba; print(f'  [OK] mitsuba {mitsuba.__version__}')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [X] mitsuba not found" -ForegroundColor Red
    $allGood = $false
}

# Check PyQt6
Write-Host "Checking PyQt6..." -ForegroundColor Yellow
python -c "import PyQt6.QtCore; print(f'  [OK] PyQt6 {PyQt6.QtCore.PYQT_VERSION_STR}')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [X] PyQt6 not found" -ForegroundColor Red
    $allGood = $false
}

# Check numpy
Write-Host "Checking numpy..." -ForegroundColor Yellow
python -c "import numpy; print(f'  [OK] numpy {numpy.__version__}')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [X] numpy not found" -ForegroundColor Red
    $allGood = $false
}

# Check Pillow
Write-Host "Checking Pillow..." -ForegroundColor Yellow
python -c "import PIL; print(f'  [OK] Pillow {PIL.__version__}')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [X] Pillow not found" -ForegroundColor Red
    $allGood = $false
}

# Check loguru
Write-Host "Checking loguru..." -ForegroundColor Yellow
python -c "import loguru; print('  [OK] loguru installed')" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  [X] loguru not found" -ForegroundColor Red
    $allGood = $false
}

Write-Host ""

if ($allGood) {
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "  Setup Complete!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Launch GUI:  .\launch_gui.ps1" -ForegroundColor White
    Write-Host "  2. Read guide:  GUI_USER_GUIDE.md" -ForegroundColor White
    Write-Host "  3. Try examples in the GUI tabs!" -ForegroundColor White
    Write-Host ""
    
    $launch = Read-Host "Launch GUI now? (y/n)"
    if ($launch -eq "y") {
        Write-Host ""
        Write-Host "Launching Mitsuba 3 Render Studio..." -ForegroundColor Cyan
        Write-Host ""
        python launch_gui.py
    }
} else {
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host "  Setup Incomplete - Some Dependencies Missing" -ForegroundColor Red
    Write-Host "============================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please try:" -ForegroundColor Yellow
    Write-Host "  1. Activate environment: .\mitsuba_venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  2. Install again: pip install -r requirements.txt" -ForegroundColor White
    Write-Host "  3. Check INSTALLATION.md for troubleshooting" -ForegroundColor White
    Write-Host ""
    pause
}
