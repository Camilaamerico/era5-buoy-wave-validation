# ERA5–Buoy Wave Validation

Reproducible Python workflow for validating ERA5 significant wave height against in-situ buoy observations.

## Overview

This project implements a reproducible scientific workflow to compare ERA5 wave reanalysis data with in-situ buoy observations.

The workflow includes:

- loading and standardizing ERA5 and buoy datasets;
- time-series preprocessing;
- temporal alignment of modeled and observed data;
- missing-data handling;
- statistical validation;
- separate evaluation of extreme wave conditions;
- generation of scientific figures;
- export of validation metrics;
- automated testing of core validation functions.

## Scientific context

The analysis focuses on significant wave height (`Hs`) and evaluates the performance of ERA5 against in-situ buoy observations.

The validation was restricted to **2025**, which corresponds to the period with a sufficiently consistent buoy record for comparison.

Two validation regimes are evaluated:

- **Global wave regime:** all matched ERA5–buoy observations in 2025;
- **Extreme wave regime:** observations where buoy-measured significant wave height is greater than or equal to 2.5 m.

The extreme-wave threshold is applied to the observed buoy data.

## Validation results

| Regime | N | R | R² | RMSE (m) | Bias (m) | Slope | Intercept |
|---|---:|---:|---:|---:|---:|---:|---:|
| Global | 8,286 | 0.903 | 0.816 | 0.294 | 0.118 | 0.776 | 0.458 |
| Extreme (`Hs ≥ 2.5 m`) | 655 | 0.866 | 0.750 | 0.324 | -0.207 | 0.902 | 0.082 |

The global validation indicates strong agreement between ERA5 and the buoy observations.

Under extreme wave conditions, ERA5 maintains a strong correlation with the observations, but the negative bias indicates an average underestimation of observed significant wave height during these conditions.

## Statistical metrics

The workflow calculates:

- number of matched observations (`N`);
- Pearson correlation coefficient (`R`);
- squared correlation coefficient (`R²`);
- root mean square error (`RMSE`);
- mean bias;
- linear regression slope;
- linear regression intercept.

Bias is defined as:

```text
ERA5 - Buoy
```

Therefore:

- positive bias indicates ERA5 overestimation;
- negative bias indicates ERA5 underestimation.

## Data preprocessing

ERA5 and buoy observations are standardized to a common datetime field before validation.

Buoy observations are aggregated to hourly timestamps to allow direct comparison with hourly ERA5 data.

Only temporally matched observations are retained in the validation dataset.

The final validation period is:

```text
2025-01-01 00:00:00 to 2025-12-31 23:00:00
```

The resulting dataset contains:

```text
8,286 matched observations
```

## Project structure

```text
era5-buoy-wave-validation/
│
├── data/
│
├── outputs/
│   ├── figures/
│   │   ├── scatter_2025.png
│   │   └── timeseries_2025.png
│   │
│   └── tables/
│       └── validation_metrics.csv
│
├── src/
│   ├── __init__.py
│   ├── load_data.py
│   ├── main.py
│   ├── metrics.py
│   ├── plots.py
│   └── preprocess.py
│
├── tests/
│   └── test_metrics.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Main technologies

- Python
- pandas
- NumPy
- Matplotlib
- pytest

## Outputs

The workflow generates three main outputs.

### Scatter validation

```text
outputs/figures/scatter_2025.png
```

The scatter figure compares in-situ buoy observations with ERA5 significant wave height for:

- the complete 2025 validation dataset;
- extreme-wave observations with `Hs ≥ 2.5 m`.

The figure also includes:

- the 1:1 reference line;
- the fitted linear regression;
- sample size;
- correlation coefficient;
- squared correlation coefficient;
- RMSE;
- bias.

### Time series

```text
outputs/figures/timeseries_2025.png
```

The time-series figure compares ERA5 and buoy significant wave height throughout 2025 and displays the 2.5 m extreme-wave threshold.

### Validation metrics

```text
outputs/tables/validation_metrics.csv
```

The CSV file contains the statistical metrics for the global and extreme-wave validation regimes.

## Running the workflow

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Run the complete validation workflow:

```bash
python src/main.py
```

The script will:

1. load ERA5 and buoy observations;
2. align the datasets temporally;
3. restrict the validation to 2025;
4. calculate global validation metrics;
5. identify extreme-wave observations;
6. calculate extreme-wave validation metrics;
7. export the results table;
8. generate the validation scatter plot;
9. generate the 2025 time series.

## Automated tests

Automated tests are included for the core validation functions.

Run:

```bash
python -m pytest -v
```

The current test suite verifies:

- validation metrics for a perfect model-observation match;
- validation metrics for a dataset with a known error;
- correct filtering of observations using the `Hs ≥ 2.5 m` threshold.

## Data

The raw datasets are not included in this repository.

The workflow expects the following files:

```text
data/era5_Marica_data.csv
data/buoy_data.csv
```

The datasets used in the workflow are derived from:

- ERA5 wave reanalysis;
- SiMCosta in-situ oceanographic buoy observations.

Raw scientific data are excluded from version control through `.gitignore`.

## Reproducibility

The project separates the workflow into independent modules for:

- data loading;
- preprocessing;
- statistical calculations;
- visualization;
- workflow execution;
- automated testing.

This structure allows each stage of the validation process to be inspected, modified, and tested independently.

## Requirements

Current dependencies:

```text
pandas
numpy
matplotlib
pytest
```

## Research application

This workflow was developed from a coastal wave-validation analysis performed for research on storm-wave conditions along the coast of Maricá, Rio de Janeiro, Brazil.

The repository focuses on the reproducible computational component of the validation procedure.

