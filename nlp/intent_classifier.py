from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer

TRAIN_DATA = [
    ("Should I buy AAPL?", "buy_recommendation"),
    ("What's the P/E of MSFT?", "fundamental_query"),
    ("News about Tesla", "news_request"),
    ("Show me Tesla news", "news_request"),
    ("What are the latest headlines?", "news_request"),
    ("Should I sell GOOGL?", "buy_recommendation"),
    ("Tell me about Amazon stock", "fundamental_query"),
]

class IntentClassifier:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.clf = LinearSVC()

    def train(self):
        texts, labels = zip(*TRAIN_DATA)
        X = self.vectorizer.fit_transform(texts)
        self.clf.fit(X, labels)
        
    def predict(self, text):
        X = self.vectorizer.transform([text])  
        return self.clf.predict(X)[0]
    
if __name__ == "__main__":
    classifier = IntentClassifier()
    classifier.train()
    
    # Test some examples
    test_queries = [
        "Should I sell GOOGL?",
        "What's happening with NVDA?",
        "Show me news about Apple?",
    ]
    
    print("Testing the classifier:")
    for query in test_queries:
        intent = classifier.predict(query)
        print(f"Query: '{query}' → Intent: {intent}")
    
      
                
        
        