---
Name: Completion Checklist
description: >
  The Final Validation checklist (10 checks), the Output Checklist (exactly one file you write),
  and the exact Handover Message template. Read once, at the very end of an audit, before
  declaring the Audit Manifest complete.
version: 1.0.0
---

## Contents

- [12.1 Final Validation](#121-final-validation)
- [12.2 Output Checklist](#122-output-checklist)
- [12.3 Handover Message](#123-handover-message)

## 12.1 Final Validation

Before you declare the audit complete, verify your Manifest against these checks:

1. **Every finding has evidence.** At least one evidence bullet per `### FINDING:` block.
2. **Every evidence bullet points to a Charter artifact.** No orphan references.
3. **Closed taxonomies are exact.** `Gap Type` and `Root Origin` match the seven allowed values exactly (case-sensitive).
4. **No duplicate signatures.** No two findings share the same Gap Type + Root Origin + Artifact + Standard Identifier.
5. **Severity is 1–5 integer.** No blanks, no decimals, no text.
6. **No standard text reproduced.** Every `Requirement Summary` is one sentence, paraphrased.
7. **Synthesis is complete.** All seven Intelligence Indicators have a narrative paragraph.
8. **Header Block is complete.** Audit ID, Charter Version, Standards, Scope, Date, Status, Skill Version, Model.
9. **No software instructions in Manifest.** No "run Python," no JSON blocks, no HTML.
10. **Every Severity 4/5 finding has real Human Approval.** You actually asked the human operator
    and recorded their real answer as `Human Approved`, never fabricated "Yes." If they approved
    it, `Approved By` (their real name/role) and `Approval Date` are also present — a bare
    "Approved" with no accountable name attached is rejected.

If any check fails, fix the Manifest before finishing. Do not hand over a broken Manifest to software.

## 12.2 Output Checklist

You produce exactly one file, named per Appendix G, written into the project's own `reports/`
folder (sibling of its `evidence/` folder):

| File                                           | You Write | Software Reads |
| ---------------------------------------------- | --------- | -------------- |
| `<project>/reports/IEMPM_AuditGap_Report_DDMMYY_HHMM.md` | ✓         | ✓              |

That is all. Software produces the matching `.json`, `.html`, and `.txt` files in the same folder,
using the same name stem:

- `<project>/reports/IEMPM_AuditGap_Report_DDMMYY_HHMM.json`
- `<project>/reports/IEMPM_AuditGap_Report_DDMMYY_HHMM.html`
- `<project>/reports/IEMPM_AuditGap_Report_DDMMYY_HHMM.txt`

You do not touch these.

## 12.3 Handover Message

When your Manifest is complete and validated, print exactly:

> **Audit Manifest complete.**
> **Findings:** [N]
> **Severity distribution:** 1=[n] · 2=[n] · 3=[n] · 4=[n] · 5=[n]
> **Root origin spread:** [List origins found]
> **Status:** [RATIFIED / PROVISIONAL]
> **Next:** Run `manifest_to_findings.py` to validate and generate canonical JSON.

Then stop. Your work is done.
