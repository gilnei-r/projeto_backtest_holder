# Task Plan: Add Multiple Data Providers and Enhance Reporting

**Version**: 1.0
**Date**: 2025-10-30

This document breaks down the implementation of the feature "Add Multiple Data Providers and Enhance Reporting" into actionable tasks.

## Implementation Strategy

The implementation will be phased. First, the foundational configuration and data loader dispatching will be set up. Second, the Metastock provider will be implemented. Third, the contribution calculation and reporting enhancements will be developed. This ensures a logical progression and allows for testing at each stage.

## Phase 1: Foundational Setup

**Goal**: Prepare the application to handle multiple data sources.

- [x] T001 Add `DATA_SOURCE` and `METASTOCK_PATH` variables to `config.py`.
- [x] T002 In `data_loader.py`, refactor the main data loading function to act as a dispatcher, calling the appropriate provider function based on the `DATA_SOURCE` value.

## Phase 2: User Story 1 - Metastock Data Provider

**Goal**: Implement the ability to load data from local Metastock CSV files.
**Independent Test Criteria**: Set `DATA_SOURCE='metastock'` in the config. The script should run without errors, and the output should reflect data loaded from the local CSV files specified in `METASTOCK_PATH`.

- [x] T003 [US1] In `data_loader.py`, create a new private function `_load_from_metastock()`.
- [x] T004 [US1] In `_load_from_metastock()`, implement the logic to check for the existence of the `METASTOCK_PATH` and raise a `FileNotFoundError` if it's invalid.
- [x] T005 [US1] In `_load_from_metastock()`, implement the ticker symbol mapping to remove the `.SA` suffix when constructing file names.
- [x] T006 [US1] In `_load_from_metastock()`, iterate through tickers, read each corresponding CSV file using `pandas`, and handle missing files by logging a warning to the console.
- [x] T007 [US1] In `_load_from_metastock()`, ensure the loaded data is processed into a DataFrame with a `DatetimeIndex` and an `Adj Close` column, matching the format of the other data loaders.
- [x] T008 [US1] In `data_loader.py`, wire the `_load_from_metastock()` function into the dispatcher logic created in T002.

## Phase 3: User Stories 2 & 3 - Enhanced Reporting

**Goal**: Calculate total contributions and display them in plots and Excel files.
**Independent Test Criteria**: Run a monthly contribution scenario. The generated `distribuicao_valor.png` must show side-by-side bars for "Current Value" and "Total Contribution". The output Excel file must contain new columns with the correct total contribution figures.

- [x] T009 [US2, US3] In `scenarios.py`, modify `run_backtest_aportes_mensais` and `run_backtest_cdb_misto` to calculate and return a DataFrame of cumulative contributions along with the other results.
- [x] T010 [US2] [P] In `plotting.py`, update the function signature of `plot_distribuicao_valor()` to accept the new contributions DataFrame.
- [x] T011 [US2] [P] In `plotting.py`, refactor `plot_distribuicao_valor()` to merge the value and contribution data into a single DataFrame suitable for plotting with `seaborn.barplot` (using a `hue` parameter).
- [x] T012 [US3] [P] In `main.py`, update the calls to the scenario functions to receive the contributions DataFrame.
- [x] T013 [US3] [P] In `main.py`, modify the logic that saves the results to Excel to include the new total contribution data as separate columns in the summary sheet.

## Phase 4: Polish & Finalization

**Goal**: Ensure code quality, verify functionality, and update documentation.

- [x] T014 [P] Review all new and modified code for clarity, comments, and adherence to project style.
- [x] T015 [P] Update the main `README.md` to explain the new `DATA_SOURCE` and `METASTOCK_PATH` configuration options.
- [x] T016 Manually run the script with each of the three data source options (`yahoofinance`, `metastock`, `metatrader5`) to ensure no regressions were introduced and that all features work as expected.

## Dependencies

- **Phase 2 (US1)** depends on **Phase 1**.
- **Phase 3 (US2, US3)** depends on **Phase 1**. The core calculation (T009) must be done before the parallel plotting and Excel tasks.
- **Phase 4** depends on all previous phases.

### Parallel Execution Opportunities

- Within Phase 3, the plotting tasks (T010, T011) and the Excel tasks (T012, T013) can be worked on in parallel after the core calculation task (T009) is complete.
- The tasks in Phase 4 can also be parallelized.
