
from pathlib import Path

import duckdb
import pandas as pd
import streamlit as st
from huggingface_hub import hf_hub_download

# Project directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Dataset location
DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "air_quality_model_ready.parquet"
)

@st.cache_resource
def get_dataset_path():
    """
    Download the model-ready dataset from Hugging Face.
    Hugging Face caches the file locally to avoid repeated downloads.
    """
    dataset_path = hf_hub_download(
        repo_id="khushimalviya/india-air-quality-data",
        filename="air_quality_model_ready.parquet",
        repo_type="dataset"
    )

    return Path(dataset_path)

@st.cache_data
def get_dataset_summary():
    """
    Return high-level information about the
    air quality dataset.
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    con = duckdb.connect(database=":memory:")

    try:
        query = f"""
            SELECT
                COUNT(*) AS total_records,

                COUNT(AQI_Valid) AS valid_records,

                COUNT(DISTINCT City) AS total_cities,

                COUNT(
                    DISTINCT
                    State || '|' || City || '|' || "Station Name"
                ) AS total_stations,

                COUNT(DISTINCT State) AS total_states,

                MIN(Timestamp) AS first_timestamp,

                MAX(Timestamp) AS last_timestamp,

                ROUND(AVG(AQI_Valid), 2) AS average_aqi

            FROM read_parquet('{get_dataset_path().as_posix()}')
        """

        result = con.execute(query).df()

        return result.iloc[0].to_dict()

    finally:
        con.close()


@st.cache_data
def get_city_options():
    """
    Return the available city names.
    """

    con = duckdb.connect(database=":memory:")

    try:
        query = f"""
            SELECT DISTINCT City
            FROM read_parquet('{get_dataset_path().as_posix()}')
            WHERE City IS NOT NULL
            ORDER BY City
        """

        return con.execute(query).df()["City"].tolist()

    finally:
        con.close()