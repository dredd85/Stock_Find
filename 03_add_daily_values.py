import yfinance as yf
import pandas as pd
import sqlite3
from datetime import date, timedelta


# -----------------------------------
# Function to fetch stock data
# -----------------------------------
def get_stock_data(ticker, start_date, end_date):
    try:
        stock_data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            auto_adjust=False,
            progress=False
        )

        if stock_data.empty:
            return None

        df = pd.DataFrame(stock_data)
        df.reset_index(inplace=True)

        # Fix MultiIndex columns returned by newer yfinance
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = [col[0] for col in df.columns]

        # Remove Adj Close if present
        if 'Adj Close' in df.columns:
            df.drop('Adj Close', axis=1, inplace=True)

        # Match database column naming
        df['ticker'] = ticker

        return df

    except Exception as e:
        print(f"Failed to fetch data for {ticker}: {e}")
        return None


# -----------------------------------
# Load tickers
# -----------------------------------
df = pd.read_csv('tickers.csv', header=None)

tickers = df[0].tolist()

print(f"Loaded {len(tickers)} tickers")


# -----------------------------------
# Connect to database
# -----------------------------------
conn = sqlite3.connect('Stocks.db')


# -----------------------------------
# Date range
# -----------------------------------
start_date = date.today() - timedelta(days=2)
end_date = date.today()

print(f"Downloading data from {start_date} to {end_date}")


# -----------------------------------
# Process tickers in batches
# -----------------------------------
batch_size = 50

for i in range(0, len(tickers), batch_size):

    batch_tickers = tickers[i:i + batch_size]

    print(f"\nStarting batch {i // batch_size + 1}")

    for ticker in batch_tickers:

        stock_df = get_stock_data(
            ticker,
            start_date,
            end_date
        )

        if stock_df is None or stock_df.empty:
            print(f"{ticker} - no data")
            continue

        try:
            # Existing dates for this ticker
            existing_dates = pd.read_sql(
                "SELECT Date FROM Prices WHERE ticker = ?",
                conn,
                params=(ticker,)
            )['Date']

            # Remove rows already stored
            stock_df = stock_df[
                ~stock_df['Date'].astype(str).isin(existing_dates)
            ]

            if stock_df.empty:
                print(f"{ticker} - no new records")
                continue

            # Keep only columns that exist in Prices table
            stock_df = stock_df[
                [
                    'ticker',
                    'Date',
                    'Open',
                    'High',
                    'Low',
                    'Close',
                    'Volume'
                ]
            ]

            stock_df.to_sql(
                'Prices',
                conn,
                if_exists='append',
                index=False
            )

            print(f"{ticker} - added {len(stock_df)} rows")

        except Exception as e:
            print(f"{ticker} - database error: {e}")

    conn.commit()

    print(f"Batch {i // batch_size + 1} completed")


# -----------------------------------
# Close database
# -----------------------------------
conn.close()

print("\nDaily price update complete")