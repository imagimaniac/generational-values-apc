"""
preprocess.py — Construct cohort and period variables for the APC model.

Given a cleaned WVS frame, builds:
    period  : survey year (S020 / A_YEAR)
    age     : respondent age at interview (X003 / Q262)
    birth   : birth year (X002, or derived as period - age when absent)
    cohort  : birth-year cohort bins (configurable width)
    country : country code (S003 / B_COUNTRY_ALPHA)
    wave    : survey wave (S002VS / A_WAVE)

Birth-year resolution (schema & bracket aware):
    - The official WVS 1981-2022 time-series stores the true birth year in
      `x002`. Prefer that when present and valid (1900 <= x002 <= period).
    - `x003r`/`x003r2` are *age-bracket recodes (1-6)*, NOT birth years, in
      both sources — they are never used for birth.
    - When no valid birth year exists, derive birth = period - age via `x003`.

APC identification note: age = period - cohort is an exact linear dependency,
central to the age-period-cohort problem. Period and cohort are treated as
cross-classified random effects in the HAPC model.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# Column mapping for the APC variables (lowercased by clean.py)
PERIOD_COL = "s020"          # official time-series survey year
AGE_COL = "x003"             # official time-series respondent age
BIRTH_YEAR_COL = "x002"      # official time-series year of birth
WAVE_COL = "s002vs"          # official time-series wave
COUNTRY_COL = "s003"         # numeric country code
COUNTRY_ALPHA_COL = "country_alpha"
WEIGHT_COL = "s017"          # standard calibration weight

# Default cohort bin width in years (5-year bins are standard for APC)
DEFAULT_COHORT_WIDTH = 5


def _resolve_birth_year(df: pd.DataFrame) -> pd.Series:
    """
    Return a birth-year series, preferring the true birth year (x002) when
    present and valid, otherwise deriving it as period - age.
    """
    period = pd.to_numeric(df[PERIOD_COL], errors="coerce").astype("float")
    birth = pd.Series(np.nan, index=df.index, dtype="float64")

    if BIRTH_YEAR_COL in df.columns:
        candidate = pd.to_numeric(df[BIRTH_YEAR_COL], errors="coerce").astype("float")
        # valid birth years must fall in [1900, period]
        plausible = candidate.between(1900, period) & period.notna()
        birth = birth.mask(plausible, candidate)

    # Where no valid birth year was found, derive from age and period.
    age = pd.to_numeric(df[AGE_COL], errors="coerce").astype("float")
    has_age = age.notna() & period.notna()
    derived = period - age
    birth = birth.mask(birth.isna() & has_age, derived)
    return birth


def add_apc_variables(
    df: pd.DataFrame,
    cohort_width: int = DEFAULT_COHORT_WIDTH,
) -> pd.DataFrame:
    """
    Add period, age, birth-year, cohort, wave, and country columns.

    Rows lacking both a valid age and period are dropped (cohort requires
    at least one of birth year or age+period).
    """
    out = df.copy()

    out["period"] = pd.to_numeric(out[PERIOD_COL], errors="coerce").astype("float")
    out["age"] = pd.to_numeric(out[AGE_COL], errors="coerce").astype("float")
    out["birth"] = _resolve_birth_year(out)
    out["cohort"] = (out["birth"] // cohort_width) * cohort_width

    out["wave"] = out[WAVE_COL] if WAVE_COL in out.columns else np.nan
    out["country"] = out[COUNTRY_COL] if COUNTRY_COL in out.columns else np.nan
    if COUNTRY_ALPHA_COL in out.columns:
        out["country_alpha"] = out[COUNTRY_ALPHA_COL]
    if WEIGHT_COL in out.columns:
        out["weight"] = pd.to_numeric(out[WEIGHT_COL], errors="coerce")

    before = len(out)
    out = out.dropna(subset=[AGE_COL, PERIOD_COL])
    print(f"Dropped {before - len(out)} rows without a valid age/period")

    return out


def add_outcomes(df: pd.DataFrame, trust_col: str = "a165") -> pd.DataFrame:
    """
    Build analysis outcome variables.

    - `trust`: binary generalized trust (A165). In WVS, 1 = "most people can
      be trusted", 2 = "can't be too careful". Recoded to 1/0 (1 = trusts).
    - `selfexpr`: standardized self-expression / survival index (SurvSAgg).
    Missing / negative values (already NaN) stay missing.
    """
    out = df.copy()

    if trust_col in out.columns:
        trust = pd.to_numeric(out[trust_col], errors="coerce")
        out["trust"] = np.where(trust == 1, 1.0, np.where(trust == 2, 0.0, np.nan))

    if "survsagg" in out.columns:
        se = pd.to_numeric(out["survsagg"], errors="coerce")
        out["selfexpr"] = (se - se.mean()) / se.std()

    return out


if __name__ == "__main__":
    import sys
    from pathlib import Path

    from clean import clean

    default = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "raw"
        / "WVS_Time_Series_1981-2022_csv_v5_0.csv"
    )
    src = sys.argv[1] if len(sys.argv) > 1 else str(default)

    df = clean(src)
    apc = add_apc_variables(df)
    print(f"APC rows: {len(apc)}")
    print(f"Period range: {int(apc['period'].min())} - {int(apc['period'].max())}")
    print(f"Age range: {int(apc['age'].min())} - {int(apc['age'].max())}")
    print(f"Birth range: {int(apc['birth'].min())} - {int(apc['birth'].max())}")
    print(f"Waves: {sorted(apc['wave'].dropna().unique().tolist())}")
    print(f"Countries: {apc['country'].nunique()}")
    print(f"Cohorts: {sorted(apc['cohort'].dropna().unique().tolist())[:8]}...")
