"""
dashboard.py — Interactive Streamlit dashboard for the APC analysis.

Launches a country-selectable view separating age vs cohort effects
(Phase 3 build). Run from the repo root:

    streamlit run src/dashboard.py
"""

from __future__ import annotations

import streamlit as st

CONTRAST_COUNTRIES = ["IND", "USA", "SWE", "JPN", "BRA"]


def _header() -> None:
    st.set_page_config(page_title="Generational Values — APC", layout="wide")
    st.title("Generational Values: Age-Period-Cohort Analysis")
    st.caption("World Values Survey | Hierarchical APC model")


def _sidebar_selectors() -> dict:
    with st.sidebar:
        st.header("Controls")
        country = st.selectbox("Country", CONTRAST_COUNTRIES)
        cohort_width = st.slider("Cohort width (years)", 5, 20, 10, 5)
    return {"country": country, "cohort_width": cohort_width}


def main() -> None:
    _header()
    sel = _sidebar_selectors()
    st.info(
        "Dashboard skeleton ready. Load cleaned APC data and fit the HAPC "
        "model (Phase 2/3) to populate cohort-trajectory and age-effect views "
        f"for {sel['country']} with {sel['cohort_width']}-year cohorts."
    )


if __name__ == "__main__":
    main()
