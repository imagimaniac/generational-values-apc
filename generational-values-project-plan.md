# Generational Values & Age–Period–Cohort Research — Project Plan

> **Status:** Planning &nbsp;|&nbsp; **Type:** Independent research project &nbsp;|&nbsp; **Duration:** 5 weeks (~20 working days)
> **Progress:** 0 / 22 tasks checked — track progress by ticking `- [ ]` items below.

---

## 01 — Objective

**What this project sets out to do:** Build and publish a rigorous, code-driven analysis of how individualism, collectivism, and related value orientations shift across generational cohorts over time — using established survey data and a statistically defensible model, not a pop-sociology narrative.

The short-term objective is a complete, working, publicly-shared research artifact: a cleaned dataset, a hierarchical age–period–cohort (APC) model, an interactive visualization, and a written case study — all pushed to GitHub. The long-term objective is for this to be the first of a recurring personal research practice that compounds credibility over time, run in parallel with an active career track, not instead of it.

| | |
|---|---|
| **Type** | Independent research project |
| **Duration** | 5 weeks (≈20 working days) |
| **Output** | Public GitHub repo + write-up + dashboard |
| **Primary data** | World Values Survey, Waves 1–7 |

---

## 02 — Scope

**What's in, what's out.** Keeping scope tight is what makes a 5-week solo timeline realistic. Anything in the "out of scope" column is a good candidate for a future, separate project — not a reason to expand this one.

### In scope
- Individualism–collectivism and traditional–secular / survival–self-expression indices from WVS
- A proper age–period–cohort decomposition, not a raw correlation
- 5–6 contrast countries (e.g. India, US, Sweden, Japan, Brazil)
- One interactive dashboard + one written case study
- Public GitHub repo with clean documentation

### Out of scope (for now)
- Primary data collection (running your own survey)
- Full global coverage (all ~100 WVS countries)
- Peer-reviewed journal submission
- Causal claims about *why* cohorts differ
- Building this into a paid product or consultancy

---

## 03 — Background & Rationale

**Why the age–period–cohort framing matters.** A claim like "Gen Z is more liberal" tangles together three different effects: an **age effect** (young people are typically more idealistic and shift as they age), a **period effect** (a historical event moves everyone's views at once, regardless of age), and a **cohort effect** (something sticks permanently with people who came of age during a specific window). Karl Mannheim's original theory of generations and Ronald Inglehart's postmaterialism research both exist specifically to disentangle these three forces.

> **Why this matters for credibility:** a paper that addresses the APC problem head-on reads as real research. A paper that doesn't reads as another "Gen Z vibes" LinkedIn post. This distinction is the entire reason the project is worth doing carefully rather than quickly.

---

## 04 — Methodology Snapshot

| Component | Approach |
|---|---|
| Data source | World Values Survey (7 waves, 1981–2022), cross-checked against Pew Global Attitudes |
| Core method | Hierarchical Age–Period–Cohort (HAPC) cross-classified model |
| Key indices | Individualism–collectivism; traditional–secular; survival–self-expression |
| Tooling | Python (pandas, statsmodels / dedicated APC package), Plotly, Streamlit |
| Validation | Sensitivity checks with alternate cohort bin widths and model specifications |

---

## 05 — Task Breakdown

Check items off as you complete them. `[SEQUENTIAL]` tasks must wait on something earlier. `[PARALLEL]` tasks can run alongside others in the same phase.

### Phase 1 — Foundation (`Week 1`)
- [x] **Set up GitHub repo & environment** — Repo structure, virtualenv, requirements.txt, README skeleton. `[SEQUENTIAL]` (0.5 day) ✅ done 2026-08-31
- [ ] **Download & inventory WVS waves 1–7** — Raw data pull, variable dictionary review. `[SEQUENTIAL]` (0.5 day)
- [ ] **Download Pew Global Attitudes cross-check data** — Secondary dataset for validating WVS findings. `[PARALLEL — with T2]` (0.5 day)
- [ ] **Build data cleaning pipeline** — Harmonize variable coding across all 7 waves. `[SEQUENTIAL — after T2]` (1.5 days)
- [x] **Construct cohort & period variables** — Birth-year bins and survey-year fields for the APC model. `[SEQUENTIAL — after T4]` (0.5 day) ✅ done 2026-08-31 (derives birth year from `A_YEAR − Q262`; see docs/data_notes.md)
- [ ] **Literature skim: Mannheim, Inglehart, APC methods** — Grounding read — can be done evenings, off the critical path. `[PARALLEL — all week]` (1 day)

### Phase 2 — Modeling (`Week 2`)
- [ ] **Build individualism–collectivism composite index** — Derive from relevant WVS item battery. `[SEQUENTIAL]` (1 day)
- [ ] **Build traditional–secular / survival–expression indices** — Independent computation, can run alongside the I–C index. `[PARALLEL]` (1 day)
- [ ] **Implement Hierarchical APC (HAPC) model** — Cross-classified random-effects model separating age, period, cohort. `[SEQUENTIAL — after indices]` (2 days)
- [ ] **Run sensitivity checks** — Alternate cohort bin widths, alternate model specs. `[SEQUENTIAL — after model]` (1 day)

### Phase 3 — Analysis & Visualization (`Week 3`)
- [ ] **Country-level comparison analysis** — India, US, Sweden, Japan, Brazil as contrast set. `[PARALLEL — per country]` (1 day)
- [ ] **Build interactive Streamlit dashboard** — Country selector + cohort trajectory view, age vs cohort effects separated. `[SEQUENTIAL — after country analysis]` (2 days)
- [ ] **Build static chart set for the write-up** — Plotly/matplotlib exports for the non-interactive summary. `[PARALLEL]` (1 day)

### Phase 4 — Writing & Packaging (`Week 4`)
- [ ] **Draft methodology & findings write-up** — ~1,500 words, plain-English, includes APC caveats honestly. `[SEQUENTIAL]` (2 days)
- [ ] **Clean repo README & code comments** — Docstrings, usage instructions, folder structure notes. `[PARALLEL]` (1 day)
- [ ] **Record short dashboard walkthrough video** — 2–3 minute Loom-style screen recording. `[PARALLEL]` (0.5 day)
- [ ] **Self-review pass: fact-check every claim against the APC caveats** — Final rigor check before anything goes public. `[SEQUENTIAL — after draft]` (0.5 day)

### Phase 5 — Distribution (`Week 5`)
- [ ] **Publish GitHub repo publicly & add case-study page to personal site** — Final polish pass on presentation. `[SEQUENTIAL]` (0.5 day)
- [ ] **Post write-up summary on LinkedIn** — Findings-first framing, not job-search framing. `[SEQUENTIAL]` (0.5 day)
- [ ] **Post working paper to SSRN** — Free distribution channel for the full write-up. `[PARALLEL]` (0.5 day)
- [ ] **Cross-post to Medium / Substack** — Wider readable-format distribution. `[PARALLEL]` (0.5 day)
- [ ] **Direct outreach: email 8–10 researchers** — WVS-affiliated institutes, Pew, Ipsos, McCrindle — lead with the finding, not a job ask. `[PARALLEL — ongoing]` (1 day)

---

## 06 — Parallel Execution Map

Three light tracks run through the project: the core analytical build (can't be parallelized much), background reading, and distribution prep. Overlapping the second and third against the first keeps the timeline to 5 weeks instead of 7–8.

| Track | Wk 1 | Wk 2 | Wk 3 | Wk 4 | Wk 5 |
|---|---|---|---|---|---|
| Core build | ● | ● | ● | ● | |
| Reading / prep | ○ | | | | |
| Write-up | | | ○ | ○ | |
| Distribution | | | | | ● |

- **●** — analytical dependency chain
- **○** — can be done in spare/parallel time

---

## 07 — Deliverables & Done-Criteria

| Deliverable | Definition of done |
|---|---|
| GitHub repo | Public, clean README, reproducible pipeline, no dead code |
| HAPC model | Age, period, and cohort effects separated and reported with sensitivity checks |
| Dashboard | Live, interactive, deployed (Streamlit Cloud or similar), works on mobile |
| Write-up | ~1,500 words, states APC caveats explicitly, no unsupported causal claims |
| Distribution | Posted publicly + 8–10 direct researcher emails sent |

---

## 08 — Risks & Open Questions

- **Data harmonization across 7 WVS waves** is usually the most time-consuming step in practice — Phase 1 has the most buffer built in for this reason.
- **HAPC models are sensitive to specification choices** — the sensitivity-check task is not optional; skipping it is the single biggest risk to credibility.
- **Scope creep toward "more countries" or "more indices"** is the most likely way this slips past 5 weeks — resist it; a tight, rigorous 5-country study beats a sprawling unfinished 30-country one.

---

## 09 — Long-Term Trajectory

This project is the first instance of a recurring practice, not a one-off. The detail above is intentionally specific to Project 1; the phases below stay at a directional level until each one is planned in its own right.

### Months 1–2 — Career track runs in parallel
Job search (LinkedIn optimization, flagship analytics portfolio project, direct outreach) proceeds alongside this research project — it remains the primary lever for the 40LPA+ move, not this project.

### Months 3–6 — Second research project
A related but distinct cohort-analysis topic (e.g. generational attitudes toward economic inequality, or migration), building a small consistent body of work rather than one isolated paper.

### Months 6–12 — Seek collaboration, not just publication
Use outreach replies from Project 1 and 2 to explore co-authorship or informal collaboration with an academic or research-institute contact — a higher-leverage outcome than another solo paper.

### Year 2+ — Decide the fork deliberately
By this point there should be enough real signal (traction, replies, possible co-authorship) to make an informed choice: continue as an analytics leader with research as a respected side-practice, or explore a partial move into applied social research — decide from evidence, not from how the idea feels today.

---

*Planning document only — not a deliverable of the research itself. Generated for task tracking.*

