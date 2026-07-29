---
Name: Minimum Evidence Sufficiency Gate
description: >
  Halt Condition 6 (SKILL.md §6.6) — how the engine decides an evidence set is too thin to support
  a credible audit, even when every artifact supplied is present and readable. Read during Phase 0,
  before proposing or ratifying a Charter, and before halting on Condition 6.
version: 0.1.0-draft
---

## Contents

- [(a) Core Artifact Categories](#a-core-artifact-categories)
- [(b) Coverage Threshold](#b-coverage-threshold)
- [(c) Halt Output — Scope Limitation Notice](#c-halt-output--scope-limitation-notice)

## (a) Core Artifact Categories

Derived from the standards, not hardcoded. For a PMI-standard audit:

| Category | Domain | What "represented" means |
| --- | --- | --- |
| A — Authorization | Charter | The endeavor is formally authorized and governed. |
| B — Scope | Scope | Scope, schedule, and cost are baselined and interlinked. |
| C — Cost | Cost | Financial authority exists and is controlled. |
| D — Schedule | Schedule | Schedule is baselined. |
| E — Risk | Risk | Uncertainty is identified, analyzed, and owned. |
| F — Change Control | Change control | Scope creep is governed; deviations are traceable. |
| G — Performance Monitoring | Reports | Actuals are measured against baselines objectively. |

For non-PMI standards (PRINCE2, ISO 21502, internal methodology), the engine performs an equivalent
mapping using that standard's native domain model (e.g., PRINCE2 Themes → categories).

## (b) Coverage Threshold

A single artifact is never enough. The engine evaluates the evidence set against three cumulative
rules.

**Rule 1 — Mandatory Categories (Non-Waivable)**
Category A (Authorization) and Category E (Risk) must each be represented by at least one artifact.
TODO(you): mandatory coverage requirement for Categories B/C/D (Scope/Cost/Schedule) — all three, at
least one, or at least two. If any mandatory category is missing → HALT immediately. No exceptions.

**Rule 2 — Minimum Breadth**
TODO(you): minimum number of the 7 categories in (a) that must be represented across the evidence
set. Below that number → HALT.

**Rule 3 — Minimum Artifact Count**
At least 3 distinct artifacts must be provided. If fewer than 3 → HALT, even if they nominally cover
enough categories to satisfy Rule 2. Prevents a single "kitchen-sink" document from gaming the gate.

Rule 1 ensures the audit has a foundation: authority to exist, a plan to measure against, and risk
governance. Rule 2 ensures breadth — PMI standards are integrated, so integration can't be credibly
assessed if most Performance Domains have no evidence. Rule 3 ensures independence of evidence: one
document cannot simultaneously prove charter authority, baseline integrity, and risk governance —
those are separate processes with separate owners and separate artifacts in any functioning PMO.

## (c) Halt Output — Scope Limitation Notice

If the evidence set fails the sufficiency gate, the engine writes:

- `reports/IEMPM_ScopeLimitation_Notice_DDMMYY_HHMM.md`
- `reports/IEMPM_ScopeLimitation_Notice_DDMMYY_HHMM.html`

No `.txt`/`.json` — there is no findings data to emit. No Gap Register, no Reporting Integrity
Score. The notice states which categories and rules failed, and why.
