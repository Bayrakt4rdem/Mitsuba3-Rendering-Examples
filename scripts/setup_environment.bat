@echo off
REM Mitsuba 3 Render Studio - Simple Setup Script
REM This batch file sets up everything you need

echo ============================================================
echo   Mitsuba 3 Render Studio - Automated Setup
echo ============================================================
echo.

REM Step 1: Check Python
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found!
    echo Please install Python 3.8+ from: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo.

REM Step 2: Create virtual environment
echo [2/5] Creating virtual environment...
if exist mitsuba_venv (
    echo Virtual environment already exists.
    set /p recreate="Delete and recreate? (y/n): "
    if /i "%recreate%"=="y" (
        echo Removing old environment...
        rmdir /s /q mitsuba_venv
        echo Creating fresh environment...
        python -m venv mitsuba_venv
    ) else (
        echo Using existing environment
    )
) else (
    python -m venv mitsuba_venv
)
echo Virtual environment ready
echo.

REM Step 3: Activate and install
echo [3/5] Activating virtual environment...
call mitsuba_venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Step 4: Upgrade pip
echo [4/5] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo pip upgraded
echo.

REM Step 5: Install dependencies
echo [5/5] Installing dependencies...
echo This may take a few minutes...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Error: Dependency installation failed!
    echo Try running manually:
    echo   mitsuba_venv\Scripts\activate.bat
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo All dependencies installed
echo.

REM Verify installation
echo ============================================================
echo   Verifying Installation
echo ============================================================
echo.

python -c "import mitsuba; print('mitsuba OK')" 2>nul
if errorlevel 1 (
    echo [X] mitsuba not found
) else (
    echo [OK] mitsuba installed
)

python -c "import PyQt6; print('PyQt6 OK')" 2>nul
if errorlevel 1 (
    echo [X] PyQt6 not found
) else (
    echo [OK] PyQt6 installed
)

python -c "import numpy; print('numpy OK')" 2>nul
if errorlevel 1 (
    echo [X] numpy not found
) else (
    echo [OK] numpy installed
)

python -c "import PIL; print('Pillow OK')" 2>nul
if errorlevel 1 (
    echo [X] Pillow not found
) else (
    echo [OK] Pillow installed
)

python -c "import loguru; print('loguru OK')" 2>nul
if errorlevel 1 (
    echo [X] loguru not found
) else (
    echo [OK] loguru installed
)

echo.
echo ============================================================
echo   Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Launch GUI:  launch_gui.ps1
echo   2. Read guide:  GUI_USER_GUIDE.md
echo   3. Try examples in the GUI tabs!
echo.

set /p launch="Launch GUI now? (y/n): "
if /i "%launch%"=="y" (
    echo.
    echo Launching Mitsuba 3 Render Studio...
    echo.
    python launch_gui.py
)
