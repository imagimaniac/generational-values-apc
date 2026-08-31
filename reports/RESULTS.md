# Results Summary — Multi-Wave HAPC Analysis of Generational Trust

> First end-to-end run on the official **WVS 1981–2022 time-series**
> (443,488 rows, **7 waves**, 34 survey years, 108 countries).
> Method: hierarchical age–period–cohort (HAPC) cross-classified model,
> age as a fixed polynomial, period × cohort as a random intercept.

---

## Headline finding

**Generalized trust declines monotonically across birth cohorts**: people born
in later generations report significantly lower trust than earlier cohorts,
and this holds after controlling for age.

| Birth decade | Trust rate | N |
|---|---|---|
| 1880s | 54% | 37 |
| 1900s | 31% | 2,899 |
| 1920s | 29% | 37,893 |
| 1940s | 29% | 111,152 |
| 1960s | 25% | 169,352 |
| 1980s | 22% | 96,383 |
| 2000s | 19% | 3,828 |

Overall trust rate: **25.7%** (n = 421,544).

The HAPC marginal cohort effects reproduce this: cohorts born 1990s–2000s carry
a **negative** cohort effect (−0.02 to −0.03), while pre-1985 cohorts are
slightly positive (+0.004 to +0.008). This pattern is **robust across cohort
widths (5/10/20 years)** — see the sensitivity tables in `reports/`.

## Age effect

A small but significant positive age coefficient on trust
(0.002, *p* = 0.002); trust rises modestly with age, but this is far smaller
than the cohort gradient.

## Period effect

Survey-year (period) effects fluctuate (1981–2023) without a single clear
monotonic trend — the across-wave descriptive trust also drifts down
(Wave 1 ≈ 31% → Wave 7 ≈ 24%), indicating a period component alongside the
cohort component.

## Outcome #2 — Self-expression (SurvSAgg)

Fitted as a robustness outcome (standardized index, n = 293,597). Age enters
negatively (−0.006, *p* = 0.03); cohort/period trajectories and charts in
`reports/hapc_selfexpr_*`.

## Method

- **Model:** `trust ~ age + I(age²)`, random intercept on `period × cohort`
  cells (cross-classified HAPC; Yang & Land style), fitted with
  statsmodels `MixedLM` (REML).
- **Sensitivity:** cohort bins of 5 / 10 / 20 years.
- **Reproduce:** `python src/analysis.py` from repo root
  (requires the WVS file at `data/raw/` — git-ignored per WVS license).

## Files

- `reports/hapc_trust_w5_cohort.csv` — marginal cohort effects
- `reports/hapc_trust_w5_period.csv` — marginal period effects
- `reports/figures/hapc_trust_w5_*.png` — cohort / period / age charts
- Same set for `selfexpr` and for widths 10/20.

## Honest caveats

- Trust is binary and here fitted with a linear mixed model; a generalized
  (logistic) mixed model is the rigorous follow-up.
- Survey weights (`S017`) are not yet applied; the variance components are
  therefore unweighted.
- Cohort and period are partly separable via the crossed cells, but the
  classical APC identification constraint still applies — interpret effect
  magnitudes, not exact attributions.
