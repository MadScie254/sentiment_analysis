"""
Real-time WebSocket server for live sentiment analysis streaming
Provides live updates and real-time monitoring capabilities
"""

import asyncio
import websockets
import json
import logging
from datetime import datetime
from typing import Set, Dict, Any
import threading
import time

# Import our components
from nlp_engine import NLPEngine
from analytics import SentimentAnalytics
from monitoring import SystemMonitor
from database import DatabaseManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentStreamingServer:
    """WebSocket server for real-time sentiment analysis streaming"""
    
    def __init__(self, host='localhost', port=8765):
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.nlp_engine = NLPEngine()
        self.analytics = SentimentAnalytics()
        self.monitor = SystemMonitor()
        self.db_manager = DatabaseManager()
        
        # Start background monitoring
        self.monitor.start_monitoring(interval=15)
        
        # Statistics
        self.stats = {
            'connections': 0,
            'total_messages': 0,
            'analyses_performed': 0,
            'start_time': datetime.now()
        }
    
    async def register_client(self, websocket, path):
        """Register a new WebSocket client"""
        self.clients.add(websocket)
        self.stats['connections'] += 1
        
        logger.info(f"Client connected. Total clients: {len(self.clients)}")
        
        # Send welcome message with current stats
        welcome_message = {
            'type': 'welcome',
            'message': 'Connected to Sentiment Analysis Streaming Server',
            'server_stats': self.get_server_stats(),
            'timestamp': datetime.now().isoformat()
        }
        
        await websocket.send(json.dumps(welcome_message))
        
        try:
            # Listen for messages from this client
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client disconnected")
        finally:
            self.clients.discard(websocket)
    
    async def handle_message(self, websocket, message):
        """Handle incoming WebSocket message"""
        try:
            self.stats['total_messages'] += 1
            data = json.loads(message)
            message_type = data.get('type', 'unknown')
            
            logger.info(f"Received message type: {message_type}")
            
            if message_type == 'analyze':
                await self.handle_analyze_request(websocket, data)
            elif message_type == 'subscribe_monitoring':
                await self.handle_monitoring_subscription(websocket, data)
            elif message_type == 'get_analytics':
                await self.handle_analytics_request(websocket, data)
            elif message_type == 'ping':
                await self.handle_ping(websocket)
            else:
                await self.send_error(websocket, f"Unknown message type: {message_type}")
                
        except json.JSONDecodeError:
            await self.send_error(websocket, "Invalid JSON format")
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await self.send_error(websocket, f"Server error: {str(e)}")
    
    async def handle_analyze_request(self, websocket, data):
        """Handle sentiment analysis request"""
        try:
            # Extract content
            video_title = data.get('video_title', '')
            video_description = data.get('video_description', '')
            comments = data.get('comments', [])
            request_id = data.get('request_id', str(time.time()))
            
            # Perform analysis
            start_time = time.time()
            result = self.nlp_engine.analyze_video_data(video_title, video_description, comments)
            analysis_time = time.time() - start_time
            
            self.stats['analyses_performed'] += 1
            
            # Add metadata
            result['metadata'] = {
                'request_id': request_id,
                'analysis_time_seconds': round(analysis_time, 3),
                'processed_at': datetime.now().isoformat(),
                'server_stats': self.get_server_stats()
            }
            
            # Send result
            response = {
                'type': 'analysis_result',
                'data': result,
                'timestamp': datetime.now().isoformat()
            }
            
            await websocket.send(json.dumps(response))
            
            # Add to analytics history
            self.analytics.add_analysis(result)
            
            # Broadcast summary to other monitoring clients
            await self.broadcast_analysis_summary(result)
            
        except Exception as e:
            await self.send_error(websocket, f"Analysis failed: {str(e)}")
    
    async def handle_monitoring_subscription(self, websocket, data):
        """Handle monitoring subscription request"""
        try:
            subscription_type = data.get('subscription_type', 'all')
            interval = data.get('interval', 30)  # seconds
            
            # Send initial monitoring data
            monitoring_data = {
                'type': 'monitoring_data',
                'data': {
                    'system_health': self.monitor.get_health_status(),
                    'current_metrics': self.monitor.get_current_metrics(),
                    'server_stats': self.get_server_stats(),
                    'database_stats': self.db_manager.get_system_stats()
                },
                'timestamp': datetime.now().isoformat()
            }
            
            await websocket.send(json.dumps(monitoring_data))
            
            # Mark client for monitoring updates
            if not hasattr(websocket, 'monitoring_subscription'):
                websocket.monitoring_subscription = {
                    'type': subscription_type,
                    'interval': interval,
                    'last_sent': time.time()
                }
            
        except Exception as e:
            await self.send_error(websocket, f"Monitoring subscription failed: {str(e)}")
    
    async def handle_analytics_request(self, websocket, data):
        """Handle analytics report request"""
        try:
            days_back = data.get('days_back', 7)
            report_type = data.get('report_type', 'comprehensive')
            
            if report_type == 'comprehensive':
                report = self.analytics.generate_comprehensive_report(days_back)
            else:
                report = self.analytics.get_trend_summary('sentiment')
            
            response = {
                'type': 'analytics_report',
                'data': report,
                'timestamp': datetime.now().isoformat()
            }
            
            await websocket.send(json.dumps(response))
            
        except Exception as e:
            await self.send_error(websocket, f"Analytics request failed: {str(e)}")
    
    async def handle_ping(self, websocket):
        """Handle ping request"""
        pong_response = {
            'type': 'pong',
            'server_time': datetime.now().isoformat(),
            'uptime_seconds': (datetime.now() - self.stats['start_time']).total_seconds()
        }
        await websocket.send(json.dumps(pong_response))
    
    async def send_error(self, websocket, error_message):
        """Send error response"""
        error_response = {
            'type': 'error',
            'message': error_message,
            'timestamp': datetime.now().isoformat()
        }
        await websocket.send(json.dumps(error_response))
    
    async def broadcast_analysis_summary(self, analysis_result):
        """Broadcast analysis summary to monitoring clients"""
        if not self.clients:
            return
        
        summary = {
            'type': 'analysis_broadcast',
            'data': {
                'video_sentiment': analysis_result.get('video_sentiment', {}),
                'comments_summary': {
                    'total_comments': len(analysis_result.get('comments', [])),
                    'sentiment_distribution': self._get_sentiment_distribution(analysis_result),
                    'emotion_distribution': self._get_emotion_distribution(analysis_result)
                }
            },
            'timestamp': datetime.now().isoformat()
        }
        
        # Send to monitoring clients only
        monitoring_clients = [
            client for client in self.clients 
            if hasattr(client, 'monitoring_subscription')
        ]
        
        if monitoring_clients:
            message = json.dumps(summary)
            await asyncio.gather(
                *[client.send(message) for client in monitoring_clients],
                return_exceptions=True
            )
    
    def _get_sentiment_distribution(self, result):
        """Get sentiment distribution from analysis result"""
        comments = result.get('comments', [])
        distribution = {'positive': 0, 'negative': 0, 'neutral': 0, 'mixed': 0}
        
        for comment in comments:
            sentiment = comment.get('sentiment', {}).get('label', 'neutral')
            if sentiment in distribution:
                distribution[sentiment] += 1
        
        return distribution
    
    def _get_emotion_distribution(self, result):
        """Get emotion distribution from analysis result"""
        comments = result.get('comments', [])
        emotions = {}
        
        for comment in comments:
            emotion_tags = comment.get('emotion_tags', [])
            for emotion in emotion_tags:
                emotions[emotion] = emotions.get(emotion, 0) + 1
        
        return emotions
    
    def get_server_stats(self):
        """Get current server statistics"""
        uptime = (datetime.now() - self.stats['start_time']).total_seconds()
        
        return {
            'active_connections': len(self.clients),
            'total_connections': self.stats['connections'],
            'total_messages': self.stats['total_messages'],
            'analyses_performed': self.stats['analyses_performed'],
            'uptime_seconds': round(uptime, 2),
            'uptime_formatted': self._format_uptime(uptime),
            'messages_per_minute': round((self.stats['total_messages'] / max(uptime / 60, 1)), 2)
        }
    
    def _format_uptime(self, seconds):
        """Format uptime in human readable format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    async def start_monitoring_broadcast(self):
        """Background task to broadcast monitoring data"""
        while True:
            try:
                await asyncio.sleep(30)  # Broadcast every 30 seconds
                
                if not self.clients:
                    continue
                
                # Get monitoring clients
                monitoring_clients = [
                    client for client in self.clients 
                    if hasattr(client, 'monitoring_subscription')
                ]
                
                if not monitoring_clients:
                    continue
                
                # Prepare monitoring update
                monitoring_update = {
                    'type': 'monitoring_update',
                    'data': {
                        'system_health': self.monitor.get_health_status(),
                        'current_metrics': self.monitor.get_current_metrics(),
                        'server_stats': self.get_server_stats()
                    },
                    'timestamp': datetime.now().isoformat()
                }
                
                message = json.dumps(monitoring_update)
                
                # Send to all monitoring clients
                await asyncio.gather(
                    *[client.send(message) for client in monitoring_clients],
                    return_exceptions=True
                )
                
            except Exception as e:
                logger.error(f"Error in monitoring broadcast: {e}")
    
    async def start_server(self):
        """Start the WebSocket server"""
        logger.info(f"🚀 Starting Sentiment Analysis WebSocket Server on {self.host}:{self.port}")
        
        # Start background monitoring broadcast
        asyncio.create_task(self.start_monitoring_broadcast())
        
        # Start WebSocket server
        server = await websockets.serve(
            self.register_client,
            self.host,
            self.port,
            ping_interval=20,
            ping_timeout=10
        )
        
        logger.info(f"✅ WebSocket server running on ws://{self.host}:{self.port}")
        logger.info("📡 Available message types:")
        logger.info("   - analyze: Perform sentiment analysis")
        logger.info("   - subscribe_monitoring: Subscribe to real-time monitoring")
        logger.info("   - get_analytics: Get analytics report")
        logger.info("   - ping: Ping server")
        
        return server

def run_streaming_server(host='localhost', port=8765):
    """Run the streaming server"""
    server = SentimentStreamingServer(host, port)
    
    async def main():
        await server.start_server()
        # Keep server running
        await asyncio.Future()  # Run forever
    
    asyncio.run(main())

if __name__ == '__main__':
    # Start the streaming server
    run_streaming_server(host='0.0.0.0', port=8765)
