from flask import Blueprint, jsonify
from database.mongo import db

bp = Blueprint('stocks_api', __name__)

@bp.route('/stock/<ticker>', methods=['GET'])
def get_stock(ticker):
    stock = db.stocks.find_one({"_id": ticker})
    if not stock:
        return jsonify({"error": "Stock not found"}), 404
    return jsonify({
        "ticker": ticker,
        "current_price": stock.get("current_price"),
        "pe_ratio": stock.get("pe_ratio"),
        "last_updated": stock.get("last_updated").isoformat() if stock.get("last_updated") else None
    })