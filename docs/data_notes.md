# Data Notes — WVS (official multi-wave time-series)

## Current dataset in use

- **File:** `data/raw/WVS_Time_Series_1981-2022_csv_v5_0.csv`
- **Size:** 1.3 GB &nbsp;|&nbsp; **Rows:** 443,488 &nbsp;|&nbsp; **Columns:** 1,046
- **Waves:** 1–7 &nbsp;|&nbsp; **Survey years:** 1981–2023 &nbsp;|&nbsp; **Countries/territories:** 108
- **Source:** World Values Survey **Time-Series 1981–2022 (v5.0)**, CSV format,
  downloaded from `worldvaluessurvey.org` after a free registration
  (the one manual step, documented in [`docs/wvs_download.md`](wvs_download.md)).
- **Retrieved:** 2026-08-31

The raw and processed data are **git-ignored** because WVS carries a
non-redistribution data-use license. To rebuild the pipeline on a fresh clone,
re-download the file at `data/raw/` (see `docs/wvs_download.md`).

> **Legacy subset:** the earlier curated `WVS_subset.csv` (OSF, Wave-7 only,
> 97,220 rows) is superseded but still supported by the pipeline via its
> `schema="subset"` path. The official time-series is now the primary input.

## Required citation (WVS)

> Haerpfer, C., Inglehart, R., Moreno, A., Welzel, C., Kizilova, K.,
> Diez-Medrano, J., Lagos, M., Norris, P., Ponarin, E. & Puranen, B. (2022).
> *World Values Survey: Round Seven — Country-Pooled Datafile, Version 4.0.0.*
> Madrid & Vienna: JD Systems Institute & WVSA Secretariat.
> DOI: https://doi.org/10.14281/18241.18
>
> (For the time-series: *World Values Survey: All Rounds — Country-Pooled
> Datafile*, JD Systems Institute & WVSA Secretariat.)

## ✅ Migrated to multi-wave — limitation resolved

The earlier Wave-7-only subset could not separate age / period / cohort
effects (no period variation). The official **1981–2022 time-series** now
provides genuine cross-wave period variation, so a full **HAPC** analysis is
runnable. See [`reports/RESULTS.md`](../reports/RESULTS.md).

## Column mapping (official time-series vs the subset)

| Concept | Subset (legacy) | **Official time-series** |
|---|---|---|
| Wave | `a_wave` | `S002VS` |
| Survey year (period) | `a_year` | `S020` |
| Country code | `b_country_alpha` | `S003` (numeric) + `COUNTRY_ALPHA` |
| Age | `q262` | **`X003`** |
| Birth year | derived (`a_year − q262`) | **`X002`** (true birth year) |
| Sex | — | `X001` |
| Weight | — | `S017` |
| Generalized trust | `a165` (recoded) | `A165` (1 = can be trusted) |
| Self-expression index | `survsagg` | `SurvSAgg` |

## Column coding notes

- **Missing / non-response:** WVS codes negatives (`-1` Don't know, `-2` No
  answer, `-3` Not applicable, `-4` Not asked, `-5` Missing). `src/clean.py`
  recodes these to `NaN`.
- **`X003R` / `X003R2` are age-bracket recodes (1–6), NOT birth years** in both
  the official file and the subset. The true birth year is **`X002`** (official
  file). `src/preprocess.py` reads `X002` and only falls back to
  `period − age` where a valid birth year is absent.
- **Birth year** range: 1890–2007; **age** range: 13–103.
- **APC rows** after cleaning/preprocessing: 438,749.

## Pipeline

- `src/clean.py` — reads only the needed columns in chunks (fast on 1.3 GB),
  recodes negatives → NaN, lowercases names. Schema-aware (`subset`/`official`).
- `src/preprocess.py` — builds `period`, `age`, `birth`, `cohort` (5-yr bins by
  default), `wave`, `country`, `weight`, plus `trust`/`selfexpr` outcomes.
- `src/analysis.py` — end-to-end run writing results + charts to `reports/`.
