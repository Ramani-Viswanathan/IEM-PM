# IEM-PM — Project Status

> Last updated: 2026-07-05. This file is the single save-point: decisions, current state, next actions.
> (Previous 2026-06-25 version referred to the old `pmo-data-gap-audit` skill and L1–L5 model — both superseded, now in `_archive/`.)

---

## 1. What is canonical (as of 2026-07-05)

| Artifact                                 | Status                                                                                              |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------- |
| **`IEM-PM BLUEPRINT-1.md`**              | ✅ **THE approved blueprint** (19 sections, Praxen-shaped, surgically aligned)                      |
| `PRAXEN-BLUEPRINT.md`                    | Reference — how the model project (Praxen) is built                                                 |
| `skills/intelligence-engine/SKILL.md`    | The v1 template — pre-filled locked content + `TODO(you)` markers; being written section-by-section |
| `skills/intelligence-engine/knowledge/`  | Baseline drop-zone — **29 licensed standards PDFs live here** (gitignored)                          |
| `skills/intelligence-engine/registries/` | Derived-at-runtime registry output (gitignored, empty until Stage 0 runs)                           |
| `_archive/`                              | Superseded: old `pmo-data-gap-audit` skill, old `IEM-PM_BLUEPRINT.md`, `remit/` — history only      |
| `stakeholder/`                           | PMI volunteer copyrighted material — **never touch, never publish, never build on**                 |

## 2. Locked decisions (do not re-litigate)

1. **No baseline, no audit** — repo ships zero standard text; org drops real standards into `knowledge/`; registry derived locally; everything standard-derived is gitignored.
2. **OPM3 is the maturity lens** — gaps are _evidence of the org's_ maturity on PMI's OPM3; IEM-PM invents no maturity scale. The **gaps→OPM3 bridge is the open core IP** (`⚠️ STUB / PENDING_BRIDGE`).
3. **Five Contracts** — 1 Standards (baseline) · 2 PMO Data Charter (what data is/means/matters; machine-proposed → human-ratified) · 3 Audit Manifest (LLM↔code boundary + compaction gate) · 4 Canonical Findings JSON · 5 Schema Validator.
4. **Anti-mirror guard** — Charter scope is proposed from the _standards_, never the data; absences surface as candidate **Missing** gaps, never "out of scope."
5. **Closed taxonomies** — 7 gaps (Missing · Ignored · Disconnected · Untrusted · Underutilized · Misclassified · Divergent) × 7 root origins (Capture · Integration · Definition/Taxonomy · Ownership · Process/Cadence · Tooling · Behavior). Closed so the validator can enforce them.
6. **LLM judges; code renders** — Stages 0–7 are LLM judgment; Stages 8–10 deterministic stdlib Python. Same findings JSON → byte-identical report.
7. **Scoring** — Reporting Integrity Score 0–100 (Severity = Decision Impact × Spread × Persistence); the 7 "intelligence indicators" are narrative labels only, never scored.
8. **Copyright-safe** — clause + short paraphrase + citation only; never verbatim; the engine stays generic (no hard-coding to any supplied dataset).

## 3. The 11-stage state machine (SKILL.md §5)

Baseline → Charter → Define → Measure → Classify → Trace → Engineer & Score → Synthesize (manifest gate) → Findings JSON → Render → Final Summary.

States: `BASELINE_READY/ABSENT → CHARTER_RATIFIED → INTENT_DEFINED → GAPS_MEASURED → GAPS_CLASSIFIED → ROOTS_TRACED → SCORED/PENDING_BRIDGE → MANIFEST_WRITTEN → JSON_VALIDATED → REPORTS_EMITTED`.

## 4. Build Order (BLUEPRINT-1 §17) and where we are

1. Define the PMO Data Charter ← **template file not yet created**
2. Define the Findings Schema (`findings.schema.json`)
3. Build the Validator (`schema.py`)
4. Build the Audit Manifest template
5. **Write SKILL.md** ← IN PROGRESS (template scaffolded 2026-07-05; user writing `TODO(you)` sections, Claude reviewing)
6. Knowledge Base derivation (scan — standards already sit in `knowledge/`)
7. Registry derivation (generated from org's standards)
8. Renderer (`render.py`)
9. Report template (`report_template.html`)
10. Regression tests
11. Package as Claude Code skill

## 5. Open design items

- **The gaps→OPM3 bridge** (SKILL §9.3): output construct (SMCI stage / attainment %), inputs, calibration — the new core IP.
- Deterministic back half (Stages 8–9 scripts) — not built.
- Severity bands (Appendix D), error codes (Appendix H), file naming (Appendix G).

## 6. Working protocol

User writes SKILL.md one section at a time → Claude reviews against: (a) BLUEPRINT-1 consistency, (b) exact per-stage template compliance, (c) no contradiction with sections already written.

Suggested writing order: **§4.2 Charter → Appendices A–D → Stage 0 → Stage 1 → §6 Cross-Cutting → remaining stages → the rest.**

# Status update : Table

| Status | Item                                                                                                                                | Source                |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| done   | Defined IEM-PM as a Claude Code skill that compares delivery evidence against declared standards and outputs HTML/JSON/TXT reports. | IEM-PM-BLUEPRINT-1.md |
| done   | Locked the core operating principle: no baseline, no audit; read-only engine; local-first execution.                                | STATUS.md             |
| done   | Defined the repository topology, including skill, knowledge, registries, validator, renderer, tests, reports, and assets.           | IEM-PM-BLUEPRINT-1.md |
| done   | Defined the 7 gap taxonomy and 7 root-origin taxonomy as closed validation sets.                                                    | IEM-PM-BLUEPRINT-1.md |
| done   | Established the LLM-versus-Python split: LLM judges, Python validates and renders.                                                  | IEM-PM-BLUEPRINT-1.md |
| done   | Set OPM3 as the maturity lens.                                                                                                      | STATUS.md             |
| next   | Create the PMO Data Charter template.                                                                                               | STATUS.md             |
| next   | Define the Findings Schema (findings.schema.json).                                                                                  | STATUS.md             |
| next   | Build the Schema Validator (schema.py).                                                                                             | STATUS.md             |
| next   | Build the Audit Manifest template.                                                                                                  | STATUS.md             |
| next   | Write SKILL.md section by section.                                                                                                  | STATUS.md             |
| next   | Build the Knowledge Base derivation from scanned standards.                                                                         | STATUS.md             |
| next   | Build the Registry derivation from org standards.                                                                                   | STATUS.md             |
| next   | Create the Renderer (render.py).                                                                                                    | STATUS.md             |
| next   | Create the Report Template (report_template.html).                                                                                  | STATUS.md             |
| next   | Build regression tests.                                                                                                             | STATUS.md             |
| next   | Package as Claude Code skill.                                                                                                       | STATUS.md             |
| open   | Design and calibrate the gaps-to-OPM3 bridge.                                                                                       | STATUS.md             |
| open   | Define severity bands and error codes.                                                                                              | STATUS.md             |
| open   | Finalize file naming conventions.                                                                                                   | STATUS.md             |
| open   | Implement the deterministic back half for stages 8–9.                                                                               | STATUS.md             |

# 6-Week Plan

| Week   | Focus            | Deliverable                                                                                                          | Status |
| ------ | ---------------- | -------------------------------------------------------------------------------------------------------------------- | ------ |
| Week 1 | PMO Data Charter | Draft the PMO Data Charter template with sections for data meaning, scope, materiality, and human ratification.      | next   |
| Week 2 | Findings Schema  | Define findings.schema.json with fields for gap type, root origin, evidence, severity, and OPM3 mapping placeholder. | next   |
| Week 3 | Validator        | Build schema.py to validate findings JSON against the schema and closed taxonomies.                                  | next   |
| Week 4 | Audit Manifest   | Create the Audit Manifest template that converts LLM analysis into a parser-friendly structure.                      | next   |
| Week 5 | SKILL.md         | Write the skill sections and lock the core logic, inputs, and stage flow.                                            | next   |
| Week 6 | Reports + Tests  | Build the renderer, report template, and regression tests; package the skill.                                        | next   |

# mapping of the five Claude Certified Architect Foundations domains to your IEM-PM modules.

| CCA-F domain                       | What it teaches                                                         | IEM-PM module it supports                                                                           |
| ---------------------------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Agentic architecture               | Designing multi-step AI systems that plan, reason, and act across tasks | Core IEM-PM orchestration: baseline → evidence → gap finding → classification → root cause → report |
| Tool use and integrations          | Connecting the model to external systems safely and reliably            | Evidence collection from standards, project data, PM tools, file systems, and local repositories    |
| Claude Code workflows              | Building and operating AI inside a code-first development environment   | Your IEM-PM Claude Code skill packaging, repo structure, stage machine, and build order             |
| Structured outputs and prompts     | Getting consistent JSON, schemas, and controlled LLM responses          | Audit Manifest, Findings JSON, schema validation, and report generation                             |
| Reliability and context management | Keeping the system stable, grounded, and able to work with long inputs  | Standards ingestion, knowledge base derivation, closed taxonomies, and evidence-first reasoning     |
