import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import requests
from database.mongo import db
from datetime import datetime

def fetch_and_store_news():
    api_key = os.getenv("NEWS_API_KEY")  # Put your NewsAPI key in .env
    url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={api_key}"
    res = requests.get(url)
    print("API response:", res.json())  # Debug print
    articles = res.json().get("articles", [])
    for art in articles:
        db.news.update_one(
            {"title": art["title"]},
            {"$set": {
                "title": art["title"],
                "source": art["source"]["name"],
                "published_at": datetime.strptime(art["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"),
            }},
            upsert=True
        )

if __name__ == "__main__":
    fetch_and_store_news()