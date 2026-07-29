"""Single source of truth for repo-relative paths.

Every path here is anchored to this file's own location, not the caller's
cwd, so scripts behave the same whether invoked as `python scripts/foo.py`
or `cd scripts && python foo.py`. This is deliberately just path arithmetic
-- no logic, no I/O -- so it stays trivial to keep correct if the repo
layout ever changes during packaging (edit this one file, not four).
"""
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent      # skills/intelligence-engine/scripts/
ENGINE_DIR = SCRIPTS_DIR.parent                    # skills/intelligence-engine/
REPO_ROOT = ENGINE_DIR.parent.parent                # repository root

KNOWLEDGE_DIR = ENGINE_DIR / "knowledge"
REGISTRIES_DIR = ENGINE_DIR / "registries"
ASSETS_DIR = ENGINE_DIR / "assets"
REPORTS_DIR = REPO_ROOT / "reports"
DEFAULT_TEMPLATE = ASSETS_DIR / "report_template.html"
