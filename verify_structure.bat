@echo off
echo ============================================================
echo   Mitsuba 3 Render Studio - Structure Verification
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/4] Checking root directory files...
if exist "setup.ps1" (echo   OK: setup.ps1) else (echo   MISSING: setup.ps1)
if exist "launch.ps1" (echo   OK: launch.ps1) else (echo   MISSING: launch.ps1)
if exist "launch_gui.py" (echo   OK: launch_gui.py) else (echo   MISSING: launch_gui.py)
if exist "requirements.txt" (echo   OK: requirements.txt) else (echo   MISSING: requirements.txt)
if exist "README.md" (echo   OK: README.md) else (echo   MISSING: README.md)
echo.

echo [2/4] Checking scripts directory...
if exist "scripts\setup_environment.ps1" (echo   OK: scripts\setup_environment.ps1) else (echo   MISSING: scripts\setup_environment.ps1)
if exist "scripts\launch_gui.ps1" (echo   OK: scripts\launch_gui.ps1) else (echo   MISSING: scripts\launch_gui.ps1)
if exist "scripts\setup_environment.bat" (echo   OK: scripts\setup_environment.bat) else (echo   MISSING: scripts\setup_environment.bat)
echo.

echo [3/4] Checking documentation...
if exist "docs\README.md" (echo   OK: docs\README.md) else (echo   MISSING: docs\README.md)
if exist "docs\INSTALLATION.md" (echo   OK: docs\INSTALLATION.md) else (echo   MISSING: docs\INSTALLATION.md)
if exist "docs\QUICKSTART.md" (echo   OK: docs\QUICKSTART.md) else (echo   MISSING: docs\QUICKSTART.md)
if exist "docs\gui\USER_GUIDE.md" (echo   OK: docs\gui\USER_GUIDE.md) else (echo   MISSING: docs\gui\USER_GUIDE.md)
if exist "docs\examples\GUI_EXAMPLES.md" (echo   OK: docs\examples\GUI_EXAMPLES.md) else (echo   MISSING: docs\examples\GUI_EXAMPLES.md)
echo.

echo [4/4] Checking source code...
if exist "gui\core\main_window.py" (echo   OK: gui\core\main_window.py) else (echo   MISSING: gui\core\main_window.py)
if exist "gui_examples\basic_scene.py" (echo   OK: gui_examples\basic_scene.py) else (echo   MISSING: gui_examples\basic_scene.py)
echo.

echo ============================================================
echo   Verification Complete!
echo ============================================================
echo.
echo To get started:
echo   1. Run: setup.ps1
echo   2. Then: launch.ps1
echo.
pause
