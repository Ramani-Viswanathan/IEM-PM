#!/usr/bin/env python3
"""Maintainer-only tool: builds a curated tester-facing release ZIP.

Not something a tester runs -- this is what produces what a tester downloads. Real audits
using `git clone`/"Download ZIP" on the main repo get everything: STATUS.md's full internal
fix log, the 19-section BLUEPRINT design doc, and (for anything not gitignored) whatever this
maintainer's own repo happens to contain.

Deliberately sourced from `git ls-files`, not a raw filesystem walk: gitignore already encodes
exactly what's real/local-only data (a maintainer's actual standards PDFs, derived registries,
the knowledge_index.json summarizing them) -- respecting it here means this script can't
silently drift out of sync with it the way a hand-maintained parallel exclusion list would.
An earlier version of this script tried exactly that (explicitly excluding the knowledge/ and
registries/ folder contents) and still leaked skills/intelligence-engine/knowledge_index.json,
because that file sits one level up from the folders it was told to exclude -- caught only by
inspecting the actual built ZIP, not by reading the code. `git ls-files` doesn't have that
class of bug: an ignored file is never tracked, so it's never listed, regardless of where it
sits in the tree.

On top of "tracked by git," an explicit top-level allowlist further narrows this to only what
a tester needs -- STATUS.md/BLUEPRINT-1.md/CLAUDE.md are all tracked (not gitignored) but
still shouldn't ship, since they're internal engineering/process docs, not tester-facing.

Usage: python build_release.py [--output dist/IEM-PM-release.zip]
"""
import argparse
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Only files under these top-level names/prefixes are eligible, even if git-tracked.
ALLOWED_PREFIXES = [
    "Public/",
    "skills/",
    "requirements.txt",
    "LICENSE",
    "setup.ps1",
    "setup.sh",
    "setup.bat",
    "setup_gui.pyw",
]

README_STRIP_LINES = [
    "See [`IEM-PM BLUEPRINT-1.md`](IEM-PM%20BLUEPRINT-1.md) for the full 19-section design and\n",
    "[`STATUS.md`](STATUS.md) for exactly what's built vs. pending right now.\n",
]


def tracked_release_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"], cwd=str(ROOT), capture_output=True, text=True, check=True,
    )
    all_tracked = result.stdout.splitlines()
    return [
        f for f in all_tracked
        if any(f == prefix.rstrip("/") or f.startswith(prefix) for prefix in ALLOWED_PREFIXES)
    ]


def build_release_readme(dst_root: Path):
    src_readme = (ROOT / "README.md").read_text(encoding="utf-8")
    lines = src_readme.splitlines(keepends=True)
    filtered = [ln for ln in lines if ln not in README_STRIP_LINES]
    text = "".join(filtered).replace("item, tracked in `STATUS.md`.", "item.")
    (dst_root / "README.md").write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "dist" / "IEM-PM-release.zip",
        help="Where to write the release ZIP (default: dist/IEM-PM-release.zip)",
    )
    args = parser.parse_args()

    files = tracked_release_files()
    if not files:
        print("No files matched the allowlist -- refusing to build an empty release.", file=sys.stderr)
        sys.exit(1)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        args.output.unlink()

    with zipfile.ZipFile(args.output, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in files:
            zf.write(ROOT / rel, rel)

        readme_lines = (ROOT / "README.md").read_text(encoding="utf-8").splitlines(keepends=True)
        readme_text = "".join(ln for ln in readme_lines if ln not in README_STRIP_LINES)
        readme_text = readme_text.replace("item, tracked in `STATUS.md`.", "item.")
        zf.writestr("README.md", readme_text)

    print(f"Built {args.output} ({len(files) + 1} files)")
    print("Source: git-tracked files only, filtered to:", ", ".join(ALLOWED_PREFIXES))
    print("Excluded even though tracked: STATUS.md, IEM-PM BLUEPRINT-1.md, CLAUDE.md, "
          "and everything else not under an allowed prefix above.")
    print("Excluded because gitignored (never tracked): real standards, derived registries, "
          "knowledge_index.json, _archive/, stakeholder/, Audit/ real content.")


if __name__ == "__main__":
    main()
