import time
import pandas as pd

# --------------------------------------------
# 1) Get the stock list (symbols) from Bankier
# --------------------------------------------
LIST_URL = "https://www.bankier.pl/gielda/notowania/akcje"
stock_table = pd.read_html(LIST_URL)[0]

# Extract first column = company codes (e.g., 06MAGNA, 11BIT)
stocks_gpw = (
    stock_table.iloc[:, 0]
    .astype(str)
    .str.strip()
    .dropna()
    .tolist()
)

print(f"Found {len(stocks_gpw)} stock codes. Taking first 5 for testing...\n")

# -------------------------------------------------
# 2) Define helper to get Ticker GPW from detail page
# -------------------------------------------------
def fetch_ticker_gpw(stock_gpw: str) -> str:
    """
    Given a company symbol from Bankier (e.g., '11BIT'),
    open the 'Podstawowe dane' page and extract 'Ticker GPW'.
    """
    details_url = f"https://www.bankier.pl/gielda/notowania/akcje/{stock_gpw}/podstawowe-dane"
    detail_tables = pd.read_html(details_url, match="Ticker GPW")
    ticker_gpw = detail_tables[0].iloc[3, 1]  # current index-based extraction
    return ticker_gpw

# -----------------------------------------------
# 3) Iterate through first 5 and collect tickers
# -----------------------------------------------
results = []

for stock_gpw in stocks_gpw[:5]:
    try:
        ticker_gpw = fetch_ticker_gpw(stock_gpw)
        ticker_openbb = f"{ticker_gpw}.WA"

        results.append({
            "stock_gpw": stock_gpw,          # Bankier list symbol (e.g., 11BIT)
            "ticker_gpw": ticker_gpw,        # GPW trading ticker (e.g., 11B)
            "ticker_openbb": ticker_openbb,  # OpenBB/Yahoo format (e.g., 11B.WA)
        })

        print(f"{stock_gpw} → GPW: {ticker_gpw}  |  OpenBB/Yahoo: {ticker_openbb}")

    except Exception as e:
        results.append({
            "stock_gpw": stock_gpw,
            "error": str(e),
        })
        print(f"{stock_gpw} → ERROR: {e}")

    time.sleep(0.8)  # be polite to the server

# -----------------------------------------------
# 4) Convert results to DataFrame and inspect
# -----------------------------------------------
tickers_df = pd.DataFrame(results)

print("\nResult preview:")
print(tickers_df.head())


tickers_df["ticker_openbb"].to_csv("tickers.csv", index=False, encoding="utf-8-sig")
