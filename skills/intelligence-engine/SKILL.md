---
name: intelligence-engine
description: Intelligence Engineering for Project, Program, Portfolio and PMO audits — measures delivery data against the org's own standards, classifies every gap into 7 types, traces each to its root origin, and exposes the org's OPM3 maturity position.
version: 1.0.0
allowed-tools: [Read, Glob, Grep, Bash, Write]
---

# IEM-PM — Intelligence Engineering Skill

> **No baseline, no audit. Find the gap. Trace it to the root. Measure maturity from evidence.**
>
> Governing question: **Does the organization's delivery data match what its standards require — and where it doesn't, why?**

---

# TABLE OF CONTENTS

1. Mission
2. Operating Principles
3. Definitions
4. Inputs & Outputs — the Five Contracts
5. The Audit State Machine (Stages 0–10)
6. Cross-Cutting Rules
7. Gap Classification
8. Root Origin Analysis
9. Scoring
10. Manifest Contract
11. Report Generation
12. Completion
13. Appendices

---

# 1. Mission

## 1.1 Purpose

TODO(you)

## 1.2 Objectives

TODO(you)

## 1.3 Success Criteria

TODO(you)

---

# 2. Operating Principles

## Principle 0 — Data-contract-first

No ratified Charter → no comparison. Never guess what the data means.

TODO(you): expand.

## Principle 1 — Baseline First

No baseline → no audit. The engine cannot judge without knowing the standard.

TODO(you): expand.

## Principle 2 — Evidence First

Every finding must point to evidence: a document, a registry item, a governance rule — or the absence of one.

TODO(you): expand.

## Principle 3 — Copyright Safe

Never reproduce standards. Reference only: clause · identifier · short paraphrase · citation.

TODO(you): expand.

## Principle 4 — Read Only

Never modify delivery data. Write only to `reports/` (and the local registry).

TODO(you): expand.

## Principle 5 — Separation

IEM-PM is not part of the PMO. It independently evaluates the PMO.

TODO(you): expand.

## Principle 6 — Local First

Runs locally. No cloud. No database. Git repository only.

TODO(you): expand.

## Principle 7 — Intelligence Native

The intelligence lives in SKILL.md + Knowledge Base + Registries — not in Python. Python only validates and renders.

TODO(you): expand.

---

# 3. Definitions

<!-- One short paragraph each. Later sections cite these; never redefine elsewhere. -->

## Project

TODO(you)

## Program

TODO(you)

## Portfolio

TODO(you)

## PMO

TODO(you)

## Delivery Evidence

TODO(you)

## Baseline

TODO(you)

## PMO Data Charter

TODO(you)

## Registry

TODO(you)

## Criterion

TODO(you)

## Gap

TODO(you)

## Finding

TODO(you)

## Root Origin

TODO(you)

---

# 4. Inputs & Outputs — the Five Contracts

IEM-PM is built around five immutable contracts — because PMO data is not self-describing.

| #   | Contract                     | Role                                                                                                         | Direction    |
| --- | ---------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------ |
| 1   | **Standards** (`knowledge/`) | Defines Expected Delivery — the baseline/ruler. Org-supplied, never bundled.                                 | Input        |
| 2   | **PMO Data Charter**         | Defines what the data **is**, what its fields **mean**, what **matters**. Machine-proposed → human-ratified. | Input        |
| 3   | **Audit Manifest**           | LLM output. Human-readable, parser-friendly. The LLM↔code boundary.                                          | Intermediate |
| 4   | **Canonical Findings JSON**  | Machine-readable single source of truth.                                                                     | Output       |
| 5   | **Schema Validator**         | Guarantees every report is internally consistent.                                                            | Gate         |

## 4.1 Contract 1 — Standards

TODO(you): what qualifies as a standard, where it goes, what happens when absent.

## 4.2 Contract 2 — PMO Data Charter

The **PMO Data Charter** is the authoritative data-interpretation contract for every IEM-PM audit. It specifies **what** the delivery data is, **how** the engine must interpret it, and **what** matters — the boundaries within which the audit operates. **It is not the baseline**; the Standards (Contract 1) are the baseline the data is judged against.

The PMO Data Charter performs five essential functions.

### 1. Artifact Declaration

The charter declares every artifact that is in scope for the audit. It identifies the organizational documents, repositories, systems, reports, registers, and datasets that constitute valid audit evidence.

Typical artifacts include, but are not limited to:

- PMO Governance Documents
- Project Charters
- Program Charters
- Portfolio Plans
- Project Schedules
- RAID Registers
- Risk Registers
- Issue Logs
- Decision Logs
- Benefits Registers
- Financial Reports
- Status Reports
- Steering Committee Packs
- Lessons Learned
- Jira, Azure DevOps, Microsoft Project, Primavera, or equivalent delivery systems

An artifact the standards expect but that is not declared does not silently fall out of scope — it surfaces at ratification as a candidate Missing gap, which the human either supplies, confirms as a finding, or explicitly waives. Only human-waived items are out of scope.

---

### 2. Field Semantics Map

The charter provides a semantic definition for every significant field contained within the delivery data.

The Field Semantics Map establishes a common understanding of what each document, attribute, metric, and data element represents. It removes ambiguity by defining the business meaning of the organization's data rather than relying solely on field names.

For example, the charter may define:

- What constitutes overall project health.
- The organization's interpretation of RAG status.
- The meaning of Schedule Performance Index (SPI) and Cost Performance Index (CPI).
- The purpose of a project owner or sponsor.
- How governance decisions are recorded.
- Which fields are mandatory, optional, calculated, or derived.

By defining field semantics before analysis begins, IEM-PM can interpret delivery information consistently across projects, programs, portfolios, and PMOs.

---

### 3. Materiality and Scope

The charter defines the scope and materiality of the audit.

Scope determines **which parts of the organization and which delivery artifacts will be evaluated**, while materiality defines **what is significant enough to influence audit findings and maturity assessments**.

Examples include:

- Organizational units included in the audit.
- Portfolios, programs, and projects included or excluded.
- Time period under review.
- Minimum project value or strategic importance.
- Governance levels to be evaluated.
- Thresholds for significant risks, issues, budget variance, or schedule variance.

Materiality ensures that the audit focuses on information capable of affecting governance decisions rather than insignificant operational detail.

---

### 4. Propose → Ratify

Before the audit begins, IEM-PM performs a discovery phase in which it proposes its understanding of the audit environment.

The engine identifies:

- Baseline standards.
- Available artifacts.
- Organizational structure.
- Delivery systems.
- Audit scope.
- Significant assumptions.

Rather than proceeding immediately, IEM-PM presents this interpretation to the user for confirmation.

The audit only begins after the proposed understanding has been reviewed and ratified. This validation step ensures that the engine has correctly interpreted the organization's environment before evaluating delivery performance.

If the user declines to ratify and demands an immediate run ("just run it"), the engine proceeds with a **PROVISIONAL Charter** — its own proposal, explicitly marked as an assumed contract — and every finding in that run carries the caveat that it rests on unratified interpretation.

---

### 5. Anti-Mirror Guard

The five functions do not carry equal risk, and the guard is asymmetric:

- **Functions 1 & 2 (Artifact Declaration, Field Semantics) are proposed from the data.** Safe — that is reading the data to understand the data.
- **Function 3 (Materiality and Scope) is proposed from the standards' expectations, never from the data.** If scope were inferred from what the upload contains, observed behaviour would define the expected standard — a circular comparison in which the audit can only confirm what the organization already supplied, and a **Missing** gap could never surface.

Scope must therefore be derived from authoritative sources such as:

- Organizational governance frameworks.
- PMO operating models.
- Project management methodologies.
- Approved policies and procedures.
- PMI or other recognised project management standards.

Once ratified, the PMO Data Charter becomes the immutable **interpretation contract** for the run. The audit compares observed delivery against the Standards (Contract 1) _as interpreted through_ the Charter — ensuring every finding represents a genuine variance between expected and actual delivery, never a comparison against a standard inferred from the evidence itself.

## 4.3 Contract 3 — Audit Manifest

TODO(you): reference §10.

## 4.4 Contract 4 — Canonical Findings JSON

TODO(you): reference `findings.schema.json`.

## 4.5 Contract 5 — Schema Validator

TODO(you): what invariants it enforces (counts match, every gap cites a real criterion, closed taxonomies).

## 4.6 Outputs

Written to `reports/` only: `findings.json` · `report.html` · `report.txt` · dashboard data.

TODO(you): file naming — reference Appendix G.

---

# 5. The Audit State Machine

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

Transition states (closed list):

`BASELINE_READY` · `BASELINE_ABSENT` · `CHARTER_RATIFIED` · `INTENT_DEFINED` · `GAPS_MEASURED` · `GAPS_CLASSIFIED` · `ROOTS_TRACED` · `SCORED` (or `PENDING_BRIDGE`) · `MANIFEST_WRITTEN` · `JSON_VALIDATED` · `REPORTS_EMITTED`

---

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

Engineer the fix-at-source for every finding, assign severity, compute the Reporting Integrity Score, and state the OPM3 maturity position (⚠️ STUB — bridge TBD, §9).

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

→ `SCORED` (or `PENDING_BRIDGE` for the OPM3 portion)

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

Console summary: evidence count · finding count · gap summary · Integrity Score · OPM3 position · file paths.

### Completion Criteria

TODO(you)

### Transition

→ `REPORTS_EMITTED`

---

# 6. Cross-Cutting Rules

<!-- A rule that applies to more than one stage lives HERE, once — never repeated per stage. -->

## 6.1 Evidence Discipline

TODO(you)

## 6.2 Confidence Rules

Every finding carries exactly one confidence level (Appendix C): Verified · High · Medium · Low · Unknown.

TODO(you)

## 6.3 Missing-Data Rules

Never invent evidence. TODO(you)

## 6.4 Traceability Rules

TODO(you): evidence ledger — Evidence ID → source → location → registry ref → finding ref.

## 6.5 Citation & Copyright Rules

Clause + identifier + short paraphrase only — never long verbatim. `knowledge/` and `registries/` are local-only and gitignored.

TODO(you)

## 6.6 Error Handling

TODO(you): reference Appendix H error codes.

## 6.7 Context Recovery

If context is compacted mid-run: re-read the Audit Manifest from disk and resume from the recorded transition state. Never restart judgment stages whose outputs are already in the manifest.

TODO(you)

---

# 7. Gap Classification

Every finding belongs to **exactly one** of seven types. Closed list (Appendix A). No overlap. No duplicates.

## 7.1 Missing — required information absent

### Definition

TODO(you)

### Detection

TODO(you)

### Examples

TODO(you)

## 7.2 Ignored — standard exists but not followed

### Definition

TODO(you)

### Detection

TODO(you)

### Examples

TODO(you)

## 7.3 Disconnected — information exists but is isolated

### Definition

TODO(you)

### Detection

TODO(you)

### Examples

TODO(you)

## 7.4 Untrusted — evidence cannot be verified

### Definition

TODO(you)

### Detection

TODO(you)

### Examples

TODO(you)

## 7.5 Underutilized — data collected but unused

### Definition

TODO(you)

### Detection

TODO(you)

### Examples

TODO(you)

## 7.6 Misclassified — wrong classification or taxonomy

### Definition

TODO(you)

### Detection

TODO(you)

### Examples

TODO(you)

## 7.7 Divergent — delivery differs from required standard

### Definition

TODO(you)

### Detection

TODO(you)

### Examples

TODO(you)

---

# 8. Root Origin Analysis

Every gap traces to **exactly one** of seven origins — the earliest point it entered the system. Closed list (Appendix B), so the validator can enforce it. The report fixes causes, not symptoms.

## 8.1 Capture

### Definition / Detection / Examples

TODO(you)

## 8.2 Integration

### Definition / Detection / Examples

TODO(you)

## 8.3 Definition / Taxonomy

### Definition / Detection / Examples

TODO(you)

## 8.4 Ownership

### Definition / Detection / Examples

TODO(you)

## 8.5 Process / Cadence

### Definition / Detection / Examples

TODO(you)

## 8.6 Tooling

### Definition / Detection / Examples

TODO(you)

## 8.7 Behavior

### Definition / Detection / Examples

TODO(you)

## 8.8 Analysis Method

TODO(you): five-whys / earliest-origin rule / structural flagging.

---

# 9. Scoring

## 9.1 Reporting Integrity Score (0–100)

TODO(you): rollup of Severity (Decision Impact × Spread × Persistence) across findings.

## 9.2 Intelligence Indicators (narrative only)

Visibility · Integrity · Connectivity · Governance · Predictability · Decision Quality · Continuous Improvement.

**Narrative diagnostic labels only — never scored or weighted.**

TODO(you)

## 9.3 OPM3 Maturity Position — ⚠️ STUB

IEM-PM does not invent a maturity scale. The gap profile maps to **PMI's OPM3 model**; the bridge rubric (gap profile → OPM3 position) is the open design item.

Until the bridge is defined, this section emits: `PENDING_BRIDGE` + the raw gap profile as evidence.

TODO(design): the bridge — output construct (SMCI stage / attainment %), inputs, calibration.

---

# 10. Manifest Contract

<!-- The Audit Manifest is Contract 3: the LLM↔code boundary AND the compaction-recovery point. -->

## 10.1 Required Sections

TODO(you)

## 10.2 Format Rules (parser-grade)

TODO(you)

## 10.3 Validation Rules

TODO(you): counts match · every gap cites a real criterion · taxonomies closed · every finding has confidence + severity.

## 10.4 Template

See `AUDIT_MANIFEST_template.md`. TODO(you)

---

# 11. Report Generation

The rendered report contains, in order:

1. Executive Summary
2. Audit Scope
3. Delivery Baseline
4. Delivery Evidence
5. Gap Register
6. Root Cause Analysis
7. Intelligence Indicators (narrative) + Reporting Integrity Score
8. Maturity Assessment (OPM3 position)
9. Recommended Actions
10. Roadmap
11. Appendix

## Per-section content rules

TODO(you): one short spec per report section.

---

# 12. Completion

## 12.1 Final Validation

TODO(you)

## 12.2 Output Checklist

TODO(you)

## 12.3 Report Locations

TODO(you)

---

# 13. Appendices

## Appendix A — The Seven Gap Taxonomy (closed) (Tells what is wrong?)

| Gap           | Meaning                                 |
| ------------- | --------------------------------------- |
| Missing       | Required information absent             |
| Ignored       | Standard exists but not followed        |
| Disconnected  | Information exists but is isolated      |
| Untrusted     | Evidence cannot be verified             |
| Underutilized | Data collected but unused               |
| Misclassified | Wrong classification or taxonomy        |
| Divergent     | Delivery differs from required standard |

## Appendix B — The Seven Root Origins (closed) (Tells where to fix?)

| Origin                | Meaning                                                                                                                                    |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Capture               | The required information was never collected, recorded or presented or maintained at the source                                            |
| Integration           | The information is available but it is not exchanged, synchronised or linked between systems                                               |
| Definition / Taxonomy | The organization lacks a common standard, definition, classification and/or data model                                                     |
| Ownership             | Accountability for creating, maintaining, approving, or using the information is unclear, missing, or ineffective.                         |
| Process / Cadence     | The governing process is missing, inconsistent, not followed, or performed at the wrong frequency.                                         |
| Tooling               | Technology limitations, poor system configuration, manual workarounds, or inadequate automation prevent reliable information management.   |
| Behavior              | People knowingly or unknowingly deviate from expected practices due to culture, training, incentives, resistance, or leadership decisions. |

## Appendix C — Confidence Scale (closed) (Tells How certain are we that we're right?)

| Level    | Meaning                                                                                                                                                                                                                                                                                    |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Verified | The finding is directly supported by authoritative evidence from one or more trusted sources. The evidence is complete, internally consistent, and independently verifiable. There is no reasonable doubt about the existence of the finding.                                              |
| High     | Strong evidence supports the finding, although complete independent verification may not be available. Multiple sources or indicators point to the same conclusion with only minor uncertainty                                                                                             |
| Medium   | The finding is supported by some credible evidence, but additional evidence would increase confidence. The conclusion is reasonable but should be interpreted with caution.                                                                                                                |
| Low      | Limited, incomplete, or indirect evidence suggests the finding. The conclusion is plausible but remains tentative until additional evidence is obtained.                                                                                                                                   |
| Unknown  | The available evidence is insufficient, contradictory, inaccessible, or absent. IEM-PM cannot determine whether the finding exists. Unknown findings are still recorded — flagged for human investigation and excluded from the Reporting Integrity Score rollup — never silently dropped. |

## Appendix D — Severity Scale (Tells How serious is it?)

Severity is determined by evaluating three dimensions:

Decision Impact – How significantly the gap affects business, governance, financial, or delivery decisions.
Spread – How widely the gap affects the organization.
Persistence – How long the gap has existed without effective resolution.

### Decision Impact

Measures how badly the gap **distorts a decision** (magnitude of consequence — _Standard for Risk Mgmt_ §3.3.1), not how widely it reaches (that is Spread's job).

| Level    | Score | Meaning                                                                       |
| -------- | ----- | ----------------------------------------------------------------------------- |
| Low      | 1     | Cosmetic — the decision is unaffected                                         |
| Medium   | 2     | Misinforms — decision-makers see a distorted picture                          |
| High     | 3     | Drives a wrong decision — funding, gating, or prioritization made on bad data |
| Critical | 4     | A strategic, regulatory, or mission-critical decision is made on bad data     |

### Spread

Measures how widely the gap reaches, on PMI's escalation ladder (_Risk Mgmt Practice Guide_ §4.1.3).

| Level      | Score | Meaning                                      |
| ---------- | ----- | -------------------------------------------- |
| Local      | 1     | Limited to a single record or artifact       |
| Project    | 2     | Affects one project                          |
| Program    | 3     | Affects multiple projects within a program   |
| Portfolio  | 4     | Affects multiple programs across a portfolio |
| Enterprise | 5     | Affects the enterprise as a whole            |

### Persistence

Measures how long the gap has survived (IEM-PM's own dimension; nearest PMI cousin: dormancy, _Practice Guide_ §X2.3.7).

| Level      | Score | Meaning                                                          |
| ---------- | ----- | ---------------------------------------------------------------- |
| Temporary  | 1     | One reporting cycle or isolated occurrence                       |
| Recurring  | 2     | Appears across multiple reporting cycles or multiple iterations  |
| Sustained  | 3     | Exists for several months and affects ongoing delivery           |
| Systematic | 4     | Embedded within organizational practices over an extended period |

### Severity Bands

- Severity measures the business significance of a finding.
- **Combination rule (pure arithmetic — the validator recomputes it):**
  `Score = Persistence (1–4) × Spread (1–5) × Decision Impact (1–4)` — range 1–80.
- **Bands:** Score ≤ 8 → **Low** · 9–24 → **Medium** · 25–48 → **High** · ≥ 49 → **Critical**.
- **Floor rule:** Decision Impact = Critical → Severity is at least **High**, regardless of score (a strategic/regulatory decision on bad data is never a low-severity finding). Marked `^` in the matrix.

### Severity Matrix (all 80 combinations — generated from the rule above)

| Persistence | Spread     | Decision Impact | Score | Severity |
| ----------- | ---------- | --------------- | ----- | -------- |
| Temporary   | Local      | Low             | 1     | Low      |
| Temporary   | Local      | Medium          | 2     | Low      |
| Temporary   | Local      | High            | 3     | Low      |
| Temporary   | Local      | Critical        | 4     | High ^   |
| Temporary   | Project    | Low             | 2     | Low      |
| Temporary   | Project    | Medium          | 4     | Low      |
| Temporary   | Project    | High            | 6     | Low      |
| Temporary   | Project    | Critical        | 8     | High ^   |
| Temporary   | Program    | Low             | 3     | Low      |
| Temporary   | Program    | Medium          | 6     | Low      |
| Temporary   | Program    | High            | 9     | Medium   |
| Temporary   | Program    | Critical        | 12    | High ^   |
| Temporary   | Portfolio  | Low             | 4     | Low      |
| Temporary   | Portfolio  | Medium          | 8     | Low      |
| Temporary   | Portfolio  | High            | 12    | Medium   |
| Temporary   | Portfolio  | Critical        | 16    | High ^   |
| Temporary   | Enterprise | Low             | 5     | Low      |
| Temporary   | Enterprise | Medium          | 10    | Medium   |
| Temporary   | Enterprise | High            | 15    | Medium   |
| Temporary   | Enterprise | Critical        | 20    | High ^   |
| Recurring   | Local      | Low             | 2     | Low      |
| Recurring   | Local      | Medium          | 4     | Low      |
| Recurring   | Local      | High            | 6     | Low      |
| Recurring   | Local      | Critical        | 8     | High ^   |
| Recurring   | Project    | Low             | 4     | Low      |
| Recurring   | Project    | Medium          | 8     | Low      |
| Recurring   | Project    | High            | 12    | Medium   |
| Recurring   | Project    | Critical        | 16    | High ^   |
| Recurring   | Program    | Low             | 6     | Low      |
| Recurring   | Program    | Medium          | 12    | Medium   |
| Recurring   | Program    | High            | 18    | Medium   |
| Recurring   | Program    | Critical        | 24    | High ^   |
| Recurring   | Portfolio  | Low             | 8     | Low      |
| Recurring   | Portfolio  | Medium          | 16    | Medium   |
| Recurring   | Portfolio  | High            | 24    | Medium   |
| Recurring   | Portfolio  | Critical        | 32    | High     |
| Recurring   | Enterprise | Low             | 10    | Medium   |
| Recurring   | Enterprise | Medium          | 20    | Medium   |
| Recurring   | Enterprise | High            | 30    | High     |
| Recurring   | Enterprise | Critical        | 40    | High     |
| Sustained   | Local      | Low             | 3     | Low      |
| Sustained   | Local      | Medium          | 6     | Low      |
| Sustained   | Local      | High            | 9     | Medium   |
| Sustained   | Local      | Critical        | 12    | High ^   |
| Sustained   | Project    | Low             | 6     | Low      |
| Sustained   | Project    | Medium          | 12    | Medium   |
| Sustained   | Project    | High            | 18    | Medium   |
| Sustained   | Project    | Critical        | 24    | High ^   |
| Sustained   | Program    | Low             | 9     | Medium   |
| Sustained   | Program    | Medium          | 18    | Medium   |
| Sustained   | Program    | High            | 27    | High     |
| Sustained   | Program    | Critical        | 36    | High     |
| Sustained   | Portfolio  | Low             | 12    | Medium   |
| Sustained   | Portfolio  | Medium          | 24    | Medium   |
| Sustained   | Portfolio  | High            | 36    | High     |
| Sustained   | Portfolio  | Critical        | 48    | High     |
| Sustained   | Enterprise | Low             | 15    | Medium   |
| Sustained   | Enterprise | Medium          | 30    | High     |
| Sustained   | Enterprise | High            | 45    | High     |
| Sustained   | Enterprise | Critical        | 60    | Critical |
| Systematic  | Local      | Low             | 4     | Low      |
| Systematic  | Local      | Medium          | 8     | Low      |
| Systematic  | Local      | High            | 12    | Medium   |
| Systematic  | Local      | Critical        | 16    | High ^   |
| Systematic  | Project    | Low             | 8     | Low      |
| Systematic  | Project    | Medium          | 16    | Medium   |
| Systematic  | Project    | High            | 24    | Medium   |
| Systematic  | Project    | Critical        | 32    | High     |
| Systematic  | Program    | Low             | 12    | Medium   |
| Systematic  | Program    | Medium          | 24    | Medium   |
| Systematic  | Program    | High            | 36    | High     |
| Systematic  | Program    | Critical        | 48    | High     |
| Systematic  | Portfolio  | Low             | 16    | Medium   |
| Systematic  | Portfolio  | Medium          | 32    | High     |
| Systematic  | Portfolio  | High            | 48    | High     |
| Systematic  | Portfolio  | Critical        | 64    | Critical |
| Systematic  | Enterprise | Low             | 20    | Medium   |
| Systematic  | Enterprise | Medium          | 40    | High     |
| Systematic  | Enterprise | High            | 60    | Critical |
| Systematic  | Enterprise | Critical        | 80    | Critical |

`^` = lifted by the floor rule (Decision Impact = Critical → minimum High).

### PMI anchors for this appendix (verified in the held documents, 2026-07-05)

The method — pre-defined qualitative levels, combined and banded — follows PMI risk practice. Anchors below cite section + PDF page in the copies held in `knowledge/`; paraphrase only, per Principle 3.

| #   | Anchor                                                                                     | What it supports                                                                                                                                                                                                                                                                                                  |
| --- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | _Risk Mgmt Practice Guide_ §X2.3.5, Probability and Impact Matrixes (p. 133, Fig. X2-11)   | The core precedent: risks rated on five qualitative levels (VH/H/M/L/VL) per dimension, combined in a matrix, **sorted into classes** — our "multiply/combine then band" pattern.                                                                                                                                 |
| 2   | _Practice Guide_ §X2.4.3, Estimating Techniques Applied to Probability and Impact (p. 135) | Impact-level definitions are **work-specific** and must be designated per objective from very low → very high — the license for IEM-PM to define its own level meanings, provided they are declared up front.                                                                                                     |
| 3   | _Practice Guide_ §X2.3.7, Assessment of Other Risk Parameters (pp. 133–134)                | PMI's own precedent for scoring dimensions **beyond** probability × impact (urgency, proximity, dormancy, connectivity, strategic impact) — legitimizes Spread and Persistence as additional parameters. **Dormancy** (time before an occurred risk's impact is discovered) is the closest cousin of Persistence. |
| 4   | _Practice Guide_ §X2.3.6, Risk Data Quality Analysis (p. 133)                              | "Results of the analysis are only as good as the data collected" — the PMI basis for the Confidence scale (Appendix C) sitting beside Severity.                                                                                                                                                                   |
| 5   | _Standard for Risk Management P/P/P_ §3.3.1, Factors for Evaluating Risk (pp. 42–43)       | Impact defined as the **magnitude/significance of consequence on objectives** — the definition Decision Impact levels must express (distortion of decisions, not organizational breadth).                                                                                                                         |
| 6   | _Standard_ §4.4.2, Key Success Factors for Qualitative Analysis (p. 51)                    | "Use agreed definitions of risk terms" — the mandate that level definitions are **pre-agreed**; in IEM-PM they are ratified in the Charter, not improvised at audit time.                                                                                                                                         |
| 7   | _Standard_ §2.1.6, Risk Threshold (p. 27)                                                  | Thresholds = qualitative/quantitative definitions of rating **plus the exposure level that triggers escalation** — the precedent for tying Severity bands to a governance response.                                                                                                                               |
| 8   | _Practice Guide_ §4.1.3, Risk Escalation (pp. 56–57)                                       | Escalation ladder project → program → portfolio → enterprise — the citable basis for the Spread ladder.                                                                                                                                                                                                           |

Persistence has no direct PMI analogue beyond dormancy/urgency (anchor 3) — it is an IEM-PM contribution, stated as such.

## Appendix E — Registry Item Format

| Attribute             | Type   | Description                                                                                         |
| --------------------- | ------ | --------------------------------------------------------------------------------------------------- |
| Identifier            | string | Unique identifier for the registry item.                                                            |
| Name                  | string | Descriptive name of the registry item.                                                              |
| Description           | string | Detailed description of the registry item.                                                          |
| Standard Source       | string | Specifies the standard or source that defines the registry item.                                    |
| Category              | string | Specifies the category or classification of the registry item.                                      |
| Evidence Required     | string | Specifies the type of evidence required to validate the registry item.                              |
| Evaluation Method     | string | Specifies the method or criteria used to evaluate the registry item.                                |
| Likely Gap Type(s)    | string | Candidate gap classification(s) as a hint — Stage 4 decides the actual gap type per finding.        |
| Likely Root Origin(s) | string | Candidate root origin(s) as a hint — Stage 5 decides the actual origin per finding.                 |
| Confidence Rules      | string | Specifies the confidence level rules associated with the registry item.                             |
| Severity Guidelines   | string | Specifies the severity guidelines associated with the registry item.                                |
| OPM3 Mapping          | string | Specifies the OPM3 process area or maturity level associated with the registry item (bridge — TBD). |
| Reference             | string | Reference to the relevant standard, policy, or guideline that defines the registry item.            |

## Appendix F — Audit Manifest Template

See `AUDIT_MANIFEST_template.md`. TODO(you)

## Appendix G — Output File Naming

TODO(you)

## Appendix H — Error Codes

TODO(you)
