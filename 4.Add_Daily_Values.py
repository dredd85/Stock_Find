import yfinance as yf
import pandas as pd
import sqlite3
from datetime import date, timedelta

# Function to fetch stock data for a given ticker and return a DataFrame
def get_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    df = pd.DataFrame(stock_data)
    df.reset_index(inplace=True)
    df.drop('Adj Close', axis=1, inplace=True)
    # Add the 'Ticker' column to the DataFrame
    df['Ticker'] = ticker
    return df

df = pd.read_csv('tickers.csv')

tickers = df.values.tolist()
unpacked_tickers = [row for rows in tickers for row in rows]

conn = sqlite3.connect('Stocks.db')
cursor = conn.cursor()

start_date = date.today() - timedelta(days=365)
end_date = date.today()
ticker = '06N.WA'
#for ticker in unpacked_tickers:
stock_df = get_stock_data(ticker, start_date, end_date)
stock_df.to_sql('Prices', conn, if_exists='append', index=False)
print(stock_df)
print(f'Added historical data for {ticker}')

conn.commit()
conn.close()
