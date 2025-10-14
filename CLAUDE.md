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

### Two-File Design
The application consists of two main files:
- **`backtest.py`**: Contains all core logic, data processing, and visualization functions
- **`config.py`**: Centralizes all configuration parameters (stocks, dates, investment amounts, automatic brake settings)

### Data Sources
- **Stock Data**: Downloaded via `yfinance` from Yahoo Finance (Brazilian stocks with `.SA` suffix)
- **Economic Indicators**: Downloaded via `python-bcb` from Banco Central do Brasil
  - Series 432: Selic (Brazilian base interest rate)
  - Series 433: IPCA (Brazilian consumer price index)
  - Series 12467: IMA-B 5+ index (fixed income benchmark)

### Key Data Flows

1. **Configuration** (config.py, lines 14-75): All parameters in separate config file
   - `EMPRESAS_INPUT`: Space-separated ticker symbols (short form)
   - `TICKERS_MAP`: Maps short tickers to full Yahoo Finance tickers (.SA suffix)
   - `VALOR_INVESTIDO_POR_EMPRESA`: Amount invested per stock (Scenario 1)
   - `APORTE_MENSAL_BASE`: Base monthly contribution amount (Scenario 2)
   - `DATA_INICIO`/`DATA_FIM`: Backtest date range
   - `FREIO_ATIVO`: Enable/disable automatic brake feature
   - `FREIO_PERIODO_APORTES`, `FREIO_QUARENTENA_INICIAL`, `FREIO_QUARENTENA_ADICIONAL`: Brake behavior parameters

2. **Data Download** (backtest.py, lines 321-341): Bulk download at start
   - Stock data downloaded via `yf.download()` with MultiIndex columns
   - BCB series downloaded in 3-year chunks with retry logic (`download_bcb_series()`)
   - IMA-B 5+ normalized to base 100 on first day
   - Returns MultiIndex DataFrame: (metric, ticker) columns for stocks

3. **Scenario 1 Processing** (backtest.py, lines 80-122): Lump-sum simulation
   - Iterates through each valid ticker's historical data
   - Tracks shares owned (including dividend reinvestment)
   - Builds daily capital curve for entire date range
   - Calculates Selic benchmark with same initial investment

4. **Scenario 2 Processing** (backtest.py, lines 124-256): Monthly contributions
   - Iterates through ALL dates (not just trading days)
   - On first day of each month (year+month tuple tracking):
     - Adjusts contribution by accumulated IPCA
     - Checks automatic brake quarantine status
     - Identifies asset with lowest monetary value (among eligible assets)
     - Invests entire contribution into that asset
     - Activates brake if asset receives multiple contributions within configured period
   - Tracks dividend reinvestment daily
   - Updates Selic benchmark values with same monthly contributions
   - Forward-fills non-trading days

5. **Output Generation** (backtest.py, lines 258-309):
   - Two separate Excel files with monthly snapshots:
     - `backtest_results_lump_sum.xlsx`: Scenario 1 results
     - `backtest_results_monthly.xlsx`: Scenario 2 results with contribution tracking
   - Three matplotlib charts (displayed, not saved):
     - Scenario 1 capital curve with Selic
     - Scenario 2 capital curve with Selic and total invested
     - Distribution of monthly contributions by asset (bar chart)

### Important Implementation Details

- **Dividend Reinvestment**: When dividends are paid, they purchase additional shares at the closing price of that day: `num_shares += (num_shares * row['Dividends']) / row['Close']`

- **Monthly Contribution Logic** (Scenario 2): Always invests in the asset with the **lowest total monetary value** (not price), implementing a self-rebalancing strategy

- **Automatic Brake Feature** (Scenario 2): Prevents portfolio concentration by tracking contributions per asset. If an asset receives more than one contribution within `FREIO_PERIODO_APORTES` months, it enters "quarentena" (quarantine) for `FREIO_QUARENTENA_INICIAL` months. Subsequent activations increase quarantine duration by `FREIO_QUARENTENA_ADICIONAL`. Controlled by `FREIO_ATIVO` flag in config.py

- **IPCA Adjustment**: Monthly contributions grow with accumulated inflation: `aporte_corrigido = aporte_mensal_base * ipca_acumulado.loc[dia]`

- **Month Tracking Fix**: Uses `(year, month)` tuple instead of just month to properly detect new months across years: `current_month = (dia.year, dia.month)`

- **Data Forward-Filling**: After download, stock data is forward-filled using `.ffill()` to ensure continuity and prevent skipped contributions on non-trading days

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

All configuration is in `config.py`:

- **Change stocks**: Edit `EMPRESAS_INPUT` string (space-separated short tickers) and ensure mapping exists in `TICKERS_MAP`
- **Change date range**: Modify `DATA_INICIO` (format: "YYYY-MM-DD") and `DATA_FIM`
- **Change investment amounts**:
  - Scenario 1: `VALOR_INVESTIDO_POR_EMPRESA` (per stock)
  - Scenario 2: `APORTE_MENSAL_BASE` (monthly contribution)
- **Configure automatic brake**:
  - `FREIO_ATIVO`: Set to True/False to enable/disable
  - `FREIO_PERIODO_APORTES`: Months to check for repeated contributions (default: 2)
  - `FREIO_QUARENTENA_INICIAL`: Initial quarantine duration in months (default: 6)
  - `FREIO_QUARENTENA_ADICIONAL`: Additional months added on subsequent activations (default: 12)

## Common Issues

### BCB Download Failures
The `download_bcb_series()` function includes chunking (3-year periods) and retry logic (3 attempts with 2-second delays) because the BCB API is unreliable. If a chunk fails after 3 attempts, it's skipped and processing continues. The script will work with partial data if needed.

### Ticker Mapping
Yahoo Finance requires `.SA` suffix for Brazilian stocks (e.g., `ITUB4.SA`). The `tickers_map` dictionary handles this conversion. When adding new stocks, both the short form and full form must be added.

### MultiIndex DataFrame Structure
`yf.download()` with multiple tickers returns MultiIndex columns. When processing individual stocks, use column slicing: `stock_data = data_historica.loc[:, (slice(None), ticker)]` then `stock_data.columns = stock_data.columns.droplevel(1)`.

## Output Files

- **backtest_results_lump_sum.xlsx**: Scenario 1 results with monthly snapshots
  - Sheet: "Aporte Unico (Mensal)"
- **backtest_results_monthly.xlsx**: Scenario 2 results with monthly snapshots
  - Sheet: "Aportes Mensais (Mensal)"
  - Includes columns: individual stock values, Total, Selic, Total Investido, Aporte, Ativo Aportado
