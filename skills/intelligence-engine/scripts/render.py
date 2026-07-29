#!/usr/bin/env python3
"""
IEM-PM Renderer — Contract 5 / Stage 9
Reads canonical findings JSON and produces HTML + TXT reports.
Deterministic: same JSON in → byte-identical out.
"""

import json
import argparse
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
from jinja2 import Template

try:
    from paths import REPORTS_DIR, DEFAULT_TEMPLATE
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent))
    from paths import REPORTS_DIR, DEFAULT_TEMPLATE


def _to_utc(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)


def _iempm_filename(dt: datetime, ext: str) -> str:
    """IEMPM_AuditGap_Report_DDMMYY_HHMM.<ext> -- see references/file-naming.md."""
    return f"IEMPM_AuditGap_Report_{_to_utc(dt).strftime('%d%m%y_%H%M')}.{ext}"


def _parse_iso(iso_string: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
    except Exception:
        return None


def load_template(template_path: Path) -> Template:
    with open(template_path, "r", encoding="utf-8") as f:
        return Template(f.read())


def render_html(canonical: dict, template: Template) -> str:
    findings = canonical.get("findings", [])
    return template.render(
        audit=canonical,
        generated_at=_format_timestamp(canonical.get("generated_at", "")),
        findings_count=len(findings),
        severity_counts=_count_by(findings, "severity"),
        gap_counts=_count_by(findings, "gap_type"),
        origin_counts=_count_by(findings, "root_origin"),
        artifact_count=len(canonical.get("baseline", {}).get("artifacts_examined", []))
    )


def render_txt(canonical: dict) -> str:
    lines = [
        "=" * 80,
        "IEM-PM  PMO DATA GAP AUDIT REPORT",
        "=" * 80,
        f"Audit ID:       {canonical['audit_id']}",
        f"Charter:        {canonical['charter_version']}",
        f"Generated:      {_format_timestamp(canonical.get('generated_at', ''))}",
        f"Schema:         {canonical['schema_version']}",
        "",
        "1. EXECUTIVE SUMMARY",
        "-" * 40,
        f"Total Findings: {len(canonical.get('findings', []))}",
        f"Reporting Integrity Score: {canonical['reporting_integrity_score']['score']}/100",
        "",
        "2. AUDIT SCOPE & BASELINE",
        "-" * 40,
        f"Standards: {', '.join(canonical['baseline']['standards_declared'])}",
        f"Artifacts Examined: {len(canonical['baseline']['artifacts_examined'])}",
        f"Scope: {', '.join(canonical['baseline']['scope'])}",
        "",
        "3. DELIVERY EVIDENCE SUMMARY",
        "-" * 40,
        f"Total artifacts: {canonical['evidence_summary']['total_artifacts']}",
        f"Field coverage: {canonical['evidence_summary']['coverage_percentage']}%",
        "",
        "4. GAP REGISTER",
        "-" * 40,
    ]

    for f in canonical.get("findings", []):
        lines.extend([
            "",
            f"  {f['id']} | {f['gap_type']} | Severity: {f['severity']}/5",
            f"  Origin: {f['root_origin']}",
            f"  Standard: {f['standard_reference']['standard']} {f['standard_reference']['identifier']}",
            f"  {f['description']}",
            "  Evidence:",
        ])
        for ev in f.get("evidence", []):
            quote = ev["quote_or_absence"][:120]
            if len(ev["quote_or_absence"]) > 120:
                quote += "..."
            lines.append(f"    - {ev['artifact_id']} @ {ev['location']}: {quote}")
        lines.append(f"  Action: {f['recommended_action']}")

    lines.extend([
        "",
        "5. ROOT CAUSE ANALYSIS",
        "-" * 40,
    ])
    for origin, count in _count_by(canonical.get("findings", []), "root_origin").items():
        pct = (count / max(len(canonical.get("findings", [])), 1)) * 100
        lines.append(f"  {origin:25s} : {count:3d} ({pct:5.1f}%)")

    lines.extend([
        "",
        "6. INTELLIGENCE INDICATORS (Narrative)",
        "-" * 40,
    ])
    for dim, text in canonical.get("intelligence_indicators", {}).items():
        lines.append(f"  {dim.replace('_', ' ').title()}:")
        suffix = "..." if len(text) > 180 else ""
        lines.append(f"    {text[:180]}{suffix}")
        lines.append("")

    lines.extend([
        "7. REPORTING INTEGRITY SCORE",
        "-" * 40,
        f"  Score: {canonical['reporting_integrity_score']['score']}/100",
        f"  Methodology: {canonical['reporting_integrity_score']['methodology']}",
        "",
        "8. RECOMMENDED ACTIONS",
        "-" * 40,
    ])
    for i, f in enumerate(canonical.get("findings", []), 1):
        lines.append(f"  {i}. [{f['id']}] {f['recommended_action']}")
        lines.append(f"      (Addresses {f['root_origin']} origin)")

    lines.extend([
        "",
        "9. ROADMAP",
        "-" * 40,
        "  Prioritize by root origin frequency and severity concentration:",
        "  1. Address highest-frequency root origin first",
        "  2. Resolve all Severity 5 gaps within 30 days",
        "  3. Close Missing gaps by updating Charter or capturing data",
        "  4. Re-run audit after remediation to measure delta",
        "",
        "10. APPENDIX",
        "-" * 40,
        f"  Schema Version: {canonical['schema_version']}",
        "  Canonical JSON: (see separate file)",
        "",
        "=" * 80,
        "END OF REPORT",
        "=" * 80,
    ])

    return "\n".join(lines)


def _count_by(findings: list, key: str) -> dict:
    counts = {}
    for f in findings:
        val = f.get(key, "Unknown")
        counts[val] = counts.get(val, 0) + 1
    return dict(sorted(counts.items()))


def _format_timestamp(iso_string: str) -> str:
    dt = _parse_iso(iso_string)
    return dt.strftime("%Y-%m-%d %H:%M UTC") if dt else (iso_string or "unknown")


def main():
    parser = argparse.ArgumentParser(description="IEM-PM: JSON → HTML + TXT")
    parser.add_argument("--canonical", required=True, type=Path, help="Path to findings.json")
    parser.add_argument(
        "--template", type=Path, default=None,
        help=f"Path to HTML template. Defaults to {DEFAULT_TEMPLATE.name}.",
    )
    parser.add_argument(
        "--output-html", type=Path, default=None,
        help="Output path for the HTML report. Defaults to reports/IEMPM_AuditGap_Report_"
             "DDMMYY_HHMM.html (Appendix G) using the audit's own Date.",
    )
    parser.add_argument(
        "--output-txt", type=Path, default=None,
        help="Output path for the TXT report. Defaults to reports/IEMPM_AuditGap_Report_"
             "DDMMYY_HHMM.txt (Appendix G) using the audit's own Date.",
    )
    args = parser.parse_args()

    if not args.canonical.exists():
        print(f"[E-RENDER-001] Canonical findings JSON not found: {args.canonical}")
        exit(1)

    canonical = json.loads(args.canonical.read_text(encoding="utf-8"))
    audit_dt = _parse_iso(canonical.get("generated_at", "")) or datetime.now(timezone.utc)

    # Explicit paths always win; otherwise use the naming convention (Appendix G).
    output_txt = args.output_txt or (REPORTS_DIR / _iempm_filename(audit_dt, "txt"))
    output_html = args.output_html or (REPORTS_DIR / _iempm_filename(audit_dt, "html"))
    template_path = args.template or DEFAULT_TEMPLATE

    if args.output_txt is None or args.output_html is None:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # TXT
    txt = render_txt(canonical)
    output_txt.write_text(txt, encoding="utf-8")
    print(f"TXT report: {output_txt}")

    # HTML
    template = load_template(template_path)
    html = render_html(canonical, template)
    output_html.write_text(html, encoding="utf-8")
    print(f"HTML report: {output_html}")


if __name__ == "__main__":
    main()