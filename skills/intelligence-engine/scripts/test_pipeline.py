#!/usr/bin/env python3
"""
IEM-PM Regression Test -- Full Pipeline Verification
Exercises the real pipeline end to end via subprocess (no mocking) against
the project's actual checked-in fixture (test_manifest.md: 3 artifacts,
2 findings) rather than a synthetic one-liner.
Run this after any code change to confirm the engine is intact.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

# Force UTF-8 stdout so this doesn't crash on Windows consoles that default
# to cp1252 -- belt-and-suspenders alongside keeping output ASCII-only below.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ENGINE_DIR = Path(__file__).parent.parent  # skills/intelligence-engine/
SCRIPTS_DIR = ENGINE_DIR / "scripts"
ASSETS_DIR = ENGINE_DIR / "assets"

# The project's real regression fixture -- "actual data", not an inline stub.
REAL_MANIFEST_PATH = SCRIPTS_DIR / "test_manifest.md"

CANONICAL_INDICATOR_ORDER = [
    "visibility", "integrity", "connectivity", "governance",
    "predictability", "decision_quality", "continuous_improvement",
]


def run_script(name: str, args: list, cwd: Path = SCRIPTS_DIR) -> subprocess.CompletedProcess:
    """Run a script and return the CompletedProcess. Does not raise."""
    cmd = [sys.executable, str(SCRIPTS_DIR / name)] + args
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(cwd))


def run_script_ok(name: str, args: list, cwd: Path = SCRIPTS_DIR) -> subprocess.CompletedProcess:
    """Run a script and raise if it exits non-zero."""
    result = run_script(name, args, cwd)
    if result.returncode != 0:
        print(f"FAILED: {name}")
        print(f"  stdout: {result.stdout}")
        print(f"  stderr: {result.stderr}")
        raise RuntimeError(f"{name} exited with code {result.returncode}")
    return result


def _generate_findings(manifest_path: Path, tmp_dir: Path) -> dict:
    """Run manifest_to_findings.py against a manifest and return the parsed JSON."""
    output_path = tmp_dir / "findings.json"
    run_script_ok("manifest_to_findings.py", [
        "--manifest", str(manifest_path),
        "--output", str(output_path),
    ])
    return json.loads(output_path.read_text(encoding="utf-8"))


# ─── Tests (each independent -- generates its own fixtures/output) ───

def test_manifest_to_findings():
    """Test 1: real fixture Manifest -> Canonical JSON."""
    with tempfile.TemporaryDirectory() as tmp:
        data = _generate_findings(REAL_MANIFEST_PATH, Path(tmp))

        assert data["schema_version"] == "1.1.0"
        assert len(data["findings"]) == 2
        assert {f["id"] for f in data["findings"]} == {"FIND-0001", "FIND-0002"}
        assert data["reporting_integrity_score"]["score"] > 0
        assert "maturity_assessment" not in data, "OPM3/maturity modeling was scrapped -- must not reappear"

        # Artifact Name resolution (regression: used to fall back to the ID)
        names = {a["artifact_id"]: a["artifact_name"] for a in data["baseline"]["artifacts_examined"]}
        assert names == {
            "ART-001": "Project Schedule",
            "ART-002": "RAID Log",
            "ART-003": "Governance Pack",
        }, f"artifact names not resolved correctly: {names}"

        # Field coverage averaged from the manifest's declared per-artifact
        # values (85%, 92%, 78% -> 85.0). Regression: used to be hardcoded 0.0.
        assert data["evidence_summary"]["coverage_percentage"] == 85.0

        # Indicator order must be canonical and stable (regression: used to be
        # a Python set, so iteration order was randomized per process).
        assert list(data["intelligence_indicators"].keys()) == CANONICAL_INDICATOR_ORDER

        print(f"  PASS: {len(data['findings'])} finding(s) parsed from real fixture")
        print(f"  PASS: RIS = {data['reporting_integrity_score']['score']}")
        print(f"  PASS: no maturity_assessment in output (scrapped, not scored)")
        print(f"  PASS: artifact names resolved: {names}")
        print(f"  PASS: coverage_percentage = {data['evidence_summary']['coverage_percentage']}")
        print(f"  PASS: indicator order is canonical")


def test_schema_validation():
    """Test 2: canonical JSON produced from the real fixture passes schema validation."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        output_path = tmp_path / "findings.json"
        run_script_ok("manifest_to_findings.py", [
            "--manifest", str(REAL_MANIFEST_PATH),
            "--output", str(output_path),
        ])
        result = run_script_ok("schema.py", [str(output_path)])
        assert "VALIDATION PASSED" in result.stdout
        print("  PASS: schema validation passed on real-fixture output")


def test_rendering():
    """Test 3: JSON -> HTML + TXT, checking real content and both prior render bugs."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        findings_path = tmp_path / "findings.json"
        html_path = tmp_path / "report.html"
        txt_path = tmp_path / "report.txt"

        run_script_ok("manifest_to_findings.py", [
            "--manifest", str(REAL_MANIFEST_PATH),
            "--output", str(findings_path),
        ])
        data = json.loads(findings_path.read_text(encoding="utf-8"))

        run_script_ok("render.py", [
            "--canonical", str(findings_path),
            "--template", str(ASSETS_DIR / "report_template.html"),
            "--output-html", str(html_path),
            "--output-txt", str(txt_path),
        ])

        html_content = html_path.read_text(encoding="utf-8")
        txt_content = txt_path.read_text(encoding="utf-8")

        assert "FIND-0001" in html_content and "FIND-0002" in html_content
        assert "Missing" in html_content and "Underutilized" in html_content

        # Artifact names actually rendered, not just IDs (regression check).
        for name in ("Project Schedule", "RAID Log", "Governance Pack"):
            assert name in html_content, f"{name!r} missing from rendered HTML"

        # TXT ellipsis regression: any indicator text shorter than 180 chars
        # must appear whole, with no phantom "..." appended.
        for dim, text in data["intelligence_indicators"].items():
            if len(text) <= 180:
                assert text in txt_content, f"{dim} text missing verbatim from TXT report"
                assert f"{text}..." not in txt_content, f"{dim} got a phantom '...' appended"

        print(f"  PASS: HTML report: {len(html_content):,} chars, artifact names resolved")
        print(f"  PASS: TXT report: {len(txt_content):,} chars, no phantom truncation")


def test_knowledge_index():
    """Test 4: knowledge index generation against the real knowledge/ folder."""
    result = run_script_ok("derive_knowledge_index.py", [])
    assert "Knowledge index written" in result.stdout
    index_path = ENGINE_DIR / "knowledge_index.json"
    assert index_path.exists(), "knowledge_index.json was not created"
    print("  PASS: knowledge index generated")


def test_duplicate_detection():
    """
    Test 5: two full findings sharing the same gap_type + root_origin +
    artifact_id + standard identifier must be rejected as a duplicate --
    specifically, not for some unrelated parse failure.
    """
    base = REAL_MANIFEST_PATH.read_text(encoding="utf-8")

    # A genuine clone of FIND-0002's signature (Underutilized / Behavior /
    # ART-002 / Process 11.7), inserted as a real, complete finding block --
    # not a mangled header with no body, which is what the old version of
    # this test accidentally produced.
    duplicate_block = """
### FINDING: FIND-0003

**Gap Type:** Underutilized
**Root Origin:** Behavior
**Standard:** PMBOK 8th Edition
**Clause:** 11.7.2.3
**Identifier:** Process 11.7
**Requirement Summary:** Risk data must inform governance decisions and steering committee reviews.
**Description:** Deliberately duplicated finding inserted to test the no-duplicate validator end to end.
**Severity:** 2
**Impact:** Test impact text for duplicate detection.
**Recommended Action:** Test recommended action for duplicate detection.
**Intelligence Dimensions:** Governance

- **Artifact:** ART-002 | **Location:** Steering Pack, months 7-9 | **Evidence:** Deliberately duplicated evidence for validator testing.

"""
    bad_manifest = base.replace("## SYNTHESIS", duplicate_block + "## SYNTHESIS", 1)
    assert "FIND-0003" in bad_manifest, "injection into the fixture failed -- test is broken"

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        manifest_path = tmp_path / "duplicate_manifest.md"
        output_path = tmp_path / "should_not_exist.json"
        manifest_path.write_text(bad_manifest, encoding="utf-8")

        result = run_script("manifest_to_findings.py", [
            "--manifest", str(manifest_path), "--output", str(output_path),
        ])
        combined = result.stdout + result.stderr

        assert result.returncode != 0, "duplicate manifest was NOT rejected"
        assert "Duplicate finding signature" in combined, (
            f"rejected, but not for the duplicate-signature reason:\n{combined}"
        )
        assert not output_path.exists(), "findings.json must not be written on validation failure"
        print("  PASS: duplicate signature (Underutilized/Behavior/ART-002/Process 11.7) correctly rejected")


def main():
    print("=" * 60)
    print("IEM-PM Regression Test Suite")
    print("=" * 60)

    tests = [
        ("Manifest -> JSON", test_manifest_to_findings),
        ("Schema Validation", test_schema_validation),
        ("JSON -> Reports", test_rendering),
        ("Knowledge Index", test_knowledge_index),
        ("Duplicate Detection", test_duplicate_detection),
    ]

    passed = 0
    failed = 0

    for name, test_fn in tests:
        print(f"\n--- {name} ---")
        try:
            test_fn()
            passed += 1
        except Exception as e:
            print(f"  FAIL: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed > 0:
        sys.exit(1)
    print("All regression tests passed.")


if __name__ == "__main__":
    main()
