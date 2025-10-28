# GEMINI.md

## Project Overview

This project consists of a Python script, `main.py`, designed to perform backtests of stock investment strategies. It uses `yfinance` to download historical stock data, `python-bcb` to fetch Brazilian economic indicators (Selic and IPCA), `pandas` for data analysis, and `matplotlib` to visualize the results.

The script runs two distinct backtesting scenarios:

1.  **Scenario 1: Lump-Sum Investment**
    *   This simulation invests a fixed initial amount, distributed equally among a predefined list of stocks.
    *   It follows a "buy and hold" strategy, automatically reinvesting any dividends received.
    *   The portfolio's performance is benchmarked against the Selic rate and an IPCA + x% benchmark.

2.  **Scenario 2: Monthly Contributions**
    *   This simulation starts with a zero balance and makes regular monthly contributions.
    *   The contribution amount starts at a base value (e.g., R$1000) and is adjusted for inflation each month using the IPCA index.
    *   Each monthly contribution is invested into a single asset: the one with the lowest total monetary value in the portfolio at the time of investment.
    *   **Automatic Brake Feature:** This scenario now includes a "freio de arrumação" (automatic brake) mechanism inspired by the Bastter.com methodology. If an asset receives more than one contribution within a configurable period, it is placed in a "quarantine" for a set duration, preventing further investment in it and thus avoiding concentration.
    *   This portfolio is also benchmarked against Selic and an IPCA + x% benchmark, considering the same monthly contributions.

The script generates and displays four separate plots: capital curves for both scenarios showing performance vs. benchmarks, a bar chart showing the distribution of monthly contributions by asset, and a bar chart showing the final value distribution of each ticker.

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

The script will run both scenarios sequentially and display four plot windows at the end. The console will show a detailed summary of the results for each scenario, including comparisons with the benchmarks and logs for when the automatic brake is activated.

## Development Conventions

*   **Configuration:** All parameters for the backtest (stock tickers, investment amounts, dates) are defined in the `config.py` file. This includes new settings to enable and configure the automatic brake feature (`FREIO_ATIVO`, `FREIO_PERIODO_APORTES`, `FREIO_QUARENTENA_INICIAL`, `FREIO_QUARENTENA_ADICIONAL`), the IPCA benchmark (`IPCA_BENCHMARK_X`), and the data update frequency (`DATA_UPDATE_DAYS`).
*   **Modularity:** The logic is organized into functions within the `main.py`, `data_loader.py`, `scenarios.py`, and `plotting.py` scripts. The main execution flow is controlled by the `main()` function.
*   **Data Handling:** The script now pre-processes historical data after download, filling in any missing values to ensure the simulation's continuity and prevent skipped contributions. It also includes a data verification feature to avoid unnecessary downloads.
*   **Output:** The script prints detailed summaries for both scenarios to the console, saves results to `backtest_results_lump_sum.xlsx` and `backtest_results_monthly.xlsx`, and displays four matplotlib charts showing capital curves, contribution distribution, and final asset value distribution.
*   **Language:** The code, comments, and output are written in Portuguese (pt-BR).
