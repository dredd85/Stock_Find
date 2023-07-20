import yfinance as yf
import pandas as pd

df = pd.read_csv('tickers.csv')
tickers = df.values.tolist()
unpacked_tickers = list()
for rows in tickers:
    for row in rows:
        unpacked_tickers.append(row)

# ticker = 'AAPL'
ticker = unpacked_tickers[0]
# Create a Ticker object for the stock
stock = yf.Ticker(ticker)

# Get additional information about the stock
stock_info = stock.info

# Access specific attributes of the stock information
stock_name = stock_info['longName']
stock_sector = stock_info['sector']

# Print the additional information
print(f'Stock Symbol: {ticker}')
print(f"Stock Name: {stock_name}")
print(f"Sector: {stock_sector}")





