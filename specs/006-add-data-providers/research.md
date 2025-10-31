# Research: Data Provider Integration

**Date**: 2025-10-30

## 1. Metastock CSV Data Structure

### Decision
The Metastock CSV data loader will be designed to read standard CSV files and will require the presence of two specific columns: `Date` and `Adj Close`.

- The `Date` column will be used as the time-series index.
- The `Adj Close` column will be used for the backtesting calculation, as it accounts for dividends and stock splits, consistent with `yfinance` data.

The loader will be robust enough to handle the presence of other common columns (e.g., `Open`, `High`, `Low`, `Close`, `Volume`) but will not require them.

### Rationale
This approach provides a good balance between establishing a clear data contract and maintaining flexibility.
- **Consistency**: Using `Adj Close` ensures that the data from the local Metastock CSVs is directly comparable to the data fetched from Yahoo Finance.
- **Robustness**: By not requiring the full OHLCV dataset, the feature is less brittle. Users can generate or source CSVs with only the essential information.
- **Simplicity**: It avoids the need to infer which column to use for the closing price, which could be error-prone.

### Alternatives Considered
1.  **Require all OHLCV + Volume columns**: This was rejected as being too strict. It would place a higher burden on the user to ensure their CSV files are complete.
2.  **Auto-detect the close price column**: This was rejected as it could lead to unpredictable behavior if column names are not standard (e.g., `close`, `closing_price`, `last`).
