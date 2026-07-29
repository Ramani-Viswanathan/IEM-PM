---
Name: Report Generation
description: >
  How your Audit Manifest becomes the 10-section rendered report — per-section content rules,
  what you must never write, and the pre-handover output checklist. Read before finishing any
  audit (SKILL.md §11).
version: 1.0.0
---

## Contents

- [The 10 Report Sections](#the-10-report-sections)
- [Per-Section Content Rules for Your Manifest](#per-section-content-rules-for-your-manifest)
- [What You Must Never Do](#what-you-must-never-do)
- [Output Checklist for Your Manifest](#output-checklist-for-your-manifest)

# 11. Report Generation

You do **not** generate the final report. Software renders it from your Audit Manifest.

However, your Manifest is the **source material** for the report. If a section is missing from your Manifest, the report cannot produce it. Write your Manifest knowing it will become these 10 sections.

---

## The 10 Report Sections

Software produces the report in this order:

| #   | Section                                                 | Source in Your Manifest                     | What You Must Provide                                                                                                              |
| --- | ------------------------------------------------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Executive Summary**                                   | Header Block + Gap Register                 | Audit ID, scope, total findings, severity distribution. Software computes the Reporting Integrity Score.                           |
| 2   | **Audit Scope**                                         | Header Block + Per-Artifact Evidence Log    | Standards declared, artifacts examined, Charter version, status (ratified/provisional).                                            |
| 3   | **Delivery Baseline**                                   | Header Block                                | List of governing standards with version/edition references.                                                                       |
| 4   | **Delivery Evidence**                                   | Per-Artifact Evidence Log                   | For each artifact: ID, path, status, field coverage, and your narrative observations.                                              |
| 5   | **Gap Register**                                        | Finding Blocks (all `### FINDING:`)         | Every finding with gap type, root origin, severity, evidence, and recommended action. This is the core of the report.              |
| 6   | **Root Cause Analysis**                                 | Finding Blocks                              | Software aggregates your root origins into a frequency table. You do not write the table — you assign the origins in each finding. |
| 7   | **Intelligence Indicators + Reporting Integrity Score** | Synthesis Section                           | Your narrative for all 7 dimensions. Software computes the score and places it alongside your text.                                |
| 8   | **Recommended Actions**                                 | Finding Blocks — `Recommended Action` field | Software extracts all recommended actions and groups them by root origin for prioritization.                                       |
| 9   | **Roadmap**                                             | Finding Blocks — severity + root origin     | Software generates a remediation roadmap from your severity scores and root origin distribution.                                   |
| 10  | **Appendix**                                            | Appendix section of Manifest                | Schema version, artifact checksums, file references.                                                                               |

---

## Per-Section Content Rules for Your Manifest

### Section 1–3: Front Matter

Keep the Header Block complete. Software pulls:

- `Audit ID` for report branding
- `Charter Version` and `Status` for scope credibility
- `Standards Baseline` for the Delivery Baseline section

### Section 4: Delivery Evidence

In your Per-Artifact Evidence Log, write observations that are:

- **Factual** — "47 of 50 required fields present"
- **Specific** — "Sheet 'Project Plan' contains baseline dates; Sheet 'Actuals' is empty"
- **Neutral** — describe what is there, not what should be there (that comes in findings)

### Section 5: Gap Register

This is the heart of the report. Every `### FINDING:` block becomes one entry. Ensure:

- Evidence bullets are **quotable** — software will reproduce them verbatim
- Descriptions are **self-contained** — a reader should understand the gap without reading the standard
- Recommended actions are **actionable** — not "fix this" but "Assign a risk owner to all open risks by [date]"

### Section 6: Root Cause Analysis

You do not write this section. You assign root origins in each finding. Software counts and charts them. But write your root origin choices as if they will be aggregated — be consistent.

### Section 7: Intelligence Indicators

Write one paragraph per dimension in the Synthesis section. Each paragraph should:

- Reference specific findings by ID (e.g., "FIND-0001 and FIND-0003 indicate...")
- Explain the pattern, not just list gaps
- Stay qualitative — no "score: 7/10" language

### Section 8–9: Recommended Actions & Roadmap

Software builds these from your findings. Make your `Recommended Action` field in each finding:

- Specific enough to execute (who should do what by when)
- Tied to the root origin (fix the cause, not the symptom)
- Prioritizable by severity

### Section 10: Appendix

Keep it minimal. Software may add computed fields (gap density, checksums, timestamps).

---

## What You Must Never Do

- **Never write HTML, CSS, or markdown tables for findings** — software renders these. Your Finding blocks are the source.
- **Never write an "Executive Summary" in your Manifest** — software generates this from your Header and Gap Register.
- **Never write "Section 1: Executive Summary" headers in your Manifest** — your Manifest has its own structure (Header, Evidence Log, Findings, Synthesis, Appendix). Software maps this to the 10 report sections.
- **Never attempt to format for print** — page breaks, fonts, and layout are renderer concerns.

---

## Output Checklist for Your Manifest

Before you finish writing, verify your Manifest contains:

- [ ] Header Block with all fields
- [ ] Per-Artifact Evidence Log for every artifact in scope
- [ ] One `### FINDING:` block per gap (minimum one evidence bullet each)
- [ ] Synthesis section with all 7 Intelligence Indicators
- [ ] Appendix with schema version and artifact list

If all are present, software can render the full report. If any are missing, the report will have gaps.

---
