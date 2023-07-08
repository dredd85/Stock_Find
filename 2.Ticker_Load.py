import requests
from bs4 import BeautifulSoup

URL = "https://infostrefa.com/infostrefa/pl/spolki"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

tickers = []

tags = soup.find("table", class_="table table-text table-text-left custom-border")

for tag in tags.find_all('tr'):
    for row in tag:
        strip_row = row.text.strip()
        if len(strip_row) !=3:
            continue
        else:
            tickers.append(strip_row)

print(*tickers)