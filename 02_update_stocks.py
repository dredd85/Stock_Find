import yfinance as yf
import pandas as pd
import sqlite3
import os
import sys

file_path = "gpw_session.xls"

# -----------------------------------
# Check if file exists
# -----------------------------------

if not os.path.exists(file_path):
    print("File gpw_session.xls not found.")
    sys.exit()

print("Loading gpw_session.xls ...")

# -----------------------------------
# Extract tickers from Excel (HTML)
# -----------------------------------

tables = pd.read_html(file_path)
df = tables[0]

# Data starts at row 3
df = df.iloc[2:]

# Column E → index 4
tickers = df.iloc[:, 4].dropna().astype(str).tolist()

# Clean
tickers = [t.strip() for t in tickers if t.strip() != ""]
tickers = list(set(tickers))
tickers.sort()

# Add Yahoo suffix
unpacked_tickers = [ticker + ".WA" for ticker in tickers]

print(f"Extracted {len(unpacked_tickers)} tickers from GPW file.")

# -----------------------------------
# Connect to database
# -----------------------------------

conn = sqlite3.connect('Stocks.db')
cursor = conn.cursor()

# Clear table (your original logic)
sql_delete_all_query = "DELETE FROM Stocks"
cursor.execute(sql_delete_all_query)

batch_size = 50
count = 0

try:
    for i in range(0, len(unpacked_tickers), batch_size):
        batch_tickers = unpacked_tickers[i : i + batch_size]

        try:
            for ticker in batch_tickers:
                stock = yf.Ticker(ticker)
                stock_info = stock.info

                stock_name = stock_info.get('longName', 'N/A')
                stock_sector = stock_info.get('sector', 'N/A')

                print(f'Stock Symbol: {ticker}')
                print(f"Stock Name: {stock_name}")
                print(f"Sector: {stock_sector}")

                cursor.execute('''
                INSERT OR IGNORE INTO Stocks (ticker, company_name, industry) 
                VALUES (?,?,?)
                ''', (ticker, stock_name, stock_sector))

                count += 1

        except Exception as e:
            print(f'Error occurred in batch {i//batch_size + 1}: {e}')

        conn.commit()
        print(f'Batch {i//batch_size + 1} uploaded to the database')

except Exception as e:
    print(f'Error occurred: {e}')

finally:
    conn.commit()
    conn.close()

print(f'Uploaded {count} ticker info to the database')