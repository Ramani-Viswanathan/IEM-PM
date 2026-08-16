# Baseline Drop-Zone

This folder is where you place your organization's **real standards** — PMI publications
(PMBOK, Practice Standards, Risk Management, Governance guides), PRINCE2, ISO 21502, or your own
internal PMO methodology. PDF or Markdown.

**Nothing runs without this.** IEM-PM ships zero standard text of its own (copyright). If this
folder is empty (aside from this file), Stage 0 of the audit stops and asks for a baseline instead
of guessing or falling back to model memory.

## What to drop here

Any real standard your organization actually declares in its PMO Data Charter. One subfolder per
publishing body is a reasonable way to organize multiple standards, e.g.:

```
knowledge/
  PMI/
  PRINCE2/
  ISO/
  Agile/
  Organizational/        (your own internal methodology, if you have one)
```

## What happens after you drop files here

At runtime, the engine scans this folder and derives local, paraphrased **registries** — checkable
criteria plus stable citation anchors, never verbatim standard text — into
`skills/intelligence-engine/registries/` (also gitignored). This starts as a skeleton on first use
and deepens on demand as audits actually need a given section, so the first audit against a new
standard is slower than later ones against the same standard.

## Why this folder is empty on a fresh clone

Both `knowledge/` and `registries/` are gitignored on purpose — the standards you hold are your
organization's own licensed content, not this repository's to redistribute. Cloning this repo on a
new machine always starts with an empty baseline; there is no automatic way to carry a prior
machine's standards or derived registries forward except copying the folders yourself.
