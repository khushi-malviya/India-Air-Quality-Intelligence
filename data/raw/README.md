# Raw Data

This directory is intended for source datasets retained in their original form.

## Historical AQI Dataset

Source repository: https://github.com/Vonter/india-cpcb-aqi

Data dictionary: https://github.com/Vonter/india-cpcb-aqi/blob/main/DATA.md

The dataset is a third-party compilation of CPCB-derived data. Consult the source repository for its licensing, attribution, and usage conditions.

## Current AQI Snapshot

A separate real-time AQI CSV from data.gov.in was investigated during project planning. It represents a snapshot rather than a historical time series.

## Data Handling Rules

- Preserve original source files without overwriting them.
- Record the source, retrieval date, and relevant license information.
- Do not commit large datasets or sensitive credentials to Git.
- Perform transformations on copies of the raw data.
- Validate schema, missingness, date coverage, and station identifiers before analysis.

Dataset files are intentionally excluded from version control.
