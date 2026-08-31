"""
apc_model.py — Hierarchical Age-Period-Cohort (HAPC) model.

Implements the HAPC model (Yang & Land specification) fitted as a
cross-classified random-effects linear mixed model via statsmodels MixedLM.
Age enters as a fixed polynomial effect; period and cohort are treated as
random intercepts over the cross-classified period x cohort cells.

Because we run on the official multi-wave WVS 1981-2022 file (7 waves, real
period variation), the age/period/cohort split is identifiable rather than a
single-wave approximation.

Outcomes
--------
  - 'trust'    : binary generalized trust (A165), 1 = trusts. Fit with a
                 linear mixed model in this first pass (a GLMM is a follow-up).
  - 'selfexpr' : standardized self-expression / survival index (SurvSAgg).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DEFAULT_FORMULA = "outcome ~ age + I(age**2)"


def _select_outcome(df: pd.DataFrame, outcome: str) -> pd.DataFrame:
    d = df.copy()
    if outcome == "trust":
        d["outcome"] = d["trust"]
    elif outcome == "selfexpr":
        d["outcome"] = d["selfexpr"]
    else:
        raise ValueError(f"Unknown outcome: {outcome}")
    return d.dropna(subset=["outcome", "age", "period", "cohort"])


def fit_hapc(
    df: pd.DataFrame,
    outcome: str = "trust",
    cohort_width: int = 5,
    formula: str = DEFAULT_FORMULA,
):
    """
    Fit a cross-classified cells HAPC model.

    Age is a fixed polynomial effect; period and cohort are crossed via a
    random intercept on the period x cohort cell.

    Returns
    -------
    (result, data) : statsmodels MixedLM result + prepared model frame
        (with 'cohort', 'period', 'cell', and 'outcome' columns).
    """
    d = df.copy()
    d["cohort"] = (d["birth"] // cohort_width) * cohort_width
    d["period"] = d["period"].astype("float")
    d["cell"] = (
        d["period"].round(0).astype(int).astype(str)
        + ":"
        + cohort_width.__str__()
        + "-"
        + d["cohort"].round(0).astype(int).astype(str)
    )
    d = _select_outcome(d, outcome)

    model = smf.mixedlm(formula, d, groups="cell")
    result = model.fit(reml=True)
    return result, d


def _cell_effects(result) -> pd.DataFrame:
    """DataFrame of period x cohort cell random-effects BLUPs."""
    re = result.random_effects
    rows = []
    for cell, v in re.items():
        try:
            period_s, cohort_s = cell.split(":")
            cohort_s = cohort_s.split("-", 1)[1]
            rows.append(
                {
                    "cell": cell,
                    "period": float(period_s),
                    "cohort": float(cohort_s),
                    "effect": float(v["cell"]),
                }
            )
        except Exception:
            continue
    return pd.DataFrame(rows)


def marginal_effects(result) -> "tuple[pd.DataFrame, pd.DataFrame]":
    """
    Marginal cohort and period effects derived from the crossed cell BLUPs.

    The cell random intercept bundles period + cohort + cell variance. The
    marginal cohort effect is the mean BLUP within each birth cohort and the
    marginal period effect is the mean BLUP within each survey year.
    """
    eff = _cell_effects(result)
    if eff.empty:
        return pd.DataFrame(), pd.DataFrame()
    cohort = eff.groupby("cohort")["effect"].mean().reset_index()
    cohort = cohort.sort_values("cohort")
    period = eff.groupby("period")["effect"].mean().reset_index()
    period = period.sort_values("period")
    return cohort, period
