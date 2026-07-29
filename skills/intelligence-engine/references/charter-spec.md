## 4.2 Contract 2 — PMO Data Charter

The **PMO Data Charter** is the authoritative data-interpretation contract for every IEM-PM audit. It specifies **what** the delivery data is, **how** the engine must interpret it, and **what** matters — the boundaries within which the audit operates. **It is not the baseline**; the Standards (Contract 1) are the baseline the data is judged against.

The PMO Data Charter performs five essential functions.

### 1. Artifact Declaration

The charter declares every artifact that is in scope for the audit. It identifies the organizational documents, repositories, systems, reports, registers, and datasets that constitute valid audit evidence.

Typical artifacts include, but are not limited to:

- PMO Governance Documents
- Project Charters
- Program Charters
- Portfolio Plans
- Project Schedules
- RAID Registers
- Risk Registers
- Issue Logs
- Decision Logs
- Benefits Registers
- Financial Reports
- Status Reports
- Steering Committee Packs
- Lessons Learned
- Jira, Azure DevOps, Microsoft Project, Primavera, or equivalent delivery systems

If the standards expect an artifact that is not declared, that is a **candidate Missing gap** — not "out of scope." The human must supply it, confirm the finding, or explicitly waive it.

---

### 2. Field Semantics Map

Defines what every significant field means. You do not interpret field names on your own.
The charter provides a semantic definition for every significant field contained within the delivery data.

The Field Semantics Map establishes a common understanding of what each document, attribute, metric, and data element represents. It removes ambiguity by defining the business meaning of the organization's data rather than relying solely on field names.

For example, the charter may define:

- What constitutes overall project health.
- The organization's interpretation of RAG status.
- The meaning of Schedule Performance Index (SPI) and Cost Performance Index (CPI).
- The purpose of a project owner or sponsor.
- How governance decisions are recorded.
- Which fields are mandatory, optional, calculated, or derived.

Another Example: the Charter tells you whether `percent_complete` means physical % complete, duration % complete, or effort % complete. Without this map, you do not guess — you flag the field as unmapped.

By defining field semantics before analysis begins, IEM-PM can interpret delivery information consistently across projects, programs, portfolios, and PMOs.

---

### 3. Materiality and Scope

The charter defines the scope and materiality of the audit.

Scope determines **which parts of the organization and which delivery artifacts will be evaluated**, while materiality defines **what is significant enough to influence audit findings**.

Examples include:

- Organizational units included in the audit.
- Portfolios, programs, and projects included or excluded.
- Time period under review.
- Minimum project value or strategic importance.
- Governance levels to be evaluated.
- Thresholds for significant risks, issues, budget variance, or schedule variance.

Materiality ensures that the audit focuses on information capable of affecting governance decisions rather than insignificant operational detail. Defines what is significant enough to influence findings: organizational units, time period, project value thresholds, governance levels, variance thresholds.

---

### 4. Propose → Ratify

Before the audit begins, IEM-PM performs a discovery phase in which it proposes its understanding of the audit environment.

The engine identifies:

- Baseline standards.
- Available artifacts.
- Organizational structure.
- Delivery systems.
- Audit scope.
- Significant assumptions.

But you **do not proceed to findings** until the user ratifies it.

The audit only begins after the proposed understanding has been reviewed and ratified. This validation step ensures that the engine has correctly interpreted the organization's environment before evaluating delivery performance.

If the user demands an immediate run without ratification, you proceed on a **PROVISIONAL Charter** — your own proposal, explicitly marked as assumed — and every finding carries the caveat that it rests on unratified interpretation.

---

### 5. Anti-Mirror Guard

This guard is asymmetric:

- **Artifact Declaration and Field Semantics** are proposed **from the data** — safe, because you are reading the data to understand the data.
- **Materiality and Scope** are proposed **from the standards' expectations** — never from the data. If scope were inferred from what the upload contains, the audit could only confirm what was supplied, and a **Missing** gap could never surface.

Scope must therefore be derived from authoritative sources such as:

- Organizational governance frameworks.
- PMO operating models.
- Project management methodologies.
- Approved policies and procedures.
- PMI or other recognised project management standards.

Once ratified, the PMO Data Charter becomes the immutable **interpretation contract** for the run. The audit compares observed delivery against the Standards (Contract 1) _as interpreted through_ the Charter — ensuring every finding represents a genuine variance between expected and actual delivery, never a comparison against a standard inferred from the evidence itself.
