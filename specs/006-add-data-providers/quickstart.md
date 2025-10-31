# Quickstart: Using Multiple Data Providers

**Version**: 1.0
**Date**: 2025-10-30

This guide explains how to configure and use the new multi-provider data loading feature.

## 1. Configuration

To select a data source, you must modify the `config.py` file. Two new variables have been introduced.

```python
# config.py

# ... (other configurations)

# DATA SOURCE SETTINGS
# Choose from: 'yahoofinance', 'metatrader5', 'metastock'
DATA_SOURCE = 'yahoofinance' 

# Path to local Metastock CSV files (only used if DATA_SOURCE is 'metastock')
METASTOCK_PATH = 'C:\path\to\your\metastock\csvs'

# ... (rest of the configurations)
```

### Variable Reference

- `DATA_SOURCE` (str):
  - `'yahoofinance'`: **(Default)** Downloads data from Yahoo Finance. Requires an internet connection.
  - `'metatrader5'`: Connects to a running MetaTrader 5 terminal to get data.
  - `'metastock'`: Reads data from local `.csv` files located in the `METASTOCK_PATH` directory.

- `METASTOCK_PATH` (str):
  - This should be the **absolute path** to the folder containing your ticker data in `.csv` format.
  - Each file should be named after the ticker symbol (e.g., `PETR4.csv`, `VALE3.csv`).
  - The CSV files must contain at least `Date` and `Adj Close` columns.

## 2. Running the Script

Once the `config.py` file is configured with your desired `DATA_SOURCE` (and `METASTOCK_PATH` if applicable), you can run the script as usual:

```bash
python main.py
```

The script will automatically use the selected data provider to fetch the historical data before running the backtest scenarios.

## 3. Viewing Enhanced Reports

After the script completes, new plots and Excel files will be generated in the `results/` directory.

- **`distribuicao_valor.png`**: This plot will now show side-by-side bars for each asset, comparing its `Valor Atual` (Current Value) against the `Aporte Total` (Total Contribution).
- **`backtest_results_monthly.xlsx`** and **`backtest_results_cdb_mixed.xlsx`**: The summary sheet in these files will contain new columns detailing the total contribution for each asset, allowing for deeper analysis.
