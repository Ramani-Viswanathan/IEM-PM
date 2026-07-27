# IEM-PM — Intelligence Engineering Methodology for Project, Program, Portfolio & PMO

A very simple and powerful open-source reference implementation of **Project Gap Intelligence
Engineering**, delivered as the **IEM-PM** framework.

- **Discipline (the practice):** Project Gap Intelligence Engineering.
- **Framework brand (the implementation):** IEM-PM.

## Definition

The systematic practice of measuring delivery data gaps across project, program, portfolio, and PMO systems, tracing discrepancies to their root origins, and engineering corrections at the source.

## Problem Statement

Organizations suffer from compromised strategic decision-making and hidden project failures due to delivery data that is missing, ignored, disconnected, untrusted, underutilized, misclassified, or divergent across PMO systems.

## Manifesto

We relentlessly measure missing, ignored, disconnected, untrusted, underutilized, misclassified, and divergent data, and trace it to its root origin — what looks like a delivery problem is often an intelligence-integrity problem.

## How it works (cornerstone)

**No baseline, no audit.** IEM-PM validates imported project/PMO artifacts against the **real
standards the org places in `skills/intelligence-engine/knowledge/`** (PMI is primary — PMBOK 8,
Portfolio 4e, EVM, Risk, etc. — plus any org standard). It ships **no bundled standard text**; if the
folder is empty it stops and asks for a baseline. At runtime it scans the standards, derives local
**registries** (paraphrased checkable criteria + stable citation anchors, never verbatim; gitignored),
then each failed criterion becomes a finding classified into one of the **7 gaps**, traced to one of
**7 root origins**, cited to the held document, and scored for **Reporting Integrity**. IEM-PM
measures and traces gaps; it does not model organizational maturity (e.g., PMI's OPM3) — that is a
distinct discipline requiring cross-project calibration and a licensed instrument, neither of which
this tool provides. Scrapped 2026-07-27, not deferred.

## Canonical documents (read in this order)

1. `STATUS.md` — **start here**: locked decisions, build-order position, next actions.
2. `IEM-PM BLUEPRINT-1.md` — **THE approved blueprint** (19 sections).
3. `PRAXEN-BLUEPRINT.md` — reference: how the model project (Praxen) is built.

## Structure

- `skills/intelligence-engine/` — the runnable Claude Code skill (the framework, v1 in progress).
  - `SKILL.md` — the 11-stage state machine (Baseline → Charter → … → Render); template being
    filled section-by-section (user writes `TODO(you)` sections, Claude reviews).
  - `knowledge/` — **the mandatory baseline drop-zone** (cornerstone; local-only, gitignored).
  - `registries/` — derived at runtime from the org's standards (local-only, gitignored).
- `_archive/` — superseded material (old `pmo-data-gap-audit` skill, old blueprint, remit). History only.
- `stakeholder/` — PMI volunteer copyrighted material. **Never touch, never publish, never build on.**
