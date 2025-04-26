from .services import StockService, NewsService, MarketService
from .models import UserQuery, init_db
from nlp.entity_recognizer import extract_financial_entities
import re
from datetime import datetime

class FinancialChatbot:
    def __init__(self):
        self.stock_service = StockService()
        self.news_service = NewsService()
        self.market_service = MarketService()
        self.db_session = init_db()
        
    def process_query(self, query: str, user_id: str = None) -> dict:
        """Process user query and generate comprehensive response."""
        try:
            # Store query in database
            db_query = UserQuery(
                query_text=query,
                user_id=user_id
            )
            
            # Extract entities
            entities = extract_financial_entities(query)
            tickers = entities.get("tickers", [])
            ticker = tickers[0] if tickers else None
            
            response = {
                "response": "",
                "data": None,
                "type": "text"
            }
            
            # Handle different types of queries
            q_lower = query.lower()
            if "market" in q_lower or "summary" in q_lower:
                market_data = self.market_service.get_market_summary()
                response["response"] = "Here's the current market summary:"
                response["data"] = market_data
                response["type"] = "market_summary"
                
            elif ticker:
                if "price" in q_lower or "current" in q_lower:
                    stock_info = self.stock_service.get_stock_info(ticker)
                    response["response"] = f"Here's the current information for {ticker}:"
                    response["data"] = stock_info
                    response["type"] = "stock_info"
                    
                elif "history" in q_lower or "chart" in q_lower:
                    stock_history = self.stock_service.get_stock_history(ticker)
                    response["response"] = f"Here's the historical data for {ticker}:"
                    response["data"] = stock_history
                    response["type"] = "stock_history"
                    
                elif "news" in q_lower:
                    news = self.news_service.get_financial_news(ticker)
                    response["response"] = f"Here are the latest news articles about {ticker}:"
                    response["data"] = news
                    response["type"] = "news"
                    
                else:
                    # Default response for ticker queries
                    stock_info = self.stock_service.get_stock_info(ticker)
                    response["response"] = f"Here's what I know about {ticker}:"
                    response["data"] = stock_info
                    response["type"] = "stock_info"
                    
            elif "news" in q_lower:
                news = self.news_service.get_financial_news()
                response["response"] = "Here are the latest financial news articles:"
                response["data"] = news
                response["type"] = "news"
                
            else:
                response["response"] = (
                    "I'm a financial chatbot. I can help you with:\n"
                    "- Stock information (e.g., 'Tell me about TSLA')\n"
                    "- Market summary (e.g., 'What's the market doing?')\n"
                    "- Financial news (e.g., 'Show me the latest news')\n"
                    "- Stock history (e.g., 'Show me TSLA history')\n"
                    "What would you like to know?"
                )
            
            # Store response in database
            db_query.response = str(response)
            self.db_session.add(db_query)
            self.db_session.commit()
            
            return response
            
        except Exception as e:
            error_response = {
                "response": f"Sorry, I encountered an error: {str(e)}",
                "data": None,
                "type": "error"
            }
            return error_response