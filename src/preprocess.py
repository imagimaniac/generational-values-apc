"""
preprocess.py — Construct cohort and period variables for the APC model.

Given a cleaned WVS frame, builds:
    period  : survey year (A_YEAR)
    age     : respondent age at interview
    birth   : birth year (taken directly, or derived as period - age)
    cohort  : birth-year cohort bins (configurable width)

Birth-year resolution (multi-wave aware):
    - The official WVS 1981-2022 time-series stores year of birth in `x003r`;
      when present and valid (roughly 1900 <= x003r <= period, and not a small
      age-bracket code), use it directly.
    - Otherwise (e.g. some curated subsets where `x003r` is an age-bracket and
      `x002_02b` birth year is empty) fall back to deriving birth as
      period - age via `q262`.

APC identification note: age = period - cohort is an exact linear dependency,
central to the age-period-cohort problem. Period and cohort are treated as
cross-classified random effects in the HAPC model.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# WVS columns this pipeline depends on (lowercased by clean.py)
PERIOD_COL = "a_year"
AGE_COL = "q262"  # age at interview
BIRTH_YEAR_COLS = ["x003r", "x002_02b"]  # candidate birth-year columns (in priority order)

# Default cohort bin width in years (5-year bins are standard for APC)
DEFAULT_COHORT_WIDTH = 5


def _resolve_birth_year(df: pd.DataFrame) -> pd.Series:
    """
    Return a birth-year series, using the true birth year if available,
    otherwise deriving it as period - age.

    The WVS full time-series stores year of birth in x003r. Some curated
    subsets instead store an age-bracket (1-6) there, so we validate before
    trusting it. A plausible birth year must be in [1900, period].
    """
    period = df[PERIOD_COL].astype("float")

    birth = pd.Series(np.nan, index=df.index, dtype="float64")
    for col in BIRTH_YEAR_COLS:
        if col in df.columns:
            candidate = pd.to_numeric(df[col], errors="coerce").astype("float")
            # Reject values that are clearly age-bracket codes (1-6) or
            # out of range for a birth year.
            plausible = candidate.between(1900, period)
            if plausible.any():
                birth = birth.mask(plausible, candidate[plausible])

    # Where no valid birth year was found, derive from age and period.
    has_age = df[AGE_COL].notna() & period.notna()
    if "birth" not in df.columns:
        derived = period - df[AGE_COL].astype("float")
        birth = birth.mask(birth.isna() & has_age, derived)

    return birth


def add_apc_variables(
    df: pd.DataFrame,
    cohort_width: int = DEFAULT_COHORT_WIDTH,
) -> pd.DataFrame:
    """
    Add period, age, birth-year, and cohort columns.

    Rows lacking a valid age and period are dropped (required for cohort).
    """
    out = df.copy()

    out["period"] = out[PERIOD_COL].astype("float")
    out["age"] = pd.to_numeric(out[AGE_COL], errors="coerce").astype("float")
    out["birth"] = _resolve_birth_year(out)
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
