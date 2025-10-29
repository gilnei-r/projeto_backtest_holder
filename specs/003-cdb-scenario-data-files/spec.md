# Feature Specification: CDB Scenario and Data Persistence

**Feature Branch**: `003-cdb-scenario-data-files`  
**Created**: 2025-10-28  
**Status**: Draft  
**Input**: User description: "Implement the code with these features: 1 - save each ticker downloaded data into single .csv files. 2 - Save SELIC and IPCA downloaded data in single .csv files. This data also shall be downloaded once a day. 3 - Create a new backtest scenario where a % of the portfolio is invested in SELIC, like a CDB fund. The % value of the CDB shall be setted in config file. The mensal contribution shall be done in CDB if the total value of it is less than the setted %."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Data Caching & Persistence (Priority: P1)

As a user, I want the application to save historical stock data (tickers, SELIC, IPCA) into local CSV files so that subsequent runs are faster and don't require repeated downloads. Data should be refreshed only if it's older than one day.

**Why this priority**: This is a foundational improvement that enhances performance and reduces reliance on external APIs, making development and repeated tests much more efficient.

**Independent Test**: Can be fully tested by running the script twice. The first run should create files. The second run (within 24 hours) should be significantly faster and show logs indicating that cached data was used.

**Acceptance Scenarios**:

1. **Given** no local data files exist, **When** the main script is executed, **Then** CSV files for each ticker, SELIC, and IPCA are created in a `data/` directory.
2. **Given** local data files exist and are less than 24 hours old, **When** the main script is executed, **Then** the script uses the data from the CSV files without downloading new data.
3. **Given** local data files exist and are more than 24 hours old, **When** the main script is executed, **Then** the script downloads new data and overwrites the old files.

---

### User Story 2 - CDB/SELIC Investment Scenario (Priority: P2)

As a user, I want to run a new backtest scenario that allocates a configurable percentage of my portfolio to a fixed-income asset (simulating a CDB linked to SELIC). This allows me to test a more defensive investment strategy.

**Why this priority**: This introduces a new core feature that expands the strategic analysis capabilities of the tool, which is the primary purpose of the application.

**Independent Test**: Can be tested by running the main script. A new set of results and plots for this specific scenario should be generated, which can be compared against the existing scenarios.

**Acceptance Scenarios**:

1. **Given** a target percentage for the CDB/SELIC asset is defined in `config.py`, **When** the main script runs, **Then** a new backtest is performed that includes this asset in the portfolio.
2. **Given** the new scenario has run, **When** the results are generated, **Then** a new Excel file (`backtest_results_cdb.xlsx`) and a corresponding capital curve plot are created.

---

### User Story 3 - CDB/SELIC Rebalancing Rule (Priority: P3)

As a user, I want the monthly contribution in the new CDB scenario to be automatically invested in the CDB/SELIC asset if its total value has fallen below the target percentage. This helps maintain the desired asset allocation without manual intervention.

**Why this priority**: This defines the core logic of the new scenario. It's essential for the scenario to function as intended, but it depends on User Story 2 being implemented first.

**Independent Test**: The logic can be verified by examining the generated Excel file for the CDB scenario, specifically the columns that show where each monthly contribution was allocated.

**Acceptance Scenarios**:

1. **Given** the CDB/SELIC asset's value is below its target percentage of the total portfolio, **When** a monthly contribution occurs, **Then** the contribution is allocated to the CDB/SELIC asset.
2. **Given** the CDB/SELIC asset's value is at or above its target percentage, **When** a monthly contribution occurs, **Then** the contribution is allocated to the stock with the lowest total monetary value (the default behavior).

---

### Edge Cases

- What happens if the `config.py` file is missing the new CDB percentage setting? The script should handle this gracefully, either by using a default value or raising a clear error.
- How does the system handle a failed data download for one of the assets? Does it proceed with stale data or stop the execution?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST save historical data for each stock ticker into a separate CSV file in a `data/` directory.
- **FR-002**: System MUST save historical SELIC and IPCA data into their own separate CSV files in the `data/` directory.
- **FR-003**: System MUST check the last modification date of the saved data files before attempting to download new data.
- **FR-004**: System MUST NOT download new data if the existing data file is less than one day old.
- **FR-005**: System MUST provide a new backtesting scenario that simulates a portfolio with a portion invested in a SELIC/CDB-like asset.
- **FR-006**: The target percentage for the SELIC/CDB asset MUST be configurable in the `config.py` file.
- **FR-007**: In the new scenario, if the SELIC/CDB asset is below its target percentage, the **entire** monthly contribution MUST be invested into the SELIC/CDB asset.
- **FR-008**: The system MUST create the `data/` directory for storing CSV files if it does not already exist.

### Key Entities *(include if feature involves data)*

- **Ticker Data CSV**: Represents a file containing historical price data for a single stock. Key attributes include Date, Open, High, Low, Close, Volume, and Dividends.
- **Economic Indicator Data CSV**: Represents a file containing historical data for an economic indicator (SELIC or IPCA). Key attributes include Date and Value.
- **CDB/SELIC Asset**: A virtual asset within the backtest scenario representing a fixed-income investment. Its value is calculated based on the compounding SELIC rate.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: On the first execution, CSV files for all configured tickers, SELIC, and IPCA are successfully created in the `data/` directory.
- **SC-002**: On subsequent executions performed within the same day, the script execution time is at least 50% faster, and console logs indicate that cached data is being used.
- **SC-003**: A new set of outputs, including `backtest_results_cdb.xlsx` and a plot titled "Capital Curve - CDB Scenario", is generated upon completion.
- **SC-004**: In the `backtest_results_cdb.xlsx` report, 100% of monthly contributions are allocated to the CDB/SELIC asset in months where its total value is below the configured target percentage of the portfolio.
