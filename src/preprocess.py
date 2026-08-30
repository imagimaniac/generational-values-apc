"""
preprocess.py — Construct cohort and period variables for the APC model.

Given a cleaned WVS frame, builds:
    period  : survey year (A_YEAR)
    age     : respondent age at interview (Q262 in this curated subset)
    birth   : derived birth year (period - age)
    cohort  : birth-year cohort bins (configurable width)

Data note: in the curated OSF/gabors WVS_subset (Wave 7), the raw X003R
column is an age-bracket recode (1-6), not a birth year, and X002_02B
(birth year) is unpopulated. We therefore take age from Q262 and derive
the birth year as period - age.

APC identification note: age = period - cohort is an exact linear dependency,
central to the age-period-cohort problem. Period and cohort are treated as
cross-classified random effects in the HAPC model.
"""

from __future__ import annotations

import pandas as pd

# WVS columns this pipeline depends on (lowercased by clean.py)
PERIOD_COL = "a_year"
AGE_COL = "q262"  # age at interview in this curated subset

# Default cohort bin width in years (10-year generations is a common choice)
DEFAULT_COHORT_WIDTH = 10


def add_apc_variables(
    df: pd.DataFrame,
    cohort_width: int = DEFAULT_COHORT_WIDTH,
) -> pd.DataFrame:
    """
    Add period, age, derived birth-year, and cohort columns.

    Rows lacking a valid age or period are dropped (required for cohort).
    """
    out = df.copy()

    out["period"] = out[PERIOD_COL]
    out["age"] = out[AGE_COL].astype("float")
    out["birth"] = out["period"] - out["age"]

    # Cohort labeled by the start of the birth-year bin.
    out["cohort"] = (out["birth"] // cohort_width) * cohort_width

    before = len(out)
    out = out.dropna(subset=[AGE_COL, PERIOD_COL])
    print(f"Dropped {before - len(out)} rows without a valid age/period")

    return out


if __name__ == "__main__":
    import sys
    from pathlib import Path

    from clean import clean

    default = Path(__file__).resolve().parents[1] / "data" / "raw" / "WVS_subset.csv"
    src = sys.argv[1] if len(sys.argv) > 1 else str(default)

    df = clean(src)
    apc = add_apc_variables(df)
    print(f"APC rows: {len(apc)}")
    print(f"Period range: {int(apc['period'].min())} - {int(apc['period'].max())}")
    print(f"Age range: {int(apc['age'].min())} - {int(apc['age'].max())}")
    print(f"Birth range: {int(apc['birth'].min())} - {int(apc['birth'].max())}")
    print(f"Cohorts: {sorted(apc['cohort'].dropna().unique().tolist())}")
