# Implementation Plan: Add Multiple Data Providers and Enhance Reporting

**Version**: 1.0
**Status**: In Progress
**Author**: Gemini
**Created**: 2025-10-30
**Last Updated**: 2025-10-30

**Feature Spec**: [spec.md](./spec.md)

## 1. Technical Context

- **Affected Components**:
  - `config.py`: To add new configuration variables for data source selection.
  - `data_loader.py`: To implement the new logic for selecting the data provider and to add the Metastock CSV reading function.
  - `scenarios.py`: To calculate and store total contributions for each asset.
  - `plotting.py`: To modify the `plot_distribuicao_valor` function to render the new side-by-side bar chart.
  - `main.py`: To handle the updated data structures and pass them to the plotting and saving functions.

- **Key Technologies**:
  - `pandas`: For data manipulation and reading CSV files.
  - `matplotlib`/`seaborn`: For plotting.
  - No new external libraries are required.

- **Integration Points**:
  - A new function in `data_loader.py` will be called based on the `DATA_SOURCE` value in `config.py`.
  - The data returned from the new loader must match the format of the existing `yfinance` loader.

- **Data Storage**:
  - The script will read from `.csv` files in the user-defined `METASTOCK_PATH`.
  - The output Excel files (`backtest_results_*.xlsx`) will be modified to include new columns for total contributions.

- **Testing Strategy**:
  - New unit tests will be created for the Metastock data loader function in `tests/test_data_loader.py`.
  - Existing tests for scenarios and plotting will be updated to assert the presence and correctness of the new contribution data.

## 2. Constitution Check

- **[✅] Code Quality**: All new code will follow existing style and be encapsulated in functions.
- **[✅] Testing Standards**: New unit tests will be added for the data loading logic. Existing tests will be adapted.
- **[✅] User Experience Consistency**: The changes are additive and maintain the existing script execution flow. Configuration is consistent with other parameters.
- **[✅] Performance Requirements**: Reading from local CSVs is expected to be faster than downloading from the network. The additional calculations are minimal and should not impact performance.

**Result**: All constitutional gates passed.

## 3. Phase 0: Outline & Research

**Status**: Completed

- **Summary**: The primary unknown was the expected structure of the Metastock CSV files. A decision was made to require `Date` and `Adj Close` columns to ensure consistency with `yfinance` data while maintaining flexibility.

- **Artifacts**:
  - [research.md](./research.md)

## 4. Phase 1: Design & Contracts

**Status**: Completed

- **Summary**: The design focuses on modifying existing components to be data-source-aware. A new data loading function will be created for Metastock, and the data structures for scenarios and plotting will be adapted to include contribution data. No external-facing APIs are affected.

- **Artifacts**:
  - [data-model.md](./data-model.md)
  - [quickstart.md](./quickstart.md)

## 5. Phase 2: Task Decomposition

**Status**: Pending

(This section will be filled by the `/speckit.tasks` command.)