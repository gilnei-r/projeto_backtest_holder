# Data Model: IPCA Benchmark, Ticker Plot, and Data Verification

## Entities

### IPCA Benchmark

Represents the calculated benchmark values over time.

**Attributes**:

-   `date`: The date of the benchmark value.
-   `cumulative_return`: The cumulative return of the benchmark up to that date.

### Ticker Value

Represents the final monetary value of a single ticker.

**Attributes**:

-   `ticker_symbol`: The stock ticker symbol.
-   `total_value`: The total monetary value of the ticker in the portfolio.

### Data File

Represents a downloaded financial data file.

**Attributes**:

-   `file_path`: The path to the data file.
-   `last_modified_date`: The date the file was last modified.
