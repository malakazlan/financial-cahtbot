import re

def extract_financial_entities(text):
    """Extract tickers, metrics, and keywords."""
    # Define financial metrics
    metrics = ["P/E", "ROI", "EPS", "volume", "market cap", "dividend"]
    
    # Common words to exclude from ticker detection
    exclude_words = {"I", "A", "THE", "IN", "ON", "AT", "TO", "FOR", "OF", "IS", "BUY", "SELL", "NEWS", "SHOW", "ME", "SHOULD", "WHAT", "ABOUT", "AND", "LATEST", "STOCK", "PRICE", "CURRENT", "HISTORY", "CHART", "RECOMMENDATION", "TELL"}
    
    # Find metrics first (case insensitive)
    found_metrics = []
    for metric in metrics:
        if re.search(r'\b' + re.escape(metric) + r'\b', text, re.IGNORECASE):
            found_metrics.append(metric.upper())
    
    # Match stock tickers (2-5 uppercase letters, excluding found metrics and common words)
    tickers = []
    for match in re.findall(r'\b[A-Z]{2,5}\b', text.upper()):
        if match not in found_metrics and match not in exclude_words:
            tickers.append(match)
    
    # Keywords (case insensitive)
    keywords = [word.lower() for word in text.split() 
               if word.lower() in ["buy", "sell", "news", "forecast", "price", "trend"]]
    
    return {
        "tickers": tickers,
        "metrics": found_metrics,
        "keywords": keywords
    }

# Test
if __name__ == "__main__":
    test_cases = [
        "Should I buy AAPL? What's its P/E?",
        "Show me TSLA's ROI and latest news",
        "What's the EPS forecast for GOOGL?",
        "The MSFT stock is trending up"
    ]
    
    for test in test_cases:
        print(f"\nInput: {test}")
        print(f"Entities: {extract_financial_entities(test)}")