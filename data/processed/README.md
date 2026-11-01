# Processed Data

This folder contains transformed and analysis-ready versions of the
India CPCB Air Quality dataset.

## Files

### 1. air_quality_hourly.parquet

- Contains the complete hourly-level dataset.
- Original wide-format data transformed into long format.
- Includes station metadata, date, hour, timestamp, AQI, and AQI status.
- Preserves missing and out-of-range AQI observations.

### 2. air_quality_analytical.parquet

- Contains the complete transformed dataset with an additional
  AQI_Valid column.
- AQI_Valid contains values only when AQI_Status is "valid".
- Missing and out-of-range readings are represented as null in AQI_Valid.
- Intended for statistical analysis and visualisation.

## Transformation Summary

- Original records: 562,878
- Original columns: 29
- Hourly observations after transformation: 13,509,072
- Valid AQI readings: 12,473,485
- Missing AQI readings: 1,035,531
- Out-of-range readings (AQI > 500): 56

## Data Handling Decisions

- Missing AQI values were not replaced with zero or averages.
- Out-of-range readings were retained in the original AQI column.
- Out-of-range readings were excluded from AQI_Valid.
- Station identity uses State, City, and Station Name.
- Parquet format was selected for efficient storage and analytical use.
