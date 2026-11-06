
import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
from pathlib import Path


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Historical Analysis | India AQI",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Historical Air Quality Analysis")

st.markdown(
    "Explore long-term pollution trends, seasonal variations, "
    "monthly patterns and hourly AQI behaviour across India."
)

st.caption(
    "Historical data coverage: January 2017 – December 2023"
)


# --------------------------------------------------
# DATASET PATH
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "air_quality_model_ready.parquet"
)


# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------

@st.cache_data
def load_yearly_trend():

    con = duckdb.connect(database=":memory:")

    try:
        query = f"""
            SELECT
                Year,
                ROUND(AVG(AQI_Valid), 2) AS Average_AQI,
                COUNT(AQI_Valid) AS Observations

            FROM read_parquet('{DATA_PATH.as_posix()}')

            WHERE AQI_Valid IS NOT NULL

            GROUP BY Year
            ORDER BY Year
        """

        return con.execute(query).df()

    finally:
        con.close()


@st.cache_data
def load_seasonal_trend():

    con = duckdb.connect(database=":memory:")

    try:
        query = f"""
            SELECT
                Season,
                ROUND(AVG(AQI_Valid), 2) AS Average_AQI,
                COUNT(AQI_Valid) AS Observations

            FROM read_parquet('{DATA_PATH.as_posix()}')

            WHERE AQI_Valid IS NOT NULL

            GROUP BY Season

            ORDER BY
                CASE Season
                    WHEN 'Winter' THEN 1
                    WHEN 'Summer' THEN 2
                    WHEN 'Monsoon' THEN 3
                    WHEN 'Post-Monsoon' THEN 4
                END
        """

        return con.execute(query).df()

    finally:
        con.close()


@st.cache_data
def load_monthly_heatmap():

    con = duckdb.connect(database=":memory:")

    try:
        query = f"""
            SELECT
                Year,
                Month,
                ROUND(AVG(AQI_Valid), 2) AS Average_AQI

            FROM read_parquet('{DATA_PATH.as_posix()}')

            WHERE AQI_Valid IS NOT NULL

            GROUP BY Year, Month

            ORDER BY Year, Month
        """

        return con.execute(query).df()

    finally:
        con.close()


@st.cache_data
def load_hourly_trend():

    con = duckdb.connect(database=":memory:")

    try:
        query = f"""
            SELECT
                Hour_Number,
                ROUND(AVG(AQI_Valid), 2) AS Average_AQI,
                COUNT(AQI_Valid) AS Observations

            FROM read_parquet('{DATA_PATH.as_posix()}')

            WHERE AQI_Valid IS NOT NULL

            GROUP BY Hour_Number

            ORDER BY Hour_Number
        """

        return con.execute(query).df()

    finally:
        con.close()


@st.cache_data
def load_category_trend():

    con = duckdb.connect(database=":memory:")

    try:
        query = f"""
            SELECT
                Year,

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

            WHERE AQI_Valid IS NOT NULL

            GROUP BY Year, AQI_Category

            ORDER BY Year
        """

        return con.execute(query).df()

    finally:
        con.close()


# --------------------------------------------------
# VALIDATE DATA
# --------------------------------------------------

if not DATA_PATH.exists():
    st.error(f"Dataset not found: {DATA_PATH}")
    st.stop()


# --------------------------------------------------
# LOAD ANALYTICAL DATA
# --------------------------------------------------

with st.spinner("Analyzing historical AQI patterns..."):

    yearly_data = load_yearly_trend()
    seasonal_data = load_seasonal_trend()
    monthly_data = load_monthly_heatmap()
    hourly_data = load_hourly_trend()
    category_data = load_category_trend()


# --------------------------------------------------
# YEARLY AQI TREND
# --------------------------------------------------

st.subheader("1. Long-Term AQI Trend")

fig_yearly = px.line(
    yearly_data,
    x="Year",
    y="Average_AQI",
    markers=True,
    title="Average AQI Across India (2017–2023)",
    hover_data=["Observations"]
)

fig_yearly.update_layout(
    xaxis_title="Year",
    yaxis_title="Average AQI",
    hovermode="x unified"
)

st.plotly_chart(
    fig_yearly,
    use_container_width=True
)

st.dataframe(
    yearly_data,
    use_container_width=True,
    hide_index=True
)

st.warning(
    "The monitoring network expanded substantially during "
    "2017–2023. Annual averages are observation-weighted and "
    "may reflect changes in station and city coverage as well "
    "as changes in pollution."
)


# --------------------------------------------------
# SEASONAL ANALYSIS
# --------------------------------------------------

st.divider()

st.subheader("2. Seasonal Pollution Analysis")

fig_season = px.bar(
    seasonal_data,
    x="Season",
    y="Average_AQI",
    color="Season",
    text_auto=".2f",
    title="Average AQI by Season",
    hover_data=["Observations"]
)

fig_season.update_layout(
    xaxis_title="Season",
    yaxis_title="Average AQI",
    showlegend=False
)

st.plotly_chart(
    fig_season,
    use_container_width=True
)


# --------------------------------------------------
# MONTHLY HEATMAP
# --------------------------------------------------

st.divider()

st.subheader("3. Monthly AQI Heatmap")

month_names = [
    "Jan", "Feb", "Mar", "Apr",
    "May", "Jun", "Jul", "Aug",
    "Sep", "Oct", "Nov", "Dec"
]

monthly_data["Month_Name"] = monthly_data["Month"].map(
    lambda month: month_names[int(month) - 1]
)

heatmap_data = monthly_data.pivot(
    index="Year",
    columns="Month_Name",
    values="Average_AQI"
)

heatmap_data = heatmap_data.reindex(
    columns=month_names
)

fig_heatmap = px.imshow(
    heatmap_data,
    labels={
        "x": "Month",
        "y": "Year",
        "color": "Average AQI"
    },
    x=month_names,
    y=heatmap_data.index,
    color_continuous_scale="RdYlGn_r",
    text_auto=".0f",
    aspect="auto",
    title="Monthly Average AQI by Year"
)

fig_heatmap.update_layout(
    height=450
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True
)


# --------------------------------------------------
# HOURLY ANALYSIS
# --------------------------------------------------

st.divider()

st.subheader("4. Hourly Pollution Patterns")

fig_hourly = px.line(
    hourly_data,
    x="Hour_Number",
    y="Average_AQI",
    markers=True,
    title="Average AQI by Hour of the Day",
    hover_data=["Observations"]
)

fig_hourly.update_layout(
    xaxis_title="Hour of the Day",
    yaxis_title="Average AQI",
    xaxis=dict(
        tickmode="linear",
        dtick=2
    )
)

st.plotly_chart(
    fig_hourly,
    use_container_width=True
)


# --------------------------------------------------
# AQI CATEGORY TRENDS
# --------------------------------------------------

st.divider()

st.subheader("5. AQI Category Distribution Over Time")

category_pivot = category_data.pivot(
    index="Year",
    columns="AQI_Category",
    values="Observations"
).fillna(0)

category_order = [
    "Good",
    "Satisfactory",
    "Moderate",
    "Poor",
    "Very Poor",
    "Severe"
]

category_pivot = category_pivot.reindex(
    columns=category_order,
    fill_value=0
)

category_percentage = category_pivot.div(
    category_pivot.sum(axis=1),
    axis=0
) * 100

category_percentage = (
    category_percentage
    .reset_index()
    .melt(
        id_vars="Year",
        var_name="AQI_Category",
        value_name="Percentage"
    )
)

fig_category = px.bar(
    category_percentage,
    x="Year",
    y="Percentage",
    color="AQI_Category",
    barmode="stack",
    category_orders={
        "AQI_Category": category_order
    },
    title="Year-wise AQI Category Distribution (%)"
)

fig_category.update_layout(
    xaxis_title="Year",
    yaxis_title="Percentage of Valid Observations",
    yaxis_range=[0, 100]
)

st.plotly_chart(
    fig_category,
    use_container_width=True
)


# --------------------------------------------------
# KEY INTERPRETATION
# --------------------------------------------------

st.divider()

st.subheader("Key Interpretation")

st.info(
    "AQI patterns can vary substantially by season and hour. "
    "Use the charts together to explore when higher pollution "
    "levels are observed and how category distributions change."
)

st.warning(
    "All charts represent historical, observation-weighted "
    "statistics. They are not live readings, population-weighted "
    "exposure estimates or evidence of causal relationships."
)

st.caption(
    "AQI categories follow the project's documented thresholds. "
    "Historical dataset ends on 31 December 2023."
)
