"""Tests for the APC preprocessing (multi-wave birth-year resolution)."""

from __future__ import annotations

import pandas as pd
import pytest

from src.preprocess import add_apc_variables


def _frame(birth_years=None, ages=None) -> pd.DataFrame:
    """A synthetic multi-wave frame with a real birth-year column (x003r)."""
    n = 5
    return pd.DataFrame(
        {
            "a_year": [1990, 2000, 2010, 2020, 1981],
            "q262": ages if ages is not None else [40, 50, 60, 30, 55],
            "x003r": birth_years if birth_years is not None else [1950, 1950, 1950, 1990, 1926],
        }
    )


def test_uses_true_birth_year_when_valid():
    df = _frame()
    out = add_apc_variables(df)
    # x003r holds real birth years; those must be used as the birth year.
    expected_birth = df["x003r"].astype("float")
    pd.testing.assert_series_equal(
        out["birth"].round(0), expected_birth.round(0), check_names=False
    )
    # Cohort width default is 5 -> 5-year bins on the birth year.
    expected_cohort = (expected_birth // 5) * 5
    pd.testing.assert_series_equal(
        out["cohort"].round(0), expected_cohort.round(0), check_names=False
    )


def test_falls_back_to_derived_birth_when_x003r_is_age_bracket():
    # Simulate the curated subset where x003r is an age-bracket (1-6).
    df = _frame(birth_years=[1, 2, 3, 4, 5])
    out = add_apc_variables(df)
    # Invalid (bracket) birth years are ignored; birth = period - age.
    expected_birth = df["a_year"].astype("float") - df["q262"].astype("float")
    pd.testing.assert_series_equal(
        out["birth"].round(0), expected_birth.round(0), check_names=False
    )


def test_adds_period_age_birth_cohort_columns():
    out = add_apc_variables(_frame())
    for col in ("period", "age", "birth", "cohort"):
        assert col in out.columns


def test_default_cohort_width_is_5():
    from src.preprocess import DEFAULT_COHORT_WIDTH

    assert DEFAULT_COHORT_WIDTH == 5
