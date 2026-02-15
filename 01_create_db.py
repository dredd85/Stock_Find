import sqlite3

conn = sqlite3.connect('Stocks.db')
cursor = conn.cursor()
 
cursor.execute('''
CREATE TABLE IF NOT EXISTS Stocks (
ticker VARCHAR(10) PRIMARY KEY UNIQUE,
company_name VARCHAR(50),
industry VARCHAR(50)
)''')
table_name = "Stocks" 
cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
result = cursor.fetchall()
if result:
    print(f"Table '{table_name}' created")
else:
    print(f"Table '{table_name}' does not exist")

cursor.execute('''
CREATE TABLE IF NOT EXISTS Prices (
id INTEGER PRIMARY KEY AUTOINCREMENT,
ticker VARCHAR(10), 
Date DATE,
Open REAL,
High REAL,
Low REAL,
Close REAL,
Volume INTEGER,
FOREIGN KEY (ticker) REFERENCES stocks (ticker)
)''')
table_name = "Prices" 
cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
result = cursor.fetchall()
if result:
    print(f"Table '{table_name}' created")
    print('Table creation complete, continue with Ticker_Load')
else:
    print(f"Table '{table_name}' does not exist")

conn.commit()
conn.close()
