import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import yfinance as yf
from database.mongo import db
from datetime import datetime

def update_stocks(tickers: list):
    for ticker in tickers:
        try:
            print(f"Fetching {ticker}...")
            ticker_obj = yf.Ticker(ticker)
            fast_info = ticker_obj.fast_info
            info = ticker_obj.info
            print(f"Fast info for {ticker}: {fast_info}")
            print(f"Info for {ticker}: {info}")
            # Try fast_info['last_price'], fallback to info['regularMarketPrice']
            price = fast_info.get("last_price") or info.get("regularMarketPrice")
            print(f"Using price for {ticker}: {price}")
            db.stocks.update_one(
                {"_id": ticker},
                {"$set": {
                    "current_price": price,
                    "pe_ratio": info.get("trailingPE"),
                    "last_updated": datetime.utcnow()
                }},
                upsert=True
            )
            print(f"Updated {ticker} in DB.")
        except Exception as e:
            print(f"Failed {ticker}: {str(e)}")

if __name__ == "__main__":
    update_stocks(["AAPL", "TSLA"])