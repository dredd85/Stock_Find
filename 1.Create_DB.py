import sqlite3

conn = sqlite3.connect('Stocks.db')
cursor = conn.cursor()
 
cursor.execute('''
CREATE TABLE IF NOT EXISTS Stocks (
id INTEGER PRIMARY KEY AUTOINCREMENT,
symbol VARCHAR(10) UNIQUE,
company_name VARCHAR(50),
industry VARCHAR(50)
)''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS Prices (
id INTEGER PRIMARY KEY AUTOINCREMENT,
stock_id INTEGER, 
date DATE,
open_price REAL,
high_price REAL,
low_price REAL,
close_price REAL,
volume INTEGER,
FOREIGN KEY (stock_id) REFERENCES stocks (id)
)''')

conn.commit()
conn.close()
