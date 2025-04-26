import yfinance as yf
import pandas as pd
from datetime import datetime
from typing import Union, List, Dict

from .database import save_to_db

def fetch_stock_data(tickers: Union[str, List[str]]) -> Dict[str, dict]:
    """
    Fetch stock data for one or more tickers
    Args:
        tickers: Single ticker string or list of ticker strings
    Returns:
        Dictionary with ticker as key and stock data as value
    """
    if isinstance(tickers, str):
        tickers = [tickers]
    
    result = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1d")
            if len(hist) == 0:
                continue
                
            info = stock.info
            result[ticker] = {
                "price": hist["Close"].iloc[-1],
                "pe_ratio": info.get("trailingPE", "N/A"),
                "high_52w": info.get("fiftyTwoWeekHigh", "N/A"),
                'change': info.get('regularMarketChangePercent', 0),
                'volume': info.get('volume', 0),
                'market_cap': info.get('marketCap', 0),
            }
        except Exception as e:
            print(f"Error fetching data for {ticker}: {str(e)}")
            continue
    
    if result:
        df = pd.DataFrame([{**data, 'Ticker': ticker} for ticker, data in result.items()])
        save_to_db(df)
        print("Data saved to database.")
    
    return result 