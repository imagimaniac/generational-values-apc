"""
clean.py — Data cleaning pipeline for the generational-values APC project.

Harmonizes the World Values Survey subset into a clean, analysis-ready
long format for the age-period-cohort model.

WVS codes negative values (-1 to -5) to represent non-answers:
    -1 Don't know / -2 No answer / -3 Not applicable / -4 Not asked /
    -5 Missing. We recode these to NaN.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

# WVS negative codes represent missing / non-response
WVS_MISSING_NEGATIVE = tuple(range(-5, 0))

# Identity / structural columns we carry through (not survey items)
IDENTITY_COLUMNS = [
    "B_COUNTRY",
    "B_COUNTRY_ALPHA",
    "C_COW_NUM",
    "C_COW_ALPHA",
    "D_INTERVIEW",
    "A_YEAR",
    "A_WAVE",
    "A_STUDY",
    "S025",
    "W_WEIGHT",
    "S018",
]


def read_raw(path: str | Path) -> pd.DataFrame:
    """Load the raw WVS subset CSV."""
    return pd.read_csv(path, low_memory=False)


def recode_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Replace WVS negative non-response codes with NaN for numeric columns."""
    out = df.copy()
    for col in out.columns:
        if out[col].dtype.kind in "iuf":
            out[col] = out[col].replace(WVS_MISSING_NEGATIVE, np.nan)
    return out


def clean(path: str | Path) -> pd.DataFrame:
    """
    End-to-end raw -> clean transformation.

    Returns a DataFrame with missing values recoded to NaN and column
    names normalized to lowercase.
    """
    df = read_raw(path)
    df = recode_missing(df)
    df.columns = [c.lower() for c in df.columns]
    return df


if __name__ == "__main__":
    import sys

    default = Path(__file__).resolve().parents[1] / "data" / "raw" / "WVS_subset.csv"
    src = sys.argv[1] if len(sys.argv) > 1 else str(default)
    out = clean(src)
    print(f"Cleaned {len(out)} rows x {len(out.columns)} cols")
    print(f"Waves: {sorted(out['a_wave'].dropna().unique().tolist())}")
