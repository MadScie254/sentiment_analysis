"""
Client demo for WebSocket streaming server
Shows how to connect and interact with the real-time sentiment analysis stream
"""

import asyncio
import websockets
import json
import time
from datetime import datetime

class SentimentStreamingClient:
    """Demo client for the sentiment analysis streaming server"""
    
    def __init__(self, uri='ws://localhost:8765'):
        self.uri = uri
        self.websocket = None
        self.running = False
    
    async def connect(self):
        """Connect to the streaming server"""
        print(f"🔌 Connecting to {self.uri}...")
        
        try:
            self.websocket = await websockets.connect(self.uri)
            self.running = True
            print("✅ Connected to sentiment analysis streaming server!")
            
            # Start message handler
            await self.listen_for_messages()
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
    
    async def listen_for_messages(self):
        """Listen for incoming messages"""
        try:
            async for message in self.websocket:
                await self.handle_message(message)
        except websockets.exceptions.ConnectionClosed:
            print("🔌 Connection closed")
            self.running = False
    
    async def handle_message(self, message):
        """Handle incoming message from server"""
        try:
            data = json.loads(message)
            message_type = data.get('type', 'unknown')
            timestamp = data.get('timestamp', datetime.now().isoformat())
            
            print(f"\n📨 [{timestamp}] Received: {message_type}")
            
            if message_type == 'welcome':
                print(f"   Welcome message: {data.get('message')}")
                server_stats = data.get('server_stats', {})
                print(f"   Server uptime: {server_stats.get('uptime_formatted', 'unknown')}")
                print(f"   Active connections: {server_stats.get('active_connections', 0)}")
            
            elif message_type == 'analysis_result':
                await self.display_analysis_result(data.get('data', {}))
            
            elif message_type == 'monitoring_data' or message_type == 'monitoring_update':
                await self.display_monitoring_data(data.get('data', {}))
            
            elif message_type == 'analysis_broadcast':
                await self.display_analysis_broadcast(data.get('data', {}))
            
            elif message_type == 'analytics_report':
                await self.display_analytics_report(data.get('data', {}))
            
            elif message_type == 'pong':
                print(f"   🏓 Pong received - Server time: {data.get('server_time')}")
            
            elif message_type == 'error':
                print(f"   ❌ Error: {data.get('message')}")
            
        except json.JSONDecodeError:
            print(f"   ⚠️  Invalid JSON received: {message}")
        except Exception as e:
            print(f"   ❌ Error handling message: {e}")
    
    async def display_analysis_result(self, result):
        """Display analysis result"""
        print("   🧠 Analysis Result:")
        
        # Video sentiment
        video_sentiment = result.get('video_sentiment', {})
        if video_sentiment:
            print(f"      📹 Video: {video_sentiment.get('label', 'unknown')} ({video_sentiment.get('confidence', 0):.2f})")
        
        # Comments summary
        comments = result.get('comments', [])
        print(f"      💬 Comments analyzed: {len(comments)}")
        
        if comments:
            # Sentiment distribution
            sentiments = {}
            emotions = {}
            tones = {}
            
            for comment in comments:
                # Count sentiments
                sentiment = comment.get('sentiment', {}).get('label', 'neutral')
                sentiments[sentiment] = sentiments.get(sentiment, 0) + 1
                
                # Count emotions
                for emotion in comment.get('emotion_tags', []):
                    emotions[emotion] = emotions.get(emotion, 0) + 1
                
                # Count tones
                tone = comment.get('tone', 'unknown')
                tones[tone] = tones.get(tone, 0) + 1
            
            print(f"      📊 Sentiment: {dict(sentiments)}")
            print(f"      😊 Emotions: {dict(emotions)}")
            print(f"      🎵 Tones: {dict(tones)}")
        
        # Metadata
        metadata = result.get('metadata', {})
        if metadata:
            print(f"      ⏱️  Analysis time: {metadata.get('analysis_time_seconds', 0)}s")
    
    async def display_monitoring_data(self, data):
        """Display monitoring data"""
        print("   📊 Monitoring Data:")
        
        health = data.get('system_health', {})
        if health:
            print(f"      🚥 Health: {health.get('health_status', 'unknown')} (score: {health.get('health_score', 0)}/100)")
            print(f"      ⚠️  Alerts: {health.get('critical_alerts', 0)} critical, {health.get('warning_alerts', 0)} warning")
        
        metrics = data.get('current_metrics', {})
        if metrics:
            print(f"      💾 Memory: {metrics.get('memory_percent', 0):.1f}%")
            print(f"      🔧 CPU: {metrics.get('cpu_percent', 0):.1f}%")
        
        server_stats = data.get('server_stats', {})
        if server_stats:
            print(f"      🌐 Connections: {server_stats.get('active_connections', 0)}")
            print(f"      📈 Analyses: {server_stats.get('analyses_performed', 0)}")
    
    async def display_analysis_broadcast(self, data):
        """Display analysis broadcast"""
        print("   📡 Analysis Broadcast:")
        
        video_sentiment = data.get('video_sentiment', {})
        if video_sentiment:
            print(f"      📹 Video sentiment: {video_sentiment.get('label', 'unknown')}")
        
        comments_summary = data.get('comments_summary', {})
        if comments_summary:
            print(f"      💬 Comments: {comments_summary.get('total_comments', 0)}")
            sentiment_dist = comments_summary.get('sentiment_distribution', {})
            if sentiment_dist:
                print(f"      📊 Sentiment distribution: {sentiment_dist}")
    
    async def display_analytics_report(self, report):
        """Display analytics report"""
        print("   📈 Analytics Report:")
        
        summary = report.get('summary', {})
        if summary:
            print(f"      📊 Total analyses: {summary.get('total_analyses', 0)}")
            print(f"      💬 Total comments: {summary.get('total_comments', 0)}")
            print(f"      🗓️  Period: {summary.get('period_days', 0)} days")
        
        # Show top emotions if available
        emotion_analysis = report.get('emotion_analysis', {})
        if emotion_analysis:
            top_emotions = emotion_analysis.get('top_emotions', [])
            if top_emotions:
                print(f"      😊 Top emotions: {[emotion['emotion'] for emotion in top_emotions[:3]]}")
    
    async def send_message(self, message_data):
        """Send message to server"""
        if self.websocket and self.running:
            try:
                message = json.dumps(message_data)
                await self.websocket.send(message)
                print(f"📤 Sent: {message_data.get('type', 'unknown')}")
            except Exception as e:
                print(f"❌ Failed to send message: {e}")
    
    async def run_demo_analysis(self):
        """Run demo analysis"""
        demo_data = {
            'type': 'analyze',
            'request_id': f'demo_{int(time.time())}',
            'video_title': 'My first day in Nairobi 🚖🔥',
            'video_description': 'Trying out local food and matatus, what an adventure!',
            'comments': [
                '😂😂 bro you look lost but it\'s vibes',
                'This city will eat you alive, trust me.',
                'Matatu rides >>> Uber any day',
                'Spam link: www.fakecrypto.com',
                'Karibu Kenya! We love you ❤️'
            ]
        }
        
        await self.send_message(demo_data)
    
    async def subscribe_to_monitoring(self):
        """Subscribe to monitoring updates"""
        monitoring_data = {
            'type': 'subscribe_monitoring',
            'subscription_type': 'all',
            'interval': 30
        }
        
        await self.send_message(monitoring_data)
    
    async def request_analytics(self):
        """Request analytics report"""
        analytics_data = {
            'type': 'get_analytics',
            'days_back': 7,
            'report_type': 'comprehensive'
        }
        
        await self.send_message(analytics_data)
    
    async def ping_server(self):
        """Ping the server"""
        ping_data = {'type': 'ping'}
        await self.send_message(ping_data)
    
    async def interactive_demo(self):
        """Run interactive demo"""
        print("\n🎯 Interactive Demo Started!")
        print("Available commands:")
        print("  1 - Run demo analysis")
        print("  2 - Subscribe to monitoring")
        print("  3 - Request analytics report")
        print("  4 - Ping server")
        print("  5 - Custom analysis")
        print("  q - Quit")
        
        while self.running:
            try:
                command = input("\nEnter command (1-5, q): ").strip()
                
                if command == 'q':
                    break
                elif command == '1':
                    await self.run_demo_analysis()
                elif command == '2':
                    await self.subscribe_to_monitoring()
                elif command == '3':
                    await self.request_analytics()
                elif command == '4':
                    await self.ping_server()
                elif command == '5':
                    await self.custom_analysis()
                else:
                    print("Invalid command. Use 1-5 or q.")
                
                # Small delay for processing
                await asyncio.sleep(0.1)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    async def custom_analysis(self):
        """Run custom analysis with user input"""
        print("\n📝 Custom Analysis:")
        
        try:
            title = input("Video title: ").strip()
            description = input("Video description: ").strip()
            
            print("Enter comments (one per line, empty line to finish):")
            comments = []
            while True:
                comment = input().strip()
                if not comment:
                    break
                comments.append(comment)
            
            if not title and not description and not comments:
                print("❌ No content provided")
                return
            
            custom_data = {
                'type': 'analyze',
                'request_id': f'custom_{int(time.time())}',
                'video_title': title,
                'video_description': description,
                'comments': comments
            }
            
            await self.send_message(custom_data)
            
        except KeyboardInterrupt:
            print("\nCustom analysis cancelled")
    
    async def disconnect(self):
        """Disconnect from server"""
        if self.websocket:
            await self.websocket.close()
            print("🔌 Disconnected from server")

async def main():
    """Main function"""
    client = SentimentStreamingClient()
    
    try:
        # Connect and run interactive demo
        await asyncio.gather(
            client.connect(),
            client.interactive_demo()
        )
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    print("🚀 Sentiment Analysis Streaming Client Demo")
    print("Make sure the streaming server is running on ws://localhost:8765")
    print("Starting client in 3 seconds...")
    
    asyncio.run(main())
