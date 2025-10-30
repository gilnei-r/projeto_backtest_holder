# GEMINI.md

## Project Overview

This project consists of a Python script, `main.py`, designed to perform backtests of stock investment strategies. It uses `yfinance` to download historical stock data, `python-bcb` to fetch Brazilian economic indicators (CDI and IPCA), `pandas` for data analysis, and `matplotlib` to visualize the results.

The script runs three distinct backtesting scenarios:

1.  **Scenario 1: Lump-Sum Investment**
    *   This simulation invests a fixed initial amount, distributed equally among a predefined list of stocks.
    *   It follows a "buy and hold" strategy, automatically reinvesting any dividends received.
    *   The portfolio's performance is benchmarked against the CDI rate and an IPCA + x% benchmark.

2.  **Scenario 2: Monthly Contributions**
    *   This simulation starts with a zero balance and makes regular monthly contributions.
    *   The contribution amount starts at a base value (e.g., R$1000) and is adjusted for inflation each month using the IPCA index.
    *   Each monthly contribution is invested into a single asset: the one with the lowest total monetary value in the portfolio at the time of investment.
    *   **Automatic Brake Feature:** This scenario now includes a "freio de arrumação" (automatic brake) mechanism inspired by the Bastter.com methodology. If an asset receives more than one contribution within a configurable period, it is placed in a "quarantine" for a set duration, preventing further investment in it and thus avoiding concentration.
    *   This portfolio is also benchmarked against CDI and an IPCA + x% benchmark, considering the same monthly contributions.

3.  **Scenario 3: Monthly Contributions with CDB Allocation**
    *   This scenario is similar to Scenario 2 but introduces a fixed-income asset (simulating a CDB linked to the CDI rate) into the portfolio.
    *   A target percentage for the CDB allocation is defined in the `config.py` file.
    *   Each month, the script checks if the current value of the CDB asset is below the target percentage. If it is, the entire monthly contribution is allocated to the CDB. Otherwise, the contribution follows the logic of Scenario 2.

The script generates and displays multiple plots for the scenarios and their results.

## Building and Running

This is a Python script with external dependencies, managed by a `requirements.txt` file.

**1. Dependencies:**

You need to install the required Python libraries. You can do this using pip and the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

**2. Running the Script:**

To run the backtests, execute the script from your terminal:

```bash
python main.py
```

The script will run all scenarios sequentially and display the plot windows at the end. The console will show a detailed summary of the results for each scenario.

## Development Conventions

*   **Configuration:** All parameters for the backtest are defined in the `config.py` file. This includes stock tickers, investment amounts, dates, and settings for features like the Automatic Brake (`FREIO_ATIVO`), the IPCA benchmark (`IPCA_BENCHMARK_X`), the data update frequency (`DATA_UPDATE_DAYS`), and the new CDB scenario (`CDB_PERCENTAGE`).
*   **Modularity:** The logic is organized into functions within the `main.py`, `data_loader.py`, `scenarios.py`, and `plotting.py` scripts.
*   **Data Handling:** The script now features a data caching mechanism. All data downloaded from `yfinance` and `python-bcb` is saved to individual CSV files in the `data/` directory. On subsequent runs, the script checks the modification date of these files. If a file is younger than `DATA_UPDATE_DAYS`, the script uses the cached data, significantly speeding up execution. Otherwise, it downloads fresh data and updates the cache file.
*   **Output:** The script prints detailed summaries for all scenarios to the console and saves the results to Excel files in the `results/` directory: `backtest_results_lump_sum.xlsx`, `backtest_results_monthly.xlsx`, and `backtest_results_cdb_mixed.xlsx`.
*   **Language:** The code, comments, and output are written in Portuguese (pt-BR).
