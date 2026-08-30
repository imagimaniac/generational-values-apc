"""
apc_model.py — Hierarchical Age-Period-Cohort (HAPC) model.

Implements the cross-classified random-effects HAPC model (Bell & Jones
style) using statsmodels MixedLM. Separates age, period, and cohort effects
by treating period and cohort as cross-classified random intercepts while
age enters as a fixed effect (linear + polynomial).

NOTE (Phase 2): This is a working skeleton. The full model needs:
  - A composite outcome index (individualism-collectivism, etc.)
  - Optional random slopes, format/weights considerations
  - Sensitivity checks (alternate cohort widths, specs)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DEFAULT_FORMULA = "outcome ~ age + I(age**2)"


def fit_hapc(
    df: pd.DataFrame,
    formula: str = DEFAULT_FORMULA,
    groups: str = "c(period) + c(cohort)",
):
    """
    Fit a cross-classified random-effects HAPC model.

    Parameters
    ----------
    df : DataFrame containing 'outcome', 'age', 'period', 'cohort'.
    formula : statsmodels-style fixed-effects formula for age.
    groups : random-effects grouping, both period and cohort (cross-classified).

    Returns
    -------
    statsmodels MixedLM results object.
    """
    model = smf.mixedlm(formula, df, groups=groups)
    result = model.fit(reml=True)
    return result


def sensitivity_check(df: pd.DataFrame, cohort_widths=(5, 10, 20)) -> dict:
    """Rerun the HAPC model across cohort bin widths (Phase 2 sensitivity)."""
    from preprocess import add_apc_variables

    results = {}
    for w in cohort_widths:
        d = add_apc_variables(df, cohort_width=w)
        d["cohort"] = d["cohort"].astype("category")
        d["period"] = d["period"].astype("category")
        results[w] = fit_hapc(d)
    return results


if __name__ == "__main__":
    from pathlib import Path

    from clean import clean
    from preprocess import add_apc_variables

    default = Path(__file__).resolve().parents[1] / "data" / "raw" / "WVS_subset.csv"
    df = clean(str(default))
    apc = add_apc_variables(df)
    # Need an outcome column before the model can run (Phase 2 work).
    print("apc_model.py is a skeleton — requires a built outcome index first.")
    print(f"Prepared frame: {len(apc)} rows, {len(apc.columns)} cols, "
          f"{apc['cohort'].nunique()} cohorts, {apc['period'].nunique()} periods")
