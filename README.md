# IEM-PM

**Intelligence Engineering Methodology for Project, Program, Portfolio & PMO** — an open-source
reference implementation of **Project Gap Intelligence Engineering**.

## What "Intelligence Engineering" means

"Intelligence" here isn't a claim about artificial intelligence — it's used the way "business
intelligence" is: evidence-based organizational insight (visibility, integrity, connectivity,
governance, predictability, decision quality) built from your own delivery data. The engine that
produces it is LLM-native — Claude does the actual reading and judgment, constrained to reason only
from the real standards and evidence you provide, never from memory or assumption — while a
separate, deterministic layer only validates and renders, never judges. "Engineering" means this is
systematic and repeatable, not one-off consulting: the same closed 7-gap/7-root-origin taxonomy,
every audit. And it isn't tied to one PM methodology — IEM-PM audits against whichever real
standard your organization actually declares (PMI/PMBOK, PRINCE2, ISO 21502, or your own internal
methodology), never a generic one it assumes.

## The objective

> Does the organization's delivery data match what its standards require — and where it doesn't, why?

IEM-PM exists to answer that one question with evidence, not opinion — then trace every gap to its
root origin so the correction happens at the source, not just in a report.

## Discipline

Project Gap Intelligence Engineering

## Definition

The systematic practice of measuring delivery data gaps across project, program, portfolio, and
PMO systems, tracing discrepancies to their root origins, and engineering corrections at the
source.

## Problem Statement

Organizations suffer from compromised strategic decision-making and hidden project failures due to
delivery data that is missing, ignored, disconnected, untrusted, underutilized, misclassified, or
divergent across PMO systems.

## Manifesto

We relentlessly measure missing, ignored, disconnected, untrusted, underutilized, misclassified,
and divergent data, and trace it to its root origin — what looks like a delivery problem is often
an intelligence-integrity problem.

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
3. **Drop your evidence.** Create `Audit/<ProjectName>/evidence/` and put your delivery
   artifacts in it.
4. **Run this as a Claude Code skill.** Open the repository in Claude Code and point it at
   `skills/intelligence-engine/SKILL.md` — it walks the 11-stage audit state machine (Baseline →
   Charter → Define → Measure → Classify → Trace → Score → Synthesize → JSON → Render → Summary).

   To make it available in every project instead of just this repo, copy or symlink
   `skills/intelligence-engine/` to `~/.claude/skills/intelligence-engine/` — it carries its own
   `.claude-plugin/plugin.json`, so Claude Code loads it as the `iem-pm` plugin (invoke directly
   with `/iem-pm:intelligence-engine`) without copying it into a versioned cache. `knowledge/` and
   `registries/` stay wherever you put the folder, so nothing is at risk on a future update.
5. **Read the results.** Reports land in `Audit/<ProjectName>/reports/` (local-only,
   gitignored) — a sibling of `evidence/`: a Markdown Audit Manifest, canonical findings JSON,
   and HTML/TXT reports.

Not a developer? See the [role-based user guide](Public/IEM-PM-User-Guide.html) for PMs, program
managers, and PMO leads — no code required to read or act on an audit.

No worked example ships in this repository yet — real pilot audits have been run against real PMI
standards during development, but their evidence and output are gitignored (`Audit/`), same as any
real engagement's, and not published here. Building a sanitized worked example is a known open
item, tracked in `STATUS.md`.

## Repository structure

- `skills/intelligence-engine/` — the runnable skill: `SKILL.md` (the state machine), `scripts/`
  (the deterministic Python pipeline), `assets/` (templates), `references/` (appendices).
- `skills/intelligence-engine/knowledge/` — your baseline drop-zone. Gitignored, local-only.
- `skills/intelligence-engine/registries/` — criteria derived at runtime from your standards.
  Gitignored, local-only.
- `Public/` — human-facing documentation (this README's companion guide, an audit playbook).
- `Audit/` — your own audit projects: evidence in, reports out. Gitignored, local-only.
- `_archive/`, `stakeholder/` — superseded material and PMI volunteer copyrighted material.
  History only; never built on, never published from.

## License

[MIT](LICENSE) for the framework code and documentation in this repository. This does **not**
cover any standards you place in `knowledge/` (those remain your organization's own licensed
content) or the contents of `stakeholder/` (PMI volunteer material, reference-only, never
redistributed).
