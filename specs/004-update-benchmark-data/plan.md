# Implementation Plan: Update Benchmark Data

**Feature Branch**: `004-update-benchmark-data`  
**Feature Spec**: [spec.md](spec.md)

## Technical Context

- **Programming Language**: Python
- **Key Libraries/Frameworks**:
  - `yfinance`: For downloading stock data.
  - `python-bcb`: For fetching Brazilian economic indicators (CDI).
  - `pandas`: For data analysis and manipulation.
  - `matplotlib`: For plotting and visualization.
- **Integration Points**:
  - Central Bank of Brazil (BCB) API: To fetch the CDI rate (series code 12).
- **Data Storage**:
  - CSV files in the `data/` directory for caching downloaded data.
- **Unknowns/Risks**:
  - The BCB API might have rate limits or other usage policies that need to be considered. (NEEDS CLARIFICATION)
  - The structure of the data returned by the BCB API for CDI might be different from the SELIC data structure, requiring adjustments in the data processing logic. (NEEDS CLARIFICATION)

## Constitution Check

- **I. Code Quality**: All new code will be written in a clean, readable, and maintainable way, following Python best practices.
- **II. Testing Standards**: New unit tests will be added to cover the new CDI data fetching and processing logic, as well as the updated IPCA+ benchmark calculation.
- **III. User Experience Consistency**: The changes are in the backend and data processing, so there are no direct UI changes. The benchmark label will be updated from "SELIC" to "CDI" in the output charts and tables, which is a minor and consistent change.
- **IV. Performance Requirements**: The performance of the data fetching and processing will be monitored to ensure no regressions are introduced.

## Phase 0: Outline & Research

- **Research Tasks**:
  - Investigate the BCB API documentation for rate limits and usage policies.
  - Analyze the data structure returned by the BCB API for CDI (series code 12) and compare it with the existing SELIC data structure.

## Phase 1: Design & Contracts

- **Data Model**:
  - No new data models are required. The existing `BenchmarkData` entity will be used, with the series name changed to "CDI" and the series code to 12.
- **API Contracts**:
  - No new API contracts are required as the changes are internal to the data processing logic.
- **Quickstart**:
  - The `README.md` will be updated to reflect the change from SELIC to CDI as the primary benchmark.

## Phase 2: Implementation Tasks

- **Task 1**: Modify the `data_loader.py` script to fetch CDI data (series code 12) from the BCB API instead of SELIC data.
- **Task 2**: Update the `scenarios.py` script to use the CDI data as the primary benchmark.
- **Task 3**: Update the `scenarios.py` script to adjust the IPCA+ benchmark value only on the last day of each month.
- **Task 4**: Update the `plotting.py` script to display "CDI" as the benchmark label in all relevant charts and tables.
- **Task 5**: Add new unit tests to `tests/test_data_loader.py` and `tests/test_scenarios.py` to cover the new functionality.
- **Task 6**: Run all tests and ensure they pass.
- **Task 7**: Update the `README.md` file.