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

## 2. Current status (as of end of Session 1 — 2026-08-31)

**Phase 1 is ~done. We are mid-migration to multi-wave data.**

| What | State |
|---|---|
| Repo scaffold + pushed to GitHub | ✅ |
| Clean pipeline (`src/clean.py`, negatives→NaN) | ✅ works, tested |
| Preprocess (`src/preprocess.py`, age/period/cohort) | ✅ multi-wave ready |
| Tests (7) | ✅ passing |
| `docs/data_notes.md`, `docs/wvs_download.md`, README | ✅ |
| **Official multi-wave WVS file (1981–2022)** | ⏳ **AWAITING USER (manual download)** |
| Full HAPC model (period effects) | ⛔ blocked on the file above |

## 3. The ONE manual task left (user action, ~3 min)

The pipeline is fully automated except one step that **cannot** be automated
(WVS issues a personalized download link after a license form):

1. Follow `publishing/docs/wvs_download.md` — register (free) at
   `worldvaluessurvey.org`, download **`WVS TimeSeries 1981 2022 Csv v5 0.zip`**.
2. Unzip, place the CSV in `publishing/data/raw/`.
3. Then just tell the assistant: *"file is at data/raw/<filename>"*.

Everything after that (verify, adapt if needed, build full HAPC, re-test,
update docs, sync, commit, push) is automated.

## 4. Key facts & decisions (context you must know)

- **Current raw data is Wave-7 ONLY** (subset of 97,220 rows, 66 countries,
  2017–2023). App crashes no: period effects are unidentifiable on one wave.
- **`X003R` in the subset is an age-bracket (1–6), NOT birth year**; in the
  official file `X003R` IS the birth year. `preprocess.py` now resolves both.
- **Cohort bins default to 5-year** (APC standard); sensitivity at 10/20.
- **HAPC method default = Yang–Land cross-classified random effects** (period &
  cohort random intercepts; age fixed polynomial). Implementation in
  `src/apc_model.py` (skeleton).
- **GitHub identity in `publishing/` only:** name `Pratik Hagawane`, email
  `87967129+imagimaniac@users.noreply.github.com`. Global git untouched.
- **gh auth = `imagimaniac`** (scopes include repo/projects). Remote is SSH.
- **WVS license:** non-redistribution. `data/raw` + `data/processed` are
  git-ignored and never pushed. Citation in `docs/data_notes.md`.
- **Profile / repo hygiene done:** 4 forks archived, 3 repos made private,
  1 project made private. Pinning flagships is a **manual GitHub UI step**.
- **Open decision for the user (not urgent):** default analysis outcome =
  generalized trust (WVS Q57); veto if wanted.

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

1. If the WVS file is present → run the swap-in/verify task (plan: Phase 1b).
2. If not → prep anything non-blocked; remind user of the one manual step.
3. Medium-term: outcome index, full HAPC, dashboard, write-up (plan Phases 2–4).

*Sister docs: `publishing/generational-values-project-plan.md` (tasks),
`publishing/master-plan-publication-outreach-roadmap.md` (long-term).*