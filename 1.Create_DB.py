import sqlite3

conn = sqlite3.connect('Stocks.db')
cursor = conn.cursor()
 
cursor.execute('''
CREATE TABLE IF NOT EXISTS Stocks (
ticker VARCHAR(10) PRIMARY KEY UNIQUE,
company_name VARCHAR(50),
industry VARCHAR(50)
)''')
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

conn.commit()
conn.close()
