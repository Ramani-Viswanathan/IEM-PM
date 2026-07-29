---
Name: Error Codes
description: >
  Appendix H — the E-BASE-*/E-PARSE-*/W-PARSE-*/E-VALID-*/E-RENDER-* error code taxonomy embedded
  across baseline.py, manifest_to_findings.py, schema.py, and render.py. Read when a script fails
  and you need to know what a code means.
version: 1.0.0
---

## Appendix H — Error Codes

Every error or validation failure the pipeline can produce carries a stable code, prefixed onto
the message wherever it's raised (e.g. `[E-PARSE-002] FIND-0001: Invalid gap_type 'Delayed'`).
Codes are for grepping/scripting against; the message text still carries the specific detail —
the code never replaces it.

### Stage 0 — `baseline.py`

| Code          | Meaning                                                          | What to do                                                               |
| ------------- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| `E-BASE-001`  | `BASELINE_ABSENT` — no standards found in `knowledge/`. Hard stop, exit 1. | Drop real standards into `knowledge/` and re-run. No baseline, no audit.  |
| `E-BASE-002`  | A file in `knowledge/` could not be fingerprinted/read.            | Check the file isn't corrupted or open in another program; re-run.        |

### Manifest parsing — `manifest_to_findings.py`

| Code           | Meaning                                                            | What to do                                                                        |
| -------------- | --------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `E-PARSE-001`  | `--manifest` path doesn't exist.                                  | Check the path passed on the command line.                                        |
| `E-PARSE-002`  | A finding's `Gap Type` isn't one of the seven closed gap types.   | Fix the Manifest — SKILL.md §3 defines the closed taxonomy.                       |
| `E-PARSE-003`  | A finding's `Root Origin` isn't one of the seven closed origins.  | Same, for Root Origin.                                                            |
| `E-PARSE-004`  | A finding block has zero evidence bullets.                        | Every finding needs at least one `**Artifact:** ... **Location:** ... **Evidence:** ...` bullet (SKILL.md §10.2.3). |
| `E-PARSE-005`  | `Severity` isn't an integer 1–5.                                   | Fix the Manifest's Severity field.                                                |
| `W-PARSE-001`  | *(warning, not fatal)* No `## SYNTHESIS` section found.            | The Manifest is incomplete per SKILL.md §10.1 — add it before handover.           |

### Validation — `schema.py`

| Code           | Meaning                                                                       | What to do                                                                     |
| -------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `E-VALID-001`  | Canonical JSON violates `findings.schema.json`'s structure.                  | The message names the exact field/rule; fix the Manifest so the parsed JSON conforms. |
| `E-VALID-002`  | Two findings share the same Gap Type + Root Origin + Artifact + Standard Identifier. | Merge into one finding with multiple evidence bullets (SKILL.md §6.5 No-Duplicate Rule). |
| `E-VALID-003`  | A finding's evidence cites an `artifact_id` never declared in the baseline.  | Check every `## ARTIFACT:` block matches every `**Artifact:**` reference used in Findings. |

### Rendering — `render.py`

| Code           | Meaning                              | What to do                              |
| -------------- | ---------------------------------------- | ---------------------------------------------- |
| `E-RENDER-001` | `--canonical` path doesn't exist.    | Run `manifest_to_findings.py` first.    |

### Why codes at all

Before this pass, the three scripts raised free-text messages with no consistent shape — a
caller (human or another agent) couldn't tell "the Manifest is malformed" from "the schema itself
was violated" without reading prose and guessing which script produced it. The codes don't change
what's checked or how strict it is; they make the existing checks addressable and groupable by
category (`E-BASE-*` = Stage 0, `E-PARSE-*` = Manifest parsing, `E-VALID-*` = schema/dedup/coverage,
`E-RENDER-*` = rendering).
