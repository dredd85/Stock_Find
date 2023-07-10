import requests
from bs4 import BeautifulSoup
import pandas as pd 

URL = "https://infostrefa.com/infostrefa/pl/spolki?market=mainMarket"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

tickers = set()

tags = soup.find("table", class_="table table-text table-text-left custom-border")

for tag in tags.find_all('tr'):
    for row in tag:
        strip_row = row.text.strip()
        if len(strip_row) !=3 or strip_row.isupper() != True:
            continue
        else:
            strip_row_gpw = strip_row + '.WA'
            tickers.add(strip_row_gpw)
tickers = list(tickers)
tickers.sort()

print('Downloaded {} GPW tickers from the website'.format(len(tickers)))

df = pd.DataFrame(tickers)
df.to_csv('tickers.csv', encoding='utf-8', index=False, header=False)
df.columns = ['Tickers']
print('Writen data into tickers.csv file')


