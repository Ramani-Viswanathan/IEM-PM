@echo off
REM IEM-PM Setup launcher -- double-click this file. No right-click menu needed.
REM
REM Why this exists: right-click "Run with PowerShell" on setup.ps1 often silently fails
REM after downloading the ZIP from GitHub -- Windows marks downloaded files as untrusted
REM ("Mark of the Web") and blocks the script regardless of execution policy. This .bat
REM file is not subject to that block, and launches setup.ps1 with the one flag that is.
echo.
echo Starting IEM-PM setup...
echo (This folder: %~dp0)
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1"
echo.
pause
