## Appendix G — Output File Naming

Every artifact produced for a given audit shares one file-name stem, differing only by extension:

```
IEMPM_AuditGap_Report_DDMMYY_HHMM.<ext>
```

- `DDMMYY` — day, month, two-digit year (e.g. 27 Jul 2026 → `270726`).
- `HHMM` — hour and minute, 24-hour, **UTC** (e.g. 14:30 UTC → `1430`).
- Both are derived from **the audit's own Date** — the same value written into the Manifest
  header's `**Date:**` field (§10.2.1) — never from the wall-clock moment an individual script
  happens to run. This is what lets every artifact from one audit share an identical name even
  when `manifest_to_findings.py` and `render.py` run minutes apart.

| Artifact                 | Extension | Written by                             |
| ------------------------- | --------- | ---------------------------------------- |
| Audit Manifest            | `.md`     | You (the LLM) — see SKILL.md §10.6     |
| Canonical Findings JSON   | `.json`   | `manifest_to_findings.py`              |
| HTML report               | `.html`   | `render.py`                            |
| TXT report                | `.txt`    | `render.py`                            |

All four live in `reports/` (gitignored, local-only — see repo `.gitignore`).

**Example**, for an audit dated `2026-07-27T14:30:00Z`:

```
reports/IEMPM_AuditGap_Report_270726_1430.md
reports/IEMPM_AuditGap_Report_270726_1430.json
reports/IEMPM_AuditGap_Report_270726_1430.html
reports/IEMPM_AuditGap_Report_270726_1430.txt
```

### Enforcement

`manifest_to_findings.py` and `render.py` compute this name automatically (see `_iempm_filename()`
in each script) from the audit's own Date, and use it whenever `--output` / `--output-html` /
`--output-txt` is not explicitly given. An explicit path always overrides the convention — useful
for tests and one-off comparisons — but production runs should let the default apply.

### Known limitation

Two audits dated to the same UTC minute would collide on this name. Given real PMO audits run at
most a few times a day, this is accepted rather than engineered around. The `audit_id` inside
every file (e.g. `IEM-20260727-MRD001`) is the true unique identifier if you ever need one.
