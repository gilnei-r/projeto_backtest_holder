# Data Model: Update Benchmark Data

No new data models are introduced in this feature. The existing `BenchmarkData` entity is used.

## BenchmarkData

- **Description**: Represents the benchmark data used for portfolio performance comparison.
- **Fields**:
  - `series_name` (string): The name of the benchmark series (e.g., "CDI").
  - `series_code` (integer): The series code from the Central Bank of Brazil (e.g., 12).
  - `data` (pandas.DataFrame): The time series data for the benchmark.