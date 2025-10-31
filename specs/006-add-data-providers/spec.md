# Feature Specification: Add Multiple Data Providers and Enhance Reporting

**Version**: 1.0
**Status**: In Review
**Author**: Gemini
**Created**: 2025-10-30
**Last Updated**: 2025-10-30

## 1. Feature Name

Add Multiple Data Providers and Enhance Reporting

## 2. Feature Description

This feature introduces the ability for users to select from multiple data sources (Yahoo Finance, MetaTrader 5, Metastock) for downloading historical stock data. It also enhances the "Value Distribution" plot and corresponding Excel reports by including total contribution data alongside the current value for each asset, providing a clearer picture of performance.

## 3. User Scenarios

### 3.1. As a user, I want to configure the script to use my local Metastock database so that I can run backtests on my own private data.

- **Given** I have a Metastock database located at a specific path on my system.
- **When** I edit the configuration file to select "metastock" as the data provider and specify the correct path.
- **And** I run the `main.py` script.
- **Then** the script fetches all required historical data from my local Metastock files instead of Yahoo Finance.
- **And** the backtest completes successfully using this data.

### 3.2. As a user, I want to see the total amount I've invested in each asset compared to its current value so that I can quickly assess its performance.

- **Given** I have run a backtest scenario with monthly contributions.
- **When** the "Value Distribution" (`distribuicao_valor`) plot is displayed.
- **Then** I can see, for each stock and for the CDB, a pair of side-by-side bars: one representing the asset's current total value and the other representing the total cumulative contribution made to that asset.

### 3.3. As a user, I want the Excel report to include the total contribution data so that I can perform my own offline analysis.

- **Given** the script has finished running and generated the Excel result files.
- **When** I open `backtest_results_monthly.xlsx` or `backtest_results_cdb_mixed.xlsx`.
- **Then** I find new columns in the summary sheet that list the total contribution amount for each individual stock and for the CDB asset, matching the values shown in the plot.

## 4. Functional Requirements

| ID | Requirement | Acceptance Criteria |
|----|-------------|---------------------|
| FR1 | **Configure Data Source** | The user can specify the desired data source (`yahoofinance`, `metatrader5`, or `metastock`) in the `config.py` file. |
| FR2 | **Metastock Data Loading** | When `metastock` is the selected source, the system must read data from the path defined in a new `METASTOCK_PATH` variable in `config.py`. |
| FR3 | **Ticker Symbol Mapping** | The system must automatically remove the `.SA` suffix from ticker symbols when fetching data from the Metastock source to ensure correct file matching. |
| FR4 | **Enhanced Value Distribution Plot** | The `distribuicao_valor.png` plot must render side-by-side bars for "Current Value" and "Total Contribution" for each stock ticker and for the CDB asset. |
| FR5 | **Enhanced Excel Reports** | The `backtest_results_monthly.xlsx` and `backtest_results_cdb_mixed.xlsx` files must contain new columns with the total contribution figures for each stock and for the CDB. |
| FR6 | **Data Source Fallback/Error** | If the configured data source is unavailable, the script must terminate gracefully with a clear error message. This includes explicitly checking that the `METASTOCK_PATH` is valid and accessible when `metastock` is the selected source. |
| FR7 | **Handle Missing Ticker Files** | When using the `metastock` source, if a ticker's data file is missing, the system must issue a warning and continue the backtest with the remaining available tickers. |

## 5. Success Criteria

## 6. Clarifications

### Session 2025-10-30

- Q: What should happen if a specific stock's data file is missing from the Metastock directory while others are present? → A: Skip the missing stock(s) and continue the backtest with the available data, issuing a warning.
- Q: How should the script behave if the `METASTOCK_PATH` configured in `config.py` is invalid or inaccessible? → A: Terminate immediately with a clear error message stating the path is invalid.

- **SC1**: A user can successfully execute a complete backtest using any of the three supported data sources without any data-related errors.
- **SC2**: The "Value Distribution" plot accurately displays both the current market value and the total contributed amount for each asset, allowing for a direct visual comparison of performance.
- **SC3**: The total contribution data in the generated Excel files for monthly scenarios exactly matches the values used for the contribution bars in the plot.
- **SC4**: Changing the data source in the configuration file correctly switches the data provider for the next script run.

## 6. Assumptions

- The Metastock database at the specified path is correctly formatted and contains files corresponding to the tickers defined in the configuration.
- The `METASTOCK_PATH` directory contains individual Comma-Separated Values (`.csv`) files for each ticker.
- The user has the necessary file system permissions to read from the configured `METASTOCK_PATH`.
- The existing `metatrader5` integration is functional and serves as a valid model for adding new data providers.

## 7. Out of Scope

- Q: How should the script behave if the `METASTOCK_PATH` configured in `config.py` is invalid or inaccessible? → A: Terminate immediately with a clear error message stating the path is invalid.
- Q: What is the expected file format for individual security files within the `METASTOCK_PATH` directory? → A: Standard Comma-Separated Values (`.csv`) files, with one file per ticker.