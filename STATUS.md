# IEM-PM — Project Status

> Last updated: 2026-07-27. This file is the single save-point: decisions, current state, next actions.
> (Previous 2026-07-05 version had SKILL.md, the schema, validator, manifest parser, and renderer
> listed as "next" — all five are now written and were verified end-to-end on 2026-07-26, then
> committed and pushed as `df71e85`. Since then: a real pilot audit ran against real PMI standards
> (`ce569ab`), a regression suite and user guide were added (`1c68116`), and OPM3/organizational-
> maturity modeling was scrapped outright (2026-07-27, uncommitted as of this update).)

---

## 1. What is canonical (as of 2026-07-27)

| Artifact                                            | Status                                                                                                    |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **`IEM-PM BLUEPRINT-1.md`**                         | ✅ **THE approved blueprint** (19 sections, Praxen-shaped, surgically aligned)                            |
| `PRAXEN-BLUEPRINT.md`                               | Reference — how the model project (Praxen) is built                                                       |
| `skills/intelligence-engine/SKILL.md`               | ✅ **Complete** — all 13 sections written (no `TODO(you)` markers remain)                                 |
| `skills/intelligence-engine/scripts/schema.py`       | ✅ Built — validates closed taxonomies, no-duplicate rule, evidence coverage. Passes on test fixture.      |
| `skills/intelligence-engine/scripts/manifest_to_findings.py` | ✅ Built — Manifest → canonical JSON, computes Reporting Integrity Score. No maturity/OPM3 modeling — scrapped, see §2.2. |
| `skills/intelligence-engine/scripts/render.py`       | ✅ Built — canonical JSON → HTML (Jinja2) + TXT. Verified byte-reproducible on test fixture.               |
| `skills/intelligence-engine/scripts/findings.schema.json` | ✅ Built — Draft-07 schema, all 5 contract objects modeled.                                            |
| `skills/intelligence-engine/scripts/baseline.py`     | ✅ Built (Stage 0 mechanics) — fingerprints `knowledge/`, extracts PDF/MD skeletons, diffs against prior run. |
| `skills/intelligence-engine/scripts/derive_knowledge_index.py` | ✅ Built — catalogs `knowledge/` (filenames/sizes only, no content) into `knowledge_index.json`.    |
| `skills/intelligence-engine/knowledge/`             | Baseline drop-zone (gitignored) — **29 real PMI standards now present** in `knowledge/PMI/` (PMBOK 8th Ed., Practice Standard for Scheduling 3rd Ed., Standard for Risk Management, Governance of Portfolios/Programs/Projects Practice Guide, and others). Used for the real pilot audit in `examples/pilot-audit/`. |
| `skills/intelligence-engine/registries/`            | Derived-at-runtime registry output (gitignored except README). Mechanism complete and specified in SKILL.md Phase 0b; `skeleton_map.json` fixed (25/29 real skeletons, up from 2/29 — see §2 locked decisions / §4 build order item 7). One real registry derived as proof (`ps_scheduling_3rd.json`, 3 items); the other 28 standards are not yet derived — deliberately deferred, not blocked. |
| `_archive/`                                          | Superseded: old `pmo-data-gap-audit` skill, old `IEM-PM_BLUEPRINT.md`, `remit/` — history only            |
| `stakeholder/`                                       | PMI volunteer copyrighted material — **never touch, never publish, never build on**                       |

## 2. Locked decisions (do not re-litigate)

1. **No baseline, no audit** — repo ships zero standard text; org drops real standards into `knowledge/`; registry derived locally; everything standard-derived is gitignored.
2. **No maturity modeling — scrapped, not deferred (2026-07-27)** — IEM-PM measures and traces gaps; it does not model organizational maturity. Organizational maturity modeling (e.g., PMI's OPM3) is a distinct discipline requiring cross-project calibration and a licensed instrument, neither of which this tool provides. The gaps→OPM3 bridge (code, schema field, report section, Manifest requirement) has been removed, not just left pending. This reverses the prior "OPM3 is the maturity lens" decision.
3. **Five Contracts** — 1 Standards (baseline) · 2 PMO Data Charter (what data is/means/matters; machine-proposed → human-ratified) · 3 Audit Manifest (LLM↔code boundary + compaction gate) · 4 Canonical Findings JSON · 5 Schema Validator.
4. **Anti-mirror guard** — Charter scope is proposed from the _standards_, never the data; absences surface as candidate **Missing** gaps, never "out of scope."
5. **Closed taxonomies** — 7 gaps (Missing · Ignored · Disconnected · Untrusted · Underutilized · Misclassified · Divergent) × 7 root origins (Capture · Integration · Definition/Taxonomy · Ownership · Process/Cadence · Tooling · Behavior). Closed so the validator can enforce them.
6. **LLM judges; code renders** — Stages 0–7 are LLM judgment; Stages 8–10 deterministic stdlib Python. Same findings JSON → byte-identical report. **Verified**: `test_manifest.md` → `manifest_to_findings.py` → `render.py` runs end-to-end without error.
7. **Scoring** — Reporting Integrity Score 0–100 (Severity = Decision Impact × Spread × Persistence); the 7 "intelligence indicators" are narrative labels only, never scored.
8. **Copyright-safe** — clause + short paraphrase + citation only; never verbatim; the engine stays generic (no hard-coding to any supplied dataset).

## 3. The 11-stage state machine (SKILL.md §5)

Baseline → Charter → Define → Measure → Classify → Trace → Engineer & Score → Synthesize (manifest gate) → Findings JSON → Render → Final Summary.

States: `BASELINE_READY/ABSENT → CHARTER_RATIFIED → INTENT_DEFINED → GAPS_MEASURED → GAPS_CLASSIFIED → ROOTS_TRACED → SCORED → MANIFEST_WRITTEN → JSON_VALIDATED → REPORTS_EMITTED`.

## 4. Build Order (BLUEPRINT-1 §17) and where we are

1. ✅ Define the PMO Data Charter — `assets/PMO_DATA_CHARTER_template.md` written (297 lines).
2. ✅ Define the Findings Schema — `scripts/findings.schema.json` written.
3. ✅ Build the Validator — `scripts/schema.py` written and passes on test fixture.
4. ⚠️ Build the Audit Manifest template — the parser-grade format is fully specified inline in SKILL.md §10; the standalone `assets/AUDIT_MANIFEST_template.md` file is still empty.
5. ✅ Write SKILL.md — complete, all 13 sections, no TODO markers remain.
6. ✅ Knowledge Base derivation — scan tooling built and fixed (`baseline.py`, `derive_knowledge_index.py`); 29 real PMI standards now live in `knowledge/PMI/`, `baseline.py` correctly recurses into subfolders (`BASELINE_READY — 29 document(s)`).
7. ✅ Registry derivation — mechanism complete. Found and fixed a real Stage 0 bug: `baseline.py`'s
   "reuse if fingerprint unchanged" cache trusted an *empty* skeleton as valid, so 27 of 29 real
   standards were silently stuck with zero TOC entries from an earlier failed extraction and never
   retried. Fixed (skills/intelligence-engine/scripts/baseline.py) — 25 of 29 now extract real
   skeletons; the remaining 4 genuinely carry no PDF bookmarks (verified, not a bug). SKILL.md
   Phase 0 now specifies the derivation procedure (file naming, reuse-by-fingerprint, when to
   re-derive — see §Phase 0b), and `references/registry-format.md` documents the file-wrapper
   schema with a real worked example. One real registry derived end-to-end as proof
   (`registries/ps_scheduling_3rd.json`, 3 items from PS_Scheduling_3rd.pdf) — gitignored,
   local-only, not committed by design. Bulk derivation across the other 28 standards is
   intentionally deferred as a separate, deliberately-run job, not part of this fix.
8. ✅ Renderer — `scripts/render.py` written and verified.
9. ✅ Report template — `assets/report_template.html` written (377 lines).
10. ✅ Regression tests — `scripts/test_pipeline.py` rebuilt against real fixtures (5 tests: Manifest→JSON, Schema Validation, JSON→Reports, Knowledge Index, Duplicate Detection), 5/5 passing, committed. Not pytest-based (stdlib only, by design), but no longer manual/informal.
11. ❌ Package as Claude Code skill — not started (no `.claude-plugin/plugin.json` or `marketplace.json`).

## 5. Open design items

- ~~The gaps→OPM3 bridge~~ — **scrapped 2026-07-27**, not an open item anymore. See locked decision #2.
- ~~Registry derivation mechanism~~ — **complete 2026-07-27**. Procedure specified in SKILL.md
  Phase 0b, file format in `references/registry-format.md`, and a real `baseline.py` bug fixed
  (25/29 skeletons were silently stuck empty). Proven on one standard. Bulk derivation across the
  remaining 28 standards is the next open item, not this one.
- **Severity bands (Appendix D)** — done: `references/severity-matrix.md` (153 lines) + SKILL.md §9.1.
- **Error codes (Appendix H)** — still `TODO(you)` (`references/error-codes.md`, 3 lines).
- **File naming (Appendix G)** — still `TODO(you)` (`references/file-naming.md`, 3 lines).
- **Charter spec reference (`references/charter-spec.md`)** — empty file; content currently lives only in SKILL.md §4.2.
- **`assets/AUDIT_MANIFEST_template.md`** — empty; the format is specified in SKILL.md §10 but has no standalone template file yet.
- **Deterministic back half (Stages 8–9)** — ✅ built and verified (was previously listed as "not built").

## 6. Working protocol

User writes SKILL.md one section at a time → Claude reviews against: (a) BLUEPRINT-1 consistency, (b) exact per-stage template compliance, (c) no contradiction with sections already written.

SKILL.md is now fully written, so this protocol's remaining scope is the stub appendices in §5 above and the knowledge base gap.

## 7. Roadmap sync (public site — `RoadmapPage.jsx`)

The public portfolio site (`RUAA Consulting/.../src/views/RoadmapPage.jsx`) carries its own copy of
this sprint plan for public display. That copy has drifted from actual repo state in four places
(⚠️ below), mainly because it still assumes the OPM3 bridge exists. This section is the corrected,
authoritative version as of 2026-07-27 — the next time an agent edits `RoadmapPage.jsx`, sync it
from here, not the other way around.

**Week 1 (Jun 22–28) — Define the Discipline — Completed.** Unchanged, still accurate. (IEM-PM +
IEM-CS discipline definitions — IEM-CS is a sibling discipline outside this repo, not build-tracked
here.)

**Week 2 (Jun 29–Jul 5) — Formalize the Method — Completed.**
- Founding principles (×7) — Done
- Closed taxonomy: seven data gaps × seven root origins — Done
- ⚠️ "Reporting Integrity Score (0–100) — OPM3 as the maturity lens" → **no maturity lens; the score
  is deterministic and gap-based only.** OPM3 was scrapped 2026-07-27 (locked decision #2) — Done
- Blueprint approved — 19 sections, 11-stage audit state machine — Done

**Weeks 3–4 (Jul 6–26) — Build the Intelligence Engine — Completed.**
- Intelligence Engine skill spec complete — Done (now v1.1.0)
- Core reference docs complete: gap taxonomy, root origins, severity matrix, audit stages — Done
- Five Contracts built: Charter template, findings schema, validator, manifest parser, renderer — Done

**Week 5 (Jul 27–Aug 2) — ⚠️ retitle "Design the Gaps→OPM3 Bridge" → "Prove the Pipeline on Real
Data".** The OPM3 bridge was never built out — it was scrapped outright on 2026-07-27 (see locked
decision #2), so there is nothing left to design. What actually happened this week instead:
- Real pilot audit run against real PMI standards (29 documents) — 4 genuine findings, Reporting
  Integrity Score 50.67/100 — Done (pulled forward three weeks from its original Week 7 slot)
- Three real `baseline.py` bugs found and fixed during the pilot and the Stage 0 follow-up
  (path resolution; non-recursive knowledge-folder scan that hid subfolders; a stale-cache bug
  that froze 27 of 29 real standards at an empty skeleton from an earlier failed extraction) — Done
- Registry derivation mechanism — now fully specified (SKILL.md Phase 0b, file format in
  `references/registry-format.md`) and proven on one real standard
  (`registries/ps_scheduling_3rd.json`) — Done. Bulk derivation across the other 28 standards —
  Upcoming

**Week 6 (Aug 3–9) — Registry & Renderer — In progress.**
- ⚠️ "Registry complete ('no baseline, no audit') — only skeleton-level derivation exists so far" →
  the *mechanism* is complete and proven on 1 of 29 standards (see Week 5); full derivation across
  all 29 remains — In progress, not Upcoming
- Deterministic renderer & report template — LLM judges, code renders — Done
- Regression tests across the audit state machine — Done (`test_pipeline.py`, 5/5 passing, committed
  in `1c68116`)

**Week 7 (Aug 10–16) — Pilot & Package — Upcoming.**
- Role-based user guide published for PMs, program managers, and PMO leads — Done
  (`Public/IEM-PM-User-Guide.html`)
- ⚠️ "End-to-end pilot audit against a real baseline" → **Done**, not Upcoming — it ran 2026-07-27,
  three weeks ahead of schedule (see Week 5 above)
- "Fix what the pilot breaks" — Done for this round (the two `baseline.py` fixes above); more may
  surface once the next pilot runs
- Package as an open-source Claude Code skill — Upcoming, not started (no `.claude-plugin/plugin.json`
  or `marketplace.json`)

**Week 8 (Aug 17–23) — White Paper — Upcoming.** Unchanged.

**Week 9 (Aug 24–30) — Publish v1.0 — Upcoming.** Unchanged.

**Longer Arc, 12–24 Months, "Codify the Discipline":** ⚠️ current description reads "...a
confidence-scoring and maturity model...". Drop "maturity model" — it is permanently out of scope
per locked decision #2 (scrapped, not deferred), not merely a later-phase deliverable. Suggested
replacement: "A long-form reference, and adoption of the shared methodology beyond the founding two
domains."

**Corrections the portfolio site needs (summary):**
1. Week 2 — drop "OPM3 as the maturity lens" from the Reporting Integrity Score item.
2. Week 5 — retitle off the OPM3 bridge; replace its items with the real pilot-audit work above.
3. Week 6 — "Registry complete" is In progress (mechanism proven), not Upcoming.
4. Week 7 — mark "End-to-end pilot audit against a real baseline" as Done.
5. Longer Arc, 12–24 months — drop "maturity model" from the description.

# Status update : Table

| Status | Item                                                                                                                                 | Source                |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------- |
| done   | Defined IEM-PM as a Claude Code skill that compares delivery evidence against declared standards and outputs HTML/JSON/TXT reports.  | IEM-PM-BLUEPRINT-1.md |
| done   | Locked the core operating principle: no baseline, no audit; read-only engine; local-first execution.                                | STATUS.md             |
| done   | Defined the repository topology, including skill, knowledge, registries, validator, renderer, tests, reports, and assets.            | IEM-PM-BLUEPRINT-1.md |
| done   | Defined the 7 gap taxonomy and 7 root-origin taxonomy as closed validation sets.                                                     | IEM-PM-BLUEPRINT-1.md |
| done   | Established the LLM-versus-Python split: LLM judges, Python validates and renders.                                                   | IEM-PM-BLUEPRINT-1.md |
| done   | Scrapped OPM3/organizational-maturity modeling as out of scope (descoped, not deferred).                                              | STATUS.md             |
| done   | Created the PMO Data Charter template.                                                                                                | STATUS.md             |
| done   | Defined the Findings Schema (findings.schema.json).                                                                                   | STATUS.md             |
| done   | Built the Schema Validator (schema.py).                                                                                               | STATUS.md             |
| done   | Wrote SKILL.md section by section — now complete.                                                                                     | STATUS.md             |
| done   | Built the Manifest → Findings converter (manifest_to_findings.py), including Reporting Integrity Score computation.                   | STATUS.md             |
| done   | Created the Renderer (render.py) — HTML + TXT, verified on test fixture.                                                              | STATUS.md             |
| done   | Created the Report Template (report_template.html).                                                                                   | STATUS.md             |
| done   | Built Knowledge Base scan tooling (baseline.py, derive_knowledge_index.py); fixed two Stage 0 bugs found during the real pilot (path resolution, non-recursive scan). | STATUS.md             |
| done   | Reconciled knowledge/ contents — 29 real PMI standards now loaded in knowledge/PMI/ (was 1).                                          | STATUS.md             |
| done   | Built a real regression suite (scripts/test_pipeline.py) against real fixtures — 5 tests, 5/5 passing.                                | STATUS.md             |
| done   | Published a role-based user guide for PMs, program managers, and PMO leads (Public/IEM-PM-User-Guide.html).                            | STATUS.md             |
| done   | Ran a real end-to-end pilot audit against the real PMI baseline (examples/pilot-audit/) — 4 findings, Reporting Integrity Score 50.67/100. | STATUS.md             |
| done   | Fixed a real Stage 0 bug (baseline.py stale-skeleton cache) that had silently frozen 27 of 29 real standards at zero TOC entries; specified the registry-derivation procedure in SKILL.md Phase 0b and the file format in registry-format.md; derived one real registry as proof. | STATUS.md             |
| next   | Build the Audit Manifest standalone template file (assets/AUDIT_MANIFEST_template.md — currently empty).                             | STATUS.md             |
| next   | Populate references/charter-spec.md, error-codes.md, file-naming.md (currently empty/TODO stubs).                                    | STATUS.md             |
| next   | Run bulk Stage 0 criteria-derivation across the remaining 28 real standards (mechanism proven on 1 of 29).                             | STATUS.md             |
| next   | Package as Claude Code skill (.claude-plugin/plugin.json, marketplace.json).                                                          | STATUS.md             |
| open   | Define error codes and finalize file naming conventions (Appendices G–H).                                                             | STATUS.md             |

# 6-Week Plan

| Week   | Focus            | Deliverable                                                                                                          | Status |
| ------ | ---------------- | ---------------------------------------------------------------------------------------------------------------------- | ------ |
| Week 1 | PMO Data Charter | Draft the PMO Data Charter template with sections for data meaning, scope, materiality, and human ratification.      | done   |
| Week 2 | Findings Schema  | Define findings.schema.json with fields for gap type, root origin, evidence, and severity.                           | done   |
| Week 3 | Validator        | Build schema.py to validate findings JSON against the schema and closed taxonomies.                                  | done   |
| Week 4 | Audit Manifest   | Create the Audit Manifest template that converts LLM analysis into a parser-friendly structure.                      | done   |
| Week 5 | SKILL.md         | Write the skill sections and lock the core logic, inputs, and stage flow.                                            | done   |
| Week 6 | Reports + Tests  | Build the renderer, report template, and regression tests; package the skill.                                        | in progress — renderer, report template, and regression tests done; packaging as a Claude Code skill remains |

# mapping of the five Claude Certified Architect Foundations domains to your IEM-PM modules.

| CCA-F domain                       | What it teaches                                                          | IEM-PM module it supports                                                                            |
| ------------------------------------ | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Agentic architecture               | Designing multi-step AI systems that plan, reason, and act across tasks  | Core IEM-PM orchestration: baseline → evidence → gap finding → classification → root cause → report |
| Tool use and integrations          | Connecting the model to external systems safely and reliably            | Evidence collection from standards, project data, PM tools, file systems, and local repositories     |
| Claude Code workflows              | Building and operating AI inside a code-first development environment   | Your IEM-PM Claude Code skill packaging, repo structure, stage machine, and build order              |
| Structured outputs and prompts     | Getting consistent JSON, schemas, and controlled LLM responses          | Audit Manifest, Findings JSON, schema validation, and report generation                              |
| Reliability and context management | Keeping the system stable, grounded, and able to work with long inputs  | Standards ingestion, knowledge base derivation, closed taxonomies, and evidence-first reasoning      |
