"""
analysis.py — end-to-end run: clean -> preprocess -> HAPC fit -> results/charts.

Runs the full multi-wave WVS 1981-2022 pipeline, fits the HAPC model for the
`trust` and `selfexpr` outcomes across cohort-width sensitivity checks, and
writes results tables + charts to reports/.

Usage (from repo root):
    python src/analysis.py [raw_csv_path] [--quick]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

import clean
import preprocess
from apc_model import fit_hapc, marginal_effects

REPO = Path(__file__).resolve().parents[1]
RAW_DEFAULT = REPO / "data" / "raw" / "WVS_Time_Series_1981-2022_csv_v5_0.csv"
FIGDIR = REPO / "reports" / "figures"
OUTDIR = REPO / "reports"


def load_data(path: Path, quick: bool = False) -> pd.DataFrame:
    df = clean.clean(str(path))
    apc = preprocess.add_apc_variables(df)
    apc = preprocess.add_outcomes(apc)
    if quick:
        apc = apc.dropna(subset=["trust", "age", "period", "birth"]).sample(
            150_000, random_state=7
        )
    return apc


def run_outcome(
    apc: pd.DataFrame,
    outcome: str,
    cohort_width: int,
    out_prefix: str,
) -> None:
    res, data = fit_hapc(apc, outcome=outcome, cohort_width=cohort_width)

    # ---- fixed (age) effects ----
    tbl = res.summary().tables[1]  # already a DataFrame in statsmodels 0.15
    fixed = tbl.reset_index() if not isinstance(tbl.index, pd.RangeIndex) else tbl
    fixed.to_csv(OUTDIR / f"{out_prefix}_fixed.csv", index=False)

    # ---- marginal cohort + period effects ----
    cohort, period = marginal_effects(res)
    cohort.to_csv(OUTDIR / f"{out_prefix}_cohort.csv", index=False)
    period.to_csv(OUTDIR / f"{out_prefix}_period.csv", index=False)

    # ---- variance component ----
    cov = res.cov_re
    vc = float(cov.to_numpy()[0, 0]) if hasattr(cov, "to_numpy") else float(cov[0, 0])
    with open(OUTDIR / f"{out_prefix}_variance.txt", "w") as fh:
        fh.write(f"period_x_cohort cell variance component: {vc:.6f}\n")

    # ---- charts ----
    _chart_cohort(cohort, outcome, cohort_width, out_prefix)
    _chart_period(period, outcome, cohort_width, out_prefix)
    _chart_age(apc, outcome, out_prefix)

    print(f"[{outcome} w={cohort_width}] model rows={len(data)} cells="
          f"{len(res.random_effects)}")


def _chart_cohort(cohort, outcome, cohort_width, prefix):
    plt.figure(figsize=(7, 4))
    plt.plot(cohort["cohort"], cohort["effect"], marker="o", ms=3, lw=1.4)
    plt.axhline(0, color="grey", lw=0.8, ls="--")
    plt.xlabel("Birth cohort (start year)")
    plt.ylabel("Marginal HAPC cohort effect")
    plt.title(f"{outcome.title()} cohort effect ({cohort_width}-yr cohorts)")
    plt.tight_layout()
    plt.savefig(FIGDIR / f"{prefix}_cohort.png", dpi=130)
    plt.close()


def _chart_period(period, outcome, cohort_width, prefix):
    plt.figure(figsize=(7, 4))
    plt.plot(period["period"], period["effect"], marker="o", ms=3, lw=1.4)
    plt.axhline(0, color="grey", lw=0.8, ls="--")
    plt.xlabel("Survey year")
    plt.ylabel("Marginal HAPC period effect")
    plt.title(f"{outcome.title()} period effect")
    plt.tight_layout()
    plt.savefig(FIGDIR / f"{prefix}_period.png", dpi=130)
    plt.close()


def _chart_age(apc, outcome, prefix):
    # descriptive age profile (mean outcome by age) — quick visual
    d = apc.dropna(subset=["age", outcome])
    yrs = pd.to_numeric(d["age"], errors="coerce")
    if outcome == "trust":
        m = d["trust"].astype(float)
    else:
        m = d["selfexpr"].astype(float)
    agg = pd.DataFrame({"age": yrs, "m": m}).dropna().groupby("age")["m"].mean()
    plt.figure(figsize=(7, 4))
    plt.plot(agg.index, agg.values, lw=1.2)
    plt.xlabel("Age")
    plt.ylabel(f"Mean {outcome}")
    plt.title(f"{outcome.title()} by age (descriptive)")
    plt.tight_layout()
    plt.savefig(FIGDIR / f"{prefix}_age.png", dpi=130)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=str(RAW_DEFAULT))
    parser.add_argument("--quick", action="store_true")
    args = parser.parse_args()

    FIGDIR.mkdir(parents=True, exist_ok=True)
    OUTDIR.mkdir(parents=True, exist_ok=True)

    print("Loading + cleaning + preprocessing...")
    apc = load_data(Path(args.path), quick=args.quick)
    print(f"  APC frame: {len(apc)} rows")

    widths = [5] if args.quick else [5, 10, 20]
    for w in widths:
        print(f"--- cohort width = {w} ---")
        run_outcome(apc, "trust", w, f"hapc_trust_w{w}")
        run_outcome(apc, "selfexpr", w, f"hapc_selfexpr_w{w}")

    print("Done. Results in reports/, charts in reports/figures/.")


if __name__ == "__main__":
    main()
