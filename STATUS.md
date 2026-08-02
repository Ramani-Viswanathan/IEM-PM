# IEM-PM — Project Status

> Last updated: 2026-08-02. This file is the single save-point: decisions, current state, next actions.
> (Previous 2026-07-05 version had SKILL.md, the schema, validator, manifest parser, and renderer
> listed as "next" — all five are now written and were verified end-to-end on 2026-07-26, then
> committed and pushed as `df71e85`. Since then: a real pilot audit ran against real PMI standards
> (`ce569ab`), a regression suite and user guide were added (`1c68116`), OPM3/organizational-
> maturity modeling was scrapped outright (`0af0b43`), a real Stage 0 stale-cache bug was fixed and
> the registry-derivation mechanism specified (`aeef25f`), and LICENSE/README/requirements.txt,
> output naming (Appendix G), error codes (Appendix H), and two more real production-run pilot
> audits landed (`336eb58`). Since then: path resolution consolidated into `scripts/paths.py`, the
> Manifest format moved out of SKILL.md into `assets/AUDIT_MANIFEST_template.md` (`771fd24`);
> `confidence-scale.md` archived as unwired, `severity-matrix.md` wired into SKILL.md §9.1 as
> calibration reference (`c7cb29e`); SKILL.md checked against Anthropic's official skill-authoring
> best practices (500-line guidance) and the Charter spec moved out to `references/charter-spec.md`
> with TOCs added to the reference files that needed them (`ff81989`); §11 Report Generation branched
> out to `references/report-generation.md`, a real gap fixed (the branch-out had left no pointer
> behind in SKILL.md at all), and the Example Finding Block reordered into its correct place in
> `AUDIT_MANIFEST_template.md` (`48f7857`); SKILL.md's main TOC linked, and every `references/*.md`
> file given a `Name`/`description`/`version` header for consistency, plus the two still-missing
> sub-TOCs (`charter-spec.md`, `report-generation.md`) added (`18a6517`). Since then: Minimum
> Evidence Sufficiency (Halt Condition 6) finalized and activated (`5061342`); the Scope Limitation
> Notice HTML renderer built (`scripts/render_scope_limitation.py`), verified against a real
> fresh-session Pilot-audit-4 run, and evidence-sufficiency.md's Category B wording fixed (`caa158b`);
> a new cross-cutting rule, Terminology Discipline (`references/terminology.md`, SKILL.md §6.7),
> added to keep all free-text narrative in the standard's own PM vocabulary rather than synonyms or
> vendor jargon — SKILL.md was v1.8.0 at that point. All of the above is pushed to `origin/master`.
> `references/audit-stages.md` was then completed end to end — all 11 stages, zero `TODO(you)`,
> `version: 1.0.0` at the time — with several real corrections along the way (Stage 6's wrong claim
> to compute the RIS; the four-part diagnostic restored; Stage 7 hardened with a real
> chain-verification check and a new `CHAIN_INTEGRITY_LOST` hard stop; stale script/path references
> fixed); then wired into SKILL.md for real — every §5 Phase now points into its matching Stage,
> promoting the file from excluded to actively-read — SKILL.md reached v1.9.0.)
>
> **2026-08-02 — real bugs found and fixed on a live re-run.** Re-ran `examples/Pilot-audit-2/`
> against the PMI baseline (a second, independent Charter/audit, alongside the existing
> `examples/Pilot-audit-3/` PMI run — see §8), which surfaced two genuine defects in
> `manifest_to_findings.py`, missed by the existing test fixtures because none of them exercised a
> standard title containing its own comma, or a "Field Coverage" line written as prose instead of a
> bare percentage: (1) `_parse_standards`/`_parse_scope` split on `,`, shredding any standard title
> with an internal comma (several real PMI titles have one) into bogus fragments — fixed, now splits
> on `;` per `AUDIT_MANIFEST_template.md`'s declared convention; (2) `_parse_percentage` accepted a
> bare number with no `%` sign, so "27 of 27 declared columns present" was misread as "27%" instead
> of 100% — fixed, now parses the "N of M" form and requires an explicit `%` for the bare-number
> form. Both covered by new regression assertions in `test_pipeline.py` (still 6/6) and verified
> against the real, re-generated Pilot-audit-2 output. Also: the Reporting Integrity Score formula's
> severity/density deduction caps saturated too easily — a routine 14-finding audit already floored
> at 0.0, indistinguishable from a genuinely catastrophic one — widened by decision (severity caps at
> total severity 50, not 30; density caps at 4/artifact, not 2), methodology bumped to v1.1.0;
> Pilot-audit-2 went from 0.0 to 21.5 under the new formula. Separately, the same live run exposed a
> real output-location bug (the Manifest was written to `examples/Pilot-audit-2/reports/` instead of
> the actual convention, repo-root `reports/`, discovered only by chasing a file path) and a
> missed-context gap (the run independently re-derived a full Charter and audit without knowing
> `Pilot-audit-3` already covered the same evidence against PMI) — both now closed at the process
> level: `references/file-naming.md`, `SKILL.md` §10.6, and `audit-stages.md` Stage 1/7 all now state
> the repo-root location explicitly, and a new Stage 1 Activity checks evidence checksums against
> existing `reports/` Manifests before drafting a new Charter. Stage 3 also picked up two
> evidence-reading rules (column-index alignment; exhaustive row counting, not sampling) after two
> real data-reading mistakes surfaced in the same run (a Cost Tracker column swap; an undercounted,
> incomplete Task Board finding). `references/audit-stages.md` is now `version: 1.1.0`; `SKILL.md` is
> now `version: 1.9.1`.
>
> **2026-08-02, later the same day — `knowledge/PMI/` reorganized; hardcoded folder-name table
> replaced with a dynamic index.** The user split `knowledge/PMI/`'s 30 files into `PMI/` (14 core
> delivery/measurement standards) plus three new sibling folders — `PMI-AI/` (3), `PMI-Other/` (8,
> including `Governance_PG.pdf`), `PMI-Sustainability/` (3) — and `Agile/` gained its first real
> content. This exposed that `SKILL.md` §13.2's Knowledge Base Reading Guide hardcoded a fixed,
> already-stale set of folder names (`PMBOK/`, `MSP/`, `ISO21502/` never actually existed; the real
> `PRINCE2/`/`PMI/`/`Agile/`/`Organizational/` folders did, but the reorg's new categories weren't,
> and couldn't be, listed). Since any organization can structure `knowledge/` however it likes, a
> fixed table can never stay correct. Fix: `baseline.py` now calls the previously-standalone
> `derive_knowledge_index.py`'s scan as part of Stage 0 itself, writing `knowledge_index.json` (the
> actual current folder/category structure, whatever it's named, with document counts) alongside the
> skeleton map and registries in one run — verified live, correctly found all 6 real categories with
> zero hardcoded names. `SKILL.md` §13.2 and §4.1 now point to that dynamic index instead of the
> fixed table; the one remaining heuristic (the org's own internal-process documents override generic
> standards) is identified by content/category name, not a required exact folder name.
> `references/audit-stages.md` Stage 0 gained a matching Activity/Output. `audit-stages.md` is now
> `version: 1.2.0`; `SKILL.md` is now `version: 1.9.2`. 6/6 regression tests still pass. Committed and
> pushed as `6663688`.

---

## 1. What is canonical (as of 2026-07-27)

| Artifact                                            | Status                                                                                                    |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **`IEM-PM BLUEPRINT-1.md`**                         | ✅ **THE approved blueprint** (19 sections, Praxen-shaped, surgically aligned)                            |
| `PRAXEN-BLUEPRINT.md`                               | Reference — how the model project (Praxen) is built                                                       |
| `skills/intelligence-engine/SKILL.md`               | ✅ **Complete**, v1.10.0 — all 13 sections written, no `TODO(you)` markers. Checked against Anthropic's official skill-authoring best practices 2026-07-29: body trimmed 1,071 → 862 lines (Charter spec → `references/charter-spec.md`; Report Generation → `references/report-generation.md`, both as pointer stubs matching the §7/§8 pattern); main TOC linked; every `references/*.md` file now has a `Name`/`description`/`version` header and a TOC where >100 lines. Now 901 lines — grew back above the trimmed figure by design: §5's 8 Phases each carry a real inline pointer into `audit-stages.md`'s now-complete Stages, promoting it from excluded to actively-read (see §5 below). Still above the documented <500-line guidance — the remaining gap needs an actual conciseness edit of core sections, not more relocation; open, see §5. Halt Condition 6 (Minimum Evidence Sufficiency) active, with a working HTML renderer. §6.7 Terminology Discipline added — free-text prose must use the declared standard's own vocabulary. §13.2/§4.1 (2026-08-02): replaced a hardcoded, already-stale `knowledge/` folder-name table with a pointer to the dynamically-generated `knowledge_index.json` — no folder name is assumed to exist anymore. |
| `skills/intelligence-engine/scripts/schema.py`       | ✅ Built — validates closed taxonomies, no-duplicate rule, evidence coverage. Passes on test fixture.      |
| `skills/intelligence-engine/scripts/manifest_to_findings.py` | ✅ Built — Manifest → canonical JSON, computes Reporting Integrity Score (Weighted Gap Profile **v1.1.0** — severity/density deduction caps widened 2026-08-02, see intro). No maturity/OPM3 modeling — scrapped, see §2.2. Two real parsing bugs found and fixed 2026-08-02 (comma-splitting on multi-comma standard titles; Field Coverage prose misread as a raw-count percentage) — see intro and `test_pipeline.py`. |
| `skills/intelligence-engine/scripts/render.py`       | ✅ Built — canonical JSON → HTML (Jinja2) + TXT. Verified byte-reproducible on test fixture.               |
| `skills/intelligence-engine/scripts/findings.schema.json` | ✅ Built — Draft-07 schema, all 5 contract objects modeled.                                            |
| `skills/intelligence-engine/scripts/baseline.py`     | ✅ Built (Stage 0 mechanics) — fingerprints `knowledge/`, extracts PDF/MD skeletons, diffs against prior run. |
| `skills/intelligence-engine/scripts/derive_knowledge_index.py` | ✅ Built — catalogs `knowledge/` (filenames/sizes only, no content) into `knowledge_index.json`.    |
| `skills/intelligence-engine/knowledge/`             | Baseline drop-zone (gitignored) — **29 real PMI standards now present** in `knowledge/PMI/` (PMBOK 8th Ed., Practice Standard for Scheduling 3rd Ed., Standard for Risk Management, Governance of Portfolios/Programs/Projects Practice Guide, and others). Used for the real pilot audit in `examples/pilot-audit/`. |
| `skills/intelligence-engine/registries/`            | Derived-at-runtime registry output (gitignored except README). Mechanism complete and specified in SKILL.md Phase 0b; `skeleton_map.json` fixed (25/29 real skeletons, up from 2/29 — see §2 locked decisions / §4 build order item 7). **6 of 29** standards now have real deep-dived registries (`ps_scheduling_3rd.json`, `standard_earned_value_management.json`, `ps_wbs_thirded.json`, `thestandardforriskmgmt.json`, `governance_pg.json`, `practice_standard_project_configuration_management.json` — 18 items total), all derived on demand by real audits (Stage 2), none pre-emptively batched; the other 23 are not yet derived — deliberately deferred, not blocked. See §5's strategy note. |
| `skills/intelligence-engine/knowledge_index.json`   | ✅ Built 2026-08-02 (gitignored, derived output) — the dynamic folder/category scan of `knowledge/`'s actual current structure (`derive_knowledge_index.py`'s logic, now called from `baseline.py` as part of Stage 0, not a separate manual step). Replaces a hardcoded folder-name table in SKILL.md §13.2 that couldn't survive the user reorganizing `knowledge/PMI/` into `PMI/`+`PMI-AI/`+`PMI-Other/`+`PMI-Sustainability/`. Zero hardcoded category names anywhere in the mechanism — verified live against the real reorg (found all 6 real categories correctly). |
| `_archive/`                                          | Superseded: old `pmo-data-gap-audit` skill, old `IEM-PM_BLUEPRINT.md`, `remit/` — history only            |
| `stakeholder/`                                       | PMI volunteer copyrighted material — **never touch, never publish, never build on**                       |
| `LICENSE`, `README.md`, `requirements.txt`           | ✅ Built — MIT license, visitor-facing README, pinned deps (jsonschema, jinja2, pypdf, cryptography, openpyxl). Packaging *prerequisites* — not the skill package itself (see §4 item 11). |
| `references/file-naming.md` (Appendix G)             | ✅ Built — `IEMPM_AuditGap_Report_DDMMYY_HHMM.<ext>`, timestamp sourced from the audit's own Date, not wall-clock run time. Wired into `manifest_to_findings.py` and `render.py` as the default. |
| `references/error-codes.md` (Appendix H)             | ✅ Built — `E-BASE-*`/`E-PARSE-*`/`E-VALID-*`/`E-RENDER-*` prefix every validation failure across `baseline.py`/`schema.py`/`manifest_to_findings.py`/`render.py`. |
| `Audit/`                                            | ✅ Built 2026-08-02 — the new drop-zone for real engagements, separate from `examples/`. Structure: `Audit/<ProjectName>/evidence/` (user-created, gitignored) + `Audit/<ProjectName>/reports/` (engine-created, gitignored) — every project gets its own `reports/` folder as a sibling of its `evidence/` folder; there is no single shared reports location anymore. Ships with only `Audit/README.md` tracked, matching `knowledge/`'s drop-zone pattern. See §9 log for the full change (removed `paths.py`'s `REPORTS_DIR`; `manifest_to_findings.py`/`render.py` now default output next to their own input file). `examples/` is untouched by this — existing example folders keep working exactly as before. |
| `examples/Pilot-audit-2/`, `examples/Pilot-audit-3/` | ✅ Real, ratified production audits — real ClientOrg Consulting evidence (not synthetic). `Pilot-audit-2` now carries **two** independent ratified Charters/audits of the same evidence: v1.0.0 (org process flow, 6 findings) and a 2026-08-02 v2.0.0 PMI-scoped re-run (14 findings) — the latter run independently, without knowledge that `Pilot-audit-3` already covered the same evidence against PMI (6 findings). Both kept deliberately; reconciling the finding-count gap between the two PMI-scoped runs is an open item, not yet done. Committed (evidence files included — repo is **private**). See §8. |
| `skills/intelligence-engine/scripts/paths.py`        | ✅ Built 2026-07-27 — single source of truth for `SCRIPTS_DIR`/`ENGINE_DIR`/`REPO_ROOT`/`KNOWLEDGE_DIR`/`REGISTRIES_DIR`/`ASSETS_DIR`/`DEFAULT_TEMPLATE`. Fixes a real inconsistency: `manifest_to_findings.py`/`render.py` had duplicated a fragile `Path(__file__).resolve().parents[3]` in two places, different from `baseline.py`/`derive_knowledge_index.py`/`test_pipeline.py`'s `.parent.parent` style. All 5 scripts now import from here; verified working from both `scripts/` and the repo root. **2026-08-02: `REPORTS_DIR` removed** — reports/ is no longer one fixed global folder; `manifest_to_findings.py`/`render.py` now default their output next to their own input file (see §9 log). 7/7 regression tests pass. |

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
4. ✅ Build the Audit Manifest template — `assets/AUDIT_MANIFEST_template.md` now holds the full parser-grade format, moved verbatim out of SKILL.md §10.2 (byte-identical, verified) and TOC'd; SKILL.md §10.2 is now a pointer.
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
   local-only, not committed by design. **Update 2026-08-02:** the real PMI re-audit of
   Pilot-audit-2 organically deep-dived 5 more standards on demand (Stage 2, as designed) —
   `standard_earned_value_management.json` (5 items), `ps_wbs_thirded.json` (3),
   `thestandardforriskmgmt.json` (3), `governance_pg.json` (3),
   `practice_standard_project_configuration_management.json` (1) — so **6 of 29** standards now
   have real deep-dived registries (18 items total, ~1,004 of ~5,265 total pages). Bulk derivation
   across the other 23 standards (~4,261 pages) is intentionally deferred as a separate,
   deliberately-run job, not part of this fix — see §5 for the strategy question.
8. ✅ Renderer — `scripts/render.py` written and verified.
9. ✅ Report template — `assets/report_template.html` written (377 lines).
10. ✅ Regression tests — `scripts/test_pipeline.py` rebuilt against real fixtures (5 tests: Manifest→JSON, Schema Validation, JSON→Reports, Knowledge Index, Duplicate Detection), 5/5 passing, committed. Not pytest-based (stdlib only, by design), but no longer manual/informal.
11. ⚠️ Package as Claude Code skill — prerequisites done (LICENSE, README, requirements.txt); the
    actual package (`.claude-plugin/plugin.json`, `marketplace.json`) not started.

## 5. Open design items

- ~~The gaps→OPM3 bridge~~ — **scrapped 2026-07-27**, not an open item anymore. See locked decision #2.
- ~~Registry derivation mechanism~~ — **complete 2026-07-27**. Procedure specified in SKILL.md
  Phase 0b, file format in `references/registry-format.md`, and a real `baseline.py` bug fixed
  (25/29 skeletons were silently stuck empty). Proven on one standard, and since 2026-08-02 organic
  on-demand derivation (Stage 2, real audits) has taken it to **6 of 29** standards deep-dived (see
  Build Order item 7). Bulk derivation across the remaining **23** standards is the next open item,
  not this one — whether it's worth doing as a dedicated batch job at all, versus continuing to let
  Stage 2 derive on demand per audit, is itself an open question (see the strategy note added
  2026-08-02 below).
- **Bulk registry derivation strategy (added 2026-08-02, not started)** — 23 of 29 PMI standards
  (~4,261 pages) remain skeleton-only. Recommendation: do **not** run this as one blind top-to-bottom
  batch. (1) The engine's own design already derives on demand (Stage 2) — every standard deep-dived
  so far, all 6, was driven by a real audit actually citing it, not a pre-emptive batch. Bulk-deriving
  all 23 up front pre-pays for standards that may never get cited by a real audit (e.g. the two
  Sustainability standards, AI Essentials) while the on-demand path has zero waste. (2) If a batch is
  still wanted (e.g. to remove Stage 2's first-audit latency for common standards), prioritize by
  expected citation frequency, not page count or file order: PMBOK 8th Ed. (401pp, cross-cutting,
  Stage 2 already falls back to it whenever a domain-specific standard doesn't fully cover a
  criterion — see `AUDIT_MANIFEST_template.md` §7.1 usage in Pilot-audit-2), the Portfolio (140pp)
  and Program (262pp) Management standards, and `pmo_practiceguide_eng.pdf` (342pp) are far more
  likely to be cited across future audits than the AI/Sustainability/Business-Analysis standards.
  (3) Deep-diving is deliberately slow by design (Principle 3 — paraphrase + citation anchor, never
  verbatim; each item needs to be individually checked against the real PDF text, not skimmed) —
  tonight's 5 standards (~782 pages, 15 items) were derived as a side effect of one live audit
  session, not a dedicated timed run, so there's no clean per-page throughput number yet. A realistic
  dedicated pass would batch 3-5 standards per session grouped by size (small <100pp, medium
  100-250pp, large 250-500pp), verify each against `registry-format.md`'s Appendix E structure and
  the No-Verbatim rule before moving to the next, and treat page count as a rough proxy for effort,
  not a precise one — a dense standard with many distinct normative statements takes longer per page
  than a narrative practice guide. Estimate: roughly 6-8 dedicated sessions for the remaining 23,
  not a single run.
- **Severity bands (Appendix D)** — done: `references/severity-matrix.md` (153 lines) + SKILL.md §9.1.
  Wired in 2026-07-29 as an explicit calibration-reference pointer from §9.1 (was previously
  unreferenced anywhere in SKILL.md despite formalizing the same Decision Impact/Spread/Persistence
  factors §9.1's calibration rules already named informally). The 1–5 field is still what the
  Manifest/schema/RIS consume — Appendix D is reference, not a parsed input.
- **`references/confidence-scale.md` (Appendix C)** — archived 2026-07-29 to
  `_archive/skills/intelligence-engine/references/`. Real, substantive content, but unreferenced
  anywhere in SKILL.md and no corresponding field in the schema/Manifest contract — not deleted,
  kept as history in case it's revisited.
- ~~Error codes (Appendix H)~~ — **done 2026-07-27**. `references/error-codes.md` documents
  `E-BASE-*`/`E-PARSE-*`/`E-VALID-*`/`E-RENDER-*`; embedded as message prefixes in the actual
  scripts, not just documented on paper.
- ~~File naming (Appendix G)~~ — **done 2026-07-27**. `references/file-naming.md` specifies
  `IEMPM_AuditGap_Report_DDMMYY_HHMM.<ext>`; `manifest_to_findings.py`/`render.py` default to it,
  smoke-tested for real.
- ~~Charter spec reference (`references/charter-spec.md`)~~ — **done 2026-07-29**. SKILL.md §4.2's
  five-function Charter spec moved out verbatim (byte-identical, verified); §4.2 is now a pointer.
  §4.1 (Standards) and §4.3 (Audit Manifest — "your only output") deliberately stayed inline: both
  are short and read every invocation, unlike the Charter's longer explanatory prose.
- ~~`assets/AUDIT_MANIFEST_template.md`~~ — **done** (see Build Order item 4 above).
- **Deterministic back half (Stages 8–9)** — ✅ built and verified (was previously listed as "not built").
- **SKILL.md line budget** — open, 2026-07-29. Checked against Anthropic's official skill-authoring
  best practices (docs.claude.com "Skill authoring best practices" + the `anthropics/skills`
  skill-creator/template repos): SKILL.md body should stay under 500 lines. Two relocations done —
  Charter spec (§4.2 → `references/charter-spec.md`) and Report Generation (§11 →
  `references/report-generation.md`) — bringing the body from 1,071 to **864 lines**. Both moves
  left a short pointer stub in place (§7/§8 pattern); the Report Generation move initially did NOT
  (a real gap — the section vanished from SKILL.md with nothing pointing to where it went — caught
  and fixed same day, see version history). Remaining gap to <500 lines can't come from more
  relocation — everything left is core, per-invocation content (§2 Operating Principles, §5 Thinking
  Phases, §6 Cross-Cutting Rules, §9 Scoring) that Anthropic's own guidance says belongs in SKILL.md.
  Closing it means a real conciseness edit — reading each section for redundant explanation, not
  cutting along a heading boundary — deliberately scoped as its own, slower, separate pass. Ground
  rule: never cut or relocate content that's read every invocation just to hit the line count —
  quality/correctness outranks the metric. May land around 500–650 rather than exactly under 500.
- **`references/audit-stages.md` — complete and wired in, 2026-07-29** (`version: 1.0.0`, was
  `0.2.0-incomplete`). All 11 stages fully written — zero `TODO(you)` markers, full
  Precondition→Transition chain verified unbroken end to end. Beyond filling blanks: Stage 6's
  Purpose was factually wrong (claimed to compute the Reporting Integrity Score, contradicting
  §9.2/§9.5 — fixed); the four-part diagnostic (Evidence · Impact · Why/Who/Scope · Fix-at-source),
  present in the original archived blueprint but absent from SKILL.md's live path, is now written
  in and mapped onto the real Finding Block fields; Stages 8–9's headings and Purpose falsely
  claimed their scripts didn't exist (both have existed and passed regression since earlier in the
  build — fixed); every stale `reports/<run>/...` path replaced with the real Appendix G naming
  convention; a dead `PENDING_BRIDGE` precondition (leftover from the scrapped OPM3 plan) removed
  from Stage 7. Stage 7's own Preconditions was hardened beyond a bare `SCORED` flag: since Stages
  0–6 write nothing to disk except the Charter, a chain-verification check (confirming every finding
  actually carries its full Stage 3–6 contributions) now runs before writing begins, with its own
  hard-stop code (`CHAIN_INTEGRITY_LOST`) for genuinely unrecoverable memory loss.
  **Wired into SKILL.md (v1.9.0):** promoted from "excluded" (§13.3, "you do not need to open
  these") to **actively read** — each §5 Phase now carries a real inline pointer into its matching
  Stage, same pattern already used for `gap-taxonomy.md`/`root-origins.md` (read on demand, not
  preloaded). §5 stays the concise index; `audit-stages.md` is the engine — the tier Claude actually
  executes from. This also closes the real regression flagged when this item was opened: Phase 5's
  pointer to Stage 6 means the four-part diagnostic is no longer silently missing from the live
  path.
  **2026-08-02, `version: 1.1.0`:** a live PMI re-run of `Pilot-audit-2` surfaced three more real
  gaps in this file, now fixed — see the intro for the full account: (1) the `reports/` output
  location was ambiguous ("the run's `reports/` folder") and the run actually wrote to the wrong
  place; Stage 1 and Stage 7 now both state the repo-root location explicitly, matching
  `scripts/paths.py`'s `REPORTS_DIR`. (2) Nothing checked whether the evidence being audited already
  had a prior audit on file; Stage 1 gained a new Activity that checksum-matches supplied evidence
  against existing `reports/` Manifests before a new Charter is drafted. (3) Two real evidence-
  reading mistakes (a spreadsheet column misread; an undercounted finding that also missed an entire
  affected subtree) prompted two new Stage 3 rules: align values to headers by column index, and
  enumerate matching rows exhaustively rather than sampling when a finding cites a count.
  **2026-08-02, later the same day, `version: 1.2.0`:** Stage 0 gained a new Activity/Output —
  building `knowledge_index.json` (the actual `knowledge/` folder/category structure this run,
  whatever it's named) via `baseline.py` now calling `derive_knowledge_index.py`'s scan internally.
  Prompted by the user reorganizing `knowledge/PMI/` into 4 folders, which exposed that SKILL.md
  §13.2 hardcoded a fixed folder-name table that could never survive an org restructuring its own
  `knowledge/` layout. See the intro for the full account.
- **`allowed-tools:` frontmatter field** — open, low priority. Not part of the general Agent Skills
  spec documented at docs.claude.com (only `name`/`description`/`compatibility` are); likely a
  Claude Code–specific packaging field. Verify against Claude Code's own skill-packaging docs when
  Build Order item 11 (`.claude-plugin/plugin.json`) is actually started — not blocking anything now.
- **Minimum Evidence Sufficiency gate (`references/evidence-sufficiency.md`, SKILL.md §6.6 condition
  6)** — spec **finalized 2026-07-29**, `version: 1.0.0`, zero `TODO(you)` markers, Halt Condition 6
  now **active** in SKILL.md (was "DRAFT, not yet active" until this). Halt Conditions 1–5 were all
  binary presence/absence checks; none caught a *readable, ratifiable* evidence set too thin to
  support a credible audit — raised by Pilot-audit-4, where one CSV was about to reach Charter
  proposal against a 6-standard PMI baseline with nothing to catch that. Modeled on a real audit
  concept (scope limitation → disclaimer of opinion) rather than a misleadingly scored result.
  Final spec: 7 core categories (A–G); Rule 1 — Categories A and E mandatory, plus at least 2 of
  B/C/D; Rule 2 — at least 4 of 7 categories represented; Rule 3 — at least 3 distinct artifacts;
  output is a `.md`+`.html`-only Scope Limitation Notice rendered from
  `assets/scope_limitation_template.html` (reuses `report_template.html`'s header/CSS, 6 sections:
  Executive Summary, Coverage Analysis, Mandatory Failures, Professional Opinion, Recommendation,
  Next Step — smoke-tested). Note: Rule 1 alone already guarantees 4 categories (A + E + 2 of
  B/C/D), so Rule 2's "at least 4" threshold can never independently trigger a halt Rule 1 wouldn't
  have already caught — not a contradiction, just currently non-binding; flagged here in case that's
  not what was intended.
  **Real-world validation, 2026-07-29:** ran on a fresh Claude Code session (no prior context) against
  the actual Pilot-audit-4 evidence (`examples/pilot-audit-4/evidence/`, 1 CSV file). Cold session
  correctly applied all 3 rules, correctly halted, and produced a calibrated `.md` notice (see
  `Public/Fresh Claude test.txt` for the transcript) — confirming the spec is self-sufficient without
  conversation history to lean on. Two issues surfaced by that run, both fixed same day: (1) Category
  B's "what represented means" text mixed in schedule/cost language, which the fresh session read
  literally into its Coverage Analysis table (`Domain: Scope/Schedule/Cost` instead of `Scope`) —
  fixed at the source. (2) No script existed to render the `.html` half of the notice — **built**:
  `scripts/render_scope_limitation.py` parses the `.md` (frontmatter + all 6 sections, including the
  Coverage Analysis table and Mandatory Failures bullets) directly to HTML via
  `assets/scope_limitation_template.html` — no canonical JSON step, matching evidence-sufficiency.md
  (c)'s "no findings data to emit." Verified against the real Pilot-audit-4 notice (7/7 categories,
  4/4 recommendations parsed correctly) and added as regression test 6/6 in `test_pipeline.py`
  (fixture: `scripts/test_scope_limitation_notice.md`). `references/file-naming.md` (Appendix G) now
  documents the `IEMPM_ScopeLimitation_Notice_...` family and `error-codes.md` documents the new
  `E-NOTICE-*` prefix. This item is now fully built, not just specified.
- **UI/UX for non-technical PMs** — parked 2026-07-27, brainstormed only, no decision made. Core
  open question: is the PM the direct operator (needs a real guided UI — stage tracker, structured
  Charter-review screen, plain-English activity feed) or does a technical operator run Claude Code
  on their behalf (current model, UI need is much lighter)? That framing choice has to be resolved
  before any UI technology is picked. See conversation log 2026-07-27 for the fuller options
  analysis (Artifact-based prototype → Agent SDK + local web app → packaged desktop app). Explicitly
  not started — "long test [runway] to go before packaging."

## 6. Working protocol

User writes SKILL.md one section at a time → Claude reviews against: (a) BLUEPRINT-1 consistency, (b) exact per-stage template compliance, (c) no contradiction with sections already written.

SKILL.md is now fully written, so this protocol's remaining scope is the stub appendices in §5 above and the knowledge base gap.

## 7. Roadmap sync (public site — `RoadmapPage.jsx`)

The public portfolio site (`RUAA Consulting/.../src/views/RoadmapPage.jsx`) carries its own copy of
this sprint plan for public display. That copy has drifted from actual repo state in four places
(⚠️ below), mainly because it still assumes the OPM3 bridge exists. This section is the corrected,
authoritative version as of 2026-07-29 — the next time an agent edits `RoadmapPage.jsx`, sync it
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
- Intelligence Engine skill spec complete — Done (now v1.6.0)
- ⚠️ "Core reference docs complete: gap taxonomy, root origins, severity matrix, audit stages" →
  **false for audit-stages.md.** Gap taxonomy, root origins, and severity matrix are complete.
  `references/audit-stages.md` is not: 44 `TODO(you)` markers across 9 of its 11 stages (only
  Stage 0 Baseline and Stage 1 Charter are fully written — Stage 2 onward have `Purpose`/
  `Preconditions`/`Transition` filled but `Inputs`/`Activities`/`Decision Logic`/`Outputs`/
  `Failure Conditions`/`Completion Criteria` are all still stubs). Found 2026-07-29 when a
  `Name`/`description`/`version: 1.0.0` header was added to the file without checking its actual
  completeness first — the version number should not have claimed "done." Does not affect any real
  audit already run: SKILL.md's own reference table marks this file "Human developer" / "you do not
  need to open these" — the operational path Claude actually follows is SKILL.md §5 (Thinking
  Phases), which is complete. This is documentation debt, not an engine defect.
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
  (`registries/ps_scheduling_3rd.json`) — Done. As of 2026-08-02, on-demand derivation from real
  audits has taken this to 6 of 29 standards. Bulk derivation across the other 23 standards —
  Upcoming, strategy noted in §5

**Week 6 (Aug 3–9) — Registry & Renderer — In progress.**
- ⚠️ "Registry complete ('no baseline, no audit') — only skeleton-level derivation exists so far" →
  the *mechanism* is complete; as of 2026-08-02, on-demand derivation from real audits has deep-dived
  6 of 29 standards (see §5's strategy note); full derivation across all 29 remains — In progress,
  not Upcoming
- Deterministic renderer & report template — LLM judges, code renders — Done
- Regression tests across the audit state machine — Done (`test_pipeline.py`, 6/6 passing —
  originally 5/5, committed in `1c68116`; a 6th test for the Scope Limitation Notice renderer added
  `caa158b`)
- Second renderer — `render_scope_limitation.py` (Halt Condition 6's `.md` → `.html`, no canonical
  JSON step) — Done, `caa158b`
- Minimum Evidence Sufficiency gate (Halt Condition 6) — new methodology, not in the original sprint
  plan: raised by real pilot evidence being too thin to support a credible audit even though
  every prior halt condition passed. Modeled on real audit-practice scope limitation / disclaimer
  of opinion. Spec finalized and active — Done, `5061342`
- Terminology Discipline (SKILL.md §6.7, `references/terminology.md`) — controlled PM vocabulary for
  all free-text narrative, cross-mapped across PMI/PRINCE2/ISO 21502 — Done, `059d8f8`

**Week 7 (Aug 10–16) — Pilot & Package — Upcoming.**
- Role-based user guide published for PMs, program managers, and PMO leads — Done
  (`Public/IEM-PM-User-Guide.html`)
- ⚠️ "End-to-end pilot audit against a real baseline" → **Done**, not Upcoming — it ran 2026-07-27,
  three weeks ahead of schedule (see Week 5 above)
- "Fix what the pilot breaks" — Done for the first round (the two `baseline.py` fixes above). A
  second round landed 2026-07-29: a fresh Claude Code session (no prior context) ran a real audit
  attempt against Pilot-audit-4's evidence, correctly triggered the new Minimum Evidence Sufficiency
  gate (Halt Condition 6), and its output surfaced two real gaps — a wording defect in
  `evidence-sufficiency.md`'s Category B definition, and a missing HTML renderer for the Scope
  Limitation Notice — both fixed same day (`caa158b`). This is the mechanism working as intended:
  real cold-session runs keep finding real gaps.
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

## 8. Real production audits (2026-07-27)

Two further audits ran after the first (synthetic-evidence) pilot, this time against **real
organizational data** — ClientOrg Consulting's "Client Rooftop Project - Rhombus 25%" project
(real Excel exports: Cost Tracker, Gate Review, Risk-Issue Log, Task Board). Both went through
full Charter propose→ratify, not a shortcut:

| Audit | Baseline measured against | Findings | Reporting Integrity Score | Charter |
| ------- | ---------------------------- | ---------- | ---------------------------- | --------- |
| `examples/Pilot-audit-2/` (v1.0.0) | ClientOrg's own Sales-PMO-Operations process flow | 6 | 41.0/100 | Ratified |
| `examples/Pilot-audit-3/` | 4 PMI standards (Scheduling, Risk Mgmt, EVM, Governance PG) | 6 | 34.0/100 | Ratified |
| `examples/Pilot-audit-2/` (v2.0.0, 2026-08-02) | 6 PMI standards (adds WBS, full Risk Mgmt Standard, Governance PG, Config Mgmt to Pilot-audit-3's set) | 14 | 21.5/100 (was 0.0 under the pre-fix RIS formula, see intro) | Ratified |

Same underlying evidence, deliberately re-audited against a stricter external baseline instead of
the org's own process — RIS dropped as expected. One real standard document
(`ClientOrg_PMO_Process_AND_GUIDELINES.pdf`) turned out to be scanned screenshots with no text layer;
formally waived out of both Charters rather than guessed at — a real "can't read this" case the
engine had not hit before.

**2026-08-02:** `Pilot-audit-2` was independently re-audited against PMI a second time (v2.0.0
Charter), without the session first checking whether this evidence had already been PMI-audited —
`Pilot-audit-3` already had, at the time this row was added three weeks earlier. The two runs used
different standard subsets (v2.0.0 pulled in two more PMI documents) and produced more than double
the findings (14 vs. 6) against materially the same evidence. Both outputs were kept, per user
decision, rather than reconciled or deleted — understanding why they diverge that much is a real
open item (different registry depth, different judgment calls, or a genuine gap in one run), not
yet investigated. The missing prior-audit check that let this happen is now fixed — see the
`audit-stages.md` entry in §5.

**Real bug found during these runs:** reading `.xlsx` evidence required `openpyxl`, installed ad
hoc mid-session and initially **not** added to `requirements.txt` — caught only when asked directly
"did you make any code changes." Now fixed. Take-away logged in Open Design Items / future work:
requirements.txt updates must land in the same step as any new `import`, and a clean-room
`pip install -r requirements.txt` + `test_pipeline.py` run (or CI) is the actual backstop, not
memory.

## 9. Errors Found & Fixed — Consolidated Log (for write-ups)

**Compiled 2026-08-02 01:13 CDT, updated 01:31, 11:38, 11:49, 12:17 CDT.** Every real defect found in
this project, how it was found, the fix, and its commit — in one place. Distinct from the narrative
in §1/§5/§7/§8 above, which is scattered by topic; this is chronological and exhaustive, kept up to
date going forward.

### A. Engine/process defects — found and fixed

| # | Date/time found | What broke | How it was found | Fix | Commit |
|---|---|---|---|---|---|
| 1 | 2026-07-27 11:34 | `baseline.py` Stage 0 scan didn't recurse into `knowledge/` subfolders — hid every standard in a subdirectory. | First real pilot audit against real PMI standards. | Fixed the scan to recurse. | `ce569ab` |
| 2 | 2026-07-27 12:57 | `baseline.py`'s "reuse if fingerprint unchanged" cache trusted an *empty* skeleton as valid — 27 of 29 real standards silently frozen at zero TOC entries from an earlier failed extraction, never retried. | Stage 0 follow-up audit of the real knowledge base. | Never trust an empty skeleton as cached-valid; always retry until a non-empty skeleton is extracted. Registry-derivation procedure specified (SKILL.md Phase 0b, `registry-format.md`). | `aeef25f` |
| 3 | 2026-07-27 ~14:00 | `openpyxl` (needed to read `.xlsx` evidence) installed ad hoc mid-session, never added to `requirements.txt`. | Only surfaced when directly asked "did you make any code changes." | Added to `requirements.txt`. Take-away: dependency additions must land in the same step as the `import`, not be caught by memory. | `336eb58` |
| 4 | 2026-07-29 16:10–16:45 | No halt condition caught a *readable, ratifiable* evidence set too thin to support a credible audit (a single CSV was about to reach Charter proposal against a 6-standard PMI baseline). | Real Pilot-audit-4 evidence deliberately this thin. | Minimum Evidence Sufficiency Gate (Halt Condition 6) designed and finalized: 7 categories, 3 cumulative rules, Scope Limitation Notice output. | `91205ae`…`5061342` |
| 5 | 2026-07-29 17:16 | Category B's "what represented means" text mixed schedule/cost language into a Scope-only category; the Scope Limitation Notice `.html` renderer didn't exist at all. | Cold, fresh-session (no prior context) real run of Halt Condition 6 against Pilot-audit-4. | Wording fixed at the source; `scripts/render_scope_limitation.py` built and regression-tested. | `caa158b` |
| 6 | 2026-08-01 23:11 | `audit-stages.md` Stage 6's Purpose falsely claimed to compute the Reporting Integrity Score (directly contradicting SKILL.md §9.2/§9.5). The four-part diagnostic (Evidence·Impact·Why/Who/Scope·Fix-at-source) was in the original design but silently absent from the live SKILL.md path. Stage 8/9 headings falsely claimed their scripts didn't exist. Stage 7's Preconditions trusted a bare `SCORED` flag with no verification that Stages 0–6's working memory actually survived intact. Stage 4 had no way to distinguish a legitimate zero-gap clean audit from Stage 3 never having run at all. | Completing `audit-stages.md` end-to-end and cross-checking every claim against the actual SKILL.md/scripts it described, not just filling in template blanks. | RIS-claim corrected; four-part diagnostic restored and mapped to real Finding Block fields; Stage 8/9 corrected; Stage 7 hardened with real chain-verification + new hard-stop `CHAIN_INTEGRITY_LOST`; Stage 4 gained `EVALUATION_UNVERIFIED`. Wired into SKILL.md (§5 pointers) — promoted from excluded to actively-read. `audit-stages.md` → v1.0.0 complete, SKILL.md → v1.9.0. | `54a54d9` |
| 7 | 2026-08-02 00:00–00:15 | `manifest_to_findings.py`: (a) `_parse_standards`/`_parse_scope` split on `,`, shredding any standard title with its own internal comma (several real PMI titles have one) into bogus fragments. (b) `_parse_percentage` accepted a bare number with no `%`, so "27 of 27 declared columns present" was misread as 27% instead of 100%. (c) RIS formula's severity/density deduction caps saturated too easily — a routine 14-finding audit already floored at 0.0, indistinguishable from a catastrophic one. (d) `reports/` output location was ambiguous in prose and the Manifest was actually written to the wrong place (`examples/Pilot-audit-2/reports/` instead of repo-root). (e) No check for whether evidence had already been audited — `Pilot-audit-2` was independently re-audited against PMI without knowing `Pilot-audit-3` already covered the same evidence. (f) Two real evidence-reading mistakes: a Cost Tracker column misread (Total Variance/Remaining Budget values swapped), and Task Board FIND-0010 undercounted affected rows (13 claimed vs. 17 actual) while missing an entire 4th affected subtree entirely. | Live PMI re-run of Pilot-audit-2, then rigorous verification of the output against the real `.xlsx` evidence (checksums, cell-by-cell reads) rather than trusting the Manifest's prose. | (a)/(b) fixed with new regression assertions. (c) Caps widened by user decision, methodology → v1.1.0. (d) `file-naming.md`/SKILL.md §10.6/`audit-stages.md` Stage 1+7 now state repo-root explicitly. (e) New Stage 1 Activity: checksum-match supplied evidence against existing `reports/` Manifests before drafting a new Charter. (f) Two new Stage 3 rules: column-index alignment, exhaustive row counting. `audit-stages.md` → v1.1.0, SKILL.md → v1.9.1. | `e3afc76` |
| 8 | 2026-08-02 ~00:20 | SKILL.md §13.2's Knowledge Base Reading Guide hardcoded a fixed, already-stale folder-name table (`PMBOK/`, `MSP/`, `ISO21502/` never existed; real folders existed but weren't all listed) — any org restructuring `knowledge/` breaks it. | User reorganized `knowledge/PMI/`'s 30 files into `PMI/`+`PMI-AI/`+`PMI-Other/`+`PMI-Sustainability/`, immediately breaking the table. | `baseline.py` now calls `derive_knowledge_index.py`'s scan as part of Stage 0 itself, writing `knowledge_index.json` (actual current folder/category structure, whatever it's named) every run. SKILL.md §13.2/§4.1 now point to that dynamic index; zero hardcoded folder names anywhere in the mechanism. `audit-stages.md` → v1.2.0, SKILL.md → v1.9.2. | `6663688` |
| 9 | 2026-08-02 00:49 | STATUS.md itself had drifted stale in 5+ places (registry-derivation count stuck at "1 of 29" through several real derivations; version numbers; the PMI folder reorg undocumented). | Direct review while answering a registry-derivation question. | All stale references corrected; new rows added throughout. | `2c94a58` |
| 14 | 2026-08-02 ~00:30 | (Was item #10/#11 below, now fixed.) (a) Cross-audit contamination: Stage 1's prior-audit checksum check (fix #7e) was worded loosely enough that a `Pilot-audit-5` Charter-proposal run read *content* from unrelated `Pilot-audit-2/3` evidence and asserted a fabricated vendor-name match ("Rhombus/TD Synnex/Amazon/IDN/RingCentral") as corroboration for the organization's identity — "Rhombus" is actually part of a different project's *name*, not a vendor, and doesn't appear anywhere in Pilot-audit-5's own evidence. (b) The same run's Charter-ratification step asked 3 separate clarifying questions (org name, CR-001 exclusion, candidate-Missing disposition) before reaching the single ratify/edit/"just run it"/decline decision Stage 1's own Decision Logic defines — unspecified friction. | (a) `grep -il "Rhombus\|TD Synnex\|RingCentral\|Amazon\|IDN\|ClientOrg" examples/Pilot-audit-5/*.md` → no output. (b) Full transcript review of the Charter-proposal run. | (a) Stage 1 Activity 2 narrowed to a strict checksum lookup — explicitly forbids opening or reasoning about another audit's content. (b) Stage 1 Activity 7 now requires proposing a default for every ambiguity and flagging it in the Charter text itself, resolved by the single ratification response — no separate question rounds. `audit-stages.md` → v1.3.0. | `e3661ff` |
| 15 | 2026-08-02 ~01:10 | Stage 3 had no systematic self-consistency check — a document could be marked 100% field-coverage while two of its own sections silently disagreed on the same figure, and Synthesis could assert "traces consistently" without that specific claim ever having been verified. This is exactly how findings #12 and #13 below both got past the engine. | Independent review (a "second opinion" audit of the audit) surfaced the same pattern twice across two unrelated evidence sets — a validated recurring miss, not a one-off. | New Stage 3 Activity 3: for every artifact, identify any figure stated more than once and verify the restatements agree; a mismatch is a raw `Untrusted` gap on its own, independent of any registry criterion. New Decision Logic rule ties it to the taxonomy. Stage 7 Activity 5 and SKILL.md §9.3 now require positive Synthesis claims ("traces consistently," "figures match") to be grounded in what Activity 3 actually checked, not asserted as general impression. `audit-stages.md` → v1.3.0, SKILL.md → v1.9.3. | `e3661ff` |
| 17 | 2026-08-02 11:38 | No standing top-level rule stated that only the evidence in the folder being audited is admissible — evidence isolation existed only as a Stage 1 Activity 2 side-effect (fix #14), not a general rule covering every stage. | User directive, generalizing from the #14 incident: "The claude should only analyse based on evidence provided in the folder that its asked to validate. It should not use previous knowledge or similar file reviewed knowledge." | New **Principle 8 — Evidence Isolation** added to SKILL.md §2 (Operating Principles): only this run's own evidence/Charter/`knowledge/` are admissible; the Stage 1 checksum lookup is the one explicit, narrow exception, checksum-only. Stage 1 Activity 2 cross-references it. SKILL.md → v1.9.4, `audit-stages.md` → v1.3.1. | `14f92c8` |
| 18 | 2026-08-02 12:17 | Reports lived in a single shared, repo-root `reports/` folder (hardened as fix #7d/#8) — every project's output mixed together in one flat directory, with real filename-collision risk across projects sharing a UTC minute (already-documented "known limitation" in `file-naming.md`). | User directive ("CRITICAL fix"): reports should be per-project, not shared. Structure specified: `Audit/<Project>/evidence/` (user) + `Audit/<Project>/reports/` (system), a new top-level `Audit/` drop-zone. | Reversed the repo-root convention by design, per explicit approval (3 clarifying questions asked and answered first: `Audit/` is new and separate from `examples/`, not a migration; `evidence/`+`reports/` under `Audit/` are gitignored/local-only, unlike `examples/`'s committed evidence; lowercase folder names, matching existing convention). Implementation: `scripts/paths.py`'s `REPORTS_DIR` constant removed — `manifest_to_findings.py`/`render.py` now default their output next to their own input file (a general "reports/ is a sibling of evidence/" rule, not hardcoded to the literal `Audit/` path, so it also applies uniformly to any future run against `examples/`). New `Audit/README.md` + `.gitignore` entry (`Audit/*` / `!Audit/README.md`). Updated: `file-naming.md` (Appendix G), `SKILL.md` §10.6/§12.2, `audit-stages.md` Stages 1/7/8/9 (11 locations), `Public/IEM-PM-User-Guide.html` (11 locations). New regression test (`test_default_output_location`, now 7/7). No code complexity added — `paths.py` lost a constant; `manifest_to_findings.py`/`render.py` gained one line each (`.resolve().parent`) in place of the removed import. `audit-stages.md` → v1.4.0, SKILL.md → v1.10.0, `file-naming.md` → v1.1.0. | `(this commit)` |
| 16 | 2026-08-02 ~02:15, fixed 11:49 | `AUDIT_MANIFEST_template.md` allowed `**Checksum:** [SHA-256 or "computed"]` — the literal word `"computed"` was a sanctioned placeholder, not a real hash. `Pilot-audit-5`'s report used it for all 11 artifacts, silently defeating fix #14's checksum-lookup mechanism: `Pilot-audit-6` tried to check whether its evidence matched a prior audit and found no real checksum to compare against, even though the two are very likely the same project. | `Pilot-audit-6`'s own Scope Limitation Notice flagged it directly: *"the existing report files record the literal placeholder text `computed`... so no real checksum match against this evidence set was possible."* Confirmed: `grep -n "Checksum" reports/IEMPM_AuditGap_Report_020826_0000.md` → `computed` × 11. | **Two .md-only edits, no code touched:** (1) `assets/AUDIT_MANIFEST_template.md` line 40 — `**Checksum:** [SHA-256 or "computed"]` → now requires a real SHA-256, explicitly forbids the literal word "computed". (2) `references/audit-stages.md` Stage 7 Activity 3 — added the actual computation method (a one-line shell/Python hash command) so the LLM computes a real hash instead of either writing "computed" or, worse, fabricating a plausible-looking fake hash string. `audit-stages.md` → v1.3.2. Deliberately left `manifest_to_findings.py`'s `or "computed"` fallback untouched — changing it to `None` would violate `findings.schema.json`'s `"checksum": {"type": "string"}` constraint, which is exactly the kind of code/schema change this fix was scoped to avoid; the fallback is now a defensive last resort for a well-behaved run, not the expected path. | `d6a06e7` |

### C. Evidence-quality issues found in example data (not tool defects — the pattern that drove fix #15)

Both un-caught by the engine's Stage 3 *at the time they appeared* — the underlying gap (no
systematic self-consistency check) is now fixed by #15 above; these two rows stay as the historical
record of what got missed and why the fix mattered.

| # | Date/time found | Document | The contradiction |
|---|---|---|---|
| 12 | 2026-08-01 ~23:50 | Pilot-audit-2's `Project_Status_Report` (via manual review, not the audit itself) | Cost Status table's own "Total" row ($241,400) omits the Contingency Reserve line entirely — doesn't reconcile against the Charter/PMP's approved $265,540 baseline. |
| 13 | 2026-08-02 ~01:10 | Pilot-audit-5's `07_Cost_Baseline` | §1's summary table shows CA-05 (Contingency) as $8,320; §4's own detailed breakdown of "Contingency Reserve (CA-05)" totals $24,140 by itself, itemized five ways. Both can't be right. |

### Open items summary (as of this log)

- **All defect-log items closed as of this update** (#10 through #17) — see table A. Nothing remains
  in "found, not yet fixed." Evidence Isolation is now a standing Principle (#17, SKILL.md §2
  Principle 8), not just a Stage 1 side-effect; the checksum-placeholder gap (#16) that undercut it
  is also closed.
- Registry derivation: **7 of 29** PMI standards now deep-dived (`requirementsmgmt_pg.json` added this
  session), all on-demand from real audits, none pre-batched. 22 remain — see §5's strategy note.
- SKILL.md conciseness pass (<500-line guidance), bulk registry derivation, `.claude-plugin/` packaging,
  CI — all still open, unchanged by this session's work. See §5.
- Not yet re-run: no audit has exercised fix #15 (the self-consistency check), fix #17 (Principle 8),
  or fix #18 (the new `Audit/` structure) live yet — first real test is the next audit run.
- **Noted, deliberately not fixed as part of #18** (out of scope, flagged for transparency):
  `Public/IEM-PM-User-Guide.html`'s workflow section already used simplified filenames
  (`audit_manifest.md`, `report.html`) that predate the real Appendix G naming convention every
  actual audit uses (`IEMPM_AuditGap_Report_DDMMYY_HHMM.<ext>`). Fix #18 corrected the *folder*
  references throughout that section but left this separate, pre-existing naming inconsistency
  alone rather than expanding scope.

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
| done   | Created LICENSE (MIT), root README.md, and requirements.txt (packaging prerequisites).                                                | STATUS.md             |
| done   | Defined and embedded output file naming (Appendix G) and error codes (Appendix H) into the actual scripts, not just docs.             | STATUS.md             |
| done   | Ran two further real production audits against real (non-synthetic) organizational data, both fully Charter-ratified — one org-baseline, one PMI-baseline. See §8. | STATUS.md             |
| done   | Found and fixed a real dependency gap (openpyxl missing from requirements.txt) surfaced by the real-data audits.                       | STATUS.md             |
| done   | Consolidated path resolution across all 5 scripts into a single source of truth (scripts/paths.py) — fixed a real duplicated/inconsistent `parents[3]` pattern in manifest_to_findings.py and render.py. | STATUS.md             |
| done   | Moved SKILL.md's Manifest format (§10.2) verbatim into assets/AUDIT_MANIFEST_template.md; §10.2 is now a pointer. Deleted the now-redundant references/manifest-template.md stub.       | STATUS.md             |
| done   | Archived references/confidence-scale.md (unreferenced anywhere in SKILL.md) to _archive/; wired references/severity-matrix.md into SKILL.md §9.1 as a calibration-reference pointer.     | STATUS.md             |
| done   | Reviewed SKILL.md against Anthropic's official skill-authoring best practices; moved §4.2's Charter spec verbatim into references/charter-spec.md; added Tables of Contents to the three reference/asset files over the 100-line threshold (severity-matrix.md, audit-stages.md, AUDIT_MANIFEST_template.md). SKILL.md body: 1,071 → 968 lines. | STATUS.md             |
| done   | Branched §11 Report Generation out to references/report-generation.md; found and fixed a real gap where the move had left no pointer behind in SKILL.md at all; reordered the Example Finding Block into its correct place in AUDIT_MANIFEST_template.md and added it to that file's TOC. SKILL.md body: 968 → 864 lines. | STATUS.md             |
| done   | Linked SKILL.md's main Table of Contents; added Name/description/version headers to every references/*.md file (charter-spec, error-codes, file-naming, registry-format, report-generation, severity-matrix, audit-stages); added the two still-missing sub-TOCs (charter-spec.md, report-generation.md, both >100 lines). | STATUS.md             |
| done   | Completed and committed `references/audit-stages.md` (v1.1.0, all 11 stages, zero `TODO(you)`) and wired it into SKILL.md v1.9.1 as actively-read, not excluded documentation. | STATUS.md |
| done   | Found and fixed two real parsing bugs in `manifest_to_findings.py` on a live PMI re-run of Pilot-audit-2: comma-splitting corrupting multi-comma standard titles, and Field Coverage prose misread as a raw-count percentage. Added regression coverage for both (still 6/6). | STATUS.md |
| done   | Widened the Reporting Integrity Score formula's severity/density deduction caps (v1.0.0 → v1.1.0) — the prior caps saturated at 0.0 for any moderately-thorough audit, losing the ability to distinguish "flawed" from "catastrophic." | STATUS.md |
| done   | Fixed an ambiguous `reports/` output-location convention that had caused a real misplaced-file mistake; now explicit (repo-root only) in `file-naming.md`, `SKILL.md` §10.6, and `audit-stages.md` Stage 1/7. | STATUS.md |
| done   | Added a Stage 1 checksum-based check for a prior audit of the same evidence, and two Stage 3 evidence-reading rules (column-index alignment; exhaustive row counting) — both prompted by real mistakes caught on the same live run. | STATUS.md |
| next   | Reconcile why `Pilot-audit-3` and `Pilot-audit-2` (v2.0.0)'s independent PMI-scoped audits of the same evidence produced 6 vs. 14 findings — not yet investigated. | STATUS.md |
| done   | Reorganized `knowledge/PMI/` into `PMI/`+`PMI-AI/`+`PMI-Other/`+`PMI-Sustainability/`; replaced SKILL.md's hardcoded, already-stale `knowledge/` folder-name table with a dynamically-generated `knowledge_index.json` (now built by `baseline.py` as part of Stage 0) so no folder name is ever assumed to exist. | STATUS.md |
| next   | User to add further pilot runs. | STATUS.md |
| next   | Further SKILL.md conciseness edit (§2/§5/§6/§9 — core, per-invocation content) to bring the body closer to Anthropic's <500-line guidance — separate, slower pass; may not land exactly under 500 without cutting real operational guidance. | STATUS.md             |
| next   | Run bulk Stage 0 criteria-derivation across the remaining 23 real standards (6 of 29 now deep-dived, all on-demand — see §5 strategy note).                             | STATUS.md             |
| next   | Package as Claude Code skill (.claude-plugin/plugin.json, marketplace.json) — prerequisites (LICENSE/README/requirements.txt) done. Verify the `allowed-tools:` frontmatter field against Claude Code's own skill-packaging docs when this starts. | STATUS.md             |
| next   | Add CI (GitHub Actions) running test_pipeline.py + a clean-room requirements.txt install on every push.                                | STATUS.md             |
| open   | UI/UX for non-technical PMs — parked, brainstormed only, no decision. See §5 Open design items.                                        | STATUS.md             |

# 6-Week Plan

| Week   | Focus            | Deliverable                                                                                                          | Status |
| ------ | ---------------- | ---------------------------------------------------------------------------------------------------------------------- | ------ |
| Week 1 | PMO Data Charter | Draft the PMO Data Charter template with sections for data meaning, scope, materiality, and human ratification.      | done   |
| Week 2 | Findings Schema  | Define findings.schema.json with fields for gap type, root origin, evidence, and severity.                           | done   |
| Week 3 | Validator        | Build schema.py to validate findings JSON against the schema and closed taxonomies.                                  | done   |
| Week 4 | Audit Manifest   | Create the Audit Manifest template that converts LLM analysis into a parser-friendly structure.                      | done   |
| Week 5 | SKILL.md         | Write the skill sections and lock the core logic, inputs, and stage flow.                                            | done   |
| Week 6 | Reports + Tests  | Build the renderer, report template, and regression tests; package the skill.                                        | in progress — renderer, report template, regression tests, and packaging prerequisites (LICENSE/README/requirements.txt) done; the actual .claude-plugin package remains |

# mapping of the five Claude Certified Architect Foundations domains to your IEM-PM modules.

| CCA-F domain                       | What it teaches                                                          | IEM-PM module it supports                                                                            |
| ------------------------------------ | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Agentic architecture               | Designing multi-step AI systems that plan, reason, and act across tasks  | Core IEM-PM orchestration: baseline → evidence → gap finding → classification → root cause → report |
| Tool use and integrations          | Connecting the model to external systems safely and reliably            | Evidence collection from standards, project data, PM tools, file systems, and local repositories     |
| Claude Code workflows              | Building and operating AI inside a code-first development environment   | Your IEM-PM Claude Code skill packaging, repo structure, stage machine, and build order              |
| Structured outputs and prompts     | Getting consistent JSON, schemas, and controlled LLM responses          | Audit Manifest, Findings JSON, schema validation, and report generation                              |
| Reliability and context management | Keeping the system stable, grounded, and able to work with long inputs  | Standards ingestion, knowledge base derivation, closed taxonomies, and evidence-first reasoning      |
