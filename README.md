# India Air Quality Intelligence

An end-to-end data analytics project investigating air quality trends across India using historical station-level Air Quality Index (AQI) data.

## Project Objectives

- Audit and clean historical air quality data.
- Analyze air quality trends across cities, states, stations, and time.
- Identify periods and locations with elevated AQI.
- Use Python, SQL, statistics, and interactive visualizations to communicate findings.
- Build a dashboard and deploy an interactive application, subject to data quality and feasibility checks.

## Planned Technology Stack

- Python, Pandas, NumPy
- Matplotlib, Seaborn, Plotly
- SQL and SQLite
- SciPy, Statsmodels, Scikit-learn
- Power BI
- Streamlit
- Git and GitHub
- Pytest

## Data Sources

### Historical AQI dataset

Repository: https://github.com/Vonter/india-cpcb-aqi

Data dictionary: https://github.com/Vonter/india-cpcb-aqi/blob/main/DATA.md

This is a third-party compilation of CPCB-derived data, not a direct download from the official CPCB interface. The dataset's reported license is Open Data Commons Open Database License (ODbL) 1.0. Review the source license and attribution/share-alike obligations before redistributing any data or derived database.

### Current AQI snapshot

The project also investigated a real-time AQI CSV from India's data.gov.in portal. This snapshot is separate from the historical dataset and does not, by itself, establish historical trends.

## Important Limitations

- AQI records may contain missing hourly observations.
- Station identifiers and station names may not map one-to-one.
- Data coverage and completeness may vary by station and date.
- Historical patterns are observational and do not establish causation.
- Forecasting will only be attempted if data quality, coverage, and validation results justify it.
- No findings, model performance, or deployment outcomes will be claimed before they are tested.

## Project Status

**Stage 1 — Project setup and version control preparation.**

The analysis, data quality checks, visualizations, and application will be developed incrementally.

## Reproducibility

A Python virtual environment and `requirements.txt` are used to manage project dependencies. Setup instructions will be expanded as the project develops.

## Data and Privacy

Large datasets and generated outputs are excluded from Git by default. Refer to the data folder documentation for source and acquisition details.
