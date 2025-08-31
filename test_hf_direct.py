import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_huggingface():
    api_key = os.getenv('HUGGINGFACE_API_KEY')
    print(f"API Key present: {bool(api_key)}")
    
    if api_key:
        url = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"
        headers = {"Authorization": f"Bearer {api_key}"}
        data = {"inputs": "I love this product!"}
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Parsed result: {result}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    print("Testing Hugging Face API directly...")
    test_huggingface()
