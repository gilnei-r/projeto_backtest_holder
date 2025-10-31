# Feature Specification: Save Plots and Add MT5 Provider

**Feature Branch**: `005-save-plots-and-add-mt5-provider`
**Created**: 2025-10-30
**Status**: Draft
**Input**: User description: "Add new features to the project: 1 - Save all plots in .png files and don't show the plots. 2 - Include Metatrader 5 as new provider for stocks data. 3 - List the tickers that failed download data. Try to download these tickers data from Metatrader 5."

## Clarifications

### Session 2025-10-30

- Q: How should the system behave if the MetaTrader 5 connection is lost during a data download? → A: Attempt to reconnect for a configurable number of times. If it fails, log the error and add the ticker to the list of failed downloads.
- Q: What should happen if the directory for saving plots doesn't exist or isn't writable? → A: Attempt to create the directory. If it fails or is not writable, stop and report the error.
- Q: What specific conditions should be considered a "failure" when downloading data from yfinance, triggering a fallback to MetaTrader 5? → A: Any exception (e.g., HTTP error, no data found) or a timeout.
- Q: Should saving plots to files be enabled by default? → A: Yes, enabled by default.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Save Plots as Files (Priority: P1)

As a user, I want the backtesting script to automatically save all generated plots as PNG image files instead of displaying them on the screen, so that I can easily review and archive the results of my backtests.

**Why this priority**: This is a core functionality change that improves the usability of the script for automated runs and record-keeping.

**Independent Test**: Run the script. After execution, check the designated output folder to confirm that all expected plot images have been created and that no plot windows were displayed.

**Acceptance Scenarios**:

1.  **Given** the script is configured to save plots, **When** the script finishes execution, **Then** a new PNG file for each generated plot exists in the output directory.
2.  **Given** the script is executed, **When** the plotting functions are called, **Then** no plot windows are shown on the screen.

---

### User Story 2 - Integrate MetaTrader 5 as a Data Provider (Priority: P2)

As a user, I want the script to be able to download historical stock data from MetaTrader 5, so that I have an alternative and potentially more reliable data source if yfinance is unavailable or fails.

**Why this priority**: This improves the robustness and reliability of the data download process, which is critical for the accuracy of the backtests.

**Independent Test**: Configure the script to use MetaTrader 5. Run the script for a single ticker. Verify that the historical data is downloaded and loaded into the application correctly.

**Acceptance Scenarios**:

1.  **Given** the script is configured to use MetaTrader 5, **When** the data download process is triggered for a valid ticker, **Then** the historical data is successfully fetched from MetaTrader 5.
2.  **Given** `yfinance` fails to download data for a ticker, **When** the script is configured to use MetaTrader 5 as a fallback, **Then** the script automatically attempts to download the data for that ticker from MetaTrader 5.

---

### User Story 3 - Report Failed Ticker Downloads (Priority: P3)

As a user, I want to receive a clear list of any stock tickers for which data could not be downloaded from any source, so that I am aware of incomplete data in my backtest.

**Why this priority**: This provides essential feedback to the user about the quality and completeness of the data used in the backtest, preventing silent failures.

**Independent Test**: Manually introduce an invalid ticker symbol into the configuration. Run the script. Verify that the final output includes a message listing the invalid ticker as failed.

**Acceptance Scenarios**:

1.  **Given** a ticker symbol is invalid or data is unavailable from all configured sources, **When** the data download process completes, **Then** the ticker symbol is added to a list of failed downloads.
2.  **Given** the list of failed downloads is not empty, **When** the script finishes execution, **Then** the complete list of failed tickers is displayed to the user in the console output.

---

### Edge Cases

-   What happens if the connection to MetaTrader 5 is lost mid-download? The system will attempt to reconnect for a configurable number of times. If it fails, it will log the error and add the ticker to the list of failed downloads.
-   How does the system handle a ticker symbol that exists in yfinance but not in MetaTrader 5, or vice-versa? If a ticker is not found in a provider, it will be logged as a warning and the next provider will be tried. If not found in any provider, it will be listed as a failed ticker.
-   What happens if the specified directory for saving plots does not exist or is not writable? The script will attempt to create the directory if it doesn't exist. If it fails or if the directory is not writable, it will stop execution and report the error.

## Requirements *(mandatory)*

### Functional Requirements

-   **FR-001**: The system MUST provide a configuration option to enable or disable saving plots to files, and this option MUST be enabled by default.
-   **FR-002**: When enabled, the system MUST save each generated plot as a separate PNG file.
-   **FR-003**: The system MUST provide a configuration option to specify the output directory for the plot images, with a default value of 'results/plots/'.
-   **FR-004**: The system MUST NOT display plot windows on the screen when file saving is enabled.
-   **FR-005**: The system MUST be able to establish a connection to a running MetaTrader 5 terminal.
-   **FR-006**: The system MUST be able to download historical stock data from MetaTrader 5 for a given ticker and date range.
-   **FR-007**: The system MUST use yfinance as the primary data provider.
-   **FR-008**: If a data download from yfinance fails for a ticker (defined as any exception or timeout), the system MUST automatically attempt to download the data from MetaTrader 5 as a fallback.
-   **FR-009**: The system MUST keep a list of all ticker symbols for which data could not be downloaded from any provider.
-   **FR-010**: At the end of the execution, the system MUST display the list of failed tickers to the user.
-   **FR-011**: The system MUST have a configurable timeout and number of retries for MetaTrader 5 connection attempts, with default values of 10 seconds and 3 retries.
-   **FR-012**: If a ticker is not found in a data provider, the system MUST log a warning.

### Key Entities

-   **Stock Data**: Represents historical price and dividend data for a ticker. Attributes include Open, High, Low, Close, Volume, and Dividends for a given date.
-   **Data Provider**: An abstraction for a source of historical stock data (e.g., yfinance, MetaTrader 5).
-   **Plot**: A graphical representation of backtest results, such as the capital curve or performance metrics.

## Success Criteria *(mandatory)*

### Measurable Outcomes

-   **SC-001**: 100% of generated plots are successfully saved as valid PNG files in the specified directory.
-   **SC-002**: The script execution time does not increase by more than 10% on average when fallback to MetaTrader 5 is triggered for a small number of tickers.
-   **SC-003**: 100% of ticker download failures from all sources are reported to the user upon script completion.
-   **SC-004**: The plot-saving feature can be enabled or disabled with a single configuration change.