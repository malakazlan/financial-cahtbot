from nlp.intent_classifier import IntentClassifier
from nlp.entity_recognizer import extract_financial_entities

def test_nlp_pipeline():
    classifier = IntentClassifier()
    classifier.train()
    
    query = "Show me TSLA's ROI and latest news"
    intent = classifier.predict(query)
    entities = extract_financial_entities(query)
    
    print(f"Intent: {intent}")
    print(f"Entities: {entities}")

if __name__ == "__main__":
    test_nlp_pipeline()