# Quickstart for "Save Plots and Add MT5 Provider"

## MetaTrader 5 Integration Setup

To use the MetaTrader 5 integration, you need to have the MetaTrader 5 terminal installed on the same machine where you run the script.

### 1. Install the MetaTrader5 Package

Install the official `MetaTrader5` Python package using pip:

```bash
pip install MetaTrader5
```

### 2. Enable Algo Trading in MetaTrader 5

In your MetaTrader 5 terminal, you need to enable "Algo Trading" to allow the Python script to connect and download data.

1.  Open the MetaTrader 5 terminal.
2.  Go to "Tools" > "Options".
3.  In the "Options" window, go to the "Expert Advisors" tab.
4.  Check the box "Allow Algo Trading".
5.  Click "OK".

### 3. Configure the Application

The new configuration options for this feature will be added to the `config.py` file. You will be able to enable or disable the MetaTrader 5 integration and the plot saving feature.

## Saving Plots

The script will now save the plots as PNG files in the `results/plots/` directory by default. You can change this directory in the `config.py` file. The plots will no longer be displayed on the screen.
