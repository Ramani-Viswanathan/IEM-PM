# IEM-PM — Project Status

> Last updated: 2026-07-26. This file is the single save-point: decisions, current state, next actions.
> (Previous 2026-07-05 version had SKILL.md, the schema, validator, manifest parser, and renderer
> listed as "next" — all five are now written and were verified end-to-end on 2026-07-26, then
> committed and pushed as `df71e85`.)

---

## 1. What is canonical (as of 2026-07-26)

| Artifact                                            | Status                                                                                                    |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **`IEM-PM BLUEPRINT-1.md`**                         | ✅ **THE approved blueprint** (19 sections, Praxen-shaped, surgically aligned)                            |
| `PRAXEN-BLUEPRINT.md`                               | Reference — how the model project (Praxen) is built                                                       |
| `skills/intelligence-engine/SKILL.md`               | ✅ **Complete** — all 13 sections written (no `TODO(you)` markers remain)                                 |
| `skills/intelligence-engine/scripts/schema.py`       | ✅ Built — validates closed taxonomies, no-duplicate rule, evidence coverage. Passes on test fixture.      |
| `skills/intelligence-engine/scripts/manifest_to_findings.py` | ✅ Built — Manifest → canonical JSON, computes Reporting Integrity Score + provisional OPM3 heuristic. |
| `skills/intelligence-engine/scripts/render.py`       | ✅ Built — canonical JSON → HTML (Jinja2) + TXT. Verified byte-reproducible on test fixture.               |
| `skills/intelligence-engine/scripts/findings.schema.json` | ✅ Built — Draft-07 schema, all 5 contract objects modeled.                                            |
| `skills/intelligence-engine/scripts/baseline.py`     | ✅ Built (Stage 0 mechanics) — fingerprints `knowledge/`, extracts PDF/MD skeletons, diffs against prior run. |
| `skills/intelligence-engine/scripts/derive_knowledge_index.py` | ✅ Built — catalogs `knowledge/` (filenames/sizes only, no content) into `knowledge_index.json`.    |
| `skills/intelligence-engine/knowledge/`             | Baseline drop-zone (gitignored) — **only 1 standard currently present** (PMI *Standard for Risk Management*). The earlier "29 licensed standards" note no longer matches what's on disk — needs reconciling. |
| `skills/intelligence-engine/registries/`            | Derived-at-runtime registry output (gitignored except README). `skeleton_map.json` / `derivation_manifest.json` exist for the current 1-document baseline; deeper criteria-derivation (the Stage 0 LLM job) not yet exercised. |
| `_archive/`                                          | Superseded: old `pmo-data-gap-audit` skill, old `IEM-PM_BLUEPRINT.md`, `remit/` — history only            |
| `stakeholder/`                                       | PMI volunteer copyrighted material — **never touch, never publish, never build on**                       |

## 2. Locked decisions (do not re-litigate)

1. **No baseline, no audit** — repo ships zero standard text; org drops real standards into `knowledge/`; registry derived locally; everything standard-derived is gitignored.
2. **OPM3 is the maturity lens** — gaps are _evidence of the org's_ maturity on PMI's OPM3; IEM-PM invents no maturity scale. The **gaps→OPM3 bridge is the open core IP** (`⚠️ STUB / PENDING_BRIDGE` in SKILL.md; code ships a labeled placeholder heuristic — see §5).
3. **Five Contracts** — 1 Standards (baseline) · 2 PMO Data Charter (what data is/means/matters; machine-proposed → human-ratified) · 3 Audit Manifest (LLM↔code boundary + compaction gate) · 4 Canonical Findings JSON · 5 Schema Validator.
4. **Anti-mirror guard** — Charter scope is proposed from the _standards_, never the data; absences surface as candidate **Missing** gaps, never "out of scope."
5. **Closed taxonomies** — 7 gaps (Missing · Ignored · Disconnected · Untrusted · Underutilized · Misclassified · Divergent) × 7 root origins (Capture · Integration · Definition/Taxonomy · Ownership · Process/Cadence · Tooling · Behavior). Closed so the validator can enforce them.
6. **LLM judges; code renders** — Stages 0–7 are LLM judgment; Stages 8–10 deterministic stdlib Python. Same findings JSON → byte-identical report. **Verified**: `test_manifest.md` → `manifest_to_findings.py` → `render.py` runs end-to-end without error.
7. **Scoring** — Reporting Integrity Score 0–100 (Severity = Decision Impact × Spread × Persistence); the 7 "intelligence indicators" are narrative labels only, never scored.
8. **Copyright-safe** — clause + short paraphrase + citation only; never verbatim; the engine stays generic (no hard-coding to any supplied dataset).

## 3. The 11-stage state machine (SKILL.md §5)

Baseline → Charter → Define → Measure → Classify → Trace → Engineer & Score → Synthesize (manifest gate) → Findings JSON → Render → Final Summary.

States: `BASELINE_READY/ABSENT → CHARTER_RATIFIED → INTENT_DEFINED → GAPS_MEASURED → GAPS_CLASSIFIED → ROOTS_TRACED → SCORED/PENDING_BRIDGE → MANIFEST_WRITTEN → JSON_VALIDATED → REPORTS_EMITTED`.

## 4. Build Order (BLUEPRINT-1 §17) and where we are

1. ✅ Define the PMO Data Charter — `assets/PMO_DATA_CHARTER_template.md` written (297 lines).
2. ✅ Define the Findings Schema — `scripts/findings.schema.json` written.
3. ✅ Build the Validator — `scripts/schema.py` written and passes on test fixture.
4. ⚠️ Build the Audit Manifest template — the parser-grade format is fully specified inline in SKILL.md §10; the standalone `assets/AUDIT_MANIFEST_template.md` file is still empty.
5. ✅ Write SKILL.md — complete, all 13 sections, no TODO markers remain.
6. ⚠️ Knowledge Base derivation — scan tooling built (`baseline.py`, `derive_knowledge_index.py`); only 1 standard is actually in `knowledge/` to scan.
7. ⚠️ Registry derivation — skeleton/TOC extraction works (`skeleton_map.json`); the deeper criteria-derivation step (Stage 0's LLM job, turning skeletons into checkable registry items per Appendix E) has not yet been run against real content.
8. ✅ Renderer — `scripts/render.py` written and verified.
9. ✅ Report template — `assets/report_template.html` written (377 lines).
10. ⚠️ Regression tests — only informal fixtures (`test_manifest.md`, `test_findings.json`) and a manual end-to-end run; no pytest suite.
11. ❌ Package as Claude Code skill — not started (no `.claude-plugin/plugin.json` or `marketplace.json`).

## 5. Open design items

- **The gaps→OPM3 bridge** (SKILL §9.3) — still the declared open core IP. `manifest_to_findings.py` ships a working but explicitly provisional heuristic (`bridge_version: "OPM3-Bridge-v0.1-TBD"`) that maps Reporting Integrity Score + gap density + severity distribution to an OPM3 level. Not calibrated against real evidence; treat as a placeholder, not the calibrated rubric.
- **Severity bands (Appendix D)** — done: `references/severity-matrix.md` (153 lines) + SKILL.md §9.1.
- **Error codes (Appendix H)** — still `TODO(you)` (`references/error-codes.md`, 3 lines).
- **File naming (Appendix G)** — still `TODO(you)` (`references/file-naming.md`, 3 lines).
- **Charter spec reference (`references/charter-spec.md`)** — empty file; content currently lives only in SKILL.md §4.2.
- **`assets/AUDIT_MANIFEST_template.md`** — empty; the format is specified in SKILL.md §10 but has no standalone template file yet.
- **Deterministic back half (Stages 8–9)** — ✅ built and verified (was previously listed as "not built").

## 6. Working protocol

User writes SKILL.md one section at a time → Claude reviews against: (a) BLUEPRINT-1 consistency, (b) exact per-stage template compliance, (c) no contradiction with sections already written.

SKILL.md is now fully written, so this protocol's remaining scope is the stub appendices in §5 above, the knowledge base gap, and the OPM3 bridge calibration.

# Status update : Table

| Status | Item                                                                                                                                 | Source                |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------- |
| done   | Defined IEM-PM as a Claude Code skill that compares delivery evidence against declared standards and outputs HTML/JSON/TXT reports.  | IEM-PM-BLUEPRINT-1.md |
| done   | Locked the core operating principle: no baseline, no audit; read-only engine; local-first execution.                                | STATUS.md             |
| done   | Defined the repository topology, including skill, knowledge, registries, validator, renderer, tests, reports, and assets.            | IEM-PM-BLUEPRINT-1.md |
| done   | Defined the 7 gap taxonomy and 7 root-origin taxonomy as closed validation sets.                                                     | IEM-PM-BLUEPRINT-1.md |
| done   | Established the LLM-versus-Python split: LLM judges, Python validates and renders.                                                   | IEM-PM-BLUEPRINT-1.md |
| done   | Set OPM3 as the maturity lens.                                                                                                        | STATUS.md             |
| done   | Created the PMO Data Charter template.                                                                                                | STATUS.md             |
| done   | Defined the Findings Schema (findings.schema.json).                                                                                   | STATUS.md             |
| done   | Built the Schema Validator (schema.py).                                                                                               | STATUS.md             |
| done   | Wrote SKILL.md section by section — now complete.                                                                                     | STATUS.md             |
| done   | Built the Manifest → Findings converter (manifest_to_findings.py), including scoring and provisional OPM3 heuristic.                  | STATUS.md             |
| done   | Created the Renderer (render.py) — HTML + TXT, verified on test fixture.                                                              | STATUS.md             |
| done   | Created the Report Template (report_template.html).                                                                                   | STATUS.md             |
| done   | Built Knowledge Base scan tooling (baseline.py, derive_knowledge_index.py).                                                           | STATUS.md             |
| next   | Build the Audit Manifest standalone template file (assets/AUDIT_MANIFEST_template.md — currently empty).                             | STATUS.md             |
| next   | Populate references/charter-spec.md, error-codes.md, file-naming.md (currently empty/TODO stubs).                                    | STATUS.md             |
| next   | Reconcile knowledge/ contents — only 1 of the expected standards is present; add the rest or update the record.                       | STATUS.md             |
| next   | Run Stage 0 criteria-derivation (skeleton → registry items per Appendix E) against real standards content.                            | STATUS.md             |
| next   | Build a formal regression test suite (pytest) — currently manual fixtures only.                                                       | STATUS.md             |
| next   | Package as Claude Code skill (.claude-plugin/plugin.json, marketplace.json).                                                          | STATUS.md             |
| open   | Design and calibrate the gaps-to-OPM3 bridge (code ships an uncalibrated placeholder heuristic).                                      | STATUS.md             |
| open   | Define error codes and finalize file naming conventions (Appendices G–H).                                                             | STATUS.md             |

# 6-Week Plan

| Week   | Focus            | Deliverable                                                                                                          | Status |
| ------ | ---------------- | ---------------------------------------------------------------------------------------------------------------------- | ------ |
| Week 1 | PMO Data Charter | Draft the PMO Data Charter template with sections for data meaning, scope, materiality, and human ratification.      | done   |
| Week 2 | Findings Schema  | Define findings.schema.json with fields for gap type, root origin, evidence, severity, and OPM3 mapping placeholder. | done   |
| Week 3 | Validator        | Build schema.py to validate findings JSON against the schema and closed taxonomies.                                  | done   |
| Week 4 | Audit Manifest   | Create the Audit Manifest template that converts LLM analysis into a parser-friendly structure.                      | done   |
| Week 5 | SKILL.md         | Write the skill sections and lock the core logic, inputs, and stage flow.                                            | done   |
| Week 6 | Reports + Tests  | Build the renderer, report template, and regression tests; package the skill.                                        | in progress — renderer + report template done; regression tests and packaging remain |

# mapping of the five Claude Certified Architect Foundations domains to your IEM-PM modules.

| CCA-F domain                       | What it teaches                                                          | IEM-PM module it supports                                                                            |
| ------------------------------------ | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Agentic architecture               | Designing multi-step AI systems that plan, reason, and act across tasks  | Core IEM-PM orchestration: baseline → evidence → gap finding → classification → root cause → report |
| Tool use and integrations          | Connecting the model to external systems safely and reliably            | Evidence collection from standards, project data, PM tools, file systems, and local repositories     |
| Claude Code workflows              | Building and operating AI inside a code-first development environment   | Your IEM-PM Claude Code skill packaging, repo structure, stage machine, and build order              |
| Structured outputs and prompts     | Getting consistent JSON, schemas, and controlled LLM responses          | Audit Manifest, Findings JSON, schema validation, and report generation                              |
| Reliability and context management | Keeping the system stable, grounded, and able to work with long inputs  | Standards ingestion, knowledge base derivation, closed taxonomies, and evidence-first reasoning      |
