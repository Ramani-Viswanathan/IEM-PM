# IEM-PM — Intelligence Engineering for Project, Program, Portfolio and PMO

## Reverse-Engineered Build Blueprint

> Purpose: document **how IEM-PM should be built**, using the proven architectural pattern adapted for Project Management Intelligence.
>
> IEM-PM is the reference implementation of **Intelligence Engineering for Project Management**—an LLM-native audit engine that measures an organization's actual project delivery capability against its declared project management standards and produces evidence-based maturity assessments.

---

# 0. The one-sentence shape

IEM-PM is a **Claude Code skill** that compares an organization's **delivery evidence** (projects, programs, portfolios, PMO artifacts, schedules, RAID logs, governance packs, dashboards, boards and operational data) against the **project management standards** it claims to follow (PMI, PMBOK, OPM3 or organizational methodology), and produces a **PMO Data Gap Audit Report** (HTML + JSON + TXT) that classifies every delivery gap into one of **7 intelligence gap types**, traces each gap back to its **root origin**, and uses that evidence to expose the organization's **Project Management Intelligence Maturity** based on PMI's OPM3 model.

> **No baseline, no audit.
> Find the gap.
> Trace it to the root.
> Measure maturity from evidence.**

Everything else is plumbing around that comparison.

---

# 1. Repository Topology

```
iem-pm/
│
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
│
├── IEM_PM_SPEC.md
├── README.md
├── PMO_DATA_CHARTER_template.md
├── STABILITY.md
├── CONTRIBUTING.md
├── LICENSE
├── CHANGELOG.md
├── build.sh
│
├── skills/
│   └── intelligence-engine/
│       ├── SKILL.md
│       │
│       ├── knowledge/ (Gitignore — empty drop-zone; the org supplies its own standards)
│       │
│       │   ├── PMI/
│       │   ├── PMBOK/
│       │   ├── OPM3/
│       │   ├── PRINCE2/
│       │   ├── Agile/
│       │   ├── MSP/
│       │   ├── ISO21502/
│       │   └── Organizational/
│       │
│       ├── registries/ (Gitignore — derived at runtime from the org's standards, never shipped)
│       │
│       │   ├── pmi_registry.json
│       │   ├── opm3_registry.json
│       │   ├── governance_registry.json
│       │   └── maturity_registry.json
│       │
│       ├── manifest_to_findings.py
│       ├── render.py
│       ├── schema.py
│       ├── findings.schema.json
│       └── report_template.html
│
├── docs/
├── examples/
├── tests/
├── reports/
└── assets/
```

---

# 2. The Governing Question (the spine)

Every audit reduces to one question.

> **Does the organization's delivery data match what its standards require — and where it doesn't, why?**

Everything exists to answer that question.

---

## Declared Intent

The organization declares:

- Governance
- Methodology
- Standards
- PMO Operating Model
- Templates
- Stage Gates
- Portfolio Framework
- Risk Processes
- Reporting Requirements

This becomes the

**Delivery Baseline**

(The **PMO Data Charter** is a separate input — it interprets the data; it is **not** part of the baseline.)

---

## Observed Reality

The engine reads

- Project plans

- RAID Logs

- Schedules

- Steering packs

- Portfolio dashboards

- PMO exports

- Jira

- Azure DevOps

- Primavera

- Microsoft Project

- Financial reports

- Lessons learned

- Status reports

- Governance records

This becomes

**Observed Delivery**

---

## Comparison

```
Expected Delivery

        vs

Observed Delivery
```

Everything after this is simply evidence collection.

---

# 3. Core Architecture

```
              LLM

      Reads Everything

             │

             ▼

     Understands Delivery

             │

             ▼

     Writes Audit Manifest

             │

             ▼

────────────────────────────────────

      Deterministic Python

             │

             ▼

        JSON Findings

             │

             ▼

     HTML Report

             │

             ▼

      TXT Report

             │

             ▼

     Executive Dashboard
```

The AI performs judgment.

Software performs rendering.

---

# 4. Design Principles

## 0. Data-contract-first

No ratified Charter.

No comparison.

Never guess what the data means.

---

## 1. Baseline First

No baseline.

No audit.

The engine cannot determine maturity without knowing the standard.

---

## 2. Evidence First

Every finding must point to evidence.

Every gap must reference

- a document

- a registry item

- a governance rule

- or the absence of one.

---

## 3. Copyright Safe

Never reproduce PMI standards.

Only reference

- clause

- identifier

- summary

- citation

---

## 4. Read Only

The engine never modifies delivery data.

It only writes

```
reports/
```

---

## 5. Separation

IEM-PM is not part of the PMO.

It independently evaluates the PMO.

---

## 6. Local First

Runs locally.

No cloud dependency.

No database required.

Git repository only.

---

## 7. Intelligence Native

The intelligence lives inside

SKILL.md

Knowledge Base

Registries

not inside Python.

Python only validates and renders.

---

# 5. Inputs

The engine consumes

## Charter declaration

Artifact declaration

Field semantics map

Materiality / scope

Machine-proposed → human-ratified.

Artifacts and field semantics are proposed **from the data**; scope is proposed **from the standards** (anti-mirror guard) — any absence surfaces as a candidate _Missing_ gap, never as "out of scope."

## Organizational Standards

PMI

PMBOK

OPM3

Internal Methodology

Governance Manuals

Policies

---

## Delivery Artifacts

Projects

Programs

Portfolios

PMO

---

## Operational Evidence

Boards

Reports

Schedules

Risk Registers

Financials

Logs

Templates

---

# 6. The Seven Gap Taxonomy

Every finding belongs to exactly one category.

| Gap           | Meaning                                 |
| ------------- | --------------------------------------- |
| Missing       | Required information absent             |
| Ignored       | Standard exists but not followed        |
| Disconnected  | Information exists but is isolated      |
| Untrusted     | Evidence cannot be verified             |
| Underutilized | Data collected but unused               |
| Misclassified | Wrong classification or taxonomy        |
| Divergent     | Delivery differs from required standard |

No overlap.

No duplicates.

---

# 7. Root Origin Taxonomy

Every gap must trace back to exactly one of seven origins.

- Capture

- Integration

- Definition / Taxonomy

- Ownership

- Process / Cadence

- Tooling

- Behavior

A closed list — so the validator can enforce it.

The report fixes causes, not symptoms.

---

# 8. Intelligence Loop

The intelligence engine operates as one repeating loop.

```
Define Baseline

↓
charter

↓

Collect Evidence

↓

Measure

↓

Find Gap

↓

Classify Gap

↓

Trace Root Cause

↓

Score Impact

↓

Synthesize Manifest

↓

Repeat
```

---

# 9. Project Management Intelligence Model

Instead of simply measuring compliance,

IEM-PM measures intelligence.

Intelligence is composed of

```
Visibility

+

Integrity

+

Connectivity

+

Governance

+

Predictability

+

Decision Quality

+

Continuous Improvement
```

These are **narrative diagnostic labels only** — they are never scored or weighted. Scoring lives in the Reporting Integrity Score and the OPM3 bridge.

---

# 10. Maturity Model

Evidence determines maturity.

Not interviews.

Not surveys.

Not opinions.

```
Evidence

↓

Gap Density

↓

Gap Severity

↓

Root Causes

↓

Weighted Score

↓

OPM3 Maturity Position (via the bridge — TBD)
```

IEM-PM does not invent a maturity scale. The gap profile maps to **PMI's OPM3 model** — the bridge rubric is the open design item.

---

# 11. The Five Contracts

IEM-PM is built around immutable contracts — because PMO data is not self-describing.

## Contract 1

PMI Standards

Defines

Expected Delivery

---

## Contract 2

PMO Data Charter

Defines

What the data **is**, what its fields **mean**, and what **matters**.

Machine-proposed. Human-ratified.

---

## Contract 3

Audit Manifest

LLM output.

Human readable.

Parser friendly.

---

## Contract 4

Canonical Findings JSON

Machine readable.

Single source of truth.

---

## Contract 5

Schema Validator

Guarantees

Every report is internally consistent.

---

# 12. Deterministic Pipeline

```
PMO Data

↓

LLM Analysis

↓

Audit Manifest

↓

Validator

↓

Canonical JSON

↓

Renderer

↓

HTML

TXT

JSON

Dashboard
```

The report is reproducible.

Only the analysis changes.

---

# 13. Knowledge Base

The Knowledge Base contains understanding.

It never contains executable rules.

Baseline: scan standards/ → build/refresh registry

Examples of what the org may drop in

PMBOK

OPM3

Portfolio Management

Program Management

Risk Management

Governance

Scheduling

Benefits Management

Stakeholder Management

Agile

Hybrid

Organizational Standards

Each document calibrates the LLM.

None contain detection code.

---

# 14. Registry

Unlike the Knowledge Base,

the Registry is structured.

Each registry item defines

Identifier

Name

Description

Evidence Required

Gap Type

Root Cause Mapping

OPM3 Mapping (bridge — TBD)

Reference

This allows deterministic scoring.

The Registry is **derived at runtime** from the org's standards (Step 0). Local only. Never shipped. Never committed.

---

# 15. Report Sections

The generated report contains

1 Executive Summary

2 Audit Scope

3 Delivery Baseline

4 Delivery Evidence

5 Gap Register

6 Root Cause Analysis

7 Intelligence Indicators (narrative) + Reporting Integrity Score

8 Maturity Assessment (OPM3 position)

9 Recommended Actions

10 Roadmap

11 Appendix

---

# 16. Engineering Philosophy

The LLM performs

Thinking

Reasoning

Classification

Judgment

Root Cause Analysis

Everything deterministic is delegated to software.

Software performs

Validation

Consistency

Scoring

Rendering

Formatting

Packaging

The separation is absolute.

---

# 17. The Build Order

Build in this order.

1.  Define the PMO Data Charter.

2.  Define the Findings Schema.

3.  Build the Validator.

4.  Build the Audit Manifest.

5.  Write SKILL.md.

6.  Build the Knowledge Base derivation (scan, not authoring).

7.  Build the Registry derivation (generated from the org's standards, not authored).

8.  Create the Renderer.

9.  Create the Report Template.

10. Build Regression Tests.

11. Package as Claude Code Skill.

---

# 18. The Intelligence Engineering Formula

Everything inside IEM-PM reduces to one equation.

```
Expected Delivery

−

Observed Delivery

=

Gap

Gap

+

Evidence

=

Finding

Finding

+

Root Cause

=

Intelligence

Intelligence

+

Weighted Scoring

=

Organizational Maturity via OPM3 maturity position
```

---

# 19. The Vision

IEM-PM is not another PMO reporting tool.

It is an **Intelligence Engineering platform** that transforms fragmented delivery data into evidence-based organizational intelligence.

Its purpose is not to report projects.

Its purpose is to explain **why projects perform the way they do**, identify the systemic causes of delivery gaps, and provide a repeatable, evidence-driven path toward higher organizational maturity.

IEM-PM entire architecture is governed by a single, relentless comparison:

> **Does observed delivery match declared standards?**

If the answer is no, IEM-PM finds the gap, traces it to its root, measures its impact, and converts that evidence into actionable intelligence.
