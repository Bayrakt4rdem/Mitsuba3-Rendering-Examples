# Mitsuba 3 Demo Launcher
# This script helps you activate the virtual environment and run demos

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Mitsuba 3 Learning Demo - Quick Launcher" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-Not (Test-Path "mitsuba_venv\Scripts\Activate.ps1")) {
    Write-Host "Error: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: python -m venv mitsuba_venv" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& ".\mitsuba_venv\Scripts\Activate.ps1"

# Check if mitsuba is installed
python -c "import mitsuba" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Mitsuba not installed in virtual environment!" -ForegroundColor Yellow
    Write-Host "Installing dependencies..." -ForegroundColor Green
    pip install -r requirements.txt
    Write-Host ""
}

# Menu
Write-Host ""
Write-Host "Select a demo to run:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  0. Quick Start (verify installation)" -ForegroundColor White
Write-Host "  1. Basic Scene (beginner)" -ForegroundColor White
Write-Host "  2. Materials Showcase (intermediate)" -ForegroundColor White
Write-Host "  3. Lighting Techniques (intermediate)" -ForegroundColor White
Write-Host "  4. Advanced Scene (advanced)" -ForegroundColor White
Write-Host "  5. Cornell Box (classic)" -ForegroundColor White
Write-Host "  Q. Quit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (0-5, Q)"

switch ($choice) {
    "0" { 
        Write-Host "`nRunning Quick Start..." -ForegroundColor Green
        python examples/00_quick_start.py 
    }
    "1" { 
        Write-Host "`nRunning Basic Scene Demo..." -ForegroundColor Green
        python examples/01_basic_scene.py 
    }
    "2" { 
        Write-Host "`nRunning Materials Showcase..." -ForegroundColor Green
        python examples/02_materials_showcase.py 
    }
    "3" { 
        Write-Host "`nRunning Lighting Techniques..." -ForegroundColor Green
        python examples/03_lighting_techniques.py 
    }
    "4" { 
        Write-Host "`nRunning Advanced Scene..." -ForegroundColor Green
        python examples/04_advanced_scene.py 
    }
    "5" { 
        Write-Host "`nRunning Cornell Box..." -ForegroundColor Green
        python examples/05_cornell_box.py 
    }
    "Q" { 
        Write-Host "`nExiting..." -ForegroundColor Yellow
        exit 0
    }
    "q" { 
        Write-Host "`nExiting..." -ForegroundColor Yellow
        exit 0
    }
    default { 
        Write-Host "`nInvalid choice!" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Demo complete! Check the 'output' folder for images." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
