import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import sys

load_dotenv()

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

class StockService:
    @staticmethod
    def get_stock_info(ticker):
        """Get comprehensive stock information."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            return {
                'symbol': ticker,
                'company_name': info.get('longName', ''),
                'current_price': info.get('currentPrice', 0),
                'market_cap': info.get('marketCap', 0),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'pe_ratio': info.get('trailingPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                '52_week_high': info.get('fiftyTwoWeekHigh', 0),
                '52_week_low': info.get('fiftyTwoWeekLow', 0),
                'volume': info.get('volume', 0)
            }
        except Exception as e:
            return {'error': str(e)}

    @staticmethod
    def get_stock_history(ticker, period='1y'):
        """Get historical stock data."""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            return hist.to_dict('records')
        except Exception as e:
            return {'error': str(e)}

class NewsService:
    @staticmethod
    def get_financial_news(ticker=None):
        """Get financial news, optionally filtered by ticker."""
        try:
            api_key = os.getenv('NEWS_API_KEY')
            if not api_key:
                return {'error': 'News API key not configured'}
            
            url = 'https://newsapi.org/v2/everything'
            params = {
                'apiKey': api_key,
                'q': ticker if ticker else 'stock market',
                'language': 'en',
                'sortBy': 'publishedAt'
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if data.get('status') == 'ok':
                return data.get('articles', [])
            return {'error': 'Failed to fetch news'}
        except Exception as e:
            return {'error': str(e)}

class MarketService:
    @staticmethod
    def get_market_summary():
        """Get overall market summary."""
        try:
            # Get major indices
            indices = {
                '^GSPC': 'S&P 500',
                '^DJI': 'Dow Jones',
                '^IXIC': 'NASDAQ'
            }
            
            summary = {}
            for symbol, name in indices.items():
                ticker = yf.Ticker(symbol)
                info = ticker.info
                summary[name] = {
                    'current_price': info.get('currentPrice', 0),
                    'change': info.get('regularMarketChange', 0),
                    'change_percent': info.get('regularMarketChangePercent', 0)
                }
            
            return summary
        except Exception as e:
            return {'error': str(e)} 