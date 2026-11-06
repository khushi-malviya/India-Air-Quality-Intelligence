
import streamlit as st
import duckdb
import pandas as pd
import numpy as np
import joblib
import json
import plotly.graph_objects as go

from pathlib import Path


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AQI Forecasting | India AQI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 24-Hour AQI Forecasting")

st.markdown(
    "Explore machine-learning-based AQI predictions "
    "using historical monitoring station observations."
)


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "air_quality_model_ready.parquet"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "aqi_24h_hist_gradient_boosting.joblib"
)

METADATA_PATH = (
    PROJECT_ROOT
    / "models"
    / "aqi_24h_model_metadata.json"
)


# --------------------------------------------------
# MODEL FEATURES
# Keep this order consistent with training.
# --------------------------------------------------

FEATURES = [
    "AQI_Valid",
    "AQI_Lag_1H",
    "AQI_Lag_24H",
    "AQI_Lag_168H",
    "AQI_Rolling_Mean_24H",
    "AQI_Rolling_Mean_7D",
    "AQI_Rolling_Count_24H",
    "AQI_Rolling_Count_7D",
    "Hour_Number",
    "Month",
    "DayOfWeek",
    "Is_Weekend",
    "Hour_Sin",
    "Hour_Cos",
    "Month_Sin",
    "Month_Cos",
    "DayOfWeek_Sin",
    "DayOfWeek_Cos"
]


# --------------------------------------------------
# VALIDATE REQUIRED FILES
# --------------------------------------------------

required_files = {
    "Historical dataset": DATA_PATH,
    "Trained model": MODEL_PATH,
    "Model metadata": METADATA_PATH
}

missing_files = [
    name
    for name, path in required_files.items()
    if not path.exists()
]

if missing_files:
    st.error(
        "Required project files are missing: "
        + ", ".join(missing_files)
    )
    st.stop()


# --------------------------------------------------
# LOAD MODEL AND METADATA
# --------------------------------------------------

@st.cache_resource
def load_model():

    return joblib.load(MODEL_PATH)


@st.cache_data
def load_metadata():

    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


model = load_model()
metadata = load_metadata()


# --------------------------------------------------
# LOAD CITY AND STATION INFORMATION
# --------------------------------------------------

@st.cache_data
def load_cities():

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
def load_stations(city):

    con = duckdb.connect(database=":memory:")

    try:
        query = f"""
            SELECT DISTINCT
                State,
                City,
                "Station Name"

            FROM read_parquet('{DATA_PATH.as_posix()}')

            WHERE City = ?
              AND "Station Name" IS NOT NULL

            ORDER BY "Station Name"
        """

        return con.execute(query, [city]).df()

    finally:
        con.close()


# --------------------------------------------------
# GET LATEST VALID OBSERVATION FOR A STATION
# --------------------------------------------------

@st.cache_data
def load_latest_station_record(city, state, station_name):

    con = duckdb.connect(database=":memory:")

    try:
        query = f"""
            SELECT
                Timestamp,
                State,
                City,
                "Station Name",

                {", ".join(f'"{feature}"' for feature in FEATURES)}

            FROM read_parquet('{DATA_PATH.as_posix()}')

            WHERE City = ?
              AND State = ?
              AND "Station Name" = ?
              AND AQI_Valid IS NOT NULL

            ORDER BY Timestamp DESC

            LIMIT 1
        """

        return con.execute(
            query,
            [city, state, station_name]
        ).df()

    finally:
        con.close()


# --------------------------------------------------
# AQI CATEGORY INTERPRETATION
# --------------------------------------------------

def get_aqi_category(aqi):

    if aqi <= 50:
        return "Good"

    elif aqi <= 100:
        return "Satisfactory"

    elif aqi <= 200:
        return "Moderate"

    elif aqi <= 300:
        return "Poor"

    elif aqi <= 400:
        return "Very Poor"

    else:
        return "Severe"


# --------------------------------------------------
# MODEL INFORMATION
# --------------------------------------------------

st.subheader("Model Information")

st.write(
    "Model: Histogram-based Gradient Boosting Regressor"
)

st.write(
    "Prediction target: AQI 24 hours after the latest "
    "available valid station observation."
)

st.caption(
    "The model was trained using chronological data splits "
    "and evaluated on a 2023 test sample."
)


# --------------------------------------------------
# SELECT CITY AND STATION
# --------------------------------------------------

st.divider()

st.subheader("Generate a Historical 24-Hour Forecast")

cities = load_cities()

selected_city = st.selectbox(
    "Select City",
    cities,
    index=cities.index("Delhi") if "Delhi" in cities else 0
)

stations = load_stations(selected_city)

if stations.empty:

    st.warning("No monitoring stations found for this city.")
    st.stop()


station_labels = (
    stations["State"]
    + " | "
    + stations["Station Name"]
)

selected_station_label = st.selectbox(
    "Select Monitoring Station",
    station_labels.tolist()
)

selected_station = stations.loc[
    station_labels == selected_station_label
].iloc[0]


# --------------------------------------------------
# LOAD LATEST RECORD
# --------------------------------------------------

latest_data = load_latest_station_record(
    selected_city,
    selected_station["State"],
    selected_station["Station Name"]
)

if latest_data.empty:

    st.warning(
        "No valid AQI observation is available "
        "for the selected station."
    )

    st.stop()


latest_record = latest_data.iloc[0]

feature_data = latest_data[FEATURES].copy()

feature_data = feature_data.apply(
    pd.to_numeric,
    errors="coerce"
)


# --------------------------------------------------
# DISPLAY LATEST OBSERVATION
# --------------------------------------------------

st.divider()

st.subheader("Latest Available Station Observation")

observation_time = pd.to_datetime(
    latest_record["Timestamp"]
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Latest Observed AQI",
    f"{latest_record['AQI_Valid']:.2f}"
)

col2.metric(
    "AQI Category",
    get_aqi_category(latest_record["AQI_Valid"])
)

col3.metric(
    "Observation Timestamp",
    observation_time.strftime("%d %b %Y, %H:%M")
)


# --------------------------------------------------
# GENERATE PREDICTION
# --------------------------------------------------

st.divider()

if st.button(
    "Generate 24-Hour AQI Forecast",
    type="primary",
    use_container_width=True
):

    try:

        prediction = float(
            model.predict(feature_data)[0]
        )

        prediction = float(
            np.clip(prediction, 1, 500)
        )

        forecast_time = (
            observation_time
            + pd.Timedelta(hours=24)
        )

        prediction_category = get_aqi_category(
            prediction
        )

        change = (
            prediction
            - float(latest_record["AQI_Valid"])
        )

        st.session_state["forecast_result"] = {
            "prediction": prediction,
            "category": prediction_category,
            "forecast_time": forecast_time,
            "change": change,
            "observation_time": observation_time,
            "observed_aqi": float(latest_record["AQI_Valid"])
        }

    except Exception as error:

        st.error(
            f"Unable to generate forecast: {error}"
        )


# --------------------------------------------------
# DISPLAY FORECAST
# --------------------------------------------------

if "forecast_result" in st.session_state:

    result = st.session_state["forecast_result"]

    st.success("24-hour forecast generated successfully!")

    st.subheader("Forecast Result")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Predicted AQI",
        f"{result['prediction']:.2f}",
        delta=f"{result['change']:+.2f}",
        delta_color="inverse"
    )

    col2.metric(
        "Predicted AQI Category",
        result["category"]
    )

    col3.metric(
        "Forecast Timestamp",
        result["forecast_time"].strftime(
            "%d %b %Y, %H:%M"
        )
    )

    # Comparison chart

    chart_data = pd.DataFrame({
        "Reading": [
            "Latest Observed AQI",
            "Predicted AQI (+24h)"
        ],
        "AQI": [
            result["observed_aqi"],
            result["prediction"]
        ]
    })

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=chart_data["Reading"],
            y=chart_data["AQI"],
            text=chart_data["AQI"].round(2),
            textposition="auto"
        )
    )

    fig.update_layout(
        title="Latest Observation vs 24-Hour Forecast",
        xaxis_title="",
        yaxis_title="AQI",
        yaxis_range=[0, 500]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# MODEL PERFORMANCE
# --------------------------------------------------

st.divider()

st.subheader("Model Performance — 2023 Test Sample")

test_metrics = metadata.get("test_metrics", {})

if test_metrics:

    baseline = test_metrics.get("baseline", {})
    model_metrics = test_metrics.get("model", {})

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Model MAE",
        f"{model_metrics.get('MAE', 0):.2f}"
    )

    col2.metric(
        "Model RMSE",
        f"{model_metrics.get('RMSE', 0):.2f}"
    )

    col3.metric(
        "Model R²",
        f"{model_metrics.get('R2', 0):.3f}"
    )

    with st.expander("Compare with persistence baseline"):

        comparison = pd.DataFrame({
            "Metric": ["MAE", "RMSE", "R²"],

            "Persistence Baseline": [
                baseline.get("MAE"),
                baseline.get("RMSE"),
                baseline.get("R2")
            ],

            "Machine Learning Model": [
                model_metrics.get("MAE"),
                model_metrics.get("RMSE"),
                model_metrics.get("R2")
            ]
        })

        st.dataframe(
            comparison,
            use_container_width=True,
            hide_index=True
        )

else:

    st.info(
        "Test metrics were not found in the metadata file."
    )


# --------------------------------------------------
# IMPORTANT LIMITATIONS
# --------------------------------------------------

st.divider()

st.subheader("Important Limitations")

st.warning(
    "This is a historical model demonstration, not a live "
    "forecasting service. The source dataset ends on "
    "31 December 2023. Forecast timestamps are based on "
    "the latest available observation for the selected station."
)

st.caption(
    "AQI predictions are regression estimates clipped to the "
    "project's valid AQI range of 1–500. They are not official "
    "CPCB forecasts or health advisories."
)