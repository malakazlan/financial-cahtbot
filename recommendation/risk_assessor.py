def calculate_risk(ticker: str, investment_amount: float) -> float:
    """Simple risk score (0-1, where 1=riskiest)"""
    # Mock logic - replace with real volatility analysis
    risk_map = {
        "TSLA": 0.8,
        "AAPL": 0.3,
        "MSFT": 0.4
    }
    return risk_map.get(ticker, 0.5) * min(1, investment_amount / 10000)

if __name__ == "__main__":
    print(f"TSLA Risk Score: {calculate_risk('TSLA', 5000):.2f}")