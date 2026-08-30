# Publishing — GitHub Public Repo

This folder is the **public-facing** side of `Outreach-v2`. Its contents get pushed to GitHub as the `generational-values-apc` repository (and related public work) and are committed to **every day** to build a consistent, visible activity record.

> This is the git repo. Commit and push from here. The sibling **`workspace/`** folder holds private working copies and must be kept in sync (see `workspace/README.md` — the sync rule).

---

## What's here

- `README.md` — this file
- `generational-values-project-plan.md` — the APC/generational-values research project plan
- `master-plan-publication-outreach-roadmap.md` — the 12-month publication/outreach/portfolio roadmap

*(HTML tracking copies are intentionally kept out of this public folder.)*

---

## Daily publishing convention

The whole point of this repo is **visible, consistent daily activity**. The habit matters more than the size of any single commit.

- **Commit something small and meaningful every day.** Doesn't have to be a feature — a chart, an index update, a curated note, a README refresh all count.
- **Use a clear, dated commit message:**
  ```
  Publish: 2026-08-31 — updated generational-values plan (Phase 1 tasks)
  ```
- **Work here, publish here.** Edits made in `workspace/` should be mirrored here via `./sync.sh` before committing.

### Typical day
1. Edit work in `publishing/` (or `workspace/` then sync).
2. `./sync.sh` — make sure both folders match.
3. `git add -A && git commit -m "Publish: <date> — <what changed>"`
4. `git push`

---

## Repo organization for visibility (overview)

Recommended flagship repos (public + own, not forks):

- `generational-values-apc` — this research project (highest-visibility differentiator)
- a **credit-risk portfolio** repo mirroring Track C topics (IFRS9/CECL, BNPL risk, thin-file scoring)
- polished versions of existing owned repos (`stock-prediction-project`, `Projects_shelf`)

Keep forks out of the pinned lineup — only owned, maintained repos signal active building.

---

## Links

- Master roadmap: [master-plan-publication-outreach-roadmap.md](./master-plan-publication-outreach-roadmap.md)
- Project plan: [generational-values-project-plan.md](./generational-values-project-plan.md)
- Workspace (private + sync rule): [../workspace/README.md](../workspace/README.md)
