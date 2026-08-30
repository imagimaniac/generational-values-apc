"""Tests for the data cleaning pipeline."""

from __future__ import annotations

import pandas as pd
import pytest

from src.clean import IDENTITY_COLUMNS, clean, recode_missing


def _sample_frame() -> pd.DataFrame:
    """A tiny synthetic frame mirroring WVS coding (negative = missing)."""
    return pd.DataFrame(
        {
            "B_COUNTRY_ALPHA": ["IND", "IND", "JPN"],
            "A_WAVE": [7, 7, 7],
            "Q1": [1, -1, 3],      # -1 = missing (don't know)
            "Q2": [2, -2, 4],      # -2 = missing
            "Q3": [-5, 1, 2],      # -5 = missing
        }
    )


def test_recode_negative_to_nan():
    df = _sample_frame()
    out = recode_missing(df)
    # Survey items should have negatives -> NaN
    assert out["Q1"].isna().tolist() == [False, True, False]
    assert out["Q2"].isna().tolist() == [False, True, False]
    assert out["Q3"].isna().tolist() == [True, False, False]
    # Identity column kept as-is
    assert out["B_COUNTRY_ALPHA"].tolist() == ["IND", "IND", "JPN"]


def test_clean_lowercases_columns(tmp_path):
    raw = tmp_path / "raw.csv"
    _sample_frame().to_csv(raw, index=False)
    df = clean(raw)
    assert all(c == c.lower() for c in df.columns)
    assert "q1" in df.columns


def test_clean_does_not_drop_identity():
    df = clean_from_frame(_sample_frame())
    assert "b_country_alpha" in df.columns


def clean_from_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Helper: run recode + lowercase without needing a file."""
    out = recode_missing(df)
    out.columns = [c.lower() for c in out.columns]
    return out
