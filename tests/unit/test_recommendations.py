from recommendation.engine import RecommendationEngine
from recommendation.risk_assessor import calculate_risk

def test_recommendation_flow():
    engine = RecommendationEngine()
    
    # Test AAPL
    result = engine.analyze_stock("AAPL")
    risk = calculate_risk("TSLA", 5000)
    
    print(f"Recommendation: {result['recommendation']}")
    print(f"Risk Score: {risk:.2f}")

if __name__ == "__main__":
    test_recommendation_flow()