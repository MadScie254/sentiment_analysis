import json
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dashboard import NLPEngine

# Test the sentiment analysis directly
nlp = NLPEngine()

# Test cases
test_cases = [
    "This is amazing! I love this wonderful experience!",
    "This is terrible! I hate this awful experience!",
    "The weather is okay today."
]

print("=== SENTIMENT ANALYSIS TEST ===")
for i, text in enumerate(test_cases, 1):
    result = nlp.analyze_sentiment(text)
    print(f"\nTest {i}: {text}")
    print(f"Result: {json.dumps(result, indent=2)}")
