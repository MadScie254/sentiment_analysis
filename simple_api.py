import json
from typing import Dict, List, Any
from nlp_engine import NLPEngine

class SimpleAPI:
    """
    Simple JSON-based API without FastAPI dependencies
    Can be used as a standalone processor or integrated with any web framework
    """
    
    def __init__(self):
        self.nlp_engine = NLPEngine()
    
    def process_video_request(self, request_data: str) -> str:
        """
        Process video analysis request from JSON string
        Returns JSON string response
        """
        try:
            data = json.loads(request_data)
            
            video_title = data.get("video_title", "")
            video_description = data.get("video_description", "")
            comments = data.get("comments", [])
            
            result = self.nlp_engine.analyze_video_data(
                video_title=video_title,
                video_description=video_description,
                comments=comments
            )
            
            # Format response as requested
            formatted_response = {
                "video_sentiment": result["video_sentiment"],
                "video_emotion": result["video_emotion"],
                "comments": [
                    {
                        "text": comment["text"],
                        "sentiment": comment["sentiment"],
                        "emotion": comment["emotion"],
                        "tag": comment["tag"]
                    }
                    for comment in result["comments"]
                ]
            }
            
            return json.dumps(formatted_response, indent=2, ensure_ascii=False)
            
        except Exception as e:
            error_response = {
                "error": f"Analysis failed: {str(e)}",
                "status": "error"
            }
            return json.dumps(error_response, indent=2)
    
    def process_text_request(self, text: str) -> str:
        """
        Process single text analysis
        """
        try:
            result = self.nlp_engine.quick_analyze(text)
            return json.dumps(result, indent=2, ensure_ascii=False)
        except Exception as e:
            error_response = {
                "error": f"Analysis failed: {str(e)}",
                "status": "error"
            }
            return json.dumps(error_response, indent=2)
    
    def get_example_analysis(self) -> str:
        """
        Return the example analysis from the prompt
        """
        try:
            video_title = "My first day in Nairobi 🚖🔥"
            video_description = "Trying out local food and matatus, what an adventure!"
            comments = [
                "😂😂 bro you look lost but it's vibes",
                "This city will eat you alive, trust me.",
                "Matatu rides >>> Uber any day",
                "Spam link: www.fakecrypto.com",
                "Karibu Kenya! We love you ❤️"
            ]
            
            result = self.nlp_engine.analyze_video_data(
                video_title=video_title,
                video_description=video_description,
                comments=comments
            )
            
            formatted_response = {
                "video_sentiment": result["video_sentiment"],
                "video_emotion": result["video_emotion"],
                "comments": [
                    {
                        "text": comment["text"],
                        "sentiment": comment["sentiment"],
                        "emotion": comment["emotion"],
                        "tag": comment["tag"]
                    }
                    for comment in result["comments"]
                ]
            }
            
            return json.dumps(formatted_response, indent=2, ensure_ascii=False)
            
        except Exception as e:
            error_response = {
                "error": f"Example analysis failed: {str(e)}",
                "status": "error"
            }
            return json.dumps(error_response, indent=2)

def main():
    """
    Demo function to show the API working with the example data
    """
    print("🚀 Sentiment Analysis Engine - Demo")
    print("=" * 50)
    
    api = SimpleAPI()
    
    # Process the example data
    result = api.get_example_analysis()
    print("📊 Example Analysis Result:")
    print(result)
    
    print("\n" + "=" * 50)
    print("✅ System is ready! You can now:")
    print("1. Use SimpleAPI for JSON-based processing")
    print("2. Run api_server.py for FastAPI web interface")
    print("3. Import NLPEngine directly for custom integration")

if __name__ == "__main__":
    main()
