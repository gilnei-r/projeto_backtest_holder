# Quickstart Guide

**Feature**: CDB Scenario and Data Persistence

This guide explains how to configure and run the new CDB investment scenario and how the data caching works.

## 1. Data Caching

- **What it does**: The script now saves all downloaded financial data (tickers, SELIC, IPCA) into a `data/` directory as CSV files.
- **How it works**: 
  1. When you run `main.py`, it first checks the `data/` directory.
  2. If a data file (e.g., `PETR4.SA.csv`) exists and is less than 24 hours old, the script uses it instantly.
  3. If the file doesn't exist or is older than 24 hours, the script downloads fresh data and saves it, overwriting the old file.
- **Your action**: None. This process is fully automatic.

## 2. Configuring the CDB Scenario

To use the new scenario, you need to add a configuration parameter to your `config.py` file.

1. **Open `config.py`**.
2. **Add the `CDB_PERCENTAGE` variable**: This variable defines the target allocation for the fixed-income (CDB/SELIC) portion of your portfolio. The value should be between 0.0 and 1.0.

   ```python
   # config.py

   # ... (your existing configurations)

   # Target percentage for the fixed-income (CDB/SELIC) asset in the new scenario
   # Example: 0.25 means the goal is to have 25% of the portfolio value in CDB.
   CDB_PERCENTAGE = 0.25
   ```

## 3. Running the Backtest

- **Execute the script** as usual:
  ```bash
  python main.py
  ```
- **What to expect**: The script will now run an additional backtest scenario. You will see new outputs:
  - A console summary for the "CDB Mixed Scenario".
  - A new Excel file named `backtest_results_cdb_mixed.xlsx`.
  - A new plot window showing the capital curve for this scenario.

## How the CDB Scenario Works

- It uses the same monthly contribution as the other scenarios.
- **Investment Logic**: Each month, it checks the current value of your CDB/SELIC asset against the `CDB_PERCENTAGE` target.
  - If `CDB Value < (Total Portfolio Value * CDB_PERCENTAGE)`, the **entire** monthly contribution is invested in the CDB.
  - Otherwise, the contribution is invested in the stock with the lowest current monetary value (the standard strategy).
