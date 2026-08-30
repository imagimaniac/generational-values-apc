# Data Notes — WVS Subset

## Current dataset in use

- **File:** `data/raw/WVS_subset.csv`
- **Rows:** 97,220 &nbsp;|&nbsp; **Columns:** 168 &nbsp;|&nbsp; **Countries:** 66
- **Source:** WVS subset curated for the Gabor–Gabor "Doing Data Analysis" materials, hosted on the Open Science Framework.
- **Download URL:** `https://osf.io/download/67pje/`
- **File node (API):** `https://api.osf.io/v2/files/67pje/`
- **SHA-256:** `33be0a38f549e286bccf3d110cce7a53e9c7111096707dc2af569dbb5611301f`
- **Retrieved:** 2026-08-31

The raw and processed data are **git-ignored** because WVS carries a
non-redistribution data-use license. To rebuild the pipeline on a fresh
clone, re-download from the OSF link above into `data/raw/`.

## Required citation (WVS)

When publishing any analysis based on WVS data, credit the source:

> Haerpfer, C., Inglehart, R., Moreno, A., Welzel, C., Kizilova, K.,
> Diez-Medrano, J., Lagos, M., Norris, P., Ponarin, E. & Puranen, B. (2022).
> *World Values Survey: Round Seven — Country-Pooled Datafile, Version 4.0.0.*
> Madrid & Vienna: JD Systems Institute & WVSA Secretariat.
> DOI: https://doi.org/10.14281/18241.18

## ⚠️ Important limitation: Wave 7 only

Although some third-party listings describe this file as spanning
"waves 1–7," inspection of the actual dataset shows **only one wave**:

- `A_WAVE` contains a single value: **7** (surveys 2017–2023)
- `A_YEAR` range: **2017–2023**

### What this means for the APC design
A proper **age–period–cohort** decomposition needs variation across all
three clocks. With a single survey wave there is effectively **no period
variation** across survey rounds — only age and (derived) cohort vary.

- **What we CAN do:** estimate **age** and **cohort** components within the
  wave, and compare cohorts across countries.
- **What we CANNOT rigorously do with this file alone:** fully separate
  period effects from age/cohort effects using cross-wave variation.

### Path to a full APC design
Obtain the **official multi-wave WVS file** via a free registration at
`worldvaluessurvey.org` (a longitudinal 1981–2022 integrated file combining
all 7 waves with a common dictionary). This repo is structured so you can
swap in that file at `data/raw/` and re-run the same pipeline.

- **Step-by-step download guide:** see [`docs/wvs_download.md`](wvs_download.md)
- **Pipeline status:** `src/preprocess.py` is now **multi-wave ready**. It
  resolves the true birth year from `x003r` when present and valid, and falls
  back to `period − age` otherwise, so it runs identically on either the
  Wave-7 subset or the full 1981–2022 file. Default cohort width is **5-year**.

## Column coding notes for this subset

- **`Q262`** — respondent **age** (16–103). This is the variable the
  pipeline uses for age.
- **`X003R`** — in this curated file this is an **age-bracket recode (1–6)**,
  **not** the birth year. (In the full WVS, `X003R` is year of birth; do not
  rely on that here.)
- **`X002_02B`** — birth year; **unpopulated** in this subset.
- **Negative codes** (`-1` to `-5`) are non-response / missing and are recoded
  to `NaN` by `src/clean.py`.
- **Birth year** is derived as `A_YEAR − Q262` in `src/preprocess.py`.
