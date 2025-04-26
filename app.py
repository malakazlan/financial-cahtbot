from data_pipeline import fetch_stock_data
from nlp.intent_classifier import IntentClassifier
from nlp.entity_recognizer import extract_financial_entities
from recommendation.engine import RecommendationEngine

def handle_query(query):
    """Process user queries and return appropriate responses"""
    # Initialize components
    classifier = IntentClassifier()
    classifier.train()
    engine = RecommendationEngine()
    
    try:
        # Get intent and entities
        intent = classifier.predict(query)
        entities = extract_financial_entities(query)
        
        # Handle different intents
        if intent == "buy_recommendation":
            if not entities["tickers"]:
                return "Please specify a stock ticker (e.g., AAPL, MSFT, GOOGL)"
            
            recommendations = []
            for ticker in entities["tickers"]:
                analysis = engine.analyze_stock(ticker)
                if "error" in analysis:
                    recommendations.append(f"{ticker}: {analysis['error']}")
                else:
                    rec = f"{ticker}: {analysis['recommendation']}\n"
                    rec += f"Price: ${analysis['current_price']}, Change: {analysis['price_change']}%\n"
                    rec += f"Reasons: {', '.join(analysis['reasons'])}"
                    recommendations.append(rec)
            
            return "\n\n".join(recommendations)
            
        elif intent == "fundamental_query":
            if not entities["tickers"]:
                return "Please specify a stock ticker (e.g., AAPL, MSFT, GOOGL)"
            
            data = fetch_stock_data(entities["tickers"])
            return str(data)
            
        else:
            return "I can help you with stock recommendations and fundamental data. Try asking something like 'Should I buy AAPL?' or 'What's the P/E ratio of MSFT?'"
            
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Test
if __name__ == "__main__":
    test_queries = [
        "Should I buy AAPL?",
        "What's the P/E ratio of MSFT?",
        "Should I invest in TSLA and GOOGL?",
        "Tell me about XYZ stock"  # Unknown ticker
    ]
    
    print("Testing Financial Chatbot:")
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = handle_query(query)
        print(f"Response: {result}")
        print("-" * 50)