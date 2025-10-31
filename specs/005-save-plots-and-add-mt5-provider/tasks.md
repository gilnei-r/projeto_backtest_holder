# Tasks for "Save Plots and Add MT5 Provider"

This file breaks down the implementation of the feature into actionable tasks, organized by user story.

## Phase 1: Setup

- [x] T001 [P] Install the `MetaTrader5` package using pip.

## Phase 2: Foundational

- [x] T002 Add new configuration options to `config.py` for enabling/disabling plot saving, specifying the plot directory, enabling/disabling the MT5 provider, and setting the MT5 connection timeout and retries.

## Phase 3: User Story 1 - Save Plots as Files

**Goal**: Modify the plotting functions to save plots instead of showing them.

**Independent Test**: Run the script and verify that the plot images are created in the output folder and that no plot windows are displayed.

- [x] T003 [US1] Modify the `plot_results` function in `plotting.py` to save the plots as PNG files in the configured directory.
- [x] T004 [US1] In `plotting.py`, use `plt.close()` after saving each plot to prevent it from being displayed.

## Phase 4: User Story 2 - Integrate MetaTrader 5 as a Data Provider

**Goal**: Add the MetaTrader 5 integration to the data loader.

**Independent Test**: Configure the script to use MetaTrader 5 and run it for a single ticker. Verify that the data is downloaded correctly.

- [x] T005 [US2] In `data_loader.py`, create a new function to connect to the MetaTrader 5 terminal.
- [x] T006 [US2] In `data_loader.py`, create a new function to download historical data from MetaTrader 5 for a given ticker.
- [x] T007 [US2] Modify the `download_stock_data` function in `data_loader.py` to use the MetaTrader 5 functions as a fallback if `yfinance` fails.

## Phase 5: User Story 3 - Report Failed Ticker Downloads

**Goal**: Modify the main script to handle and report failed downloads.

**Independent Test**: Introduce an invalid ticker symbol in the configuration and run the script. Verify that the failed ticker is reported in the output.

- [x] T008 [US3] In `main.py`, modify the main function to keep a list of failed tickers.
- [x] T009 [US3] In `main.py`, print the list of failed tickers at the end of the execution.

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T010 [P] Create a new test file `tests/test_mt5_integration.py` to test the MetaTrader 5 integration.
- [x] T011 [P] Add unit tests to `tests/test_plotting.py` to verify that plots are saved correctly.
- [x] T012 [P] Add unit tests to `tests/test_data_loader.py` to test the fallback mechanism.

## Dependencies

- User Story 1 (Phase 3) depends on Phase 2.
- User Story 2 (Phase 4) depends on Phase 2.
- User Story 3 (Phase 5) depends on Phase 4.

## Parallel Execution

- Tasks within Phase 3 can be executed in parallel.
- Tasks within Phase 4 can be executed in parallel.
- Tasks within Phase 6 can be executed in parallel.

## Implementation Strategy

The implementation will follow the phases in order, starting with the foundational setup and then implementing each user story independently. The MVP (Minimum Viable Product) will consist of completing Phase 3 (User Story 1).
