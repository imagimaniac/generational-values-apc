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
| 1 | Foundation: repo, env, data, cleaning pipeline | 🔄 In progress (pipeline skeleton working) |
| 2 | Modeling: indices + HAPC model | ⏳ Not started |
| 3 | Analysis & Visualization: dashboard | ⏳ Not started (skeleton) |
| 4 | Writing & Packaging | ⏳ Not started |
| 5 | Distribution | ⏳ Not started |

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
├── data/
│   ├── raw/                 # WVS raw data (git-ignored — WVS license)
│   └── processed/           # cleaned/intermediate outputs (git-ignored)
├── src/
│   ├── clean.py             # data cleaning pipeline (negatives -> NaN)
│   ├── preprocess.py        # age/period/cohort variable construction
│   ├── apc_model.py         # HAPC model (Phase 2)
│   └── dashboard.py         # Streamlit dashboard (Phase 3)
├── notebooks/               # exploration notebooks
├── docs/
│   ├── data_notes.md        # data provenance + WVS citation + limitations
│   └── wvs_download.md      # how to get the official multi-wave WVS file
├── reports/figures/         # chart outputs
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
mkdir -p data/raw data/processed
curl -L "https://osf.io/download/67pje/" -o data/raw/WVS_subset.csv

# 4. Sanity check the pipeline
pytest -q
python src/preprocess.py
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

> ⚠️ **Limitation:** the current subset is **Wave 7 only** (2017–2023), which
> limits period variation. The pipeline is **multi-wave ready**; to enable a
> full HAPC design, obtain the official 1981–2022 WVS file via the step-by-step
> guide in [docs/wvs_download.md](./docs/wvs_download.md) and drop it into
> `data/raw/`. See also [docs/data_notes.md](./docs/data_notes.md).

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
