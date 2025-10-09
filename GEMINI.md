# GEMINI.md

## Project Overview

This project consists of a single Python script, `backtest.py`, designed to perform backtests of stock investment strategies. It uses `yfinance` to download historical stock data, `python-bcb` to fetch Brazilian economic indicators (Selic, IPCA, and IMA-B 5+), `pandas` for data analysis, and `matplotlib` to visualize the results.

The script runs two distinct backtesting scenarios:

1.  **Scenario 1: Lump-Sum Investment**
    *   This simulation invests a fixed initial amount, distributed equally among a predefined list of stocks.
    *   It follows a "buy and hold" strategy, automatically reinvesting any dividends received.
    *   The portfolio's performance is benchmarked against the Selic rate and IMA-B 5+ index.

2.  **Scenario 2: Monthly Contributions**
    *   This simulation starts with a zero balance and makes regular monthly contributions.
    *   The contribution amount starts at a base value (e.g., R$1000) and is adjusted for inflation each month using the IPCA index.
    *   Each monthly contribution is invested into a single asset: the one with the lowest total monetary value in the portfolio at the time of investment.
    *   This portfolio is also benchmarked against Selic and IMA-B 5+, considering the same monthly contributions.

The script generates and displays three separate plots: capital curves for both scenarios showing performance vs. Selic and IMA-B 5+ benchmarks, plus a bar chart showing the distribution of monthly contributions by asset.

## Building and Running

This is a single-file Python script with external dependencies.

**1. Dependencies:**

You need to install the required Python libraries. You can do this using pip:

```bash
pip install yfinance pandas matplotlib python-bcb
```

**2. Running the Script:**

To run the backtests, execute the script from your terminal:

```bash
python backtest.py
```

The script will run both scenarios sequentially and display three plot windows at the end. The console will show a detailed summary of the results for each scenario, including comparisons with Selic and IMA-B 5+ benchmarks.

## Development Conventions

*   **Configuration:** All parameters for the backtest (stock tickers, investment amounts, dates) are hardcoded in the "Configuração do Backtest" section of the script. To run different scenarios, you will need to modify these variables directly in the code.
*   **Modularity:** The logic for each scenario is implemented as a direct processing loop in the main script flow.
*   **Output:** The script prints detailed summaries for both scenarios to the console, saves results to `backtest_results.xlsx`, and displays three matplotlib charts showing capital curves and contribution distribution.
*   **Language:** The code, comments, and output are written in Portuguese (pt-BR).