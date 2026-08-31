"""Tests for the APC preprocessing (official multi-wave schema)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.preprocess import DEFAULT_COHORT_WIDTH, add_apc_variables, add_outcomes


def _frame(birth_years=None, ages=None) -> pd.DataFrame:
    """A synthetic official-schema multi-wave frame (s020/x003/x002)."""
    n = 5
    return pd.DataFrame(
        {
            "s020": [1990, 2000, 2010, 2020, 1981],          # period (survey year)
            "x003": ages if ages is not None else [40, 50, 60, 30, 55],  # age
            "x002": birth_years if birth_years is not None else [1950, 1950, 1950, 1990, 1926],
            "s002vs": [3, 4, 5, 7, 2],                       # wave
            "s003": [356, 840, 752, 392, 76],                # country code
        }
    )


def test_uses_true_birth_year_when_valid():
    df = _frame()
    out = add_apc_variables(df)
    # x002 holds real birth years; they must be used as the birth year.
    expected_birth = df["x002"].astype("float")
    pd.testing.assert_series_equal(
        out["birth"].round(0), expected_birth.round(0), check_names=False
    )
    # Cohort width default is 5 -> 5-year bins.
    expected_cohort = (expected_birth // 5) * 5
    pd.testing.assert_series_equal(
        out["cohort"].round(0), expected_cohort.round(0), check_names=False
    )
    # period and age come from official columns.
    pd.testing.assert_series_equal(
        out["period"].round(0), df["s020"].astype("float").round(0), check_names=False
    )
    pd.testing.assert_series_equal(
        out["age"].round(0), df["x003"].astype("float").round(0), check_names=False
    )


def test_falls_back_to_derived_birth_when_x002_missing():
    # x002 all missing -> birth derived as period - age.
    df = _frame(birth_years=[np.nan] * 5)
    out = add_apc_variables(df)
    expected_birth = df["s020"].astype("float") - df["x003"].astype("float")
    pd.testing.assert_series_equal(
        out["birth"].round(0), expected_birth.round(0), check_names=False
    )


def test_adds_period_age_birth_cohort_wave_country():
    out = add_apc_variables(_frame())
    for col in ("period", "age", "birth", "cohort", "wave", "country"):
        assert col in out.columns


def test_ignores_age_bracket_x003r_for_birth():
    # x003r is an age bracket (1-6), never used for birth even if present.
    df = _frame()
    df["x003r"] = [1, 2, 3, 4, 5]
    out = add_apc_variables(df)
    expected_birth = df["x002"].astype("float")
    pd.testing.assert_series_equal(
        out["birth"].round(0), expected_birth.round(0), check_names=False
    )


def test_default_cohort_width_is_5():
    assert DEFAULT_COHORT_WIDTH == 5


def test_add_outcomes_trust_and_selfexpr():
    df = pd.DataFrame({"a165": [1, 2, 1, -1]})
    out = add_outcomes(df)
    # A165: 1 = trusts -> 1; 2 = careful -> 0; -1 missing -> NaN
    tr = out["trust"].tolist()
    assert tr[0] == 1.0 and tr[1] == 0.0 and tr[2] == 1.0
    assert pd.isna(tr[3])


def test_add_outcomes_handles_missing_trust_col():
    df = pd.DataFrame({"survsagg": [0.5, -1.2, 2.0]})
    out = add_outcomes(df)
    assert "selfexpr" in out.columns
    assert "trust" not in out.columns  # a165 absent -> no trust column
