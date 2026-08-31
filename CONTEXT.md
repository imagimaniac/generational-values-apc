# CONTEXT.md — Project handoff snapshot

> Read this first in any new session. It is the current-state summary of the
> **Outreach-v2 / generational-values-apc** work. Full history lives in the
> git log and the plan docs; this file is the "what changed + where are we".

---

## 1. What this is

A daily-publishing research project: **Age–Period–Cohort (APC) analysis of
generational values** using the World Values Survey, hosted publicly at
`https://github.com/imagimaniac/generational-values-apc`.

Two folders exist everywhere:
- **`Outreach-v2/publishing/`** — the git repo (= the public GitHub project) + code.
- **`Outreach-v2/workspace/`** — everything else (HTML originals of plans, notes).
- **`Outreach-v2/sync.sh`** — enforces the **SYNC RULE**: *every edit to a
  common file must be reflected in BOTH folders.* `COMMON_FILES` list at top.

## 2. Current status (as of Session 2 — 2026-08-31)

**Migration to multi-wave data COMPLETE. First HAPC analysis done + pushed.**

| What | State |
|---|---|
| Repo scaffold + pushed to GitHub | ✅ |
| Official WVS 1981–2022 file loaded (443K rows, 7 waves, 108 countries) | ✅ done |
| Clean pipeline (`src/clean.py`, schema-aware, chunked) | ✅ works, tested |
| Preprocess (`src/preprocess.py`, multi-wave APC vars + outcomes) | ✅ |
| Full HAPC model fitted (trust + self-expression, 5/10/20-yr cohorts) | ✅ |
| Results + charts in `reports/` + `reports/RESULTS.md` | ✅ |
| Tests (7) | ✅ passing |
| **Headline finding** | trust declines across cohorts (younger = less trust), robust to cohort width |

## 3. Manual step — DONE

The one manual download (WVS registration) is complete: the official
1981–2022 CSV is at `data/raw/`. No further manual data steps remain.

## 4. Key facts & decisions (context you must know)

- **Current raw data is the official multi-wave WVS 1981–2022** (443,488 rows,
  7 waves, 108 countries, 1981–2023) at `data/raw/WVS_Time_Series_...csv`.
  Genuine period variation → full HAPC possible. (Legacy Wave-7-only subset
  still supported via `clean(..., schema="subset")`.)
- **`X003R`/`X003R2` are age-bracket recodes (1–6), NOT birth year, in BOTH
  the subset and the official file.** The true birth year is `X002` (official
  file); age is `X003`. `preprocess.py` reads `X002` and falls back to
  `period − age` when absent.
- **Cohort bins default to 5-year** (APC standard); sensitivity at 10/20.
- **HAPC implementation = cross-classified period × cohort CELL model**
  (age fixed polynomial; random intercept on the period × cohort cell),
  fitted with statsmodels MixedLM. See `src/apc_model.py` + `reports/RESULTS.md`.
- **GitHub identity in `publishing/` only:** name `Pratik Hagawane`, email
  `87967129+imagimaniac@users.noreply.github.com`. Global git untouched.
- **gh auth = `imagimaniac`** (scopes include repo/projects). Remote is SSH.
- **WVS license:** non-redistribution. `data/raw` + `data/processed` are
  git-ignored and never pushed. Citation in `docs/data_notes.md`.
- **Profile / repo hygiene done:** 4 forks archived, 3 repos made private,
  1 project made private. Pinning flagships is a **manual GitHub UI step**.
- **Default analysis outcome = generalized trust (A165)** — used in the first
  HAPC run; `selfexpr` (SurvSAgg) as robustness. Non-urgent open question:
  should I build the individualism–collectivism battery from scratch next?

## 5. Commands / environment

```bash
cd /Users/impro/Projects/CV/outreach/Outreach-v2/publishing
.venv/bin/python -m pytest -q          # 7 tests, should pass
.venv/bin/python src/preprocess.py     # prints APC rows/ranges
cd /Users/impro/Projects/CV/outreach/Outreach-v2
./sync.sh check                        # verify common-file sync
./sync.sh                              # mirror newest common files
```

Commit convention (publishing/): `Publish: <date> — <summary>`, then `git push`.
Branch: `main`, remote: `origin` = `git@github.com:imagimaniac/generational-values-apc.git`.

## 6. Next steps (for the next session)

1. Refine the model: generalized (logistic) mixed model for binary trust,
   apply survey weights (`S017`), run the analysis for the 5 contrast
   countries (India/US/Sweden/Japan/Brazil).
2. Build the interactive Streamlit dashboard on the real HAPC results
   (`src/dashboard.py` is a skeleton).
3. Deeper write-up + more outcomes (individualism-collectivism battery).

*Sister docs: `publishing/generational-values-project-plan.md` (tasks),
`publishing/master-plan-publication-outreach-roadmap.md` (long-term).*