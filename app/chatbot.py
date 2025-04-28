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
            db_query = UserQuery(
                query_text=query,
                user_id=user_id
            )
            entities = extract_financial_entities(query)
            tickers = entities.get("tickers", [])
            ticker = tickers[0] if tickers else None
            q_lower = query.lower()
            response = {
                "response": "",
                "data": None,
                "type": "text"
            }
            # Conversational logic
            if ticker:
                if "buy" in q_lower:
                    stock_info = self.stock_service.get_stock_info(ticker)
                    if stock_info.get("error"):
                        response["response"] = f"Sorry, I couldn't fetch data for {ticker}."
                    else:
                        pe = stock_info.get("pe_ratio", 'N/A')
                        price = stock_info.get("current_price", 'N/A')
                        response["response"] = (
                            f"Here's my take on {ticker}:\n"
                            f"Current price: ${price}\nP/E Ratio: {pe}\n"
                            f"(This is a demo. For real investment advice, consult a professional.)"
                        )
                        response["data"] = stock_info
                elif "sell" in q_lower:
                    response["response"] = f"Thinking of selling {ticker}? Consider recent performance and your investment goals. (This is a demo response.)"
                elif "news" in q_lower:
                    news = self.news_service.get_financial_news(ticker)
                    if isinstance(news, list) and news:
                        response["response"] = f"Latest news for {ticker}:\n" + '\n'.join([n.get('title', '') for n in news[:3]])
                        response["data"] = news
                    else:
                        response["response"] = f"No recent news found for {ticker}."
                elif "price" in q_lower or "current" in q_lower:
                    stock_info = self.stock_service.get_stock_info(ticker)
                    if stock_info.get("error"):
                        response["response"] = f"Sorry, I couldn't fetch data for {ticker}."
                    else:
                        response["response"] = f"The current price of {ticker} is ${stock_info.get('current_price', 'N/A')}"
                        response["data"] = stock_info
                else:
                    stock_info = self.stock_service.get_stock_info(ticker)
                    if stock_info.get("error"):
                        response["response"] = f"Sorry, I couldn't fetch data for {ticker}."
                    else:
                        response["response"] = f"Here's what I know about {ticker}:\nPrice: ${stock_info.get('current_price', 'N/A')}\nP/E Ratio: {stock_info.get('pe_ratio', 'N/A')}"
                        response["data"] = stock_info
            elif "news" in q_lower:
                news = self.news_service.get_financial_news()
                if isinstance(news, list) and news:
                    response["response"] = "Here are the latest financial news headlines:\n" + '\n'.join([n.get('title', '') for n in news[:3]])
                    response["data"] = news
                else:
                    response["response"] = "No recent financial news found."
            elif "market" in q_lower or "summary" in q_lower:
                market_data = self.market_service.get_market_summary()
                response["response"] = "Here's the current market summary:"
                response["data"] = market_data
                response["type"] = "market_summary"
            else:
                response["response"] = (
                    "I'm a financial chatbot. I can help you with:\n"
                    "- Stock recommendations (e.g., 'Should I buy TSLA?')\n"
                    "- Stock prices (e.g., 'What is the price of AAPL?')\n"
                    "- Financial news (e.g., 'Show me news about Tesla')\n"
                    "- Market summary (e.g., 'What's the market doing?')\n"
                    "What would you like to know?"
                )
            db_query.response = str(response)
            self.db_session.add(db_query)
            self.db_session.commit()
            return response
        except Exception as e:
            return {
                "response": f"Sorry, I encountered an error: {str(e)}",
                "data": None,
                "type": "error"
            }