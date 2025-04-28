from pymongo import MongoClient, ASCENDING
from contextlib import contextmanager
import os
from dotenv import load_dotenv

load_dotenv()

class MongoDB:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
        self.db = self.client[os.getenv("MONGO_DB_NAME", "financial_chatbot")]
        # self._create_indexes()
    
    def _create_indexes(self):
        # self.db.stocks.create_index([("ticker", ASCENDING)], unique=True)
        self.db.news.create_index([("published_at", ASCENDING)])
    
    @contextmanager
    def session(self):
        with self.client.start_session() as session:
            yield session

db = MongoDB().db  # Single global instance