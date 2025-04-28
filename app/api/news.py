from flask import Blueprint, jsonify, request
from database.mongo import db

news_bp = Blueprint('news_api', __name__)

@news_bp.route('/news', methods=['GET'])
def get_news():
    limit = int(request.args.get('limit', 10))
    news_cursor = db.news.find().sort('published_at', -1).limit(limit)
    news_list = [
        {
            'title': n.get('title'),
            'source': n.get('source'),
            'published_at': n.get('published_at').isoformat() if n.get('published_at') else None
        }
        for n in news_cursor
    ]
    return jsonify({'data': news_list})
