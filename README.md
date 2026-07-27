# IEM-PM

**Intelligence Engineering Methodology for Project, Program, Portfolio & PMO** — an open-source
reference implementation of **Project Gap Intelligence Engineering**.

## The problem

Organizations suffer from compromised strategic decision-making and hidden project failures
because delivery data is missing, ignored, disconnected, untrusted, underutilized, misclassified,
or divergent across PMO systems. What looks like a delivery problem is often an
intelligence-integrity problem.

## What IEM-PM does

IEM-PM audits imported project/PMO artifacts (schedules, RAID logs, governance packs, status
reports) against the **real standards your organization holds** — PMI's PMBOK, Practice
Standards, Risk Management, Governance guides, or your own internal methodology. It finds gaps,
classifies each into one of **7 gap types** (Missing · Ignored · Disconnected · Untrusted ·
Underutilized · Misclassified · Divergent), traces each to one of **7 root origins** (Capture ·
Integration · Definition/Taxonomy · Ownership · Process/Cadence · Tooling · Behavior), cites the
exact clause it's measured against, and scores the result as a deterministic **Reporting
Integrity Score (0–100)**.

**IEM-PM measures and traces gaps. It does not model organizational maturity** (e.g., PMI's
OPM3) — that's a distinct discipline requiring cross-project calibration and a licensed
instrument, neither of which this tool provides.

## The cornerstone rule: no baseline, no audit

This repository ships **zero standard text**. IEM-PM validates against the real standards *you*
place in `skills/intelligence-engine/knowledge/` — PMI publications, ISO, PRINCE2, or your own
internal methodology. If that folder is empty, the engine stops and asks for a baseline. It never
audits from assumption or model memory.

## Architecture

- **LLM judges, code renders.** Claude reads your standards and evidence, classifies gaps, traces
  root origins, and writes a structured Audit Manifest. Python only validates, scores, and
  renders — it never judges.
- **Five Contracts:** Standards (baseline) → PMO Data Charter (what the data means) → Audit
  Manifest (the LLM↔code boundary) → Canonical Findings JSON → Schema Validator.
- **Copyright-safe by construction:** every citation is clause + short paraphrase + citation
  anchor — standard text is never reproduced, and nothing standard-derived is ever committed
  (`knowledge/` and `registries/` are gitignored).

See [`IEM-PM BLUEPRINT-1.md`](IEM-PM%20BLUEPRINT-1.md) for the full 19-section design and
[`STATUS.md`](STATUS.md) for exactly what's built vs. pending right now.

## Quickstart

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
2. **Provide a baseline.** Drop your organization's real standards (PDF or Markdown) into
   `skills/intelligence-engine/knowledge/`. Nothing runs without this.
3. **Run this as a Claude Code skill.** Open the repository in Claude Code and point it at
   `skills/intelligence-engine/SKILL.md` — it walks the 11-stage audit state machine (Baseline →
   Charter → Define → Measure → Classify → Trace → Score → Synthesize → JSON → Render → Summary).
4. **Read the results.** Reports land in `reports/` (local-only, gitignored): a Markdown Audit
   Manifest, canonical findings JSON, and HTML/TXT reports.

Not a developer? See the [role-based user guide](Public/IEM-PM-User-Guide.html) for PMs, program
managers, and PMO leads — no code required to read or act on an audit.

A full worked example — a real pilot audit run against 29 real PMI standards, with planted gaps
and cited findings — lives in [`examples/pilot-audit/`](examples/pilot-audit/).

## Repository structure

- `skills/intelligence-engine/` — the runnable skill: `SKILL.md` (the state machine), `scripts/`
  (the deterministic Python pipeline), `assets/` (templates), `references/` (appendices).
- `skills/intelligence-engine/knowledge/` — your baseline drop-zone. Gitignored, local-only.
- `skills/intelligence-engine/registries/` — criteria derived at runtime from your standards.
  Gitignored, local-only.
- `Public/` — human-facing documentation (this README's companion guide, an audit playbook).
- `examples/` — a full worked pilot audit, evidence included.
- `_archive/`, `stakeholder/` — superseded material and PMI volunteer copyrighted material.
  History only; never built on, never published from.

## License

[MIT](LICENSE) for the framework code and documentation in this repository. This does **not**
cover any standards you place in `knowledge/` (those remain your organization's own licensed
content) or the contents of `stakeholder/` (PMI volunteer material, reference-only, never
redistributed).
