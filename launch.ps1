# Mitsuba 3 Render Studio - Quick Launcher
# Wrapper that calls the main launcher script

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

& ".\scripts\launch_gui.ps1"
