
import streamlit as st
import duckdb
import plotly.express as px
import pandas as pd

from pathlib import Path


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="City Risk Assessment | India AQI",
    page_icon="🏙️",
    layout="wide"
)

st.title("🏙️ City Pollution & Risk Assessment")

st.markdown(
    "Explore historical air quality conditions, pollution "
    "severity and seasonal patterns across Indian cities."
)


# --------------------------------------------------
# DATASET PATH
# --------------------------------------------------

from utils.data_loader import get_dataset_path

DATA_PATH = get_dataset_path()

# --------------------------------------------------
# DATA LOADING FUNCTIONS
# --------------------------------------------------

@st.cache_data
def get_cities():

    con = duckdb.connect(database=":memory:")

    try:
        query = f"""
            SELECT DISTINCT City
            FROM read_parquet('{DATA_PATH.as_posix()}')
            WHERE City IS NOT NULL
            ORDER BY City
        """

        return con.execute(query).df()["City"].tolist()

    finally:
        con.close()


@st.cache_data
def get_city_summary(city):

    con = duckdb.connect(database=":memory:")

    try:
        query = f"""
            SELECT
                ROUND(AVG(AQI_Valid), 2) AS Average_AQI,

                ROUND(MEDIAN(AQI_Valid), 2) AS Median_AQI,

                COUNT(AQI_Valid) AS Valid_Observations,

                COUNT(DISTINCT State) AS States,

                COUNT(
                    DISTINCT
                    State || '|' || City || '|' || "Station Name"
                ) AS Monitoring_Stations,

                ROUND(
                    100.0 * COUNT(
                        CASE WHEN AQI_Valid > 200
                        THEN 1 END
                    ) / NULLIF(COUNT(AQI_Valid), 0),
                    2
                ) AS High_Pollution_Percentage

            FROM read_parquet('{DATA_PATH.as_posix()}')

            WHERE City = ?
              AND AQI_Valid IS NOT NULL
        """

        return con.execute(query, [city]).df().iloc[0]

    finally:
        con.close()


@st.cache_data
def get_city_categories(city):

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
                    ELSE 'Severe'
                END AS AQI_Category,

                COUNT(*) AS Observations

            FROM read_parquet('{DATA_PATH.as_posix()}')

            WHERE City = ?
              AND AQI_Valid IS NOT NULL

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

        return con.execute(query, [city]).df()

    finally:
        con.close()


@st.cache_data
def get_city_monthly_trend(city):

    con = duckdb.connect(database=":memory:")

    try:
        query = f"""
            SELECT
                Month,

                ROUND(AVG(AQI_Valid), 2) AS Average_AQI

            FROM read_parquet('{DATA_PATH.as_posix()}')

            WHERE City = ?
              AND AQI_Valid IS NOT NULL

            GROUP BY Month
            ORDER BY Month
        """

        return con.execute(query, [city]).df()

    finally:
        con.close()


@st.cache_data
def get_city_comparison():

    con = duckdb.connect(database=":memory:")

    try:
        query = f"""
            SELECT
                City,

                ROUND(AVG(AQI_Valid), 2) AS Average_AQI,

                COUNT(AQI_Valid) AS Observations

            FROM read_parquet('{DATA_PATH.as_posix()}')

            WHERE AQI_Valid IS NOT NULL

            GROUP BY City

            HAVING COUNT(AQI_Valid) >= 500

            ORDER BY Average_AQI DESC
        """

        return con.execute(query).df()

    finally:
        con.close()


# --------------------------------------------------
# CHECK DATA
# --------------------------------------------------

if not DATA_PATH.exists():
    st.error("Model-ready dataset not found.")
    st.stop()


# --------------------------------------------------
# CITY SELECTION
# --------------------------------------------------

cities = get_cities()

selected_city = st.selectbox(
    "Select an Indian city",
    cities,
    index=cities.index("Delhi") if "Delhi" in cities else 0
)

st.markdown(f"### Historical Pollution Profile: {selected_city}")


# --------------------------------------------------
# CITY METRICS
# --------------------------------------------------

with st.spinner("Analyzing city pollution data..."):

    summary = get_city_summary(selected_city)
    category_data = get_city_categories(selected_city)
    monthly_data = get_city_monthly_trend(selected_city)
    comparison_data = get_city_comparison()


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average AQI",
    f"{summary['Average_AQI']:,.2f}"
)

col2.metric(
    "Median AQI",
    f"{summary['Median_AQI']:,.2f}"
)

col3.metric(
    "High Pollution Observations",
    f"{summary['High_Pollution_Percentage']:.2f}%"
)

col4.metric(
    "Valid Observations",
    f"{summary['Valid_Observations']:,.0f}"
)

st.caption(
    f"Monitoring stations: {int(summary['Monitoring_Stations'])}"
)


# --------------------------------------------------
# AQI CATEGORY DISTRIBUTION
# --------------------------------------------------

st.divider()

st.subheader(f"AQI Category Distribution — {selected_city}")

fig_category = px.pie(
    category_data,
    names="AQI_Category",
    values="Observations",
    hole=0.48,
    title="Distribution of Historical AQI Categories"
)

fig_category.update_traces(
    textinfo="percent+label"
)

st.plotly_chart(
    fig_category,
    use_container_width=True
)


# --------------------------------------------------
# MONTHLY POLLUTION PATTERN
# --------------------------------------------------

st.divider()

st.subheader("Monthly Pollution Pattern")

month_names = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

monthly_data["Month_Name"] = monthly_data["Month"].map(
    lambda x: month_names[int(x) - 1]
)

fig_month = px.bar(
    monthly_data,
    x="Month_Name",
    y="Average_AQI",
    title=f"Average AQI by Calendar Month — {selected_city}",
    text_auto=".2f"
)

fig_month.update_layout(
    xaxis_title="Month",
    yaxis_title="Average AQI"
)

st.plotly_chart(
    fig_month,
    use_container_width=True
)


# --------------------------------------------------
# CITY COMPARISON
# --------------------------------------------------

st.divider()

st.subheader("City-wise Pollution Comparison")

st.caption(
    "Cities with at least 500 valid observations are included. "
    "This is a minimum data-volume filter, not a guarantee "
    "of equivalent monitoring coverage."
)

top_cities = comparison_data.head(15).copy()

top_cities = top_cities.sort_values(
    "Average_AQI",
    ascending=True
)

fig_comparison = px.bar(
    top_cities,
    x="Average_AQI",
    y="City",
    orientation="h",
    title="15 Cities with Highest Historical Average AQI",
    text_auto=".2f",
    hover_data=["Observations"]
)

fig_comparison.update_layout(
    height=600,
    xaxis_title="Average AQI",
    yaxis_title="City"
)

st.plotly_chart(
    fig_comparison,
    use_container_width=True
)


# --------------------------------------------------
# INTERPRETATION AND LIMITATIONS
# --------------------------------------------------

st.divider()

st.subheader("How to Interpret These Results")

st.info(
    "High pollution observations are defined here as valid "
    "AQI readings greater than 200, covering Poor, Very Poor "
    "and Severe categories."
)

st.warning(
    "These are historical, observation-weighted indicators. "
    "They do not represent population exposure, individual "
    "health risk or current air quality. Monitoring station "
    "coverage varies between cities and over time."
)

st.caption(
    "Historical dataset coverage: 2017–2023. "
    "Source: CPCB-derived dataset."
)
