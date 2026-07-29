## Appendix D — Severity Scale (Tells How serious is it?)

## Contents

- [Decision Impact](#decision-impact)
- [Spread](#spread)
- [Persistence](#persistence)
- [Severity Bands](#severity-bands)
- [Severity Matrix (all 80 combinations)](#severity-matrix-all-80-combinations--generated-from-the-rule-above)
- [PMI anchors for this appendix](#pmi-anchors-for-this-appendix-verified-in-the-held-documents-2026-07-05)

Severity is determined by evaluating three dimensions:

Decision Impact – How significantly the gap affects business, governance, financial, or delivery decisions.
Spread – How widely the gap affects the organization.
Persistence – How long the gap has existed without effective resolution.

### Decision Impact

Measures how badly the gap **distorts a decision** (magnitude of consequence — _Standard for Risk Mgmt_ §3.3.1), not how widely it reaches (that is Spread's job).

| Level    | Score | Meaning                                                                       |
| -------- | ----- | ----------------------------------------------------------------------------- |
| Low      | 1     | Cosmetic — the decision is unaffected                                         |
| Medium   | 2     | Misinforms — decision-makers see a distorted picture                          |
| High     | 3     | Drives a wrong decision — funding, gating, or prioritization made on bad data |
| Critical | 4     | A strategic, regulatory, or mission-critical decision is made on bad data     |

### Spread

Measures how widely the gap reaches, on PMI's escalation ladder (_Risk Mgmt Practice Guide_ §4.1.3).

| Level      | Score | Meaning                                      |
| ---------- | ----- | -------------------------------------------- |
| Local      | 1     | Limited to a single record or artifact       |
| Project    | 2     | Affects one project                          |
| Program    | 3     | Affects multiple projects within a program   |
| Portfolio  | 4     | Affects multiple programs across a portfolio |
| Enterprise | 5     | Affects the enterprise as a whole            |

### Persistence

Measures how long the gap has survived (IEM-PM's own dimension; nearest PMI cousin: dormancy, _Practice Guide_ §X2.3.7).

| Level      | Score | Meaning                                                          |
| ---------- | ----- | ---------------------------------------------------------------- |
| Temporary  | 1     | One reporting cycle or isolated occurrence                       |
| Recurring  | 2     | Appears across multiple reporting cycles or multiple iterations  |
| Sustained  | 3     | Exists for several months and affects ongoing delivery           |
| Systematic | 4     | Embedded within organizational practices over an extended period |

### Severity Bands

- Severity measures the business significance of a finding.
- **Combination rule (pure arithmetic — the validator recomputes it):**
  `Score = Persistence (1–4) × Spread (1–5) × Decision Impact (1–4)` — range 1–80.
- **Bands:** Score ≤ 8 → **Low** · 9–24 → **Medium** · 25–48 → **High** · ≥ 49 → **Critical**.
- **Floor rule:** Decision Impact = Critical → Severity is at least **High**, regardless of score (a strategic/regulatory decision on bad data is never a low-severity finding). Marked `^` in the matrix.

### Severity Matrix (all 80 combinations — generated from the rule above)

| Persistence | Spread     | Decision Impact | Score | Severity |
| ----------- | ---------- | --------------- | ----- | -------- |
| Temporary   | Local      | Low             | 1     | Low      |
| Temporary   | Local      | Medium          | 2     | Low      |
| Temporary   | Local      | High            | 3     | Low      |
| Temporary   | Local      | Critical        | 4     | High ^   |
| Temporary   | Project    | Low             | 2     | Low      |
| Temporary   | Project    | Medium          | 4     | Low      |
| Temporary   | Project    | High            | 6     | Low      |
| Temporary   | Project    | Critical        | 8     | High ^   |
| Temporary   | Program    | Low             | 3     | Low      |
| Temporary   | Program    | Medium          | 6     | Low      |
| Temporary   | Program    | High            | 9     | Medium   |
| Temporary   | Program    | Critical        | 12    | High ^   |
| Temporary   | Portfolio  | Low             | 4     | Low      |
| Temporary   | Portfolio  | Medium          | 8     | Low      |
| Temporary   | Portfolio  | High            | 12    | Medium   |
| Temporary   | Portfolio  | Critical        | 16    | High ^   |
| Temporary   | Enterprise | Low             | 5     | Low      |
| Temporary   | Enterprise | Medium          | 10    | Medium   |
| Temporary   | Enterprise | High            | 15    | Medium   |
| Temporary   | Enterprise | Critical        | 20    | High ^   |
| Recurring   | Local      | Low             | 2     | Low      |
| Recurring   | Local      | Medium          | 4     | Low      |
| Recurring   | Local      | High            | 6     | Low      |
| Recurring   | Local      | Critical        | 8     | High ^   |
| Recurring   | Project    | Low             | 4     | Low      |
| Recurring   | Project    | Medium          | 8     | Low      |
| Recurring   | Project    | High            | 12    | Medium   |
| Recurring   | Project    | Critical        | 16    | High ^   |
| Recurring   | Program    | Low             | 6     | Low      |
| Recurring   | Program    | Medium          | 12    | Medium   |
| Recurring   | Program    | High            | 18    | Medium   |
| Recurring   | Program    | Critical        | 24    | High ^   |
| Recurring   | Portfolio  | Low             | 8     | Low      |
| Recurring   | Portfolio  | Medium          | 16    | Medium   |
| Recurring   | Portfolio  | High            | 24    | Medium   |
| Recurring   | Portfolio  | Critical        | 32    | High     |
| Recurring   | Enterprise | Low             | 10    | Medium   |
| Recurring   | Enterprise | Medium          | 20    | Medium   |
| Recurring   | Enterprise | High            | 30    | High     |
| Recurring   | Enterprise | Critical        | 40    | High     |
| Sustained   | Local      | Low             | 3     | Low      |
| Sustained   | Local      | Medium          | 6     | Low      |
| Sustained   | Local      | High            | 9     | Medium   |
| Sustained   | Local      | Critical        | 12    | High ^   |
| Sustained   | Project    | Low             | 6     | Low      |
| Sustained   | Project    | Medium          | 12    | Medium   |
| Sustained   | Project    | High            | 18    | Medium   |
| Sustained   | Project    | Critical        | 24    | High ^   |
| Sustained   | Program    | Low             | 9     | Medium   |
| Sustained   | Program    | Medium          | 18    | Medium   |
| Sustained   | Program    | High            | 27    | High     |
| Sustained   | Program    | Critical        | 36    | High     |
| Sustained   | Portfolio  | Low             | 12    | Medium   |
| Sustained   | Portfolio  | Medium          | 24    | Medium   |
| Sustained   | Portfolio  | High            | 36    | High     |
| Sustained   | Portfolio  | Critical        | 48    | High     |
| Sustained   | Enterprise | Low             | 15    | Medium   |
| Sustained   | Enterprise | Medium          | 30    | High     |
| Sustained   | Enterprise | High            | 45    | High     |
| Sustained   | Enterprise | Critical        | 60    | Critical |
| Systematic  | Local      | Low             | 4     | Low      |
| Systematic  | Local      | Medium          | 8     | Low      |
| Systematic  | Local      | High            | 12    | Medium   |
| Systematic  | Local      | Critical        | 16    | High ^   |
| Systematic  | Project    | Low             | 8     | Low      |
| Systematic  | Project    | Medium          | 16    | Medium   |
| Systematic  | Project    | High            | 24    | Medium   |
| Systematic  | Project    | Critical        | 32    | High     |
| Systematic  | Program    | Low             | 12    | Medium   |
| Systematic  | Program    | Medium          | 24    | Medium   |
| Systematic  | Program    | High            | 36    | High     |
| Systematic  | Program    | Critical        | 48    | High     |
| Systematic  | Portfolio  | Low             | 16    | Medium   |
| Systematic  | Portfolio  | Medium          | 32    | High     |
| Systematic  | Portfolio  | High            | 48    | High     |
| Systematic  | Portfolio  | Critical        | 64    | Critical |
| Systematic  | Enterprise | Low             | 20    | Medium   |
| Systematic  | Enterprise | Medium          | 40    | High     |
| Systematic  | Enterprise | High            | 60    | Critical |
| Systematic  | Enterprise | Critical        | 80    | Critical |

`^` = lifted by the floor rule (Decision Impact = Critical → minimum High).

### PMI anchors for this appendix (verified in the held documents, 2026-07-05)

The method — pre-defined qualitative levels, combined and banded — follows PMI risk practice. Anchors below cite section + PDF page in the copies held in `knowledge/`; paraphrase only, per Principle 3.

| #   | Anchor                                                                                     | What it supports                                                                                                                                                                                                                                                                                                  |
| --- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | _Risk Mgmt Practice Guide_ §X2.3.5, Probability and Impact Matrixes (p. 133, Fig. X2-11)   | The core precedent: risks rated on five qualitative levels (VH/H/M/L/VL) per dimension, combined in a matrix, **sorted into classes** — our "multiply/combine then band" pattern.                                                                                                                                 |
| 2   | _Practice Guide_ §X2.4.3, Estimating Techniques Applied to Probability and Impact (p. 135) | Impact-level definitions are **work-specific** and must be designated per objective from very low → very high — the license for IEM-PM to define its own level meanings, provided they are declared up front.                                                                                                     |
| 3   | _Practice Guide_ §X2.3.7, Assessment of Other Risk Parameters (pp. 133–134)                | PMI's own precedent for scoring dimensions **beyond** probability × impact (urgency, proximity, dormancy, connectivity, strategic impact) — legitimizes Spread and Persistence as additional parameters. **Dormancy** (time before an occurred risk's impact is discovered) is the closest cousin of Persistence. |
| 4   | _Practice Guide_ §X2.3.6, Risk Data Quality Analysis (p. 133)                              | "Results of the analysis are only as good as the data collected" — the PMI basis for the Confidence scale (Appendix C) sitting beside Severity.                                                                                                                                                                   |
| 5   | _Standard for Risk Management P/P/P_ §3.3.1, Factors for Evaluating Risk (pp. 42–43)       | Impact defined as the **magnitude/significance of consequence on objectives** — the definition Decision Impact levels must express (distortion of decisions, not organizational breadth).                                                                                                                         |
| 6   | _Standard_ §4.4.2, Key Success Factors for Qualitative Analysis (p. 51)                    | "Use agreed definitions of risk terms" — the mandate that level definitions are **pre-agreed**; in IEM-PM they are ratified in the Charter, not improvised at audit time.                                                                                                                                         |
| 7   | _Standard_ §2.1.6, Risk Threshold (p. 27)                                                  | Thresholds = qualitative/quantitative definitions of rating **plus the exposure level that triggers escalation** — the precedent for tying Severity bands to a governance response.                                                                                                                               |
| 8   | _Practice Guide_ §4.1.3, Risk Escalation (pp. 56–57)                                       | Escalation ladder project → program → portfolio → enterprise — the citable basis for the Spread ladder.                                                                                                                                                                                                           |

Persistence has no direct PMI analogue beyond dormancy/urgency (anchor 3) — it is an IEM-PM contribution, stated as such.
