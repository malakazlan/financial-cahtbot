from flask import Blueprint, request, jsonify
from .chatbot import FinancialChatbot
from datetime import datetime

bp = Blueprint('api', __name__)
chatbot = FinancialChatbot()

@bp.route('/')
def home():
    """Serve the homepage."""
    return {
        "message": "Welcome to the Financial Chatbot API",
        "endpoints": {
            "/chat": "POST - Send queries to the chatbot",
            "/market": "GET - Get market summary",
            "/news": "GET - Get latest financial news",
            "/stock/<ticker>": "GET - Get stock information"
        }
    }

@bp.route('/chat', methods=['POST'])
def chat():
    """Handle user queries and return responses."""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                "error": "Please provide a query in the request body",
                "example": {"query": "Tell me about TSLA"}
            }), 400
            
        user_query = data.get('query', '')
        user_id = data.get('user_id')  # Optional user identification
        
        response = chatbot.process_query(user_query, user_id)
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "An error occurred while processing your request"
        }), 500

@bp.route('/market', methods=['GET'])
def market_summary():
    """Get current market summary."""
    try:
        market_data = chatbot.market_service.get_market_summary()
        return jsonify({
            "response": "Current market summary",
            "data": market_data,
            "type": "market_summary"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Failed to fetch market data"
        }), 500

@bp.route('/news', methods=['GET'])
def news():
    """Get latest financial news."""
    try:
        ticker = request.args.get('ticker')
        news_data = chatbot.news_service.get_financial_news(ticker)
        return jsonify({
            "response": "Latest financial news",
            "data": news_data,
            "type": "news"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Failed to fetch news"
        }), 500

@bp.route('/stock/<ticker>', methods=['GET'])
def stock_info(ticker):
    """Get information about a specific stock."""
    try:
        stock_data = chatbot.stock_service.get_stock_info(ticker)
        return jsonify({
            "response": f"Information for {ticker}",
            "data": stock_data,
            "type": "stock_info"
        })
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": f"Failed to fetch information for {ticker}"
        }), 500