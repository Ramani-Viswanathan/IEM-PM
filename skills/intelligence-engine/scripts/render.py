#!/usr/bin/env python3
"""
IEM-PM Renderer — Contract 5 / Stage 9
Reads canonical findings JSON and produces HTML + TXT reports.
Deterministic: same JSON in → byte-identical out.
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from jinja2 import Template


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
    try:
        dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return iso_string or "unknown"


def main():
    parser = argparse.ArgumentParser(description="IEM-PM: JSON → HTML + TXT")
    parser.add_argument("--canonical", required=True, type=Path, help="Path to findings.json")
    parser.add_argument("--template", type=Path, help="Path to HTML template")
    parser.add_argument("--output-html", type=Path, help="Output path for report.html")
    parser.add_argument("--output-txt", type=Path, help="Output path for report.txt")
    args = parser.parse_args()

    canonical = json.loads(args.canonical.read_text(encoding="utf-8"))

    # TXT
    if args.output_txt:
        txt = render_txt(canonical)
        args.output_txt.write_text(txt, encoding="utf-8")
        print(f"TXT report: {args.output_txt}")

    # HTML
    if args.output_html and args.template:
        template = load_template(args.template)
        html = render_html(canonical, template)
        args.output_html.write_text(html, encoding="utf-8")
        print(f"HTML report: {args.output_html}")

    if not args.output_txt and not args.output_html:
        print("ERROR: Specify at least one of --output-html or --output-txt")
        exit(1)


if __name__ == "__main__":
    main()