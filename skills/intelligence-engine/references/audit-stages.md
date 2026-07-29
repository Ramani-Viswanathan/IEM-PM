---
Name: Audit State Machine
description: >
  Full stage-by-stage specification (Stage 0-10) of the audit state machine — purpose,
  preconditions, inputs, activities, decision logic, outputs, failure conditions, and transitions
  for every stage. Reference for human developers; SKILL.md §5's Thinking Phases is the
  operational summary the LLM actually follows.
version: 1.0.0
---

# Audit State Machine — Full Stage Specifications

> **Read this file before executing any audit stage.**
> Every stage uses EXACTLY the template below. No exceptions.

## Contents

- [Stage 0 — Baseline](#stage-0--baseline)
- [Stage 1 — Charter](#stage-1--charter)
- [Stage 2 — Define](#stage-2--define)
- [Stage 3 — Measure](#stage-3--measure)
- [Stage 4 — Classify](#stage-4--classify)
- [Stage 5 — Trace](#stage-5--trace)
- [Stage 6 — Engineer & Score](#stage-6--engineer--score)
- [Stage 7 — Synthesize (the Manifest Gate)](#stage-7--synthesize-the-manifest-gate)
- [Stage 8 — Findings JSON (deterministic)](#stage-8--findings-json-deterministic--script-to-build)
- [Stage 9 — Render (deterministic)](#stage-9--render-deterministic--script-to-build)
- [Stage 10 — Final Summary](#stage-10--final-summary)

<!--
  RULE: every stage uses EXACTLY this template. No exceptions.

  ## Stage X — Name
  ### Purpose            (one sentence)
  ### Preconditions      (which transition state must already be set)
  ### Inputs
  ### Activities         (numbered; imperative)
  ### Decision Logic     (if/then rules — where judgment is constrained)
  ### Outputs
  ### Failure Conditions (what triggers a hard stop, and the exact message)
  ### Completion Criteria
  ### Transition         (state emitted)
-->

## Stage 0 — Baseline

### Purpose

Verify the engine is intact, scan `knowledge/`, and build or refresh the local registry — so the audit knows what artifacts should exist and which standards govern them before any data is read.

### Preconditions

None — Stage 0 is the entry point. It runs at the start of every audit.

### Inputs

1. `knowledge/` — the org-supplied standards (the baseline; Contract 1). The only external input.
2. `registries/` — the previously derived registry, **if one exists** (input to the refresh-or-reuse decision only).
3. Engine files (preflight targets, not baseline): `PMO_DATA_CHARTER_template.md`, `AUDIT_MANIFEST_template.md`, `findings.schema.json`, `schema.py`, `manifest_to_findings.py`, `render.py`, `report_template.html`.

### Activities

1. **Preflight** — verify every engine file in Inputs (3) exists. This checks the skill, not the org.
2. **Inventory** — list every document in `knowledge/` (filename, format, size, modified date).
3. **Skeleton scan** — for each document, extract the table of contents / bookmarks / heading structure only. Record: document ID, title, edition, structure map with section numbers and page anchors. Do **not** read body text at this stage.
4. **Derive registry items** — from the skeletons, create or update registry items in Appendix E format: paraphrased checkable criteria + stable citation anchors (section + page). **Never verbatim text** (Principle 3). Depth here is skeleton-level; deep dives happen on demand in Stage 2.
5. **Build the applicability map** — artifact type → governing document(s) and section(s) (e.g., risk register → Standard for Risk Management §4.3, Risk Practice Guide §X2.2). This map is what Stage 1 uses to propose scope and what makes Missing gaps detectable.
6. **Write** the registry files to `registries/` with a derivation timestamp and a fingerprint (hash) of each source document.

### Decision Logic

- IF `knowledge/` contains no standards (README only) → `BASELINE_ABSENT`, hard stop (see Failure Conditions).
- IF a registry exists AND every source fingerprint matches the current `knowledge/` contents → **reuse** it; skip Activities 3–6.
- IF documents were added → derive registry entries for the new documents only.
- IF documents were removed or changed → refresh the affected entries; flag orphaned registry items (whose source is gone) and remove them.
- Deep-dive extraction is **never** done in Stage 0 — Stage 2 requests it per governing section. Stage 0 stays fast and shallow.
- A document that cannot be parsed (corrupt, image-only, encrypted) is logged and reported to the user — it is skipped, not guessed at.

### Outputs

Written to `registries/` (local-only, gitignored):

1. **Skeleton map** — every document in `knowledge/` with its structure and anchors.
2. **Registry items** — the checkable criteria (Appendix E format).
3. **Applicability map** — artifact type → governing standards/sections.
4. **Derivation manifest** — timestamp + source fingerprints (drives the reuse decision next run).

### Failure Conditions

- `knowledge/` empty or contains only its README → **HARD STOP**, emit `BASELINE_ABSENT`, print exactly:
  > **BASELINE_ABSENT — no standards found in `knowledge/`.** IEM-PM ships no bundled standard text and never audits from assumption or model memory. Place the organization's real standards (PMI or organizational; PDF/MD) in `skills/intelligence-engine/knowledge/` and re-run. _No baseline, no audit._
- Any engine file missing (preflight) → **HARD STOP**, print:
  > **ENGINE_INCOMPLETE — `<filename>` is missing.** This is a skill-installation problem, not a baseline problem. Reinstall or restore the file, then re-run.
- Every document in `knowledge/` unparseable → **HARD STOP** with the list of failed documents and the reason each failed.

### Completion Criteria

- Every readable document in `knowledge/` appears in the skeleton map.
- Every registry item carries a citation anchor (document ID + section + page) and contains no verbatim standard text.
- The applicability map is non-empty.
- The derivation manifest records a fingerprint for every source document.

### Transition

→ `BASELINE_READY` (or `BASELINE_ABSENT` + hard stop)

---

## Stage 1 — Charter

### Purpose

Propose the PMO Data Charter (artifacts + field semantics from the **data**; scope from the **standards** — anti-mirror guard) and obtain human ratification — so every later stage interprets the data through one agreed contract, never through guesswork.

### Preconditions

`BASELINE_READY`

### Inputs

1. **The org's delivery data** (the upload) — feeds Charter functions 1–2 (Artifact Declaration, Field Semantics). See §4.2.
2. `PMO_DATA_CHARTER_template.md` — the shape the proposal must fill (Contract 2's template).
3. **Registry + applicability map** from Stage 0 — feed Charter function 3 (Materiality & Scope), which is proposed from the standards' expectations, **never from the data**.

The input split _is_ the anti-mirror guard: input 1 may only inform functions 1–2; input 3 may only inform function 3.

### Activities

1. **Inventory the data** — list every supplied artifact (name, type, format, size, record count where readable). Read to identify, not yet to audit.
2. **Propose Artifact Declaration (function 1)** — from the data: classify each supplied artifact by type (risk register, schedule, status report, …).
3. **Propose Field Semantics Map (function 2)** — from the data: for each significant field, propose its business meaning, flagging every assumption.
4. **Propose Materiality & Scope (function 3)** — from the applicability map: which artifact types, governance levels, thresholds, and time period the _standards_ expect to be in evidence.
5. **Surface candidate Missing gaps** — every artifact the applicability map expects but the upload lacks is listed for the human to **supply, confirm as a finding, or explicitly waive**.
6. **Present the draft Charter** for ratification: the three proposals, all assumptions, and the candidate-Missing list, each marked with what it was derived from (data vs. standards).
7. **Record the outcome and write the Charter** to the run's `reports/` folder — ratified (with ratifier and date) or PROVISIONAL.

### Decision Logic

- IF the human **ratifies** → Charter becomes the immutable interpretation contract for the run.
- IF the human **edits** → incorporate the edits and re-present; only the human-approved version is ratified.
- IF the human says **"just run it"** → proceed with a **PROVISIONAL Charter** (§4.2 function 4); the flag is carried in the Charter and every finding in the run inherits the unratified-interpretation caveat.
- IF the human **declines and does not proceed** → hard stop (see Failure Conditions). A declined Charter is not a PROVISIONAL Charter.
- An absence vs. the standards' expectations surfaces as a candidate **Missing** gap for the human to confirm or waive — never inferred "out of scope" from the data alone. Only human-waived items are out of scope.
- After ratification the Charter cannot change mid-run; new data or a scope change means re-entering Stage 1.

### Outputs

Written to the run's `reports/` folder:

1. **The PMO Data Charter** — ratified (ratifier + date) or marked PROVISIONAL.
2. **Candidate Missing gap dispositions** — each standards-expected absence with its outcome: supplied / confirmed (carried into Stage 3 as a finding seed) / waived (with the human's stated reason).

### Failure Conditions

- No delivery data supplied → **HARD STOP**, emit `DATA_ABSENT`, print:
  > **DATA_ABSENT — no delivery data found.** The baseline is ready, but there is nothing to audit against it. Supply the organization's delivery artifacts and re-run.
- Human declines to ratify and does not choose "just run it" → **HARD STOP**, emit `CHARTER_DECLINED`, print:
  > **CHARTER_DECLINED — no ratified Charter.** No ratified Charter, no comparison (Principle 0). Correct the proposal and re-run Stage 1.
- The data is unreadable in its entirety (corrupt, encrypted, unsupported formats) → **HARD STOP** with the list of failed artifacts and the reason each failed.

### Completion Criteria

- Every supplied artifact appears in the Artifact Declaration with a type.
- Every significant field has a semantic definition, with assumptions flagged.
- Every scope and materiality item cites a standards anchor (registry item), not the data.
- Every standards-expected-but-absent artifact has a human disposition: supplied, confirmed, or waived.
- The Charter records its ratification status: ratifier + date, or PROVISIONAL.

### Transition

→ `CHARTER_RATIFIED` (PROVISIONAL is a flag carried inside the Charter, not a separate state; declined = hard stop, no transition)

---

## Stage 2 — Define

### Purpose

Resolve which standards govern each declared artifact; deep-dive those registry sections; request companion data.

### Preconditions

`CHARTER_RATIFIED`

### Inputs

- the outputs defined in stage 1 (The PMO Data Charter + Candidate missing gap dispositions)
- Standards and methodologies in `knowledge/` (baseline)
- the derived registry and applicability map from stage 0
- the projects, programs, portfolios, and PMO artifacts declared in the Charter

### Activities

TODO(you)

### Decision Logic

TODO(you)

### Outputs

TODO(you)

### Failure Conditions

TODO(you)

### Completion Criteria

TODO(you)

### Transition

→ `INTENT_DEFINED`

---

## Stage 3 — Measure

### Purpose

Evaluate every applicable registry criterion against the delivery evidence; each failure becomes a gap.

### Preconditions

`INTENT_DEFINED`

### Inputs

TODO(you)

### Activities

TODO(you)

### Decision Logic

TODO(you)

### Outputs

TODO(you)

### Failure Conditions

TODO(you)

### Completion Criteria

TODO(you)

### Transition

→ `GAPS_MEASURED`

---

## Stage 4 — Classify

### Purpose

Assign each gap exactly one of the 7 gap types (§7). No overlap, no duplicates.

### Preconditions

`GAPS_MEASURED`

### Inputs

TODO(you)

### Activities

TODO(you)

### Decision Logic

TODO(you): the disambiguation order when a gap could fit two types.

### Outputs

TODO(you)

### Failure Conditions

TODO(you)

### Completion Criteria

TODO(you)

### Transition

→ `GAPS_CLASSIFIED`

---

## Stage 5 — Trace

### Purpose

Trace each gap to exactly one of the 7 root origins (§8) — the earliest point the gap entered the system.

### Preconditions

`GAPS_CLASSIFIED`

### Inputs

TODO(you)

### Activities

TODO(you)

### Decision Logic

TODO(you)

### Outputs

TODO(you)

### Failure Conditions

TODO(you)

### Completion Criteria

TODO(you)

### Transition

→ `ROOTS_TRACED`

---

## Stage 6 — Engineer & Score

### Purpose

Engineer the fix-at-source for every finding, assign severity, and compute the Reporting Integrity Score. IEM-PM does not model organizational maturity (scrapped, not deferred — see §9.4).

### Preconditions

`ROOTS_TRACED`

### Inputs

TODO(you)

### Activities

TODO(you): four-part diagnostic — Evidence · Impact · Why/Who/Scope · Fix-at-source.

### Decision Logic

TODO(you): severity = Decision Impact × Spread × Persistence.

### Outputs

TODO(you)

### Failure Conditions

TODO(you)

### Completion Criteria

TODO(you)

### Transition

→ `SCORED`

---

## Stage 7 — Synthesize (the Manifest Gate)

### Purpose

Write the complete Audit Manifest to disk (§10) — the compaction-survival gate. Everything after this is deterministic.

### Preconditions

`SCORED` / `PENDING_BRIDGE`

### Inputs

TODO(you)

### Activities

TODO(you)

### Decision Logic

TODO(you)

### Outputs

`reports/<run>/audit_manifest.md`

### Failure Conditions

TODO(you)

### Completion Criteria

TODO(you): manifest is self-sufficient — the pipeline can run from it alone.

### Transition

→ `MANIFEST_WRITTEN`

---

## Stage 8 — Findings JSON _(deterministic — script to build)_

### Purpose

Run `manifest_to_findings.py`: manifest → validator (`schema.py`) → canonical findings JSON.

### Preconditions

`MANIFEST_WRITTEN`

### Inputs / Activities / Decision Logic

TODO(you) — ⚠️ STUB: script does not exist yet. The LLM never hand-writes the JSON.

### Outputs

`reports/<run>/findings.json`

### Failure Conditions

Validator rejects → fix the **manifest**, re-run. Never patch the JSON.

### Completion Criteria

TODO(you)

### Transition

→ `JSON_VALIDATED`

---

## Stage 9 — Render _(deterministic — script to build)_

### Purpose

Run `render.py`: findings JSON → HTML + TXT (+ dashboard data). Same JSON in → byte-identical out.

### Preconditions

`JSON_VALIDATED`

### Inputs / Activities / Decision Logic

TODO(you) — ⚠️ STUB: script does not exist yet. The LLM never edits rendered reports.

### Outputs

`reports/<run>/report.html` · `reports/<run>/report.txt`

### Failure Conditions

TODO(you)

### Completion Criteria

TODO(you)

### Transition

→ (reports rendered)

---

## Stage 10 — Final Summary

### Purpose

Print the TXT summary and the output file pointers; confirm the run checklist (§12).

### Preconditions

Reports rendered.

### Activities

TODO(you)

### Outputs

Console summary: evidence count · finding count · gap summary · Integrity Score · file paths.

### Completion Criteria

TODO(you)

### Transition

→ `REPORTS_EMITTED`
