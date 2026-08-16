#!/usr/bin/env bash
# IEM-PM Setup -- run this once per Mac/Linux computer.
#
# How to run it: open Terminal, type "cd " (with a trailing space), drag this folder onto
# the Terminal window (this pastes its path), press Enter, then type:  bash setup.sh

set -e

# Always operate on this script's own folder, never whatever folder Terminal happened to
# start in -- protects against cd landing in the wrong place before this runs.
cd "$(dirname "${BASH_SOURCE[0]}")"

echo ""
echo "=== IEM-PM Setup ==="
echo ""

# 1. Check Python. command -v only confirms something named python3 is on PATH, not that it
# actually runs -- on a factory-fresh Mac without Xcode Command Line Tools, /usr/bin/python3
# is a stub that pops a blocking "Install developer tools?" dialog the first time it's run.
if ! command -v python3 &> /dev/null; then
    echo "Python was not found on this computer."
    echo "Install it from https://python.org/downloads, then run this script again."
    exit 1
fi
echo "If a window just popped up asking to install 'Command Line Developer Tools' or"
echo "similar, that's expected on a Mac that's never run Python before -- click Install,"
echo "wait for it to finish, then run this script again."
PYTHON_VERSION="$(python3 --version 2>&1)"
if [[ "$PYTHON_VERSION" != Python\ [0-9]* ]]; then
    echo "Python did not respond as expected (got: $PYTHON_VERSION)."
    echo "Install it from https://python.org/downloads, then run this script again."
    exit 1
fi
echo "Found $PYTHON_VERSION"

# 2. Install dependencies. A normal install can fail on newer macOS/Linux systems with
# "externally-managed-environment" (PEP 668) -- retry with --user before giving up, since
# that resolves it on most (not all) systems non-technical users are likely to hit.
echo ""
echo "Installing dependencies (this can take a minute)..."
if ! python3 -m pip install -r requirements.txt 2>/tmp/iempm_pip_error.log; then
    echo "First attempt failed, trying again with --user..."
    if ! python3 -m pip install --user -r requirements.txt; then
        echo ""
        echo "Dependency install failed. Common fix -- run these two commands, then this"
        echo "script again:"
        echo "  python3 -m venv .venv"
        echo "  source .venv/bin/activate"
        echo "(The second command must be run every time, in every new Terminal window,"
        echo "before using IEM-PM -- or ask whoever manages this computer for help.)"
        cat /tmp/iempm_pip_error.log 2>/dev/null || true
        exit 1
    fi
fi
echo "Dependencies installed."

# 3. Create the folders you'll need, if they aren't there already. Fail loudly rather than
# silently if something unexpected (e.g. a plain file, not a folder) already sits at that
# path, so a later confusing failure doesn't lose its link back to this script.
new_project_folder() {
    if [ -e "$1" ] && [ ! -d "$1" ]; then
        echo "Expected '$1' to be a folder, but a file already exists there."
        echo "Rename or delete that file, then run this script again."
        exit 1
    fi
    mkdir -p "$1"
}
new_project_folder "Audit"
new_project_folder "skills/intelligence-engine/knowledge"

# 4. Check for Claude Code (best-effort -- just a heads-up, not a hard requirement to proceed)
echo ""
if command -v claude &> /dev/null; then
    echo "Claude Code found on this computer."
else
    echo "Claude Code was not found on this computer."
    echo "Install it from https://claude.com/claude-code and sign in before continuing."
fi

# 5. Plain-language next steps -- the things this script cannot do for you
echo ""
echo "=== Setup complete. A few things left -- only you can do these: ==="
echo ""
echo "1. Put your organization's real PM standards into this folder:"
echo "     skills/intelligence-engine/knowledge/"
echo "   PMBOK, PRINCE2, ISO 21502, or your own internal methodology -- PDF or Word/Markdown."
echo "   This never leaves your computer and is never uploaded anywhere."
echo ""
echo "2. Open Claude Code FROM INSIDE THIS FOLDER (this exact folder -- not a shortcut,"
echo "   not a different one). That's what makes the skill available. Then type:"
echo "     Audit my project using the intelligence-engine skill"
echo ""
echo "Full step-by-step guide (open in any web browser):"
echo "  Public/IEM-PM-User-Guide.html"
echo ""
