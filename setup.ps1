# IEM-PM Setup -- run this once per Windows computer.
#
# How to run it: right-click this file in File Explorer and choose "Run with PowerShell".
# If Windows blocks it ("running scripts is disabled on this system"), open PowerShell in
# this folder instead and run:  powershell -ExecutionPolicy Bypass -File setup.ps1

$ErrorActionPreference = "Stop"

# Always operate on this script's own folder, never whatever folder PowerShell happened to
# start in -- right-click-and-run does not reliably set the working directory to here.
Set-Location -Path $PSScriptRoot

Write-Host ""
Write-Host "=== IEM-PM Setup ===" -ForegroundColor Cyan
Write-Host ""

# 1. Check Python. Get-Command alone isn't enough: on a stock Windows machine with no real
# Python installed, "python" resolves to the Microsoft Store's App Execution Alias stub,
# which exists on PATH but isn't a working interpreter -- it just opens the Store when run.
# Actually running --version and checking the exit code catches that; the stub returns
# non-zero and prints its own "Install Python now?" message instead of a version string.
$pythonOk = $false
$pythonVersionText = $null
try {
    $pythonVersionText = (python --version) 2>&1
    if ($LASTEXITCODE -eq 0 -and $pythonVersionText -match "^Python \d") {
        $pythonOk = $true
    }
} catch {
    $pythonOk = $false
}
if (-not $pythonOk) {
    Write-Host "Python was not found on this computer." -ForegroundColor Red
    Write-Host "Install it from https://python.org/downloads -- during install, check the box"
    Write-Host "that says 'Add python.exe to PATH' -- then run this script again."
    Write-Host ""
    Write-Host "(If you saw a Microsoft Store window pop up just now, close it -- that's not" -ForegroundColor Yellow
    Write-Host "a real Python install. Use the link above instead.)" -ForegroundColor Yellow
    exit 1
}
Write-Host "Found $pythonVersionText"

# 2. Install dependencies
Write-Host ""
Write-Host "Installing dependencies (this can take a minute)..."
python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Dependency install failed -- see the error above." -ForegroundColor Red
    Write-Host "If you're on a work/managed computer, this is often a permissions issue -- try" -ForegroundColor Yellow
    Write-Host "running: python -m pip install --user -r requirements.txt" -ForegroundColor Yellow
    Write-Host "If that also fails, ask whoever manages this computer for help." -ForegroundColor Yellow
    exit 1
}
Write-Host "Dependencies installed." -ForegroundColor Green

# 3. Create the folders you'll need, if they aren't there already. Fail loudly rather than
# silently if something unexpected (e.g. a plain file, not a folder) already sits at that path
# -- New-Item -Force stays quiet in that case, which would otherwise surface as a confusing
# audit failure later with no link back to this script.
function New-ProjectFolder($path) {
    if ((Test-Path $path) -and -not (Test-Path $path -PathType Container)) {
        Write-Host "Expected '$path' to be a folder, but a file already exists there." -ForegroundColor Red
        Write-Host "Rename or delete that file, then run this script again."
        exit 1
    }
    New-Item -ItemType Directory -Force -Path $path | Out-Null
}
New-ProjectFolder "Audit"
New-ProjectFolder "skills\intelligence-engine\knowledge"

# 4. Check for Claude Code (best-effort -- just a heads-up, not a hard requirement to proceed)
Write-Host ""
$claude = Get-Command claude -ErrorAction SilentlyContinue
if ($claude) {
    Write-Host "Claude Code found on this computer." -ForegroundColor Green
} else {
    Write-Host "Claude Code was not found on this computer." -ForegroundColor Yellow
    Write-Host "Install it from https://claude.com/claude-code and sign in before continuing."
}

# 5. Plain-language next steps -- the things this script cannot do for you
Write-Host ""
Write-Host "=== Setup complete. A few things left -- only you can do these: ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Put your organization's real PM standards into this folder:"
Write-Host "     skills\intelligence-engine\knowledge\"
Write-Host "   PMBOK, PRINCE2, ISO 21502, or your own internal methodology -- PDF or Word/Markdown."
Write-Host "   This never leaves your computer and is never uploaded anywhere."
Write-Host ""
Write-Host "2. Open Claude Code FROM INSIDE THIS FOLDER" -NoNewline
Write-Host " (this exact folder -- not a shortcut, not a different one)."
Write-Host "   That's what makes the skill available. Then type:"
Write-Host "     Audit my project using the intelligence-engine skill"
Write-Host ""
Write-Host "Full step-by-step guide (open in any web browser):"
Write-Host "  Public\IEM-PM-User-Guide.html"
Write-Host ""
