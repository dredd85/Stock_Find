import yfinance as yf
import pandas as pd
import sqlite3

df = pd.read_csv('tickers.csv')
tickers = df.values.tolist()
unpacked_tickers = [row for rows in tickers for row in rows]

count = 0
batch_size = 50
conn = sqlite3.connect('Stocks.db')
cursor = conn.cursor()

try:
    for i in range(0, len(unpacked_tickers), batch_size):
        batch_tickers = unpacked_tickers[i : i + batch_size]

        for ticker in batch_tickers:
            try:
                stock = yf.Ticker(ticker)
                stock_info = stock.info
                stock_name = stock_info.get('longName', 'N/A')
                stock_sector = stock_info.get('sector', 'N/A')
                print(f'Stock Symbol: {ticker}')
                print(f"Stock Name: {stock_name}")
                print(f"Sector: {stock_sector}")
                cursor.execute('''
                    INSERT OR IGNORE INTO Stocks (ticker, company_name, industry) 
                    VALUES (?,?,?)''', (ticker, stock_name, stock_sector))
                count += 1
            except Exception as e:
                # Ignore the 404 errors and continue with the next ticker
                print(f'Error occurred for ticker {ticker}: {e}')

        conn.commit()
        print(f'Batch {i//batch_size + 1} uploaded to the database')

except Exception as e:
    print(f'Error occurred: {e}')

finally:
    conn.commit()
    conn.close()

print(f'Uploaded {count} ticker info to the database')