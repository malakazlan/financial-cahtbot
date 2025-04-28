from flask import Blueprint, request, jsonify, render_template_string
from .chatbot import FinancialChatbot
from datetime import datetime

bp = Blueprint('api', __name__)
chatbot = FinancialChatbot()

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Financial Chatbot</title>
  <style>
    body { font-family: sans-serif; max-width: 700px; margin: 2rem auto; }
    .card { border: 1px solid #ccc; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; }
    .chatbox { border: 1px solid #ccc; border-radius: 8px; padding: 1rem; margin-top: 2rem; }
    .messages { min-height: 100px; margin-bottom: 1rem; }
    .user { text-align: right; color: #0074d9; }
    .bot { text-align: left; color: #111; }
    .error { color: red; }
  </style>
</head>
<body>
  <h1>Financial Chatbot</h1>
  <div id="stock-cards"></div>
  <div id="news-section"></div>
  <div class="chatbox">
    <h2>Chat with the Bot</h2>
    <div class="messages" id="messages"></div>
    <form id="chat-form">
      <input id="chat-input" type="text" placeholder="Ask a financial question..." style="width:80%;padding:8px;" />
      <button type="submit" style="padding:8px 16px;">Send</button>
    </form>
  </div>
  <script>
    // Stock info
    async function loadStock(ticker) {
      const res = await fetch(`/stock/${ticker}`);
      const data = await res.json();
      return `<div class='card'><h3>${ticker}</h3><p>Price: $${data.data?.current_price ?? 'N/A'}</p><p>P/E Ratio: ${data.data?.pe_ratio ?? 'N/A'}</p></div>`;
    }
    async function showStocks() {
      const tickers = ['AAPL', 'TSLA'];
      let html = '';
      for (const t of tickers) html += await loadStock(t);
      document.getElementById('stock-cards').innerHTML = html;
    }
    // News
    async function showNews() {
      const res = await fetch('/news');
      const data = await res.json();
      let html = `<div class='card'><h3>Latest News</h3>`;
      if (Array.isArray(data.data)) {
        html += '<ul>' + data.data.slice(0,5).map(n => `<li><b>${n.title}</b> <small>(${n.source})</small></li>`).join('') + '</ul>';
      } else {
        html += '<p>No news available.</p>';
      }
      html += '</div>';
      document.getElementById('news-section').innerHTML = html;
    }
    // Chat
    const messages = [];
    function renderMessages() {
      document.getElementById('messages').innerHTML = messages.map(m => `<div class='${m.from}'>${m.from === 'user' ? 'You' : 'Bot'}: ${m.text}</div>`).join('');
    }
    document.getElementById('chat-form').onsubmit = async (e) => {
      e.preventDefault();
      const input = document.getElementById('chat-input');
      const text = input.value.trim();
      if (!text) return;
      messages.push({ from: 'user', text });
      renderMessages();
      input.value = '';
      try {
        const res = await fetch('/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: text })
        });
        const data = await res.json();
        messages.push({ from: 'bot', text: data.response });
        renderMessages();
      } catch (err) {
        messages.push({ from: 'bot', text: 'Error: ' + err });
        renderMessages();
      }
    };
    showStocks();
    showNews();
  </script>
</body>
</html>
'''

@bp.route('/')
def home():
    return render_template_string(HTML_PAGE)

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