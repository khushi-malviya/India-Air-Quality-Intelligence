
import streamlit as st
import duckdb
import plotly.express as px
import pandas as pd

from pathlib import Path


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="National Overview | India AQI",
    page_icon="🇮🇳",
    layout="wide"
)

st.title("🇮🇳 National Air Quality Overview")

st.markdown(
    "Explore historical air quality patterns across India "
    "from 2017 to 2023."
)

st.caption(
    "Source: Historical CPCB-derived dataset | "
    "Coverage: January 2017 – December 2023"
)


# --------------------------------------------------
# DATASET CONNECTION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "air_quality_model_ready.parquet"
)


@st.cache_data
def load_national_kpis():

    con = duckdb.connect(database=":memory:")

    try:
        query = f"""
            SELECT
                ROUND(AVG(AQI_Valid), 2) AS average_aqi,
                COUNT(AQI_Valid) AS valid_observations,
                COUNT(DISTINCT City) AS total_cities,
                COUNT(DISTINCT State) AS total_states,
                COUNT(
                    DISTINCT
                    State || '|' || City || '|' || "Station Name"
                ) AS total_stations

            FROM read_parquet('{DATA_PATH.as_posix()}')
        """

        return con.execute(query).df().iloc[0]

    finally:
        con.close()


@st.cache_data
def load_category_distribution():

    con = duckdb.connect(database=":memory:")

    try:
        query = f"""
            SELECT
                CASE
                    WHEN AQI_Valid <= 50 THEN 'Good'
                    WHEN AQI_Valid <= 100 THEN 'Satisfactory'
                    WHEN AQI_Valid <= 200 THEN 'Moderate'
                    WHEN AQI_Valid <= 300 THEN 'Poor'
                    WHEN AQI_Valid <= 400 THEN 'Very Poor'
                    WHEN AQI_Valid <= 500 THEN 'Severe'
                END AS AQI_Category,

                COUNT(*) AS Observations

            FROM read_parquet('{DATA_PATH.as_posix()}')

            WHERE AQI_Valid IS NOT NULL

            GROUP BY AQI_Category

            ORDER BY
                CASE AQI_Category
                    WHEN 'Good' THEN 1
                    WHEN 'Satisfactory' THEN 2
                    WHEN 'Moderate' THEN 3
                    WHEN 'Poor' THEN 4
                    WHEN 'Very Poor' THEN 5
                    WHEN 'Severe' THEN 6
                END
        """

        return con.execute(query).df()

    finally:
        con.close()


@st.cache_data
def load_yearly_trend():

    con = duckdb.connect(database=":memory:")

    try:
        query = f"""
            SELECT
                Year,
                ROUND(AVG(AQI_Valid), 2) AS Average_AQI

            FROM read_parquet('{DATA_PATH.as_posix()}')

            WHERE AQI_Valid IS NOT NULL

            GROUP BY Year

            ORDER BY Year
        """

        return con.execute(query).df()

    finally:
        con.close()


@st.cache_data
def load_state_rankings():

    con = duckdb.connect(database=":memory:")

    try:
        query = f"""
            SELECT
                State,
                ROUND(AVG(AQI_Valid), 2) AS Average_AQI,
                COUNT(AQI_Valid) AS Valid_Observations

            FROM read_parquet('{DATA_PATH.as_posix()}')

            WHERE AQI_Valid IS NOT NULL

            GROUP BY State

            ORDER BY Average_AQI DESC
        """

        return con.execute(query).df()

    finally:
        con.close()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

if not DATA_PATH.exists():
    st.error(f"Dataset not found: {DATA_PATH}")
    st.stop()

with st.spinner("Analyzing historical air quality data..."):

    kpis = load_national_kpis()
    category_data = load_category_distribution()
    yearly_data = load_yearly_trend()
    state_data = load_state_rankings()


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

st.subheader("National Air Quality Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average AQI",
    f"{kpis['average_aqi']:,.2f}"
)

col2.metric(
    "Valid Observations",
    f"{kpis['valid_observations']:,.0f}"
)

col3.metric(
    "Cities Covered",
    f"{kpis['total_cities']:,.0f}"
)

col4.metric(
    "Monitoring Stations",
    f"{kpis['total_stations']:,.0f}"
)

st.caption(
    f"Coverage: {int(kpis['total_states'])} states"
)


# --------------------------------------------------
# AQI CATEGORY DISTRIBUTION
# --------------------------------------------------

st.divider()

st.subheader("AQI Category Distribution")

col1, col2 = st.columns(2)

with col1:

    fig_category = px.pie(
        category_data,
        names="AQI_Category",
        values="Observations",
        hole=0.5,
        title="Distribution of Valid AQI Observations"
    )

    fig_category.update_traces(
        textinfo="percent+label"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

with col2:

    fig_bar = px.bar(
        category_data,
        x="AQI_Category",
        y="Observations",
        title="Observations by AQI Category",
        text_auto=".2s"
    )

    fig_bar.update_layout(
        xaxis_title="AQI Category",
        yaxis_title="Number of Observations"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )


# --------------------------------------------------
# YEARLY AQI TREND
# --------------------------------------------------

st.divider()

st.subheader("Year-wise Average AQI")

fig_year = px.line(
    yearly_data,
    x="Year",
    y="Average_AQI",
    markers=True,
    title="Historical Average AQI (2017–2023)"
)

fig_year.update_layout(
    xaxis_title="Year",
    yaxis_title="Average AQI"
)

st.plotly_chart(
    fig_year,
    use_container_width=True
)


# --------------------------------------------------
# STATE RANKINGS
# --------------------------------------------------

st.divider()

st.subheader("State-wise Average AQI")

fig_state = px.bar(
    state_data.head(15).sort_values(
        "Average_AQI",
        ascending=True
    ),
    x="Average_AQI",
    y="State",
    orientation="h",
    title="15 States with Highest Average AQI",
    text_auto=".2f"
)

fig_state.update_layout(
    xaxis_title="Average AQI",
    yaxis_title="State",
    height=600
)

st.plotly_chart(
    fig_state,
    use_container_width=True
)

st.dataframe(
    state_data,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# DATA INTERPRETATION AND LIMITATIONS
# --------------------------------------------------

st.divider()

st.subheader("Understanding the Results")

st.info(
    "AQI category thresholds used: Good (0–50), "
    "Satisfactory (51–100), Moderate (101–200), "
    "Poor (201–300), Very Poor (301–400), "
    "and Severe (401–500)."
)

st.warning(
    "These are historical observation-weighted averages, "
    "not population-weighted city or state exposure estimates. "
    "Monitoring network coverage changes over time, so "
    "year-to-year differences should be interpreted cautiously."
)

st.caption(
    "This dashboard uses historical data ending on "
    "31 December 2023. It does not display live AQI."
)
