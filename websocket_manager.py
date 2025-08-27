"""
Real-time WebSocket implementation for live sentiment updates
Provides instant feedback and live dashboard updates
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Set, Any
import websockets
from websockets.server import WebSocketServerProtocol
import threading
import queue
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self.clients: Set[WebSocketServerProtocol] = set()
        self.message_queue = queue.Queue()
        self.server = None
        self.running = False
    
    async def register_client(self, websocket: WebSocketServerProtocol):
        """Register a new client connection"""
        self.clients.add(websocket)
        client_id = str(uuid.uuid4())[:8]
        logger.info(f"Client {client_id} connected. Total clients: {len(self.clients)}")
        
        # Send welcome message with current stats
        welcome_message = {
            "type": "connection",
            "message": "Connected to SentimentAI WebSocket",
            "client_id": client_id,
            "timestamp": datetime.now().isoformat(),
            "connected_clients": len(self.clients)
        }
        await websocket.send(json.dumps(welcome_message))
    
    async def unregister_client(self, websocket: WebSocketServerProtocol):
        """Unregister a client connection"""
        self.clients.discard(websocket)
        logger.info(f"Client disconnected. Total clients: {len(self.clients)}")
    
    async def broadcast_message(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients"""
        if not self.clients:
            return
        
        message_str = json.dumps(message)
        disconnected_clients = set()
        
        for client in self.clients.copy():
            try:
                await client.send(message_str)
            except websockets.exceptions.ConnectionClosed:
                disconnected_clients.add(client)
            except Exception as e:
                logger.error(f"Error sending message to client: {e}")
                disconnected_clients.add(client)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            self.clients.discard(client)
    
    async def send_sentiment_update(self, analysis_result: Dict[str, Any]):
        """Send real-time sentiment analysis update"""
        message = {
            "type": "sentiment_update",
            "data": analysis_result,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast_message(message)
    
    async def send_metrics_update(self, metrics: Dict[str, Any]):
        """Send real-time metrics update"""
        message = {
            "type": "metrics_update",
            "data": metrics,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast_message(message)
    
    async def send_system_notification(self, notification: str, level: str = "info"):
        """Send system notification"""
        message = {
            "type": "notification",
            "level": level,
            "message": notification,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast_message(message)
    
    async def send_data_update(self, data_type: str, data: Any):
        """Send general data update"""
        message = {
            "type": "data_update",
            "data_type": data_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        await self.broadcast_message(message)
    
    async def handle_client_message(self, websocket: WebSocketServerProtocol, message: str):
        """Handle incoming messages from clients"""
        try:
            data = json.loads(message)
            message_type = data.get("type", "unknown")
            
            if message_type == "ping":
                # Respond to ping with pong
                pong_message = {
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send(json.dumps(pong_message))
            
            elif message_type == "subscribe":
                # Handle subscription to specific data types
                subscription = data.get("subscription", "all")
                response = {
                    "type": "subscription_confirmed",
                    "subscription": subscription,
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send(json.dumps(response))
            
            elif message_type == "request_stats":
                # Send current statistics
                from database_manager import db_manager
                stats = db_manager.get_dashboard_summary()
                
                response = {
                    "type": "stats_response",
                    "data": stats,
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send(json.dumps(response))
            
            else:
                logger.warning(f"Unknown message type: {message_type}")
        
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON received: {message}")
        except Exception as e:
            logger.error(f"Error handling client message: {e}")
    
    async def client_handler(self, websocket: WebSocketServerProtocol, path: str = "/"):
        """Handle individual client connections"""
        await self.register_client(websocket)
        
        try:
            async for message in websocket:
                await self.handle_client_message(websocket, message)
        
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client connection closed")
        except Exception as e:
            logger.error(f"Error in client handler: {e}")
        finally:
            await self.unregister_client(websocket)
    
    async def start_server(self, host: str = "localhost", port: int = 8765):
        """Start the WebSocket server"""
        self.running = True
        
        try:
            self.server = await websockets.serve(
                self.client_handler,
                host,
                port,
                ping_interval=30,
                ping_timeout=10
            )
            logger.info(f"WebSocket server started on ws://{host}:{port}")
            
            # Send periodic updates
            asyncio.create_task(self.periodic_updates())
            
            await self.server.wait_closed()
        
        except Exception as e:
            logger.error(f"Error starting WebSocket server: {e}")
            self.running = False
    
    async def stop_server(self):
        """Stop the WebSocket server"""
        self.running = False
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            logger.info("WebSocket server stopped")
    
    async def periodic_updates(self):
        """Send periodic updates to clients"""
        while self.running:
            try:
                # Send heartbeat every 30 seconds
                if self.clients:
                    heartbeat = {
                        "type": "heartbeat",
                        "connected_clients": len(self.clients),
                        "timestamp": datetime.now().isoformat()
                    }
                    await self.broadcast_message(heartbeat)
                
                await asyncio.sleep(30)
                
            except Exception as e:
                logger.error(f"Error in periodic updates: {e}")
                await asyncio.sleep(5)

class AsyncMessageBroker:
    """Async message broker for handling real-time updates"""
    
    def __init__(self, websocket_manager: WebSocketManager):
        self.websocket_manager = websocket_manager
        self.message_queue = asyncio.Queue()
        self.running = False
    
    async def start(self):
        """Start the message broker"""
        self.running = True
        asyncio.create_task(self.process_messages())
    
    async def stop(self):
        """Stop the message broker"""
        self.running = False
    
    async def process_messages(self):
        """Process queued messages"""
        while self.running:
            try:
                # Wait for message with timeout
                message = await asyncio.wait_for(
                    self.message_queue.get(), 
                    timeout=1.0
                )
                
                # Process based on message type
                if message["type"] == "sentiment_analysis":
                    await self.websocket_manager.send_sentiment_update(message["data"])
                elif message["type"] == "metrics":
                    await self.websocket_manager.send_metrics_update(message["data"])
                elif message["type"] == "notification":
                    await self.websocket_manager.send_system_notification(
                        message["message"], 
                        message.get("level", "info")
                    )
                elif message["type"] == "data_update":
                    await self.websocket_manager.send_data_update(
                        message["data_type"], 
                        message["data"]
                    )
                
                self.message_queue.task_done()
                
            except asyncio.TimeoutError:
                # No message received, continue
                continue
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    
    async def queue_sentiment_update(self, analysis_result: Dict[str, Any]):
        """Queue sentiment analysis update"""
        await self.message_queue.put({
            "type": "sentiment_analysis",
            "data": analysis_result
        })
    
    async def queue_metrics_update(self, metrics: Dict[str, Any]):
        """Queue metrics update"""
        await self.message_queue.put({
            "type": "metrics",
            "data": metrics
        })
    
    async def queue_notification(self, message: str, level: str = "info"):
        """Queue system notification"""
        await self.message_queue.put({
            "type": "notification",
            "message": message,
            "level": level
        })
    
    async def queue_data_update(self, data_type: str, data: Any):
        """Queue general data update"""
        await self.message_queue.put({
            "type": "data_update",
            "data_type": data_type,
            "data": data
        })

# Global WebSocket manager instance
websocket_manager = WebSocketManager()
message_broker = AsyncMessageBroker(websocket_manager)

def start_websocket_server(host: str = "localhost", port: int = 8765):
    """Start WebSocket server in a separate thread"""
    def run_server():
        asyncio.set_event_loop(asyncio.new_event_loop())
        loop = asyncio.get_event_loop()
        
        # Start message broker
        loop.run_until_complete(message_broker.start())
        
        # Start WebSocket server
        try:
            loop.run_until_complete(websocket_manager.start_server(host, port))
        except KeyboardInterrupt:
            logger.info("WebSocket server interrupted")
        finally:
            loop.run_until_complete(message_broker.stop())
            loop.run_until_complete(websocket_manager.stop_server())
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    return server_thread

# Real-time update functions for easy integration
def send_realtime_sentiment(analysis_result: Dict[str, Any]):
    """Send real-time sentiment update (sync wrapper)"""
    try:
        asyncio.create_task(message_broker.queue_sentiment_update(analysis_result))
    except RuntimeError:
        # If no event loop is running, start one temporarily
        asyncio.run(message_broker.queue_sentiment_update(analysis_result))

def send_realtime_metrics(metrics: Dict[str, Any]):
    """Send real-time metrics update (sync wrapper)"""
    try:
        asyncio.create_task(message_broker.queue_metrics_update(metrics))
    except RuntimeError:
        asyncio.run(message_broker.queue_metrics_update(metrics))

def send_realtime_notification(message: str, level: str = "info"):
    """Send real-time notification (sync wrapper)"""
    try:
        asyncio.create_task(message_broker.queue_notification(message, level))
    except RuntimeError:
        asyncio.run(message_broker.queue_notification(message, level))

def send_realtime_data(data_type: str, data: Any):
    """Send real-time data update (sync wrapper)"""
    try:
        asyncio.create_task(message_broker.queue_data_update(data_type, data))
    except RuntimeError:
        asyncio.run(message_broker.queue_data_update(data_type, data))
