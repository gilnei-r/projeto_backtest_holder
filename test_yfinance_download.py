# Test script to check what yfinance returns
import yfinance as yf

ticker = "ABEV3.SA"
print(f"Downloading {ticker} from 2015-01-01 to 2015-01-31...")
data = yf.download(ticker, start="2015-01-01", end="2015-01-31", progress=False)
print("\nColumns returned:")
print(data.columns)
print("\nFirst 5 rows:")
print(data.head())
print("\nData types:")
print(data.dtypes)
