---
Name: Minimum Evidence Sufficiency Gate
description: >
  Halt Condition 6 (SKILL.md §6.6) — how the engine decides an evidence set is too thin to support
  a credible audit, even when every artifact supplied is present and readable. Read during Phase 0,
  before proposing or ratifying a Charter, and before halting on Condition 6.
version: 0.1.0-draft
---

## Contents

- [Status](#status)
- [(a) Core Artifact Categories — Derived from Standards, Not Hardcoded](#a-core-artifact-categories--derived-from-standards-not-hardcoded)
- [(b) Coverage Threshold — The Rules That Trigger the Halt](#b-coverage-threshold--the-rules-that-trigger-the-halt)
- [(c) Halt Output — Scope Limitation Notice](#c-halt-output--scope-limitation-notice)
- [Open Questions Before This Is Final](#open-questions-before-this-is-final)

## Status

**Draft — not yet ratified.** Authored 2026-07-29 in response to Pilot-audit-4 (a 1-artifact
evidence set that reached Charter proposal instead of halting). Two internal inconsistencies are
flagged below and need a decision before this gate goes live — see
[Open Questions](#open-questions-before-this-is-final). Do not treat this file as authoritative
until `version` above is bumped past `0.1.0-draft`.

## (a) Core Artifact Categories — Derived from Standards, Not Hardcoded

If the Audit Gap is performed against a PMI standard, these are the observable artifact categories:

| Category                   | Domain         | What "represented" means                                 |
| -------------------------- | -------------- | -------------------------------------------------------- |
| A — Authorization          | Charter        | The endeavor is formally authorized and governed.        |
| B — Scope                  | Scope          | Scope, schedule, and cost are baselined and interlinked. |
| C — Cost                   | Cost           | Financial authority exists and is controlled.            |
| D — Schedule               | Schedule       | Schedule is baselined.                                   |
| E — Risk                   | Risk           | Uncertainty is identified, analyzed, and owned.          |
| F — Change Control         | Change control | Scope creep is governed; deviations are traceable.       |
| G — Performance Monitoring | Reports        | Actuals are measured against baselines objectively.      |

Seven categories, confirmed 2026-07-29 — reconciles with Rule 2's "7 derived categories" below.

For non-PMI standards (PRINCE2, ISO 21502, internal methodology), the engine performs an equivalent
mapping using that standard's native domain model (e.g., PRINCE2 Themes → categories).

## (b) Coverage Threshold — The Rules That Trigger the Halt

A single artifact is never enough. The engine evaluates the evidence set against three cumulative
rules.

**Rule 1 — Mandatory Categories (Non-Waivable)**
Category A (Authorization) and Category E (Risk) must each be represented by at least one artifact.
⚠️ **Open question (see below):** the original draft also required "Planning & Baselines" as one
mandatory category — now that Scope/Cost/Schedule are three separate categories (B/C/D), does Rule 1
require _all three_, _at least one_, or _at least two_ of them, in addition to A and E? If any
mandatory category/combination is missing → HALT immediately. No exceptions.

**Rule 2 — Minimum Breadth**
At least 4 of the 7 derived categories must be represented across the evidence set. If coverage < 5
categories → HALT.

**Rule 3 — Minimum Artifact Count**
At least 3 distinct artifacts must be provided. If < 3 artifacts → HALT, even if they nominally
cover 5+ categories. (Prevents a single "kitchen-sink" document from gaming the gate.)

**Why each rule exists:**

- Rule 1 ensures the audit has a foundation: authority to exist, a plan to measure against, and risk
  governance. Without any one of these, you are not auditing a managed project — you are describing
  an unmanaged initiative.
- Rule 2 ensures breadth. PMI standards are integrated; you cannot credibly assess integration if
  half the Performance Domains have no evidence.
- Rule 3 ensures independence of evidence. One document cannot simultaneously prove charter
  authority, baseline integrity, and risk governance — those are separate processes with separate
  owners and separate artifacts in any functioning PMO.

## (c) Halt Output — Scope Limitation Notice

If the evidence set fails the sufficiency gate, the engine writes:

- `reports/IEMPM_ScopeLimitation_Notice_DDMMYY_HHMM.md`
- `reports/IEMPM_ScopeLimitation_Notice_DDMMYY_HHMM.html`

Confirmed 2026-07-29: `.md` + `.html` only — no `.txt`, no `.json`. There's no findings data to
emit (that's the point of the halt), so the 4-file Audit Gap Report parity doesn't apply here.

No Gap Register, no Reporting Integrity Score — the notice states which categories/rules failed
and why, not a scored result.

## Open Questions Before This Is Final

Flagging these rather than silently resolving them — both change what the gate actually does:

1. ~~Category count doesn't reconcile~~ — **resolved 2026-07-29.** Confirmed 7 distinct categories
   (A–G): Scope, Cost, and Schedule are three separate categories, not one combined "Planning &
   Baselines" row. Table above updated.
2. **New, from resolving #1: what does Rule 1 require of B/C/D (Scope/Cost/Schedule)?** The
   original "Planning & Baselines" was a single mandatory category; split three ways, Rule 1 needs
   to say explicitly whether all three, any one, or a minimum of two are mandatory alongside A and
   E. Flagged inline in Rule 1 above.
3. **Rule 2's own threshold contradicts itself.** First sentence: "at least 4 ... must be
   represented." Second sentence: "if coverage < 5 categories → HALT." Those are two different
   thresholds (halting below 4 vs. below 5) — pick one. Still open.
4. ~~Output formats~~ — **resolved 2026-07-29.** `.md` + `.html` only, confirmed. No `.txt`/`.json` —
   there's no findings data to emit, so the 4-file Audit Gap Report parity doesn't apply.
5. **Not yet done:** `references/file-naming.md` (Appendix G) only documents the
   `IEMPM_AuditGap_Report_...` pattern. Once this gate is final, Appendix G needs the
   `IEMPM_ScopeLimitation_Notice_...` pattern added alongside it, and `manifest_to_findings.py`/
   `render.py` (or a new script) need to actually implement Rules 1–3 and this halt output —
   none of that exists yet. This file specifies the _design_, not the _build_.
