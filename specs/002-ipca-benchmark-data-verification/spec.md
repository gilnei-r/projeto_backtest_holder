# Feature Specification: IPCA Benchmark, Ticker Plot, and Data Verification

**Feature Branch**: `002-ipca-benchmark-data-verification`
**Created**: 2025-10-28
**Status**: Draft
**Input**: User description: "Implement benchmark based on IPCA + x% like it is done with SELIC. The "x" value shall be informed in config.py file. Create new bar plot with the total value of each ticker. Implement a feature that verify the downloaded data and only download again if idata is not update up to current day."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - IPCA+x% Benchmark (Priority: P1)

As a user, I want to see my portfolio performance benchmarked against IPCA + x%, so that I can evaluate its real return above inflation. The value of 'x' should be configurable in `config.py`.

**Why this priority**: This is a core feature that provides a key performance indicator for Brazilian investors.

**Independent Test**: The benchmark calculation can be tested independently of the plotting by providing a set of portfolio values and IPCA data and verifying the calculated benchmark values.

**Acceptance Scenarios**:

1. **Given** a portfolio history and corresponding IPCA data, **When** the backtest is run, **Then** the final report must include a comparison against the IPCA + x% benchmark.
2. **Given** the user specifies a value for x in `config.py`, **When** the backtest is run, **Then** the benchmark must be calculated as IPCA + the specified x percentage.

---

### User Story 2 - Ticker Value Plot (Priority: P2)

As a user, I want to see a bar plot showing the total current value of each ticker in my portfolio, so that I can easily visualize the distribution of my assets.

**Why this priority**: This provides an intuitive visualization of portfolio composition.

**Independent Test**: The plotting function can be tested independently by providing a list of tickers and their values and verifying the generated plot.

**Acceptance Scenarios**:

1. **Given** a portfolio with multiple tickers, **When** the backtest is complete, **Then** a bar plot is generated showing the total value of each ticker.

---

### User Story 3 - Data Verification (Priority: P1)

As a user, I want the application to verify if the downloaded financial data is up-to-date, so that I don't have to re-download data unnecessarily and the backtest runs faster.

**Why this priority**: This improves the performance and efficiency of the application.

**Independent Test**: The data verification logic can be tested by checking mock data files with different timestamps.

**Acceptance Scenarios**:

1. **Given** that the financial data files are up-to-date, **When** the application starts, **Then** it should not re-download the data.
2. **Given** that the financial data files are outdated, **When** the application starts, **Then** it should download the new data.

### Edge Cases

- What happens if the IPCA data is not available for a specific period?
- How does the system handle a portfolio with only one ticker for the bar plot?
- What happens if the user provides an invalid format for the date in the data files?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST allow the user to configure the 'x' value for the IPCA + x% benchmark in the `config.py` file.
- **FR-002**: The system MUST fetch historical IPCA data from a reliable source.
- **FR-003**: The system MUST calculate the cumulative IPCA + x% return over the backtest period.
- **FR-004**: The system MUST display the IPCA + x% benchmark alongside the portfolio performance in the final report and/or plot.
- **FR-005**: The system MUST generate a bar plot visualizing the total final value of each individual stock ticker in the portfolio.
- **FR-006**: The bar plot MUST have clear labels for each ticker and the corresponding value.
- **FR-007**: The system MUST check the last modified date of the downloaded data files.
- **FR-008**: The system MUST only download new data if the existing data is not updated to the current day.

*Example of marking unclear requirements:*

- **FR-009**: The ticker value bar plot MUST be sorted by descending by total value.

### Key Entities *(include if feature involves data)*

- **IPCA Benchmark**: Represents the calculated benchmark values over time. Attributes: date, cumulative_return.
- **Ticker Value**: Represents the final monetary value of a single ticker. Attributes: ticker_symbol, total_value.
- **Data File**: Represents a downloaded financial data file. Attributes: file_path, last_modified_date.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The IPCA + x% benchmark is correctly calculated and displayed on the performance chart, allowing for a direct visual comparison against the portfolio's equity curve.
- **SC-002**: A new bar chart is generated and displayed, clearly showing the name and total value of each asset held at the end of the simulation period.
- **SC-003**: The user can successfully configure the 'x' value for the IPCA benchmark in `config.py` and see the change reflected in the results.
- **SC-004**: The application startup time is significantly reduced when the financial data is already up-to-date.