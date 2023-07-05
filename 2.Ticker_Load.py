import requests
from bs4 import BeautifulSoup

URL = "https://www.gpw.pl/spolki"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

tags = soup('span', class_='grey')

stock_symbols = list()

for tag in tags:
    symbol = tag.text.strip()
    symbol = symbol.replace("(", "").replace(")", "")  # Remove parentheses
    stock_symbols.append(symbol)

for stock in stock_symbols:
    print(stock)
