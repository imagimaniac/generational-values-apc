# How to Download the Official Multi-Wave WVS File

This is the **only manual step** in the whole pipeline. It takes ~3 minutes and
cannot be automated because WVS issues a **personalized download link by email**
after you accept their non-redistribution license. Everything after this step is
automated.

> **Why we need this file:** the current `WVS_subset.csv` is Wave 7 only, which
> gives no cross-wave "period" variation — so a full age-period-cohort (HAPC)
> model isn't possible on it. The official **1981–2022 time-series** combines
> all 7 WVS waves into one harmonized file with a common dictionary, enabling a
> proper HAPC analysis.

## What to download

- **File:** `WVS TimeSeries 1981 2022 Csv v5 0.zip` (CSV version)
- It is part of the WVS *Longitudinal / Time-Series (1981–2022)* documentation.
- The CSV file inside is large (the full 7-wave file is on the order of
  hundreds of thousands of rows).

## Step-by-step

1. **Go to** the WVS data portal:
   `https://www.worldvaluessurvey.org/`
2. Click **Data & Documentation** (left menu) → **Longitudinal /
   Time-Series (1981–2022)** (or follow the "Time Series 1981 2022" links).
3. You will be asked to **register** (free). Fill in:
   - Title / Full name
   - Company / Institution
   - Email
   - Project title (suggestion: *"Age–Period–Cohort analysis of generational
     values using the World Values Survey"*)
   - Intended use: *Academic research project*
   - Brief purpose (one line is enough)
   - **Check the box** agreeing to the Conditions of Use.
4. WVS **emails you a download link** for the time-series file.
5. Open the email link and download **`WVS TimeSeries 1981 2022 Csv v5 0.zip`**.
6. **Unzip** it. You should get a `.csv` file.
7. **Save that CSV into:**
   `publishing/data/raw/`
8. Tell the assistant the **exact filename** you saved (e.g.
   `WVS_TimeSeries_1981_2022.csv`).

## License / what stays local

The WVS **non-redistribution** license means:

- The raw file is **git-ignored** and **never pushed** to GitHub
  (already enforced by this repo's `.gitignore`).
- Correct citation is included in `docs/data_notes.md`.
- Do not re-upload the file anywhere public.

## Alternative formats

If you prefer, you may download the same data in `Rdata`/`Rds`, `Stata`,
`SPSS`, or `SAS` instead of CSV. The pipeline is CSV-first, so **CSV is
easiest** — but tell the assistant if you grab another format and we'll adapt.

## Registration fields checklist

| Field               | Suggestion                                        |
|---------------------|---------------------------------------------------|
| Title / Name        | (your details)                                    |
| Institution         | (your affiliation, or "Independent researcher")    |
| Email               | (a real address — WVS emails the link)            |
| Project title       | Age-Period-Cohort analysis of generational values |
| Intended use        | Academic research project                         |
| Purpose (1 line)    | Study how values differ across generations/waves  |
| Conditions of Use   | **accept**                                        |
