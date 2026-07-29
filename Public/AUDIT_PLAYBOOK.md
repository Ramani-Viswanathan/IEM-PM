Here is the **real-world playbook** — a single page you can hand to any PM, Program Manager, or PMO lead.

# IEM-PM Audit Playbook

## How to Run a Real-World PMO Data Gap Audit

> **One-sentence purpose:** Compare what your organization _claims_ it does (standards) against what your _evidence_ actually shows (delivery data), find the gaps, trace them to root causes, and know your maturity.

**Who this is for:** Project Managers, Program Managers, PMO Leads, Portfolio Directors, Governance Officers.

**Time required:** 2–4 hours for the first audit (most of it is waiting for the AI to read and think). 30 minutes for repeat audits.

**What you need:** A computer with Python 3.10+, your project files, and your methodology documents.

---

## Before You Start: The 3-Box Checklist

You cannot audit without these three boxes checked. Do not skip.

| Box                       | What You Need                                                                              | Why                                                                         |
| ------------------------- | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- |
| **1. Standards**          | PDF or Word files of your methodology: PMBOK, PRINCE2, OPM3, or your internal PMO handbook | The audit measures you against _something_. No standard = no audit.         |
| **2. Delivery Evidence**  | Real project files: schedules, RAID logs, status reports, governance packs, financials     | The audit reads what you actually produced. Not templates — real artifacts. |
| **3. A Ratified Charter** | A signed data contract saying "this is what our data means"                                | The AI never guesses what a field means. You tell it. Then you sign it.     |

---

## Step 1: Drop Your Standards into the Engine

**Do this:** Copy your standards documents into the `knowledge/` folder.

```
IEM-PM/skills/intelligence-engine/knowledge/
├── Organizational/          ← Put your internal PMO handbook here
├── PMBOK/                   ← Put PMBOK guides here (if you use them)
├── OPM3/                    ← Put OPM3 references here (if you use them)
├── PRINCE2/                 ← Put PRINCE2 manuals here
└── Agile/                   ← Put SAFe, Scrum guides, or hybrid frameworks here
```

**Rule:** Do not put copyrighted text in Git. These folders are `.gitignore`-friendly. Keep them local.

**Run the index:**

```bash
python scripts/derive_knowledge_index.py
```

You should see your documents listed. If not, check the folder path.

---

## Step 2: Gather Your Delivery Evidence

Collect **real artifacts** from one project, one program, or one portfolio. Do not use templates. Use what was actually delivered.

**Minimum viable set (start here):**

- 1 Project Schedule (MS Project, Excel, or Primavera export)
- 1 RAID Log (Excel or CSV export from your tool)
- 1 Status Report or Governance Pack (PDF or Word)
- 1 Financial/Budget Report (Excel)

**Ideal set (for a full audit):**

- Project Charter
- Program/Portfolio Plan
- Risk Register (separate from RAID)
- Issue Log
- Change Log
- Decision Log
- Lessons Learned
- Steering Committee Minutes/Pack
- Dashboard export (Jira, Azure DevOps, Smartsheet, Power BI)

**Format:** PDF, Excel, CSV, Word, Markdown, or plain text. The AI reads all of these. If your data is in a tool (Jira, ADO, Primavera), **export it to file first**. The engine does not log into tools.

**Place them in a working folder:**

```
C:\Users\you\Documents\IEM-PM-Audit-2026-07-26\
├── schedule.xlsx
├── raid_log.xlsx
├── governance_pack_july.pdf
├── status_report.docx
└── budget.xlsx
```

---

## Step 3: Create and Ratify the PMO Data Charter

This is **the most important step.** The Charter is a contract between you and the audit engine. It says: _"Here is what our data is, what the fields mean, and what matters."_

**How to create it:**

1. Open `assets/PMO_DATA_CHARTER_template.md`
2. Fill in your organization name and audit scope
3. List every artifact you gathered in Step 2 (give each an ID: ART-001, ART-002, etc.)
4. For each artifact, map the **fields** that matter:
   - What does `percent_complete` mean in _your_ organization?
   - What does `RAG` mean — is it schedule, budget, or overall health?
   - What is your risk scoring scale (1–5? 1–3? High/Medium/Low?)
5. Define **materiality**: What is big enough to care about? (e.g., "Projects over $100K," "Schedule variance > 5 days")
6. **Sign it.** Literally. Type your name, role, and date. The audit will not run without ratification.

**If you skip this:** The AI will propose a Charter from your data, but every finding will carry a warning: _"Based on unratified Charter interpretation."_ You do not want this for a real audit.

**Save the ratified Charter as:**

```
reports/PMO_DATA_CHARTER_ratified.md
```

---

## Step 4: Load IEM-PM into Claude Code

**In Claude Code:**

1. Ensure the `skills/intelligence-engine/SKILL.md` file is loaded as a skill (or paste it into context).
2. Tell Claude: _"Load the IEM-PM Intelligence Engine skill."_

Claude now knows:

- The 7 Gap Types
- The 7 Root Origins
- That it must cite evidence for every finding
- That it only writes the Audit Manifest — nothing else

---

## Step 5: Execute the Audit (The Prompt)

Give Claude exactly this sequence. Do not skip steps.

### Prompt 1: Load the Baseline

```
Read the standards in knowledge/Organizational/ and knowledge/PMBOK/.
Build your understanding of what is required.
Confirm: which standards govern this audit?
```

### Prompt 2: Load the Charter

```
Read the ratified PMO Data Charter at reports/PMO_DATA_CHARTER_ratified.md.
Confirm: which artifacts are in scope? What do the fields mean?
Do not proceed until you confirm the Charter is ratified.
```

### Prompt 3: Read the Evidence

```
Read the following delivery artifacts:
- /path/to/schedule.xlsx
- /path/to/raid_log.xlsx
- /path/to/governance_pack_july.pdf
- /path/to/status_report.docx
- /path/to/budget.xlsx

For each artifact, record what you observe. Note field completeness, anomalies, and anything that stands out.
```

### Prompt 4: Find and Classify Gaps

```
Compare the observed delivery evidence against the standards baseline.
For every variance you find:
1. Cite the exact evidence (artifact, location, quote or absence)
2. Classify the gap type (Missing, Ignored, Disconnected, Untrusted, Underutilized, Misclassified, Divergent)
3. Trace the root origin (Capture, Integration, Definition/Taxonomy, Ownership, Process/Cadence, Tooling, Behavior)
4. Assign severity (1=Cosmetic, 5=Critical)
5. Write a specific recommended action that fixes the root cause, not the symptom

Write each finding into the Audit Manifest format immediately. Do not hold them in memory.
```

### Prompt 5: Synthesize

```
Write the SYNTHESIS section with narrative diagnostics for all 7 Intelligence Indicators:
Visibility, Integrity, Connectivity, Governance, Predictability, Decision Quality, Continuous Improvement.

Use the exact PENDING_BRIDGE statement for OPM3 Maturity Position.

Then print the Handover Message.
```

### Prompt 6: Save the Manifest

```
Save the complete Audit Manifest to:
reports/audit_manifest.md
```

**Claude will now write the Manifest.** This takes 2–10 minutes depending on artifact count. Let it finish.

---

## Step 6: Run the Deterministic Pipeline (You, Not Claude)

Claude has finished. Its job is done. Now **you** run the software.

**Open your terminal in the `scripts/` folder:**

```bash
# Step 6a: Manifest → Canonical JSON
python manifest_to_findings.py \
  --manifest ../reports/audit_manifest.md \
  --charter ../reports/PMO_DATA_CHARTER_ratified.md \
  --output ../reports/findings.json
```

**Expected output:**

```
Canonical findings written to ../reports/findings.json
Total findings: [N]
Reporting Integrity Score: [X]
OPM3 Position: PENDING_BRIDGE
```

If you see `VALIDATION FAILED`, read the errors. They usually mean:

- A gap type or root origin is misspelled (must match exactly)
- A finding has no evidence bullets
- An evidence bullet references an artifact not in the Charter
- Severity is not 1–5

Fix the Manifest (or ask Claude to fix it), then re-run.

```bash
# Step 6b: JSON → Reports
python render.py \
  --canonical ../reports/findings.json \
  --template ../assets/report_template.html \
  --output-html ../reports/audit_report.html \
  --output-txt ../reports/audit_report.txt
```

**Expected output:**

```
TXT report: ../reports/audit_report.txt
HTML report: ../reports/audit_report.html
```

---

## Step 7: Read Your Report

Open `reports/audit_report.html` in your browser. This is your executive deliverable.

**How to read it:**

| Section                        | What to Look For                                                                                                                         |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Executive Summary**       | Total findings, Reporting Integrity Score, OPM3 Position. The score is deterministic — not opinion.                                      |
| **2. Audit Scope**             | Did we audit what we intended? Check artifact count and standards.                                                                       |
| **4. Gap Register**            | The evidence. Every finding has a direct quote from your files. If you disagree with a finding, the evidence is right there — verify it. |
| **5. Root Cause Analysis**     | Where do your problems come from? If 80% are "Ownership," you have an accountability crisis, not a tools problem.                        |
| **7. Intelligence Indicators** | The narrative story. Read these to understand _why_ your projects perform the way they do.                                               |
| **9. Recommended Actions**     | Prioritized by severity. Actions address root causes, not symptoms.                                                                      |

**Share the HTML** with your steering committee, PMO director, or portfolio board. Keep the `findings.json` as the single source of truth.

---

## Step 8: Remediate and Re-Audit

The report is not the end. It is the beginning.

**30-Day Sprint:**

1. **Week 1:** Address all Severity 5 and 4 findings (Critical and Major).
2. **Week 2:** Fix the highest-frequency root origin. (If most gaps are "Ownership," assign owners. If "Capture," build templates.)
3. **Week 3:** Close Missing gaps by updating the Charter or establishing the missing process.
4. **Week 4:** Re-run the audit with the same Charter and same artifacts.

**Measure the delta:**

- Did the Reporting Integrity Score improve?
- Did gap density decrease?
- Did the root origin distribution shift?

**Re-audit command:**

```bash
# Same pipeline, new manifest
python manifest_to_findings.py --manifest ../reports/audit_manifest_v2.md --output ../reports/findings_v2.json
python render.py --canonical ../reports/findings_v2.json --template ../assets/report_template.html --output-html ../reports/audit_report_v2.html --output-txt ../reports/audit_report_v2.txt
```

---

## Troubleshooting

| Problem                               | Cause                                           | Fix                                                                                  |
| ------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------ |
| `BASELINE_ABSENT`                     | No standards in `knowledge/`                    | Drop your methodology PDFs into `knowledge/Organizational/`                          |
| `VALIDATION FAILED: Invalid gap_type` | Claude used wrong spelling or invented a type   | Edit Manifest to match the 7 allowed types exactly                                   |
| `VALIDATION FAILED: unknown artifact` | Evidence bullet cites ART-999 not in Charter    | Add the artifact to Charter or remove the bullet                                     |
| `PENDING_BRIDGE` forever              | OPM3 bridge not calibrated                      | Normal. The gap profile is recorded. Maturity assessment requires a ratified rubric. |
| Claude wants to run Python            | Architecture confusion                          | Remind Claude: _"You write the Manifest. I run the Python."_                         |
| Report says `coverage_percentage: 0%` | Old bug — update your `manifest_to_findings.py` | Pull latest from repo                                                                |

---

## The Golden Rules (Never Break These)

1. **No ratified Charter → no audit.** Never let Claude guess what your data means.
2. **Every finding needs evidence.** If Claude cannot cite a quote or an absence, it is not a finding.
3. **The AI judges. You run the software.** Claude writes the Manifest. You run `manifest_to_findings.py` and `render.py`.
4. **Read-only.** Never let Claude edit your source files. Only the Manifest and `reports/` are written.
5. **Local first.** No cloud APIs, no databases. Everything stays on your machine.

---

## Quick-Start Checklist

- [ ] Standards copied to `knowledge/`
- [ ] `derive_knowledge_index.py` run successfully
- [ ] Real delivery artifacts gathered (not templates)
- [ ] `PMO_DATA_CHARTER_template.md` filled out and ratified
- [ ] Claude Code loaded with `SKILL.md`
- [ ] Audit Manifest generated by Claude
- [ ] `manifest_to_findings.py` run — JSON created and validated
- [ ] `render.py` run — HTML and TXT reports created
- [ ] Report reviewed with stakeholders
- [ ] Remediation plan assigned
- [ ] Re-audit scheduled

---

**End of Playbook**

_Version 1.0.0 | IEM-PM Intelligence Engine_
