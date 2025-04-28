import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.mongo import db
# print(list(db.news.find()))
print(list(db.stocks.find()))

"""
MongoDB Collections:

users:
{
  _id: ObjectId(...),
  email: "user@example.com",
  risk_profile: "moderate",
  portfolio: [
    { ticker: "AAPL", shares: 10, avg_cost: 150.20 }
  ]
}

stocks:
{
  _id: "AAPL",  # Using ticker as _id
  price: 182.63,
  pe_ratio: 28.3,
  last_updated: datetime
}

news:
{
  _id: ObjectId(...),
  title: "Fed raises interest rates",
  source: "Reuters",
  stocks: ["^DJI", "^GSPC"],
  published_at: datetime
}
"""
