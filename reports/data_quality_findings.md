# Data Quality Findings — India Air Quality Intelligence

## 1. Dataset Overview

- Total records: 562,878
- Total columns: 29
- Time period: 1 January 2017 – 31 December 2023
- Unique station identity combinations: 529
- Valid hourly AQI measurements: 12,473,541
- Missing hourly measurements: 1,035,531 (7.67%)

## 2. Duplicate Record Analysis

No duplicate records were identified using the composite key:

`State + City + Station Name + Date`

However, Station ID is not reliable as a standalone station identifier in this dataset because some IDs map to multiple station names.

The composite station identity will therefore be used for station-level analysis.

## 3. AQI Range Anomalies

A total of 56 hourly readings exceed 500. All 56 occur in 2017.

The maximum recorded value is 3,797.

The most affected stations are:
- Punjab Agricultural University, Ludhiana: 40 readings
- Sector 125, Noida: 7 readings
- Rabindra Bharati University, Kolkata: 3 readings
- PWD Grounds, Vijayawada: 3 readings
- NSIT Dwarka, Delhi: 2 readings
- Sirifort, Delhi: 1 reading

The value 900 occurs 33 times, primarily at the Ludhiana station over consecutive hourly observations.

These values are treated as suspicious and flagged for quality review. Their original values are retained.

## 4. Missing Data

Approximately 7.67% of possible hourly AQI measurements are missing. Missing values will not be automatically replaced with zero or mean values.

Missingness patterns will be examined before selecting any imputation strategy.

## 5. Data Limitations

- Station ID is not a reliable unique station identifier in the compiled dataset.
- Station coverage and record counts increase substantially over the years.
- Extreme AQI values are concentrated in 2017 and require further investigation.
- The dataset contains hourly measurements in a wide format.

## 6. Cleaning Strategy

1. Preserve the original raw dataset.
2. Use State, City, and Station Name as the station identity.
3. Convert hourly columns into a structured analytical format.
4. Flag AQI values above 500.
5. Retain missing values until their patterns are understood.
6. Compare analytical results with and without flagged readings.
7. Account for changing station coverage in historical comparisons.

**Status:** Initial data-quality audit completed. Further validation and transformation are pending.