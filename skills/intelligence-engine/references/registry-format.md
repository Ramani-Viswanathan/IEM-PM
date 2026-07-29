---
Name: Registry Item Format
description: >
  Appendix E — the file-wrapper schema for locally-derived standard registries (skeleton_map.json,
  per-standard registry files). Read during Phase 0b (Derivation) before deriving or reading a
  registry.
version: 1.0.0
---

## Appendix E — Registry Item Format

| Attribute             | Type   | Description                                                                                         |
| --------------------- | ------ | --------------------------------------------------------------------------------------------------- |
| Identifier            | string | Unique identifier for the registry item.                                                            |
| Name                  | string | Descriptive name of the registry item.                                                              |
| Description           | string | Detailed description of the registry item.                                                          |
| Standard Source       | string | Specifies the standard or source that defines the registry item.                                    |
| Category              | string | Specifies the category or classification of the registry item.                                      |
| Evidence Required     | string | Specifies the type of evidence required to validate the registry item.                              |
| Evaluation Method     | string | Specifies the method or criteria used to evaluate the registry item.                                |
| Likely Gap Type(s)    | string | Candidate gap classification(s) as a hint — Stage 4 decides the actual gap type per finding.        |
| Likely Root Origin(s) | string | Candidate root origin(s) as a hint — Stage 5 decides the actual origin per finding.                 |
| Confidence Rules      | string | Specifies the confidence level rules associated with the registry item.                             |
| Severity Guidelines   | string | Specifies the severity guidelines associated with the registry item.                                |
| Reference             | string | Reference to the relevant standard, policy, or guideline that defines the registry item.            |

### File format

One registry file per standard: `registries/<slug>.json`, where `<slug>` is the source filename
in `knowledge/`, lowercased, with any run of non-alphanumeric characters collapsed to a single
underscore (e.g. `PS_Scheduling_3rd.pdf` → `ps_scheduling_3rd.json`). See SKILL.md §Phase 0b for
when to derive vs. reuse.

```json
{
  "standard": "<full standard title as commonly cited>",
  "source_document": "<filename in knowledge/>",
  "source_fingerprint": "<sha256, from derivation_manifest.json>",
  "derived_at": "<ISO 8601 date>",
  "items": [
    {
      "identifier": "...", "name": "...", "description": "...",
      "standard_source": "...", "category": "...",
      "evidence_required": "...", "evaluation_method": "...",
      "likely_gap_types": ["..."], "likely_root_origins": ["..."],
      "confidence_rules": "...", "severity_guidelines": "...",
      "reference": "..."
    }
  ]
}
```

### Worked example (real, from `knowledge/PMI/PS_Scheduling_3rd.pdf`)

```json
{
  "identifier": "PS-SCHED-3.3.5",
  "name": "Update the Baseline Schedule Model on Major Change",
  "description": "When a project is impacted by a major, formally approved scope change, the schedule model should be rebaselined, with the reasons and stakeholder agreement documented.",
  "standard_source": "PMI Practice Standard for Scheduling, 3rd Edition",
  "category": "Schedule Model Maintenance",
  "evidence_required": "A change request/approval record plus a corresponding baseline update in the schedule for the affected tasks.",
  "evaluation_method": "For each approved change request that adds or resizes schedule scope, confirm the affected tasks carry a baseline consistent with the approval date.",
  "likely_gap_types": ["Missing", "Divergent"],
  "likely_root_origins": ["Process / Cadence"],
  "confidence_rules": "High confidence when the change request is explicitly referenced in both the schedule and another artifact (e.g., a steering pack) but the baseline fields remain blank.",
  "severity_guidelines": "Higher severity the larger the share of active or completed work under the un-rebaselined scope.",
  "reference": "Section 3.3.5, \"Update the Baseline Schedule Model\""
}
```

This exact item was independently reasoned to by the real pilot audit in `examples/pilot-audit/`
(as FIND-0001) before this registry layer existed — confirming the two approaches converge on the
same criterion.
