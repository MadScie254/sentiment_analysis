#!/usr/bin/env python3
"""
Test script to verify the sentiment analysis API endpoint
"""

import requests
import json

def test_analyze_endpoint():
    """Test the /api/analyze endpoint"""
    
    # Test data
    test_text = "This is a wonderful day and I'm feeling great!"
    
    # API endpoint
    url = "http://localhost:5003/api/analyze"
    
    # Request data
    data = {
        "text": test_text
    }
    
    try:
        # Make POST request
        response = requests.post(
            url, 
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"Text: {result.get('text', 'N/A')}")
            print(f"Sentiment: {result.get('sentiment', 'N/A')}")
            print(f"Confidence: {result.get('confidence', 'N/A'):.2%}")
            print(f"Model: {result.get('model_used', 'N/A')}")
            print(f"Processing Time: {result.get('processing_time', 'N/A')} seconds")
            
            if 'scores' in result:
                print("Sentiment Scores:")
                for sentiment, score in result['scores'].items():
                    print(f"  {sentiment}: {score:.2%}")
                    
        else:
            print("❌ ERROR!")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection Error: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")

if __name__ == "__main__":
    print("🧪 Testing Sentiment Analysis API...")
    test_analyze_endpoint()
