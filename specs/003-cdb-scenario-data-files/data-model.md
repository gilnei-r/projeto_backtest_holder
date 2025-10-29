# Data Model

**Feature**: CDB Scenario and Data Persistence

This document outlines the structure of the key data entities for this feature. As this feature focuses on data persistence in CSV files rather than a structured database, this model describes the file formats.

## 1. Ticker Data CSV

- **Description**: Represents a file containing historical price data for a single stock, used for caching.
- **Filename Convention**: `{TICKER}.csv` (e.g., `PETR4.SA.csv`)
- **Location**: `data/`
- **Fields**:
  - `Date`: (datetime) The trading day.
  - `Open`: (float) Opening price.
  - `High`: (float) Highest price of the day.
  - `Low`: (float) Lowest price of the day.
  - `Close`: (float) Closing price.
  - `Volume`: (integer) Trading volume.
  - `Dividends`: (float) Dividend payments.

## 2. Economic Indicator Data CSV

- **Description**: Represents a file containing historical data for an economic indicator, used for caching.
- **Filename Convention**: `{INDICATOR_NAME}.csv` (e.g., `SELIC.csv`, `IPCA.csv`)
- **Location**: `data/`
- **Fields**:
  - `Date`: (datetime) The date of the indicator value.
  - `Value`: (float) The value of the indicator.

## 3. CDB/SELIC Asset (Virtual Entity)

- **Description**: This is not a persisted entity but a virtual one calculated during the backtest simulation. It represents a fixed-income investment whose value is compounded daily based on the SELIC rate.
- **Key Attributes (in memory)**:
  - `total_value`: (float) The current monetary value of the asset within the portfolio.
  - `target_percentage`: (float) The desired allocation percentage for this asset, loaded from `config.py`.
