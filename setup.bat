@echo off
REM IEM-PM Setup launcher -- double-click this file. No right-click menu needed.
REM
REM Why this exists: right-click "Run with PowerShell" on setup.ps1 often silently fails
REM after downloading the ZIP from GitHub -- Windows marks downloaded files as untrusted
REM ("Mark of the Web") and blocks the script regardless of execution policy. This .bat
REM file is not subject to that block. It prefers the graphical wizard (setup_gui.pyw) and
REM only falls back to the console script if tkinter isn't available on this Python.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo Python was not found on this computer.
    echo Install it from https://python.org/downloads -- during install, check the box
    echo that says "Add python.exe to PATH" -- then run this file again.
    echo.
    pause
    exit /b 1
)

python -c "import tkinter" >nul 2>nul
if %errorlevel% equ 0 (
    echo Starting IEM-PM setup...
    where pythonw >nul 2>nul
    if %errorlevel% equ 0 (
        start "" pythonw "%~dp0setup_gui.pyw"
    ) else (
        start "" python "%~dp0setup_gui.pyw"
    )
    exit /b 0
)

echo.
echo Starting IEM-PM setup (console mode -- graphical wizard unavailable on this Python)...
echo (This folder: %~dp0)
echo.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup.ps1"
echo.
pause
