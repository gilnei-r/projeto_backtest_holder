# Quickstart: IPCA Benchmark, Ticker Plot, and Data Verification

This document provides instructions on how to use the new features.

## 1. Configure the IPCA Benchmark

Open the `config.py` file and set the `IPCA_BENCHMARK_X` variable to your desired value. This value represents the 'x' in the IPCA + x% benchmark.

```python
# config.py

IPCA_BENCHMARK_X = 6.0  # Represents IPCA + 6%
```

## 2. Run the Backtest

Execute the main script from your terminal:

```bash
python main.py
```

## 3. View the Results

-   The backtest report will now include the performance comparison against the IPCA + x% benchmark.
-   A new window will appear displaying a bar plot of the total value of each ticker in your portfolio.

## 4. Data Verification

The script will automatically check if the financial data is up-to-date. If it is, the script will use the existing data, resulting in a faster execution time. If the data is outdated, it will be automatically downloaded.
