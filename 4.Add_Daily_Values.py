import yfinance as yf
import pandas as pd
import sqlite3
from datetime import date, timedelta

# Function to fetch stock data for a given ticker and return a DataFrame
def get_stock_data(ticker, start_date, end_date):
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        df = pd.DataFrame(stock_data)
        df.reset_index(inplace=True)
        df.drop('Adj Close', axis=1, inplace=True)
        # Add the 'Ticker' column to the DataFrame
        df['Ticker'] = ticker
        return df
    except Exception as e:
        print(f"Failed to fetch data for {ticker}: {e}")
        return None

df = pd.read_csv('tickers.csv')

tickers = df.values.tolist()
unpacked_tickers = [row for rows in tickers for row in rows]

conn = sqlite3.connect('Stocks.db')
cursor = conn.cursor()

start_date = date.today() - timedelta(days=2)
end_date = date.today()

batch_size = 50

for i in range(0, len(unpacked_tickers), batch_size):
    batch_tickers = unpacked_tickers[i : i + batch_size]
    batch_data = []

    for ticker in batch_tickers:
        stock_df = get_stock_data(ticker, start_date, end_date)
        print(f'{ticker} data fetched')
        batch_data.append(stock_df)
    
    combined_batch = pd.concat(batch_data, ignore_index=True)
    # Checking if the data is already uploaded
    existing_dates = pd.read_sql(f"SELECT DISTINCT Date FROM Prices WHERE ticker = '{ticker}'", conn)['Date']
    combined_batch = combined_batch[~combined_batch['Date'].isin(existing_dates)]
    combined_batch.to_sql('Prices', conn, if_exists='append', index=False)
    print(f'Batch {i//batch_size + 1} added to database')

conn.commit()
conn.close()
