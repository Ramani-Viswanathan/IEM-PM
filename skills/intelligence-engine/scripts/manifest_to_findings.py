#!/usr/bin/env python3
"""
IEM-PM Manifest → Canonical Findings
Reads the LLM-generated Audit Manifest (markdown) and converts it to
validated canonical findings JSON (Contract 4).

The LLM judges. This script validates, scores, and canonicalizes.
"""

import json
import re
import argparse
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional, Tuple

# Import our validator from the same directory
try:
    from schema import validate_canonical, validate_no_duplicates, validate_evidence_coverage
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from schema import validate_canonical, validate_no_duplicates, validate_evidence_coverage

# ─── Path Resolution ───
ENGINE_DIR = Path(__file__).parent.parent  # scripts/ → intelligence-engine/

# ─── Closed Taxonomies (must match schema and SKILL.md) ───
GAP_TYPES = {
    "Missing", "Ignored", "Disconnected", "Untrusted",
    "Underutilized", "Misclassified", "Divergent"
}
ROOT_ORIGINS = {
    "Capture", "Integration", "Definition / Taxonomy",
    "Ownership", "Process / Cadence", "Tooling", "Behavior"
}
INTELLIGENCE_DIMS = [
    "Visibility", "Integrity", "Connectivity", "Governance",
    "Predictability", "Decision Quality", "Continuous Improvement"
]


class ManifestParser:
    """
    Parses the Audit Manifest markdown into canonical findings JSON.
    """

    def __init__(self, manifest_path: Path, charter_path: Optional[Path] = None):
        self.manifest_path = manifest_path
        self.charter_path = charter_path
        self.raw = manifest_path.read_text(encoding="utf-8")
        self.errors: List[str] = []
        self.warnings: List[str] = []

    # ─── Public API ───

    def parse(self) -> Dict[str, Any]:
        """Main entry: manifest → canonical JSON dict."""
        header = self._parse_header()
        artifacts = self._parse_artifacts()
        findings = self._parse_findings()
        synthesis = self._parse_synthesis()

        # Build canonical structure
        canonical = {
            "audit_id": header.get("audit_id", self._generate_audit_id()),
            "schema_version": "1.0.0",
            "charter_version": header.get("charter_version", "unknown"),
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "baseline": {
                "standards_declared": self._parse_standards(header.get("standards_baseline", "")),
                "artifacts_examined": artifacts,
                "scope": self._parse_scope(header.get("scope", ""))
            },
            "evidence_summary": self._compute_evidence_summary(artifacts),
            "findings": findings,
            "intelligence_indicators": synthesis["indicators"],
            "reporting_integrity_score": self._compute_ris(findings),
            "maturity_assessment": self._compute_maturity(findings, artifacts)
        }

        return canonical

    def validate(self, canonical: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Run all validations and return (is_valid, errors)."""
        all_errors: List[str] = []

        all_errors.extend(validate_canonical(canonical))
        all_errors.extend(validate_no_duplicates(canonical))
        all_errors.extend(validate_evidence_coverage(canonical))
        all_errors.extend(self.errors)

        return len(all_errors) == 0, all_errors

    # ─── Header Parsing ───

    def _parse_header(self) -> Dict[str, str]:
        """Extract header metadata from the manifest."""
        header = {}
        patterns = {
            "audit_id": r'\*\*Audit ID:\*\*\s*(.+?)(?=\n|$)',
            "charter_version": r'\*\*Charter Version:\*\*\s*(.+?)(?=\n|$)',
            "standards_baseline": r'\*\*Standards Baseline:\*\*\s*(.+?)(?=\n|$)',
            "scope": r'\*\*Scope:\*\*\s*(.+?)(?=\n|$)',
            "status": r'\*\*Status:\*\*\s*(.+?)(?=\n|$)',
            "date": r'\*\*Date:\*\*\s*(.+?)(?=\n|$)',
        }
        for key, pattern in patterns.items():
            match = re.search(pattern, self.raw, re.IGNORECASE)
            if match:
                header[key] = match.group(1).strip()
        return header

    def _parse_standards(self, text: str) -> List[str]:
        """Parse comma-separated standards list."""
        return [s.strip() for s in text.split(",") if s.strip()]

    def _parse_scope(self, text: str) -> List[str]:
        """Parse comma-separated scope list."""
        return [s.strip() for s in text.split(",") if s.strip()]

    # ─── Artifact Parsing ───

    def _parse_artifacts(self) -> List[Dict[str, Any]]:
        """Extract all ## ARTIFACT: blocks."""
        artifacts = []
        pattern = r'## ARTIFACT:\s*(ART-\d{3})\n(.*?)(?=## ARTIFACT:|## SYNTHESIS|### FINDING:|$)'
        for match in re.finditer(pattern, self.raw, re.DOTALL):
            art_id = match.group(1)
            block = match.group(2)
            art = {
                "artifact_id": art_id,
                "artifact_name": self._extract_field(block, "Artifact Name") or art_id,
                "source_path": self._extract_field(block, "Path") or "unknown",
                "checksum": self._extract_field(block, "Checksum") or "computed"
            }
            coverage = self._parse_percentage(self._extract_field(block, "Field Coverage"))
            if coverage is not None:
                art["field_coverage_pct"] = coverage
            artifacts.append(art)
        return artifacts

    # ─── Finding Parsing ───

    def _parse_findings(self) -> List[Dict[str, Any]]:
        """Extract all ### FINDING: blocks."""
        findings = []
        pattern = r'### FINDING:\s*(FIND-\d{4})\n(.*?)(?=### FINDING:|## SYNTHESIS|$)'
        for match in re.finditer(pattern, self.raw, re.DOTALL):
            fid = match.group(1)
            block = match.group(2)
            finding = self._parse_single_finding(fid, block)
            if finding:
                findings.append(finding)
        return findings

    def _parse_single_finding(self, fid: str, block: str) -> Optional[Dict[str, Any]]:
        """Parse one finding block."""
        gap_type = self._extract_field(block, "Gap Type")
        root_origin = self._extract_field(block, "Root Origin")

        # Validate closed taxonomies
        if gap_type not in GAP_TYPES:
            self.errors.append(f"{fid}: Invalid gap_type '{gap_type}'")
            return None
        if root_origin not in ROOT_ORIGINS:
            self.errors.append(f"{fid}: Invalid root_origin '{root_origin}'")
            return None

        # Parse evidence bullets
        evidence = self._parse_evidence_bullets(block)
        if not evidence:
            self.errors.append(f"{fid}: No evidence bullets found")
            return None

        # Parse intelligence dimensions
        dims_text = self._extract_field(block, "Intelligence Dimensions") or ""
        dims = [d.strip() for d in dims_text.split(",") if d.strip() in INTELLIGENCE_DIMS]

        # Parse severity
        sev_str = self._extract_field(block, "Severity") or "3"
        try:
            severity = int(sev_str)
            if not 1 <= severity <= 5:
                raise ValueError
        except ValueError:
            self.errors.append(f"{fid}: Invalid severity '{sev_str}'")
            severity = 3

        return {
            "id": fid,
            "gap_type": gap_type,
            "root_origin": root_origin,
            "description": self._extract_field(block, "Description") or "",
            "evidence": evidence,
            "standard_reference": {
                "standard": self._extract_field(block, "Standard") or "",
                "clause": self._extract_field(block, "Clause") or "",
                "identifier": self._extract_field(block, "Identifier") or "",
                "summary": self._extract_field(block, "Requirement Summary") or ""
            },
            "severity": severity,
            "impact": self._extract_field(block, "Impact") or "",
            "recommended_action": self._extract_field(block, "Recommended Action") or "",
            "intelligence_dimensions": dims
        }

    def _parse_evidence_bullets(self, block: str) -> List[Dict[str, str]]:
        """Parse '- **Artifact:** ... | **Location:** ... | **Evidence:** ...' bullets."""
        evidence = []
        pattern = r'-\s*\*\*Artifact:\*\*\s*(.*?)\s*\|\s*\*\*Location:\*\*\s*(.*?)\s*\|\s*\*\*Evidence:\*\*\s*(.*?)(?=\n- \*\*Artifact:|\n\n|$)'
        for match in re.finditer(pattern, block, re.DOTALL):
            evidence.append({
                "artifact_id": match.group(1).strip(),
                "location": match.group(2).strip(),
                "quote_or_absence": match.group(3).strip()
            })
        return evidence

    # ─── Synthesis Parsing ───

    def _parse_synthesis(self) -> Dict[str, Any]:
        """Extract intelligence indicators and OPM3 statement from ## SYNTHESIS."""
        indicators = {}

        match = re.search(r'## SYNTHESIS(.*?)(?=## APPENDIX|$)', self.raw, re.DOTALL | re.IGNORECASE)
        if not match:
            self.warnings.append("No SYNTHESIS section found")
            return {"indicators": indicators, "opm3": "PENDING_BRIDGE"}

        synth_text = match.group(1)

        for dim in INTELLIGENCE_DIMS:
            dim_key = dim.lower().replace(" ", "_")
            indicators[dim_key] = "No significant evidence observed."
            dim_pattern = rf'###\s*{re.escape(dim)}\n(.*?)(?=###\s|## |$)'
            dim_match = re.search(dim_pattern, synth_text, re.DOTALL | re.IGNORECASE)
            if dim_match:
                indicators[dim_key] = dim_match.group(1).strip()

        # Extract OPM3 statement
        opm3_match = re.search(r'###\s*OPM3.*?Position.*?\n(.*?)(?=###|##|$)', synth_text, re.DOTALL | re.IGNORECASE)
        opm3 = opm3_match.group(1).strip() if opm3_match else "PENDING_BRIDGE"

        return {"indicators": indicators, "opm3": opm3}

    # ─── Scoring (Deterministic) ───

    def _compute_ris(self, findings: List[Dict]) -> Dict[str, Any]:
        """
        Reporting Integrity Score v1.0.0 — deterministic.
        Formula:
        - Base: 100
        - Deduct severity points: sum(severity * 2) capped at 60
        - Deduct density penalty: (findings / artifacts) * 10, capped at 20
        - Deduct root cause diversity penalty: unique origins > 4 ? 10 : 0
        - Deduct Missing gap penalty: count(Missing) * 3, capped at 20
        """
        if not findings:
            return {"score": 100.0, "methodology": "Weighted Gap Profile v1.0.0", "version": "1.0.0"}

        total_severity = sum(f["severity"] for f in findings)
        severity_deduction = min(total_severity * 2, 60)

        # Artifact count from manifest or default to 1
        art_count = max(len(self._parse_artifacts()), 1)
        density = len(findings) / art_count
        density_deduction = min(density * 10, 20)

        origins = {f["root_origin"] for f in findings}
        diversity_deduction = 10 if len(origins) > 4 else 0

        missing_count = sum(1 for f in findings if f["gap_type"] == "Missing")
        missing_deduction = min(missing_count * 3, 20)

        score = max(0.0, 100.0 - severity_deduction - density_deduction - diversity_deduction - missing_deduction)

        return {
            "score": round(score, 2),
            "methodology": "Weighted Gap Profile v1.0.0",
            "version": "1.0.0"
        }

    def _compute_maturity(self, findings: List[Dict], artifacts: List[Dict]) -> Dict[str, Any]:
        """
        OPM3 Maturity Assessment.
        
        Rule: No bridge rubric → PENDING_BRIDGE.
        The bridge is loaded from registries/opm3_bridge.json.
        If absent or empty, we do not guess maturity.
        """
        bridge_path = ENGINE_DIR / "registries" / "opm3_bridge.json"
        ris = self._compute_ris(findings)["score"]
        art_count = max(len(artifacts), 1)
        gap_density = len(findings) / art_count
        severity_dist = {str(i): sum(1 for f in findings if f["severity"] == i) for i in range(1, 6)}

        # Try to load ratified bridge rubric
        if bridge_path.exists():
            try:
                bridge = json.loads(bridge_path.read_text(encoding="utf-8"))
                if bridge.get("status") == "RATIFIED" and bridge.get("rubric"):
                    position = self._apply_opm3_bridge(findings, bridge["rubric"])
                    return {
                        "opm3_position": position,
                        "evidence_summary": f"Bridge: {bridge.get('version', 'unknown')}. "
                                            f"{len(findings)} findings, {gap_density:.2f} gaps/artifact, RIS {ris}",
                        "bridge_version": bridge.get("version", "unknown"),
                        "gap_density": round(gap_density, 4),
                        "gap_severity_distribution": severity_dist
                    }
            except Exception as e:
                self.warnings.append(f"OPM3 bridge found but unreadable: {e}")

        # Default: PENDING_BRIDGE — we do not invent maturity
        return {
            "opm3_position": "PENDING_BRIDGE",
            "evidence_summary": f"Gap profile recorded: {len(findings)} findings, "
                                f"{gap_density:.2f} gaps/artifact, RIS {ris}. "
                                f"OPM3 bridge rubric not yet calibrated.",
            "bridge_version": "OPM3-Bridge-PENDING",
            "gap_density": round(gap_density, 4),
            "gap_severity_distribution": severity_dist
        }

    def _apply_opm3_bridge(self, findings: List[Dict], rubric: List[Dict]) -> str:
        """
        Apply a ratified OPM3 bridge rubric to the gap profile.
        Each rubric item defines a maturity level and the gap conditions that indicate it.
        """
        # Sort rubric by level priority (highest maturity first, or as defined)
        for rule in sorted(rubric, key=lambda r: r.get("priority", 0), reverse=True):
            if self._matches_rubric_rule(findings, rule):
                return rule["opm3_position"]
        return "Undetermined"

    def _matches_rubric_rule(self, findings: List[Dict], rule: Dict) -> bool:
        """
        Check if the current gap profile matches a rubric rule.
        Rules define thresholds for gap density, severity distribution, root origin patterns, etc.
        """
        # This is a placeholder for the actual rubric logic.
        # The rubric structure is defined in the bridge file.
        # Example rule: {"max_gap_density": 0.5, "max_severity_5": 0, "min_ris": 85, "opm3_position": "Level 3 - Defined"}
        gap_count = len(findings)
        art_count = max(len(self._parse_artifacts()), 1)
        density = gap_count / art_count
        ris = self._compute_ris(findings)["score"]
        
        checks = []
        if "max_gap_density" in rule:
            checks.append(density <= rule["max_gap_density"])
        if "min_gap_density" in rule:
            checks.append(density >= rule["min_gap_density"])
        if "max_severity_5" in rule:
            checks.append(sum(1 for f in findings if f["severity"] == 5) <= rule["max_severity_5"])
        if "min_ris" in rule:
            checks.append(ris >= rule["min_ris"])
        if "max_ris" in rule:
            checks.append(ris <= rule["max_ris"])
        if "required_origins" in rule:
            origins = {f["root_origin"] for f in findings}
            checks.append(all(o in origins for o in rule["required_origins"]))
        if "forbidden_gap_types" in rule:
            gap_types = {f["gap_type"] for f in findings}
            checks.append(not any(g in gap_types for g in rule["forbidden_gap_types"]))
        
        return all(checks) if checks else False

    def _compute_evidence_summary(self, artifacts: List[Dict]) -> Dict[str, Any]:
        """
        Averages the per-artifact Field Coverage the Manifest declares.
        total_fields_mapped is not derivable from the Manifest format (there is
        no per-field enumeration, only a per-artifact percentage) and stays 0
        until the Charter's Field Semantics Map is wired in as a source.
        """
        coverages = [a["field_coverage_pct"] for a in artifacts if "field_coverage_pct" in a]
        avg_coverage = round(sum(coverages) / len(coverages), 1) if coverages else 0.0
        return {
            "total_artifacts": len(artifacts),
            "total_fields_mapped": 0,
            "coverage_percentage": avg_coverage
        }

    # ─── Helpers ───

    def _extract_field(self, text: str, field: str) -> Optional[str]:
        """
        Extract **Field:** value from markdown.
        Uses non-greedy match and requires the field label to be explicitly present.
        """
        pattern = rf'\*\*{re.escape(field)}:\*\*\s*(.*?)(?=\n\*\*|\n\n\*\*|$)'
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if not match:
            return None
        value = match.group(1).strip()
        # Defensive: if the captured value starts with another **Label:**, we bled.
        # This happens when the original field was blank and greedy \s* ate the newline.
        if value.startswith("**") and ":" in value.split("**")[1].split("\n")[0]:
            # We captured the next field's label. Treat as blank.
            return ""
        return value

    @staticmethod
    def _parse_percentage(text: Optional[str]) -> Optional[float]:
        """Parse '85%' or '85' into 85.0. Returns None if unparseable."""
        if not text:
            return None
        match = re.search(r'(\d+(?:\.\d+)?)\s*%?', text)
        return float(match.group(1)) if match else None

    def _generate_audit_id(self) -> str:
        """Generate fallback audit ID."""
        return f"IEM-{datetime.now(timezone.utc).strftime('%Y%m%d')}-{hashlib.sha256(self.raw.encode()).hexdigest()[:6].upper()}"


# ─── CLI ───

def main():
    parser = argparse.ArgumentParser(description="IEM-PM: Manifest → Canonical Findings")
    parser.add_argument("--manifest", required=True, type=Path, help="Path to Audit Manifest markdown")
    parser.add_argument("--charter", type=Path, help="Optional: Path to ratified PMO Data Charter")
    parser.add_argument("--output", required=True, type=Path, help="Output path for findings.json")
    args = parser.parse_args()

    if not args.manifest.exists():
        print(f"ERROR: Manifest not found: {args.manifest}")
        exit(1)

    # Parse
    parser_engine = ManifestParser(args.manifest, args.charter)
    canonical = parser_engine.parse()

    # Validate
    is_valid, errors = parser_engine.validate(canonical)

    if not is_valid:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        exit(1)

    # Write
    args.output.write_text(json.dumps(canonical, indent=2), encoding="utf-8")
    print(f"Canonical findings written to {args.output}")
    print(f"Total findings: {len(canonical['findings'])}")
    print(f"Reporting Integrity Score: {canonical['reporting_integrity_score']['score']}")
    print(f"OPM3 Position: {canonical['maturity_assessment']['opm3_position']}")

    if parser_engine.warnings:
        print("\nWarnings:")
        for w in parser_engine.warnings:
            print(f"  - {w}")


if __name__ == "__main__":
    main()