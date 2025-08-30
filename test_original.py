#!/usr/bin/env python3
"""
Test the original dashboard analyze endpoint
"""

import requests
import json

def test_original_dashboard():
    """Test the original dashboard analyze endpoint"""
    
    url = "http://localhost:5003/api/analyze"
    data = {"text": "This is a wonderful test message!"}
    
    try:
        response = requests.post(
            url, 
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(json.dumps(result, indent=2))
        else:
            print("❌ ERROR!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Testing Original Dashboard...")
    test_original_dashboard()
