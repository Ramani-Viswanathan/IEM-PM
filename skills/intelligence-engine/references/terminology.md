---
Name: PMO Terminology Discipline
description: >
  Cross-cutting rule (SKILL.md §6.7) — the controlled vocabulary IEM-PM writes in whenever it
  produces free-text prose: Executive Summary, Professional Opinion, Recommended Action, evidence
  narrative, Synthesis. Read before writing any narrative content in a Manifest, Report, or Scope
  Limitation Notice.
version: 1.0.1
---

## Contents

- [(a) Why this exists](#a-why-this-exists)
- [(b) The rule](#b-the-rule)
- [(c) Core vocabulary](#c-core-vocabulary)
- [(d) Cross-standard terminology](#d-cross-standard-terminology)
- [(e) What to avoid](#e-what-to-avoid)
- [(f) Where this applies](#f-where-this-applies)

## (a) Why this exists

The seven gap types (§7) and seven root origins (§8) are closed enums — the validator rejects
anything that isn't an exact match, so there's no drift possible there. Free-text prose has no such
structural constraint. Left unconstrained, it drifts toward generic business language, synonyms, or
whatever a specific evidence artifact happened to call something — not the vocabulary a PM, PgM, or
PMO lead actually expects from a professional audit output. This file is that constraint, for prose.

## (b) The rule

Use the term the standard being cited actually uses for a concept. Never substitute a synonym, an
undefined abbreviation, generic business-speak, or a vendor/tool's term for a standard concept. If
the audit is scoped to a declared standard (Charter §4.2), that standard's own terminology governs
the entire Manifest — do not mix in another standard's term for the same concept partway through.

## (c) Core vocabulary

Universal PM concepts, and the term each major standard uses for it. Cite in whichever column
matches the audit's declared standard; default to the PMI column when auditing against an
organizational methodology that doesn't define its own term.

| Concept                       | PMI / PMBOK                 | PRINCE2                          | ISO 21502            |
| ------------------------------ | ---------------------------- | ---------------------------------- | ---------------------- |
| Formal authorization document | Project Charter               | Project Initiation Documentation   | Project mandate       |
| Governance/sponsoring body     | Sponsor / Steering Committee | Project Board                      | Governing body        |
| Scope baseline                 | Scope Baseline / WBS         | Product Description / PBS          | Project scope         |
| Cost baseline                  | Cost Baseline                | Business Case (financial case)     | Budget                |
| Schedule baseline               | Schedule Baseline            | Stage Plan / Project Plan          | Schedule               |
| Risk artifact                  | Risk Register                 | Risk Register                      | Risk register          |
| Change control record          | Change Log / Change Request  | Issue and Change Control           | Change control record |
| Performance report              | Status Report / Performance Report | Highlight Report / End Stage Report | Progress report        |
| Lessons record                 | Lessons Learned Register     | Lessons Log                        | Lessons learned        |

## (d) Cross-standard terminology

When the declared standard is not PMI, that standard's own term wins for the whole audit — not a
blend. The (c) table exists to look up the right term quickly, not to justify mixing vocabularies
because one sounds clearer than another.

## (e) What to avoid

- Vague business-speak in place of a defined term (e.g. "a plan for what could go wrong" instead of
  "risk register").
- Vendor or tool jargon presented as PM vocabulary (Jira "Epic", "Sprint" outside an Agile-standard
  audit, "Work Item").
- Inventing new terminology for a concept a standard already names.
- Switching terms for the same concept mid-Manifest — if evidence genuinely uses two different
  artifact types (a RAID log and a separate risk register), name both explicitly; don't alternate
  labels for what is actually one artifact.
- Colloquial severity language in place of the defined 1–5 scale (`scoring.md` §9.1) — state the
  severity number and its rationale, not "this is a huge problem."

## (f) Where this applies

**Applies to:** Executive Summary, Professional Opinion (Scope Limitation Notice), Recommendation /
Recommended Action, evidence descriptions, Synthesis (Intelligence Indicators narrative).

**Does not apply to:** the closed taxonomies (§7/§8 — already enum-enforced), standard citation
blocks (§6.4 — clause/identifier must match the standard exactly, not be translated), artifact IDs
and file paths (must match the evidence verbatim).
