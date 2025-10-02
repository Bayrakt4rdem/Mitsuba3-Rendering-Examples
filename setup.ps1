# Mitsuba 3 Render Studio - Quick Setup
# Wrapper that calls the main setup script

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

& ".\scripts\setup_environment.ps1"
