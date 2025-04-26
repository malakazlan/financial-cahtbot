import unittest
from app import create_app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()
    
    def test_stock_recommendation(self):
        response = self.app.post('/chat', json={"query": "Should I buy AAPL?"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("AAPL", response.json["response"])

if __name__ == "__main__":
    unittest.main()