# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Brazilian stock market backtesting project that simulates two distinct investment strategies:

1. **Lump-Sum Investment**: Single initial investment distributed equally across stocks, following buy-and-hold with automatic dividend reinvestment
2. **Monthly Contributions**: Regular monthly contributions adjusted for inflation (IPCA), always investing in the asset with the lowest portfolio value

Both strategies are benchmarked against Brazilian economic indicators (Selic rate, IMA-B index).

## Language and Locale

**All code, comments, output, and user-facing text must be in Portuguese (pt-BR).** This is a Brazilian investment project using Brazilian stocks, indices, and economic data.

## Architecture

### Single-File Design
The entire application is contained in `backtest.py`. There are no modules, packages, or separate configuration files.

### Data Sources
- **Stock Data**: Downloaded via `yfinance` from Yahoo Finance (Brazilian stocks with `.SA` suffix)
- **Economic Indicators**: Downloaded via `python-bcb` from Banco Central do Brasil
  - Series 432: Selic (Brazilian base interest rate)
  - Series 433: IPCA (Brazilian consumer price index)
  - Series 12467: IMA-B 5+ index (fixed income benchmark)

### Key Data Flows

1. **Configuration** (lines 54-76): All parameters hardcoded at top
   - `empresas_input`: Space-separated ticker symbols (short form)
   - `tickers_map`: Maps short tickers to full Yahoo Finance tickers (.SA suffix)
   - `valor_investido_por_empresa`: Amount invested per stock (Scenario 1)
   - `aporte_mensal_base`: Base monthly contribution amount (Scenario 2)
   - `data_inicio`/`data_fim`: Backtest date range

2. **Data Download** (lines 77-103): Bulk download at start
   - Stock data downloaded via `yf.download()` with MultiIndex columns
   - BCB series downloaded in 3-year chunks with retry logic (`download_bcb_series()`)
   - IMA-B 5+ normalized to base 100 on first day
   - Returns MultiIndex DataFrame: (metric, ticker) columns for stocks

3. **Scenario 1 Processing** (lines 105-147): Lump-sum simulation
   - Iterates through each valid ticker's historical data
   - Tracks shares owned (including dividend reinvestment)
   - Builds daily capital curve for entire date range
   - Calculates Selic and IMA-B 5+ benchmarks with same initial investment

4. **Scenario 2 Processing** (lines 149-227): Monthly contributions
   - Iterates through ALL dates (not just trading days)
   - On first day of each month (year+month tuple tracking):
     - Adjusts contribution by accumulated IPCA
     - Identifies asset with lowest monetary value
     - Invests entire contribution into that asset
   - Tracks dividend reinvestment daily
   - Updates Selic and IMA-B 5+ benchmark values with same monthly contributions
   - Forward-fills non-trading days

5. **Output Generation** (lines 229-270):
   - Excel file with monthly snapshots: `backtest_results.xlsx`
   - Three matplotlib charts (displayed, not saved):
     - Scenario 1 capital curve with Selic and IMA-B 5+
     - Scenario 2 capital curve with benchmarks and total invested
     - Distribution of monthly contributions by asset (bar chart)

### Important Implementation Details

- **Dividend Reinvestment**: When dividends are paid, they purchase additional shares at the closing price of that day: `num_shares += (num_shares * row['Dividends']) / row['Close']`

- **Monthly Contribution Logic** (Scenario 2): Always invests in the asset with the **lowest total monetary value** (not price), implementing a self-rebalancing strategy

- **IPCA Adjustment**: Monthly contributions grow with accumulated inflation: `aporte_corrigido = aporte_mensal_base * ipca_acumulado.loc[dia]`

- **Month Tracking Fix**: Uses `(year, month)` tuple instead of just month to properly detect new months across years: `current_month = (dia.year, dia.month)`

- **IMA-B 5+ Normalization**: Index values are normalized to start at 1.0 on the first day, then daily returns are calculated from the normalized series

- **Date Range Handling**: Creates a complete daily date range (`pd.date_range`) then forward-fills missing trading days

- **MultiIndex Column Access**: Downloaded data has structure `(metric, ticker)`, accessed as `data_historica.loc[date, ('Close', ticker)]`

## Running the Backtest

### Install Dependencies
```bash
pip install yfinance pandas matplotlib python-bcb
```

### Execute Backtest
```bash
python backtest.py
```

The script will:
1. Download all data (can take 2-5 minutes)
2. Process both scenarios
3. Print console summaries with CAGR and final values
4. Save `backtest_results.xlsx` with monthly data
5. Display three charts (requires closing windows to continue)

## Modifying Parameters

All configuration is at the top of `backtest.py` (lines 54-76):

- **Change stocks**: Edit `empresas_input` string (space-separated short tickers) and ensure mapping exists in `tickers_map`
- **Change date range**: Modify `data_inicio` (format: "YYYY-MM-DD")
- **Change investment amounts**:
  - Scenario 1: `valor_investido_por_empresa` (per stock)
  - Scenario 2: `aporte_mensal_base` (monthly contribution)

## Common Issues

### BCB Download Failures
The `download_bcb_series()` function includes chunking (3-year periods) and retry logic (3 attempts with 2-second delays) because the BCB API is unreliable. If a chunk fails after 3 attempts, it's skipped and processing continues. The script will work with partial data if needed.

**Note**: IMA-B 5+ series (12467) may not have recent data (typically ends around 2023). This is expected behavior and the script handles it gracefully.

### Ticker Mapping
Yahoo Finance requires `.SA` suffix for Brazilian stocks (e.g., `ITUB4.SA`). The `tickers_map` dictionary handles this conversion. When adding new stocks, both the short form and full form must be added.

### MultiIndex DataFrame Structure
`yf.download()` with multiple tickers returns MultiIndex columns. When processing individual stocks, use column slicing: `stock_data = data_historica.loc[:, (slice(None), ticker)]` then `stock_data.columns = stock_data.columns.droplevel(1)`.

## Output Files

- **backtest_results.xlsx**: Contains two sheets with monthly snapshots:
  - "Aporte Unico (Mensal)": Scenario 1 results
  - "Aportes Mensais (Mensal)": Scenario 2 results with contribution tracking
