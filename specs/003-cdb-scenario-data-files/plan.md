# Implementation Plan: CDB Scenario and Data Persistence

**Branch**: `003-cdb-scenario-data-files` | **Date**: 2025-10-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `C:\Git\Projeto_B&H\specs\003-cdb-scenario-data-files\spec.md`

## Summary

This feature introduces two main capabilities: 1) A data caching mechanism to save financial data (tickers, economic indicators) into local CSV files, which are updated only once a day. 2) A new backtesting scenario where a configurable percentage of the portfolio is allocated to a fixed-income asset (CDB/SELIC), with monthly contributions automatically rebalancing the allocation.

The technical approach will involve modifying the existing `data_loader.py` to check file modification times for caching, creating a new `run_scenario_cdb_mixed` function in `scenarios.py`, and adding a `CDB_PERCENTAGE` parameter to `config.py`.

## Technical Context

**Language/Version**: Python 3.x
**Primary Dependencies**: `pandas`, `yfinance`, `python-bcb`, `matplotlib`
**Storage**: CSV files stored in a `./data/` directory.
**Testing**: `pytest` (inferred from existing `tests/` structure).
**Target Platform**: Local machine (desktop).
**Project Type**: Single project (script-based).
**Performance Goals**: Subsequent script executions within 24 hours should be at least 50% faster due to data caching.
**Constraints**: N/A
**Scale/Scope**: The feature is scoped to the existing backtesting script and its current operational scale.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

*   **Code Quality:** **PASS**. The plan is to extend the existing modular design (`data_loader.py`, `scenarios.py`), ensuring the new code is clean and maintainable.
*   **Testing Standards:** **PASS**. New unit tests will be created for the data caching logic and the new CDB scenario logic to meet the testing requirements.
*   **User Experience Consistency:** **PASS**. N/A for a CLI script, but configuration changes in `config.py` are consistent with existing practices.
*   **Performance Requirements:** **PASS**. The data caching feature is explicitly designed to improve performance by reducing redundant API calls, aligning with this principle.

## Project Structure

### Documentation (this feature)

```text
specs/003-cdb-scenario-data-files/
├── plan.md              # This file
├── research.md          # Phase 0 output: Decisions on caching and storage
├── data-model.md        # Phase 1 output: CSV and virtual entity structures
├── quickstart.md        # Phase 1 output: How to use the new feature
└── contracts/           # Phase 1 output: (empty, not an API-driven feature)
```

### Source Code (repository root)

```text
# Single project structure
.
├── config.py           # MODIFIED: Add CDB_PERCENTAGE
├── data_loader.py      # MODIFIED: Add caching logic
├── scenarios.py         # MODIFIED: Add run_scenario_cdb_mixed
├── main.py             # MODIFIED: Call the new scenario
├── plotting.py         # MODIFIED: Add plotting for the new scenario
|
├── data/                 # CREATED: To store *.csv data files
│   ├── PETR4.SA.csv      # Example created file
│   ├── SELIC.csv         # Example created file
│   └── ...
|
└── tests/
    ├── test_data_loader.py # MODIFIED: Add tests for caching
    └── test_scenarios.py   # MODIFIED: Add tests for CDB scenario
```

**Structure Decision**: The existing single-project structure will be maintained. Changes will be made to existing modules to incorporate the new functionality. A new `data/` directory will be created at the project root to house the cached CSV files, separating data from source code as per standard practice.

## Complexity Tracking

N/A - No constitutional violations were identified.