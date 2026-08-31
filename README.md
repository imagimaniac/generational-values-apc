# Generational Values — Age-Period-Cohort (APC) Analysis

A code-driven, reproducible analysis of how **individualism, collectivism,
and related value orientations** shift across generational cohorts over time,
using World Values Survey data and a statistically defensible
**Hierarchical Age-Period-Cohort (HAPC)** model — not a pop-sociology
narrative.

This repository is the public home of the research: the pipeline, the model,
the dashboard, and the write-up. It is committed to **daily**, so activity
here is visible and continuous.

---

## Status

| Phase | Focus | Status |
|---|---|---|
| 1 | Foundation: repo, env, data, cleaning pipeline | ✅ Complete (official 1981–2022 data) |
| 2 | Modeling: indices + HAPC model | 🔄 First full HAPC run done (trust + selfexpr) |
| 3 | Analysis & Visualization: dashboard | ⏳ Not started (skeleton) |
| 4 | Writing & Packaging | ⏳ Not started |
| 5 | Distribution | ⏳ Not started |

> Latest results: [`reports/RESULTS.md`](./reports/RESULTS.md)
> Full task breakdown: [generational-values-project-plan.md](./generational-values-project-plan.md)
> Longer-term roadmap: [master-plan-publication-outreach-roadmap.md](./master-plan-publication-outreach-roadmap.md)

---

## What this project is

A claim like "Gen Z is more liberal" conflates three distinct effects:

- **Age effect** — people become less idealistic as they age.
- **Period effect** — a historical event shifts everyone at once.
- **Cohort effect** — a permanent mark on those who came of age at a
  specific time (Mannheim, Inglehart).

This project separates those forces with a cross-classified random-effects
HAPC model on contrast countries **(India, US, Sweden, Japan, Brazil)**.

---

## Repository layout

```
.
├── CONTEXT.md                  # session handoff / current-state snapshot
├── data/
│   ├── raw/                 # WVS raw data (git-ignored — WVS license)
│   └── processed/           # cleaned/intermediate outputs (git-ignored)
├── src/
│   ├── clean.py             # data cleaning pipeline (schema-aware, chunked)
│   ├── preprocess.py        # APC variables + outcomes construction
│   ├── apc_model.py         # HAPC cross-classified model
│   ├── analysis.py          # end-to-end run -> results + charts
│   └── dashboard.py         # Streamlit dashboard (Phase 3)
├── notebooks/               # exploration notebooks
├── docs/
│   ├── data_notes.md        # data provenance + WVS citation + column map
│   └── wvs_download.md      # how to get the official multi-wave WVS file
├── reports/                 # results (CSV) + charts; RESULTS.md summary
├── tests/                   # pytest suite
├── requirements.txt         # Python dependencies
└── README.md
```

---

## Setup

Requires Python 3.10+.

```bash
# 1. Create the virtual environment
python -m venv .venv
source .venv/bin/activate        # (Windows: .venv\Scripts\activate)

# 2. Install dependencies
pip install -r requirements.txt

# 3. Get the data (WVS has a non-redistribution license, so it's git-ignored)
#    Official 1981-2022 time-series (one free registration; see docs/wvs_download.md)
mkdir -p data/raw data/processed
# ...place WVS_Time_Series_1981-2022_csv_v5_0.csv in data/raw/

# 4. Sanity check the pipeline
pytest -q
python src/preprocess.py

# 5. Run the full HAPC analysis (writes results + charts to reports/)
python src/analysis.py
```

---

## Usage

```bash
# Clean the raw data (recode non-response to missing)
python src/clean.py

# Build age / period / cohort variables
python src/preprocess.py

# Launch the dashboard (Phase 3)
streamlit run src/dashboard.py
```

---

## Data & citation

- Data source and column-coding notes: [docs/data_notes.md](./docs/data_notes.md)
- **Citation:** Haerpfer, C., Inglehart, R., Moreno, A., Welzel, C.,
  Kizilova, K., Diez-Medrano, J., Lagos, M., Norris, P., Ponarin, E. &
  Puranen, B. (2022). *World Values Survey: Round Seven — Country-Pooled
  Datafile, Version 4.0.0.* JD Systems Institute & WVSA Secretariat.
  DOI: <https://doi.org/10.14281/18241.18>

> ℹ️ **Data note:** the project uses the official **WVS 1981–2022 time-series**
> (7 waves, 108 countries), which provides genuine period variation for the
> HAPC model. Obtain the file via [docs/wvs_download.md](./docs/wvs_download.md);
> it is git-ignored per the WVS license.

---

## Daily publishing convention

This repo exists to build a **visible, consistent daily activity record**.
Commit something small and meaningful every day — a chart, an index update,
a note — with a dated message:

```
Publish: 2026-08-31 — scaffold repo + working cleaning pipeline
```

---

## License / use note

The analysis code is this repository's own work. The underlying WVS data is
subject to the World Values Survey non-redistribution data-use license; raw
data is intentionally not committed here.
