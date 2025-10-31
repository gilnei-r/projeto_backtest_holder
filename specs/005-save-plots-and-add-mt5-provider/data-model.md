# Data Model for "Save Plots and Add MT5 Provider"

No changes are required to the existing data model.

The data downloaded from MetaTrader 5 will be transformed into a `pandas` DataFrame with the same structure as the data from `yfinance`. The DataFrame will have the following columns:

*   `Open`
*   `High`
*   `Low`
*   `Close`
*   `Volume`
*   `Dividends`

The index of the DataFrame will be the date of the data.
