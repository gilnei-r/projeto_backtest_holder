# Feature Specification: Update Benchmark Data

**Feature Branch**: `004-update-benchmark-data`  
**Created**: 2025-10-29  
**Status**: Draft  
**Input**: User description: "Change the banchmark data from SELIC to \"Taxa de juros - CDI\", wich is series code 12. For the IPCA+ benchmark, use the same series code, but do the adjustment only in the last day of the month."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Use CDI as the primary benchmark (Priority: P1)

As a user, I want to see the portfolio performance benchmarked against the CDI rate instead of the SELIC rate, so that I can compare my investments against a more relevant market indicator.

**Why this priority**: The CDI rate is a more common and relevant benchmark for investments in Brazil.

**Independent Test**: The application can be run and the benchmark chart will show CDI data instead of SELIC data.

**Acceptance Scenarios**:

1. **Given** the application is configured to use the new benchmark, **When** the user runs a backtest, **Then** the performance chart displays the CDI rate as the benchmark.
2. **Given** the application is configured to use the new benchmark, **When** the user views the results summary, **Then** the benchmark is labeled as "CDI".

---

### User Story 2 - Adjust IPCA+ benchmark monthly (Priority: P2)

As a user, I want the IPCA+ benchmark to be adjusted only on the last day of the month, so that the benchmark reflects a more stable and predictable behavior.

**Why this priority**: This change aligns the benchmark calculation with common market practices and makes it easier to understand.

**Independent Test**: The IPCA+ benchmark data can be inspected and it will only show changes on the last day of each month.

**Acceptance Scenarios**:

1. **Given** the IPCA+ benchmark is calculated, **When** the user inspects the benchmark data for a given month, **Then** the value is constant for all days except the last day of the month.

---

### Edge Cases

- If the Central Bank of Brazil API for CDI (series 12) is unavailable, the system MUST fail the operation and show an error message to the user.
- If there are missing data points in the CDI series, the system MUST use 0 to fill the gaps.

## Clarifications

### Session 2025-10-29

- Q: If the Central Bank of Brazil API for CDI (series 12) is unavailable, how should the system behave? → A: Fail the operation and show an error message to the user.
- Q: How should the system handle missing data points (gaps) in the CDI time series data? → A: Use 0 to fill gaps.
- Q: How should the IPCA+ benchmark be calculated for the days before the last day of the month? → A: The value should be carried over from the previous day until the last day of the month, where the new value is calculated.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST fetch the "Taxa de juros - CDI" from the Central Bank of Brazil's API using series code 12.
- **FR-002**: The system MUST replace the SELIC rate with the CDI rate as the primary benchmark for portfolio performance.
- **FR-003**: The system MUST calculate the CDI benchmark using the CDI series (code 12).
- **FR-004**: The system MUST adjust the IPCA+ benchmark value only on the last day of each month. The value should be carried over from the previous day until the last day of the month, where the new value is calculated.

### Key Entities *(include if feature involves data)*

- **BenchmarkData**: Represents the benchmark data, including the series name (CDI), series code (12), and the time series data.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The application correctly displays "CDI" as the benchmark in all relevant charts and tables.
- **SC-002**: The benchmark data used for calculations matches the data from the Central Bank of Brazil for series code 12.
- **SC-003**: The IPCA+ benchmark value remains constant throughout the month and only changes on the last day.