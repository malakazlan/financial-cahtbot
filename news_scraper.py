import requests
import json
from datetime import datetime

def fetch_finance_news():
    """Fetch financial news using Alpha Vantage API."""
    # You need to get a free API key from https://www.alphavantage.co/support/#api-key
    api_key = "YOUR_API_KEY"  # Replace with your Alpha Vantage API key
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&apikey={api_key}&topics=financial_markets&sort=LATEST"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if "feed" in data:
            news_items = []
            for item in data["feed"][:5]:  # Get top 5 news items
                title = item["title"]
                time_published = datetime.strptime(item["time_published"], "%Y%m%dT%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
                news_items.append(f"{time_published}: {title}")
            return news_items
        else:
            print("No news data found in the response")
            return []
            
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return []

# Test
if __name__ == "__main__":
    print("To use this script, you need to:")
    print("1. Sign up for a free API key at https://www.alphavantage.co/support/#api-key")
    print("2. Replace 'YOUR_API_KEY' in the code with your actual API key")
    print("\nOnce you have done that, you'll get the latest financial news!\n")
    
    news = fetch_finance_news()
    if news:
        print("Latest Financial News:")
        for i, headline in enumerate(news, 1):
            print(f"{i}. {headline}")
    else:
        print("No headlines found. Please check your API key and internet connection.")