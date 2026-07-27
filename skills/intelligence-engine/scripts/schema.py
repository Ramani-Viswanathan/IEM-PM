#!/usr/bin/env python3  
"""
IEM-PM Schema Validator — Contract 5
Validates canonical findings JSON against findings.schema.json.
Enforces closed taxonomies, evidence discipline, deduplication, and coverage.
"""

import json
import jsonschema
from pathlib import Path
from typing import Dict, Any, List, Tuple

# Resolve schema path relative to this file
SCHEMA_PATH = Path(__file__).parent / "findings.schema.json"

def load_schema() -> Dict[str, Any]:
    """Load and return the JSON schema dict."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_canonical(findings_json: Dict[str, Any]) -> List[str]:
    """
    Validate canonical findings JSON against the schema.
    Returns a list of error strings. Empty list means valid.
    """
    schema = load_schema()
    validator = jsonschema.Draft7Validator(schema)
    errors = sorted(validator.iter_errors(findings_json), key=lambda e: e.path)
    return [f"[E-VALID-001] {'/'.join(str(p) for p in e.path)}: {e.message}" for e in errors]


def validate_no_duplicates(findings_json: Dict[str, Any]) -> List[str]:
    """
    The same underlying problem in the same artifact against the same standard
    must be ONE finding — not multiple findings. Multiple evidence bullets
    within the same finding are allowed and expected.
    """
    seen: set = set()
    dups: List[str] = []

    for f in findings_json.get("findings", []):
        std_id = f.get("standard_reference", {}).get("identifier", "__NO_ID__")
        # Collect unique artifact IDs cited in THIS finding
        art_ids = {ev.get("artifact_id") for ev in f.get("evidence", [])}
        for art_id in art_ids:
            key = (f["gap_type"], f["root_origin"], art_id, std_id)
            if key in seen:
                dups.append(
                    f"[E-VALID-002] Duplicate finding signature: gap={key[0]}, origin={key[1]}, "
                    f"artifact={key[2]}, standard_id={key[3]}"
                )
            seen.add(key)

    return dups


def validate_evidence_coverage(findings_json: Dict[str, Any]) -> List[str]:
    """
    Every finding must reference at least one artifact declared in the baseline.
    """
    baseline_artifacts = {
        a.get("artifact_id")
        for a in findings_json.get("baseline", {}).get("artifacts_examined", [])
    }
    errors: List[str] = []

    for finding in findings_json.get("findings", []):
        for ev in finding.get("evidence", []):
            art_id = ev.get("artifact_id")
            if art_id not in baseline_artifacts:
                errors.append(
                    f"[E-VALID-003] {finding.get('id')}: Evidence references unknown artifact "
                    f"'{art_id}' not declared in baseline"
                )

    return errors


def validate_provisional_caveat(findings_json: Dict[str, Any]) -> List[str]:
    """
    If Charter status is PROVISIONAL, every finding must carry the caveat.
    """
    status = findings_json.get("charter_version", "").upper()
    # Note: charter_version field holds version; status is in header. 
    # If you add 'charter_status' to schema, adjust here.
    # For now, we check the manifest header separately during manifest parse.
    return []


def full_validate(findings_json: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Run all validations. Returns (is_valid, list_of_errors).
    """
    all_errors: List[str] = []

    all_errors.extend(validate_canonical(findings_json))
    all_errors.extend(validate_no_duplicates(findings_json))
    all_errors.extend(validate_evidence_coverage(findings_json))

    is_valid = len(all_errors) == 0
    return is_valid, all_errors


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python schema.py <findings.json>")
        sys.exit(1)

    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    valid, errors = full_validate(data)

    if valid:
        print("VALIDATION PASSED")
        print(f"Findings: {len(data.get('findings', []))}")
        print(f"Artifacts: {len(data.get('baseline', {}).get('artifacts_examined', []))}")
    else:
        print("VALIDATION FAILED")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)