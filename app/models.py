from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class Stock(Base):
    __tablename__ = 'stocks'
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), unique=True)
    company_name = Column(String(100))
    sector = Column(String(50))
    industry = Column(String(50))
    last_price = Column(Float)
    last_updated = Column(DateTime, default=datetime.utcnow)

class UserQuery(Base):
    __tablename__ = 'user_queries'
    
    id = Column(Integer, primary_key=True)
    query_text = Column(Text)
    response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String(50))  # Can be session ID or actual user ID

# Database setup
def init_db(db_url='sqlite:///financial_chatbot.db'):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session() 