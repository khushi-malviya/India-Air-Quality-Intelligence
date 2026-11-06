# 🇮🇳 India Air Quality Intelligence
### From Raw Data to Pollution Risk Insights & 24-Hour AQI Forecasting

An end-to-end data analytics and machine learning project that transforms historical Indian air-quality observations into actionable insights through exploratory data analysis, statistical testing, feature engineering, predictive modeling, and an interactive Streamlit dashboard.

---

## 📌 Project Overview

Air pollution is a major environmental and public-health challenge in India. Understanding how air quality changes across cities, seasons, and time periods can help identify pollution hotspots, assess historical patterns, and support data-informed environmental decisions.

**India Air Quality Intelligence** analyzes historical air-quality data from Indian monitoring stations between January 2017 and December 2023.

The project follows a complete data workflow:

- Data understanding and quality assessment
- Data cleaning and transformation
- Exploratory data analysis (EDA)
- Statistical analysis and hypothesis testing
- Temporal feature engineering
- 24-hour-ahead AQI prediction
- Interactive dashboard development

The final application allows users to explore national air-quality patterns, assess city-level pollution risks, investigate historical trends, and view experimental AQI forecasts for individual monitoring stations.

## 🎯 Project Objectives

1. Analyze historical AQI patterns across Indian cities and states.
2. Identify seasonal, monthly, and hourly pollution trends.
3. Investigate differences in air quality across selected cities and seasons.
4. Assess data quality, missing observations, and monitoring-network limitations.
5. Engineer temporal and historical AQI features for forecasting.
6. Build and evaluate a machine learning model for 24-hour-ahead AQI prediction.
7. Present insights through an interactive business-style dashboard.

## 📊 Dataset

**Source:** [India CPCB AQI Dataset – GitHub](https://github.com/Vonter/india-cpcb-aqi)

The dataset is a third-party CPCB-derived compilation of historical air-quality observations. It is not a live CPCB data feed.

| Attribute | Details |
|---|---|
| Data period | January 2017 – December 2023 |
| Original records | 562,878 |
| Original columns | 29 |
| States | 29 |
| Cities | 248 |
| Monitoring stations | 529 |
| Observation frequency | Hourly AQI readings |
| Raw dataset size | Approximately 78.8 MB |

The original dataset contains station information, dates, and 24 hourly AQI columns. It was transformed from a wide format into an analytical hourly format.

**Important data-quality considerations:**

- Missing AQI readings were preserved rather than replaced with zero or arbitrary averages.
- 56 observations above the project's valid AQI range of 1–500 were flagged and excluded from standard AQI calculations.
- Station IDs were reused across different station names. Therefore, `(State, City, Station Name)` was used as the station identity for time-series operations.
- Monitoring-station coverage increased considerably over the study period. Annual national averages must therefore be interpreted with caution.

## 🛠️ Technology Stack

| Area | Tools and Technologies |
|---|---|
| Programming | Python |
| Data manipulation | Pandas, NumPy |
| Data processing | DuckDB, PyArrow |
| Database / Querying | SQL, DuckDB SQL |
| Visualization | Matplotlib, Seaborn, Plotly |
| Statistical analysis | SciPy, Statsmodels, PyMannKendall |
| Machine learning | Scikit-learn |
| Model persistence | Joblib |
| Dashboard | Streamlit |
| Development | Jupyter Notebook, VS Code |
| Version control | Git, GitHub |

## 🏗️ Project Workflow

```text
Raw CPCB-derived AQI Dataset
              |
              v
     Data Understanding
              |
              v
     Data Transformation
       (Wide to Long)
              |
              v
 Exploratory Data Analysis
              |
              v
    Statistical Analysis
              |
              v
     Feature Engineering
              |
              v
    Predictive Modeling
              |
              v
    Model Evaluation
              |
              v
    Streamlit Dashboard
```

## 📁 Repository Structure

```text
India-Air-Quality-Intelligence/
│
├── app/
│   ├── Home.py
│   ├── pages/
│   │   ├── 1_National_Overview.py
│   │   ├── 2_City_Risk_Assessment.py
│   │   ├── 3_Historical_Analysis.py
│   │   └── 4_AQI_Forecasting.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── data_loader.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   ├── aqi_24h_hist_gradient_boosting.joblib
│   └── aqi_24h_model_metadata.json
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_transformation.ipynb
│   ├── 03_exploratory_data_analysis.ipynb
│   ├── 04_statistical_analysis.ipynb
│   ├── 05_feature_engineering.ipynb
│   └── 06_predictive_modeling.ipynb
│
├── reports/
│   └── data_quality_findings.md
│
├── .gitignore
├── requirements.txt
└── README.md
```

*Note: Raw and processed datasets are excluded from GitHub to keep the repository lightweight. The processed files are generated locally through the notebook workflow.*

## 🔍 Analytical Work

### 1. Data Understanding and Quality Assessment

The initial dataset contained 562,878 records and 29 columns.

Key activities:

- Inspected schema, data types, date ranges, and missing values.
- Examined missingness across years, stations, and hours.
- Identified duplicated and reused station identifiers.
- Flagged out-of-range AQI values.
- Documented data-quality limitations.

### 2. Data Transformation

The original dataset stored 24 hourly readings in separate columns.

It was transformed into a long-format analytical dataset containing:

- Station information
- Timestamp
- AQI value
- AQI validity status
- Supporting analytical fields

The transformed dataset contains **13,509,072 hourly station records**.

### 3. Exploratory Data Analysis

The EDA investigated:

- AQI category distribution
- City-wise and state-wise pollution patterns
- Seasonal and monthly AQI trends
- Hourly AQI patterns
- Historical annual trends
- Balanced city comparisons
- Severe pollution observations

**Selected findings:**

| AQI Category | Observations | Share |
|---|---:|---:|
| Satisfactory | 3,958,356 | 31.73% |
| Moderate | 3,656,970 | 29.32% |
| Good | 2,278,540 | 18.27% |
| Very Poor | 1,106,391 | 8.87% |
| Poor | 1,023,263 | 8.20% |
| Severe | 449,965 | 3.61% |

**Seasonal observations:**

| Season | Average AQI |
|---|---:|
| Winter | 188.96 |
| Post-Monsoon | 170.70 |
| Summer | 133.22 |
| Monsoon | 81.25 |

Winter showed the highest average AQI, while the monsoon season showed the lowest average AQI in this dataset.

For balanced comparisons, 17 cities met the project's requirement of having at least 500 valid observations in each of the 28 year-season combinations.

### 4. Statistical Analysis

Statistical techniques were used to investigate seasonal differences and historical trends.

Methods included:

- Descriptive statistics
- Distribution and outlier analysis
- Friedman test
- Pairwise Wilcoxon signed-rank tests with Holm correction
- Kendall's coefficient of concordance
- Mann-Kendall trend analysis
- Theil-Sen slope estimation
- Correlation analysis

**Seasonal hypothesis testing:**

The Friedman test produced:

- Chi-square statistic: 44.7882
- p-value: approximately 0.000000001
- Kendall's W: 0.8782

The results indicated statistically significant seasonal differences across the selected 17 balanced cities.

Pairwise testing with Holm correction found significant differences for five of the six seasonal comparisons. Winter and Post-Monsoon were not significantly different at the 0.05 level.

City-level annual trend tests did not show statistically significant trends after Holm correction.

### 5. Feature Engineering

Temporal and historical features were created to support forecasting.

**Temporal features:**
- Year, month, day, hour, quarter
- Day of week and weekend indicator
- Season
- Cyclical hour, month, and weekday encoding

**Historical AQI features:**
- 1-hour lag
- 24-hour lag
- 168-hour lag
- 24-hour rolling mean
- 7-day rolling mean
- Rolling observation counts

DuckDB was used for large-scale timestamp joins and rolling-window calculations to manage memory efficiently.

The final model-ready dataset contains 13,509,072 records and 37 columns.

## 🤖 Predictive Modeling: 24-Hour AQI Forecasting

The project builds a machine learning model to estimate AQI 24 hours ahead for an individual monitoring station.

### Prediction Target

The target is the valid AQI observation at the exact timestamp 24 hours after the current observation, matched using:

`State + City + Station Name + Timestamp`

### Model

**HistGradientBoostingRegressor**

The model uses current AQI, historical lag values, rolling averages, and temporal features.

### Evaluation Strategy

A chronological split was used to reduce future-data leakage:

| Dataset | Target period | Records |
|---|---|---:|
| Training | Before 2022 | 5,970,924 |
| Validation | 2022 | 2,398,361 |
| Test | 2023 | 3,294,948 |

A deterministic sample was used for model training and evaluation:

- Training sample: 300,000
- Validation sample: 100,000
- Test sample: 100,000

### Test Performance

The model was compared against a persistence baseline, which predicts that the AQI 24 hours ahead will equal the current AQI.

| Metric | Persistence Baseline | HistGradientBoosting |
|---|---:|---:|
| MAE | 38.86 | **35.91** |
| RMSE | 66.64 | **56.57** |
| R² | 0.527 | **0.659** |

**Observed improvements on the test sample:**

- MAE improved by approximately 7.59%.
- RMSE improved by approximately 15.11%.
- R² increased by approximately 0.132.

### Feature Importance

Permutation importance identified the following as the strongest predictors:

1. Current AQI
2. 7-day rolling mean AQI
3. 24-hour rolling mean AQI
4. 1-hour lag AQI
5. 24-hour lag AQI
6. 168-hour lag AQI

These results highlight the importance of recent pollution conditions and historical AQI patterns in short-term forecasting.

**Model evaluation caveat:** The reported test metrics are based on a 100,000-record sample from the 2023 test population, not the entire test population.

## 📈 Interactive Streamlit Dashboard

The dashboard brings the analysis and forecasting results together in four interactive pages.

### 1. National Overview

Explore national-level AQI indicators and pollution distribution.

### 2. City Risk Assessment

Explore city-level pollution indicators, AQI statistics, category distribution, and monthly patterns.

### 3. Historical Analysis

Investigate annual, seasonal, monthly, and hourly AQI patterns.

### 4. AQI Forecasting

Select a monitoring station and explore its historical observation and experimental 24-hour-ahead AQI prediction.

## ⚙️ Installation and Local Setup

### Prerequisites

- Python 3.13
- Git
- Jupyter Notebook or VS Code

### 1. Clone the repository

```bash
git clone https://github.com/khushi-malviya/India-Air-Quality-Intelligence.git

cd India-Air-Quality-Intelligence
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download and prepare the dataset

Download the source dataset from:

https://github.com/Vonter/india-cpcb-aqi

Place the raw CSV at:

```text
data/raw/cpcb-aqi.csv
```

Create the required directories if they do not exist.

### 5. Run the notebooks in sequence

Execute the notebooks in this order:

1. `01_data_understanding.ipynb`
2. `02_data_transformation.ipynb`
3. `03_exploratory_data_analysis.ipynb`
4. `04_statistical_analysis.ipynb`
5. `05_feature_engineering.ipynb`
6. `06_predictive_modeling.ipynb`

The notebooks generate the processed datasets and saved model artifacts required by the application.

### 6. Launch the dashboard

From the project root:

```bash
streamlit run app/Home.py
```

The dashboard will open in your browser.

## ⚠️ Limitations and Considerations

This project is an analytical and forecasting prototype, not an operational pollution-alert system.

1. **Historical data:** The source dataset covers 2017–2023 and does not provide live AQI observations.
2. **Monitoring coverage:** The number of reporting stations changes over time, affecting national and city-level comparisons.
3. **Missing observations:** Missing readings and station timestamp gaps may affect feature availability.
4. **Station-specific forecasting:** The model was evaluated on future observations from the historical monitoring network; generalization to entirely unseen stations has not been established.
5. **Test sampling:** Reported model metrics use a 100,000-record sample from the 2023 test population.
6. **AQI ceiling:** Values at 500 occur in the dataset and may limit the interpretation of extreme pollution predictions.
7. **No causal inference:** The analysis identifies patterns and associations, not causal relationships.
8. **Not a live forecast:** Predictions are based on the latest available historical observation in the dataset.

## 🚀 Future Improvements

- Integrate updated AQI observations from reliable data sources.
- Add pollutant-level analysis for PM2.5, PM10, NO₂, SO₂, CO, and O₃ where suitable data is available.
- Explore additional forecasting models and compare their performance.
- Evaluate generalization to unseen monitoring stations.
- Improve model evaluation with station-wise and seasonal breakdowns.
- Add uncertainty intervals to predictions.
- Build automated data ingestion and model retraining workflows.
- Deploy the dashboard with an appropriate hosted data-storage solution.

## 📜 Data Attribution and License

The dataset is sourced from the third-party repository [VonTer/india-cpcb-aqi](https://github.com/Vonter/india-cpcb-aqi).

The source repository identifies its dataset under the **Open Database License (ODbL) 1.0**. Please review the original repository and license terms before redistributing the dataset or derivative database.

This project is an independent analytical project and is not affiliated with or officially endorsed by the Central Pollution Control Board (CPCB).

## 👩‍💻 Author

**Khushi Malviya**

B.Tech Computer Science Engineering | Data Science & AI

Interested in Data Analytics, Machine Learning, and transforming data into actionable business insights.

- GitHub: [khushi-malviya](https://github.com/khushi-malviya)
- Project Repository: [India Air Quality Intelligence](https://github.com/khushi-malviya/India-Air-Quality-Intelligence)

---

*Built as an end-to-end data analytics and machine learning portfolio project.*