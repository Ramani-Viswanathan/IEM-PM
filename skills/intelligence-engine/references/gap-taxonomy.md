---
Name: Gap Taxonomy
description: >  
The Seven Gap Taxonomy — full definitions, detection logic, examples, and disambiguation rules for classifying PMO delivery gaps. Read during Stage 4 (Classify) before assigning any gap type.
version: 1.0.0
---

## Contents

- [Master Disambiguation Example] (##Master Disambiguation Example — The Risk Register)
- [1 Missing](#1-Missing)
- [2 Ignored](#2-ignored)
- [3 Disconnected](#3-disconnected)
- [4 Untrusted](#4-untrusted)
- [5 Underutilized](#5-underutilized)
- [6 Misclassified](#6-misclassified)
- [7 Divergent](#7-divergent)

Note: The classification order differs from the table order above.
The table is a reference list. The classification order is the
testing sequence — test in THIS order, stop at first match.

## Appendix A — The Seven Gap Taxonomy (closed) (Tells what is wrong?)

> Every finding belongs to exactly one of seven types. No overlap. No duplicates.
> Classification order: Missing → Ignored → Divergent → Disconnected →
> Untrusted → Underutilized → Misclassified. Test in this sequence.
> Stop at the first match.

| Gap           | Meaning                                 |
| ------------- | --------------------------------------- |
| Missing       | Required information absent             |
| Ignored       | Standard exists but not followed        |
| Disconnected  | Information exists but is isolated      |
| Untrusted     | Evidence cannot be verified             |
| Underutilized | Data collected but unused               |
| Misclassified | Wrong classification or taxonomy        |
| Divergent     | Delivery differs from required standard |

## Master Disambiguation Example — The Risk Register

The same artifact, the same standard, the same organization.
Only the problem changes.

A standard defines what SHOULD exist. If the delivery evidence doesn't have what the standard requires, that's a gap.

| Situation                                                         | Does it "not satisfy the standards"? | Gap Type          |
| ----------------------------------------------------------------- | ------------------------------------ | ----------------- |
| The Risk Register **doesn't exist at all**                        | Yes                                  | **Missing**       |
| The Risk Register exists but **nobody updates it**                | Yes                                  | **Ignored**       |
| The Risk Register exists but **isn't connected to governance**    | Yes                                  | **Disconnected**  |
| The Risk Register exists but **the data can't be verified**       | Yes                                  | **Untrusted**     |
| The Risk Register exists, is updated, but **nobody reads it**     | Yes                                  | **Underutilized** |
| The Risk Register exists but **risks are categorized wrong**      | Yes                                  | **Misclassified** |
| The Risk Register exists but **uses a 3×3 matrix instead of 5×5** | Yes                                  | **Divergent**     |

# Gap Classification

---

## 1 Missing — required information absent

### Definition

Missing means the required information does not exist. Not "exists but is wrong." Not "exists but is ignored." Does. Not. Exist.

### Detection

> Step 1: Check all the organization's delivery evidence
> Step 2: Review that with declared project management standards
> Step 3: Search by **Function** not by name (An org might call it a "Threat Log" instead of "Risk Register" — that's NOT Missing.)
> Step 4: If zero instances → check the Charter. Was it waived by the human?
> Step 5: If waived → out of scope, not a finding. If confirmed → Missing.

### Examples

**Example 1 — Risk Register (from Master Table):**
The Standard for Risk Management §3.2 requires a Risk Register.
A search of all declared artifacts finds zero instances.
No document, no system record, no spreadsheet, no field set
functions as a risk register. The human confirmed this absence
during Charter ratification.
→ **Missing.** The required artifact does not exist.

**Example 2 — Lessons Learned Register:**
PMBOK 8 expects lessons learned to be captured and maintained.
The organization has no lessons learned repository, no template,
no log, and no process for capturing lessons.
→ **Missing.**

**Counter-example — NOT Missing:**
The standard expects a "Decision Log." The org has no document
called "Decision Log." However, decisions are recorded in
Steering Committee Minutes under "Resolutions." The artifact
functionally exists under a different name.
→ **NOT Missing.** Possibly Disconnected or Misclassified —
but not Missing.

### Common Misclassification Traps

| Trap                                                       | Why It's Wrong                                           | Correct Type                                             |
| ---------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| "The risk register is 8 months out of date" → Missing      | The register EXISTS. It's stale, not absent.             | **Ignored**                                              |
| "We track risks in Jira tickets, not a register" → Missing | The risk information EXISTS in a different format.       | **Not Missing** (possibly Disconnected or Misclassified) |
| "The template exists but nobody uses it" → Missing         | The template EXISTS. The practice of using it is absent. | **Ignored**                                              |

### PMI Anchors

| #   | Anchor                                                                  | What It Supports                                                                                                 |
| --- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| 1   | Standard for Risk Management §3.2 — risk register as key process output | The basis for Missing: if the process output doesn't exist, the gap is Missing.                                  |
| 2   | PMBOK 8 §2.5 (Tailoring) — tailoring must be documented                 | The boundary between Missing and out-of-scope: undocumented absence = Missing; documented waiver = out of scope. |

---

## 2 Ignored — standard exists but not followed

### Definition

The standard/rule/policy/process EXISTS. The practice does not follow it. Not performed. Not enforced. Not applied. Not maintained."Does. Exist. Not. Followed."

### Detection

> Step 1: Confirm the standard/rule/policy EXISTS in the organization's baseline or knowledge base.(If it doesn't exist → this is Missing, not Ignored. Go back to §7.1.)

> Step 2: Compare the registry criterion's expected evidence (from the applicability map, Stage 0) against the delivery evidence declared in the Charter. What artifact does the standard expect? Does ANY instance of it exist?

> Step 3: Examine the delivery evidence for conformance.

    - Is the practice being performed?
    - Is the output being produced?
    - Is the cadence being met?
    - Is the content meeting the standard?

> Step 4: If the practice DEVIATES from the rule:

    - Check for a documented tailoring decision or approved waiver.
        - If a valid waiver/tailoring EXISTS → NOT Ignored.
    - Governed deviation. Record as a tailoring note.
        - If NO waiver/tailoring exists → Ignored.

> Step 5: Assess the PATTERN:

- Isolated (one project, one cycle) → lower Persistence.
- Systematic (across projects, across cycles) → higher Persistence and Spread.

### Examples

**Example 1 — Risk Register (from Master Table):**
The Risk Register exists. It was created 14 months ago at
project kickoff. It contains 6 risks, all dated to the
initial workshop. No new risks have been added. No risk
reviews have been recorded. No status updates appear in
any of the last 8 reporting cycles. The register exists
but has not been maintained.
→ **Ignored.** The standard requires ongoing maintenance.
The practice does not follow it.

**Example 2-: Weekly Status Report **
The Reporting Policy requires weekly status reports by Friday 5 PM. The policy exists. The template exists. Over 12 weeks, 4 reports are missing and 5 are late. The standard exists. The cadence is not followed.
→ **Ignored.**

**Example 3-: Project management Plan**
The PMBOK 8 standard expects a full Project Management Plan. The org's PMO Policy (§2.1) states: "Small projects (<$100K) shall use a Lightweight Brief in lieu of a full plan." Small projects use the Brief. This is a documented, approved tailoring decision.
→ **NOT Ignored**. Governed deviation. Not a finding.

### Common Misclassification Traps

| Trap                                                                     | Why It's Wrong                                                                                                                                                                                                                                                 | Correct Type                                                |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| "Nobody follows the change control process" → Ignored (without checking) | First check: does the process document EXIST? If not → Missing.                                                                                                                                                                                                | **Depends on existence**                                    |
| "Teams use their own format instead of the template" → Ignored           | The critical distinction from Divergent: Ignored means the practice is NOT PERFORMED (the action doesn't happen). Divergent means the practice IS PERFORMED but produces a DIFFERENT RESULT than the standard requires. Test: Is the action being done at all? | If NO → Ignored. If YES but the output differs → Divergent. |
| "The governance board meets but skips risk review" → Ignored             | Correct — the specific required practice within the meeting is not performed.                                                                                                                                                                                  | **Ignored** ✅                                              |

### PMI Anchors

| #   | Anchor                                                                        | What It Supports                                                        |
| --- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| 1   | PMBOK 8 §2.5 (Tailoring) — deviation must be deliberate and documented        | Undocumented deviation = Ignored. Documented tailoring = not a finding. |
| 2   | Standard for Project Management §4 (Governance) — mandatory reviews and gates | When a governance rule exists and the review doesn't happen → Ignored.  |
| 3   | OPM3 capability assessment — practices must be PERFORMED, not just documented | Policy without practice = the OPM3 basis for Ignored.                   |
