---
Name: Output File Naming
description: >
  Appendix G — the IEMPM_AuditGap_Report_DDMMYY_HHMM.<ext> and IEMPM_ScopeLimitation_Notice_
  DDMMYY_HHMM.<ext> naming conventions shared by every artifact generated for a given audit or
  halt, and why the timestamp comes from the audit's own Date, not wall-clock run time. Read
  before Stage 9 (Render), when writing the Manifest's Date field, or on Halt Condition 6.
version: 1.1.0
---

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

All four live in a `reports/` folder that is a **sibling of the `evidence/` folder** for the project
being audited — e.g. `Audit/<ProjectName>/reports/`, next to `Audit/<ProjectName>/evidence/`. There
is no single shared reports location: every project gets its own. `manifest_to_findings.py` and
`render.py` derive this automatically from their own input path (the `--manifest` / `--canonical`
file's parent folder) whenever an explicit `--output`/`--output-html`/`--output-txt` isn't given —
see `scripts/paths.py`'s header comment. Gitignored, local-only — see repo `.gitignore`
(`Audit/*` / `!Audit/README.md`).

**Example**, for a project at `Audit/Acme-Q3-2026/` with an audit dated `2026-07-27T14:30:00Z`:

```
Audit/Acme-Q3-2026/evidence/...                                    <- your artifacts
Audit/Acme-Q3-2026/reports/IEMPM_AuditGap_Report_270726_1430.md
Audit/Acme-Q3-2026/reports/IEMPM_AuditGap_Report_270726_1430.json
Audit/Acme-Q3-2026/reports/IEMPM_AuditGap_Report_270726_1430.html
Audit/Acme-Q3-2026/reports/IEMPM_AuditGap_Report_270726_1430.txt
```

### Enforcement

`manifest_to_findings.py` and `render.py` compute this name automatically (see `_iempm_filename()`
in each script) from the audit's own Date, and write into the same folder as their own input file
whenever `--output` / `--output-html` / `--output-txt` is not explicitly given. An explicit path
always overrides the convention — useful for tests and one-off comparisons — but production runs
should let the default apply.

### Known limitation

Two audits dated to the same UTC minute would collide on this name. Given real PMO audits run at
most a few times a day, this is accepted rather than engineered around. The `audit_id` inside
every file (e.g. `IEM-20260727-MRD001`) is the true unique identifier if you ever need one.

## Halt Condition 6 — Scope Limitation Notice naming

A halted audit (Minimum Evidence Sufficiency Gate — see references/evidence-sufficiency.md) shares
the same stem convention, on its own prefix:

```
IEMPM_ScopeLimitation_Notice_DDMMYY_HHMM.<ext>
```

`DDMMYY_HHMM` is derived the same way — from the notice's own `generated_at` frontmatter field, not
wall-clock run time.

| Artifact           | Extension | Written by                             |
| ------------------- | --------- | ---------------------------------------- |
| Scope Limitation Notice | `.md`     | You (the LLM) — see evidence-sufficiency.md (c) |
| HTML notice          | `.html`   | `render_scope_limitation.py`           |

No `.json`/`.txt` variant exists for this family — a halted audit produces no findings data to
canonicalize (evidence-sufficiency.md (c)). `render_scope_limitation.py` defaults `--output-html`
to the `--notice` path with its extension swapped, so both files always share one stem.

**Example**, for a notice dated `2026-07-29T00:00:00Z`, project `Audit/Acme-Q3-2026/`:

```
Audit/Acme-Q3-2026/reports/IEMPM_ScopeLimitation_Notice_290726_0000.md
Audit/Acme-Q3-2026/reports/IEMPM_ScopeLimitation_Notice_290726_0000.html
```
