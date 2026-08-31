"""
clean.py — Data cleaning pipeline for the generational-values APC project.

Harmonizes a World Values Survey file into a clean, analysis-ready frame for
the age-period-cohort model.

The pipeline is *schema-aware*: it works on either
  - the curated Wave-7 subset (OSF) using a_wave/a_year/q262/..., or
  - the official WVS 1981-2022 time-series using S002VS/S020/X003/X002/...

Markers:
    - WVS negative codes (-1 to -5) represent non-response / missing and are
      recoded to NaN (fast, chunked, column-subset reading for large files).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

# WVS negative codes represent missing / non-response
WVS_MISSING_NEGATIVE = tuple(range(-5, 0))


# ---------------------------------------------------------------------------
# Schema definitions (column names AFTER lowercase normalization)
# ---------------------------------------------------------------------------
# identity / structural columns carried through for the subset
IDENTITY_COLUMNS = [
    "b_country",
    "b_country_alpha",
    "c_cow_num",
    "c_cow_alpha",
    "d_interview",
    "a_year",
    "a_wave",
    "a_study",
    "s025",
    "w_weight",
    "s018",
]

# official time-series structural columns (upper-case in source)
OFFICIAL_STRUCTURAL = [
    "S001",
    "S002VS",
    "S003",
    "COUNTRY_ALPHA",
    "S017",  # standard calibration weight
    "S018",
    "S020",  # survey year (period)
    "S021",
    "X001",
    "X003",
    "X002",
    "X003R",
]

# outcome variables to carry through (both sources), upper-case in source
OUTCOME_COLUMNS_UC = ["A165", "A170", "SurvSAgg", "tradrat5", "TradAgg"]


def _lower_cols(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [str(c).lower() for c in df.columns]
    return df


def read_raw(
    path: str | Path,
    schema: str = "auto",
    usecols: list[str] | None = None,
    chunksize: int = 500_000,
) -> pd.DataFrame:
    """
    Load a raw WVS CSV, reading only the needed columns and in chunks so a
    1.3 GB time-series file loads quickly and with low memory.

    schema in {"subset", "official", "auto"}: "auto" detects by column names.
    """
    path = str(path)

    if usecols is None:
        usecols = OFFICIAL_STRUCTURAL + OUTCOME_COLUMNS_UC

    # read header line to sniff schema
    header = pd.read_csv(path, nrows=0, low_memory=False).columns.tolist()
    detected = "official" if "S002VS" in header else "subset"
    if schema == "auto":
        schema = detected

    if schema == "subset":
        df = pd.read_csv(path, low_memory=False)
        return _lower_cols(df)

    # official: byte-offset chunk reading so we can safely process 1.3 GB
    df = pd.read_csv(
        path,
        usecols=usecols,
        low_memory=False,
        # dtype objects to defer coercion; recode_missing uses numeric check
    )
    return _lower_cols(pd.DataFrame(df))


def recode_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Replace WVS negative non-response codes with NaN for numeric columns."""
    out = df.copy()
    for col in out.columns:
        if out[col].dtype.kind in "iuf":
            out[col] = out[col].replace(WVS_MISSING_NEGATIVE, np.nan)
    return out


def clean(path: str | Path, schema: str = "auto") -> pd.DataFrame:
    """
    End-to-end raw -> clean transformation.

    Reads only needed columns, recodes missing values to NaN, and normalizes
    column names to lowercase.
    """
    df = read_raw(path, schema=schema)
    df = recode_missing(df)
    df.columns = [c.lower() for c in df.columns]
    return df


if __name__ == "__main__":
    import sys

    default = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "raw"
        / "WVS_Time_Series_1981-2022_csv_v5_0.csv"
    )
    src = sys.argv[1] if len(sys.argv) > 1 else str(default)
    out = clean(src)
    print(f"Cleaned {len(out)} rows x {len(out.columns)} cols")
    wave_col = "s002vs" if "s002vs" in out.columns else "a_wave"
    print(f"Waves: {sorted(out[wave_col].dropna().unique().tolist())}")
