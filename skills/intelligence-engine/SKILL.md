---
name: intelligence-engine
description: >
  Intelligence Engineering engine for Project, Program, Portfolio and PMO
  audits. Compares an organization's delivery evidence (projects, schedules,
  RAID logs, governance packs, dashboards, boards) against its declared
  project management standards (PMBOK, OPM3, PRINCE2, or internal methodology),
  classifies every gap into 7 types, traces each to its root origin, scores
  severity, and produces an evidence-based OPM3 maturity assessment with
  HTML + JSON + TXT reports. Use this skill whenever the user mentions PMO
  audits, project delivery gaps, governance assessments, maturity evaluations,
  data integrity reviews, standards compliance checks, delivery evidence
  analysis, or wants to understand why their project data doesn't match their
  methodology — even if they don't explicitly say "IEM-PM" or "intelligence
  engineering." Also trigger when the user uploads or references project
  artifacts (RAID logs, schedules, status reports, governance packs, Jira
  exports, Primavera files) and asks for analysis, review, assessment, or
  gap identification. If the user asks "where is our data breaking down,"
  "are we following our methodology," "what's our maturity level," or
  "audit our PMO," use this skill.
version: 1.0.0
allowed-tools: [Read, Glob, Grep, Bash, Write]
compatibility: Requires Python 3.10+ for scripts/ (validator, renderer).
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

## 3. Definitions

| Term              | Definition                                                                                                                 |
| ----------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Project           | A temporary endeavor undertaken to create a unique product, service, or result.                                            |
| Program           | A group of related projects managed in a coordinated way to obtain benefits not available from managing them individually. |
| Portfolio         | A collection of projects, programs, and operations managed as a group to achieve strategic objectives.                     |
| PMO               | Project Management Office — the organizational unit that centralizes and coordinates project management.                   |
| Delivery Evidence | Any artifact, record, dataset, or output that demonstrates how delivery is actually performed.                             |
| Baseline          | The declared standards against which delivery is measured. Sourced from `knowledge/`.                                      |
| PMO Data Charter  | The human-ratified contract defining what the data is, what fields mean, and what matters. Contract 2.                     |
| Registry          | Structured, machine-readable criteria derived from the baseline. Each item is checkable.                                   |
| Criterion         | A single checkable expectation within a registry item.                                                                     |
| Gap               | A variance between expected delivery (criterion) and observed delivery (evidence).                                         |
| Finding           | A gap + its evidence + its classification + its root origin + its severity.                                                |
| Root Origin       | The earliest structural point at which the gap entered the system. One of 7.                                               |

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

## 5. The Audit State Machine

The audit runs as an 11-stage state machine (Stages 0–10).
Each stage follows the same template. Read
`references/audit-stages.md` for full specifications.

Transition states (closed list):
`BASELINE_READY` · `BASELINE_ABSENT` · `CHARTER_RATIFIED` ·
`INTENT_DEFINED` · `GAPS_MEASURED` · `GAPS_CLASSIFIED` ·
`ROOTS_TRACED` · `SCORED` (or `PENDING_BRIDGE`) ·
`MANIFEST_WRITTEN` · `JSON_VALIDATED` · `REPORTS_EMITTED`

| Stage | Name          | Purpose                                              | Transition           |
| ----- | ------------- | ---------------------------------------------------- | -------------------- |
| 0     | Baseline      | Verify engine, scan `knowledge/`, build registry.    | → `BASELINE_READY`   |
| 1     | Charter       | Propose PMO Data Charter, obtain human ratification. | → `CHARTER_RATIFIED` |
| 2     | Define        | Resolve governing standards per artifact.            | → `INTENT_DEFINED`   |
| 3     | Measure       | Evaluate criteria against evidence.                  | → `GAPS_MEASURED`    |
| 4     | Classify      | Assign each gap one of 7 types.                      | → `GAPS_CLASSIFIED`  |
| 5     | Trace         | Trace each gap to one root origin.                   | → `ROOTS_TRACED`     |
| 6     | Score         | Severity + Integrity Score + OPM3 position.          | → `SCORED`           |
| 7     | Synthesize    | Write the Audit Manifest.                            | → `MANIFEST_WRITTEN` |
| 8     | Findings JSON | Run `scripts/manifest_to_findings.py`.               | → `JSON_VALIDATED`   |
| 9     | Render        | Run `scripts/render.py`.                             | → reports rendered   |
| 10    | Summary       | Print summary + file pointers.                       | → `REPORTS_EMITTED`  |

Stages 8–9 are deterministic. The LLM never hand-writes
JSON or edits rendered reports.

Read `references/audit-stages.md` before executing any stage.

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

Every finding belongs to exactly one of seven types (closed list).
Read `references/gap-taxonomy.md` for full definitions, detection logic, examples, misclassification traps and PMI Anchors.
Do NOT classify a gap without reading the full taxonomy first.

---

# 8. Root Origin Analysis

Every gap traces to **exactly one** of seven origins — the earliest point it entered the system. Closed list (`references/root-origins.md`), so the validator can enforce it.
Read `references/root-origins.md` for full definitions, detection logic, examples.
The report fixes causes, not symptoms.

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

## 13. Appendices

Appendices have been moved to `references/` for progressive disclosure.
Read them when the corresponding stage requires them.

| Appendix              | File                              | Read When                   |
| --------------------- | --------------------------------- | --------------------------- |
| A — Gap Taxonomy      | `references/gap-taxonomy.md`      | Before Stage 4 (Classify)   |
| B — Root Origins      | `references/root-origins.md`      | Before Stage 5 (Trace)      |
| C — Confidence Scale  | `references/confidence-scale.md`  | Before Stage 6 (Score)      |
| D — Severity Scale    | `references/severity-matrix.md`   | Before Stage 6 (Score)      |
| E — Registry Format   | `references/registry-format.md`   | During Stage 0 (Baseline)   |
| F — Manifest Template | `references/manifest-template.md` | During Stage 7 (Synthesize) |
| G — File Naming       | `references/file-naming.md`       | During Stage 9 (Render)     |
| H — Error Codes       | `references/error-codes.md`       | On any error condition      |

## Knowledge Base Reading Guide

| Standard in `knowledge/`      | Read When                                                                |
| ----------------------------- | ------------------------------------------------------------------------ |
| `Organizational/`             | FIRST — during Stage 0. Overrides generic standards where they conflict. |
| `PMBOK/`                      | Stage 0 (skeleton scan) + Stage 2 (deep-dive per governing section)      |
| `OPM3/`                       | Stage 6 only (maturity scoring)                                          |
| `PRINCE2/`                    | Stage 0 + Stage 2 (if org declares PRINCE2)                              |
| `PMI/`                        | Stage 0 + Stage 2 (practice guides, standards)                           |
| `Agile/`, `MSP/`, `ISO21502/` | Stage 0 + Stage 2 (if org declares these)                                |

Never read all knowledge files at once. Read only what the applicability
map (Stage 0) says governs the artifacts in scope.
