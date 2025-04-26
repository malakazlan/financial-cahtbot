import pandas as pd
from data.pipeline import fetch_stock_data

class RecommendationEngine:
    def __init__(self):
        # Define sector benchmarks
        self.sector_benchmarks = {
            "tech": {
                "pe_ratio": 25.0,
                "tickers": ["AAPL", "MSFT", "GOOGL"],
                "growth_threshold": 15.0
            },
            "automotive": {
                "pe_ratio": 20.0,
                "tickers": ["TSLA"],
                "growth_threshold": 20.0
            }
        }
    
    def analyze_stock(self, ticker: str) -> dict:
        """Generate detailed stock recommendation"""
        try:
            # Fetch stock data
            data = fetch_stock_data(ticker)
            if isinstance(data, str) or ticker not in data:
                return {"error": f"Could not fetch data for {ticker}"}
            
            stock_data = data[ticker]
            
            # Determine sector
            sector = self._get_sector(ticker)
            if not sector:
                return {"error": f"Unknown sector for {ticker}"}
            
            # Analyze metrics
            analysis = {
                "ticker": ticker,
                "current_price": stock_data['price'],
                "pe_ratio": stock_data.get('pe_ratio', 'N/A'),
                "volume": stock_data['volume'],
                "price_change": stock_data['change']
            }
            
            # Generate recommendation
            recommendation = self._generate_recommendation(analysis, sector)
            analysis.update(recommendation)
            
            return analysis
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def _get_sector(self, ticker: str) -> str:
        """Determine stock sector"""
        for sector, info in self.sector_benchmarks.items():
            if ticker in info["tickers"]:
                return sector
        return None
    
    def _generate_recommendation(self, analysis: dict, sector: str) -> dict:
        """Generate detailed recommendation based on analysis"""
        benchmark = self.sector_benchmarks[sector]
        score = 0
        reasons = []
        
        # Check P/E ratio
        if analysis['pe_ratio'] != 'N/A':
            if float(analysis['pe_ratio']) < benchmark['pe_ratio']:
                score += 1
                reasons.append("P/E ratio below sector average")
            else:
                reasons.append("P/E ratio above sector average")
        
        # Check price momentum
        if analysis['price_change'] > 0:
            score += 1
            reasons.append("Positive price momentum")
        else:
            reasons.append("Negative price momentum")
        
        # Generate recommendation
        if score >= 2:
            recommendation = "STRONG BUY"
        elif score == 1:
            recommendation = "BUY"
        else:
            recommendation = "HOLD"
        
        return {
            "recommendation": recommendation,
            "score": score,
            "reasons": reasons,
            "sector": sector
        }

# Test
if __name__ == "__main__":
    engine = RecommendationEngine()
    
    # Test with different stocks
    test_tickers = ["AAPL", "MSFT", "TSLA"]
    print("Testing Recommendation Engine:")
    for ticker in test_tickers:
        print(f"\nAnalyzing {ticker}:")
        result = engine.analyze_stock(ticker)
        for key, value in result.items():
            print(f"{key}: {value}")