# Test script to check data structure
import pandas as pd

# Test reading one CSV file
file_path = "data/ABEV3.SA.csv"
print("Reading CSV with multi-header...")
ticker_data = pd.read_csv(file_path, header=[0, 1], index_col=0, parse_dates=True)
print("\nColumns after reading:")
print(ticker_data.columns)
print("\nFirst 5 rows:")
print(ticker_data.head())
print("\nData types:")
print(ticker_data.dtypes)

# Drop second level
ticker_data.columns = ticker_data.columns.droplevel(1)
print("\nColumns after droplevel:")
print(ticker_data.columns)
print("\nFirst 5 rows after droplevel:")
print(ticker_data.head())
print("\nData types after droplevel:")
print(ticker_data.dtypes)
