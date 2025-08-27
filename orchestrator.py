"""
Master orchestrator for the entire sentiment analysis system
Coordinates all components and provides unified management interface
"""

import asyncio
import threading
import time
import signal
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
import logging

# Import all system components
from nlp_engine import NLPEngine
from sentiment_engine import SentimentAnalyzer
from emotion_detector import EmotionDetector
from comment_classifier import CommentClassifier
from analytics import SentimentAnalytics
from database import DatabaseManager
from monitoring import SystemMonitor, PerformanceTracker
from config_manager import ConfigurationManager, get_config
from dashboard import app as dashboard_app
from streaming_server import SentimentStreamingServer

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SentimentAnalysisOrchestrator:
    """Master orchestrator for the entire sentiment analysis system"""
    
    def __init__(self, config_file: str = 'config.ini', environment: str = 'development'):
        self.config = ConfigurationManager(config_file, environment)
        self.running = False
        self.services = {}
        
        # Initialize core components
        self.nlp_engine = NLPEngine()
        self.analytics = SentimentAnalytics()
        self.database = DatabaseManager()
        self.monitor = SystemMonitor()
        self.performance_tracker = PerformanceTracker(self.monitor)
        
        # Services
        self.dashboard_thread = None
        self.streaming_server = None
        self.streaming_thread = None
        
        # Statistics
        self.start_time = datetime.now()
        self.stats = {
            'total_analyses': 0,
            'total_comments_processed': 0,
            'system_restarts': 0,
            'errors_handled': 0
        }
        
        logger.info("🚀 Sentiment Analysis Orchestrator initialized")
    
    def start_system(self):
        """Start the complete sentiment analysis system"""
        logger.info("🏁 Starting Sentiment Analysis System...")
        
        try:
            self.running = True
            
            # Print configuration summary
            self.config.print_summary()
            
            # Validate configuration
            issues = self.config.validate_config()
            if issues:
                logger.warning(f"Configuration issues detected: {issues}")
            
            # Initialize database
            self._initialize_database()
            
            # Start monitoring
            self._start_monitoring()
            
            # Start core services
            if self.config.streaming.enabled:
                self._start_streaming_server()
            
            # Start dashboard
            self._start_dashboard()
            
            # Setup signal handlers
            self._setup_signal_handlers()
            
            # System ready
            self._system_ready()
            
            # Keep main thread alive
            self._main_loop()
            
        except Exception as e:
            logger.error(f"Failed to start system: {e}")
            self.shutdown_system()
            raise
    
    def _initialize_database(self):
        """Initialize database connection and tables"""
        logger.info("💾 Initializing database...")
        
        try:
            # Test database connection
            stats = self.database.get_system_stats()
            logger.info(f"✅ Database connected. Videos: {stats.get('total_videos_analyzed', 0)}, Comments: {stats.get('total_comments_analyzed', 0)}")
            
            self.services['database'] = {
                'status': 'running',
                'started_at': datetime.now(),
                'component': self.database
            }
            
        except Exception as e:
            logger.error(f"❌ Database initialization failed: {e}")
            raise
    
    def _start_monitoring(self):
        """Start system monitoring"""
        if not self.config.monitoring.enabled:
            logger.info("📊 Monitoring disabled in configuration")
            return
        
        logger.info("📊 Starting system monitoring...")
        
        try:
            # Start monitoring thread
            self.monitor.start_monitoring(interval=self.config.monitoring.metrics_interval_seconds)
            
            self.services['monitoring'] = {
                'status': 'running',
                'started_at': datetime.now(),
                'component': self.monitor
            }
            
            logger.info("✅ System monitoring started")
            
        except Exception as e:
            logger.error(f"❌ Monitoring startup failed: {e}")
            # Don't raise - monitoring is not critical
    
    def _start_streaming_server(self):
        """Start WebSocket streaming server"""
        logger.info("📡 Starting WebSocket streaming server...")
        
        try:
            self.streaming_server = SentimentStreamingServer(
                host=self.config.streaming.host,
                port=self.config.streaming.port
            )
            
            def run_streaming():
                asyncio.set_event_loop(asyncio.new_event_loop())
                loop = asyncio.get_event_loop()
                try:
                    loop.run_until_complete(self.streaming_server.start_server())
                    loop.run_forever()
                except Exception as e:
                    logger.error(f"Streaming server error: {e}")
            
            self.streaming_thread = threading.Thread(target=run_streaming, daemon=True)
            self.streaming_thread.start()
            
            self.services['streaming'] = {
                'status': 'running',
                'started_at': datetime.now(),
                'component': self.streaming_server,
                'thread': self.streaming_thread
            }
            
            logger.info(f"✅ WebSocket server started on ws://{self.config.streaming.host}:{self.config.streaming.port}")
            
        except Exception as e:
            logger.error(f"❌ Streaming server startup failed: {e}")
            # Don't raise - streaming is optional
    
    def _start_dashboard(self):
        """Start web dashboard"""
        logger.info("🌐 Starting web dashboard...")
        
        try:
            def run_dashboard():
                dashboard_app.run(
                    host=self.config.api.host,
                    port=self.config.api.port,
                    debug=self.config.api.debug,
                    threaded=True,
                    use_reloader=False
                )
            
            self.dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
            self.dashboard_thread.start()
            
            self.services['dashboard'] = {
                'status': 'running',
                'started_at': datetime.now(),
                'component': dashboard_app,
                'thread': self.dashboard_thread
            }
            
            logger.info(f"✅ Dashboard started on http://{self.config.api.host}:{self.config.api.port}")
            
        except Exception as e:
            logger.error(f"❌ Dashboard startup failed: {e}")
            # Don't raise - dashboard is important but not critical
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            logger.info(f"🛑 Received signal {signum}, shutting down gracefully...")
            self.shutdown_system()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def _system_ready(self):
        """System is ready notification"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        logger.info("🎉 Sentiment Analysis System is READY!")
        logger.info("=" * 60)
        logger.info(f"🚀 Environment: {self.config.env}")
        logger.info(f"⏱️  Startup time: {uptime:.2f} seconds")
        logger.info(f"🌐 Dashboard: http://{self.config.api.host}:{self.config.api.port}")
        
        if self.config.streaming.enabled:
            logger.info(f"📡 WebSocket: ws://{self.config.streaming.host}:{self.config.streaming.port}")
        
        logger.info(f"🧠 NLP Engine: Ready for analysis")
        logger.info(f"📊 Analytics: {self.analytics.get_total_analyses()} historical analyses")
        logger.info(f"💾 Database: {self.database.get_system_stats().get('total_videos_analyzed', 0)} videos, {self.database.get_system_stats().get('total_comments_analyzed', 0)} comments")
        logger.info("=" * 60)
        
        # Log available endpoints
        logger.info("🔗 Available Endpoints:")
        logger.info(f"   GET  http://{self.config.api.host}:{self.config.api.port}/ - Dashboard")
        logger.info(f"   POST http://{self.config.api.host}:{self.config.api.port}/api/analyze - Analyze content")
        logger.info(f"   GET  http://{self.config.api.host}:{self.config.api.port}/api/system/health - Health check")
        logger.info(f"   GET  http://{self.config.api.host}:{self.config.api.port}/api/analytics/report - Analytics report")
        logger.info(f"   GET  http://{self.config.api.host}:{self.config.api.port}/api/example/demo - Demo analysis")
        
        if self.config.streaming.enabled:
            logger.info(f"   WS   ws://{self.config.streaming.host}:{self.config.streaming.port} - Real-time streaming")
    
    def _main_loop(self):
        """Main system loop"""
        try:
            while self.running:
                # Periodic health checks
                self._periodic_health_check()
                
                # Sleep for a bit
                time.sleep(30)
                
        except KeyboardInterrupt:
            logger.info("🛑 Keyboard interrupt received")
        except Exception as e:
            logger.error(f"❌ Main loop error: {e}")
            self.stats['errors_handled'] += 1
        finally:
            self.shutdown_system()
    
    def _periodic_health_check(self):
        """Perform periodic health checks"""
        try:
            # Check service health
            for service_name, service_info in self.services.items():
                if service_info['status'] == 'running':
                    # Basic health check
                    if hasattr(service_info['component'], 'get_health_status'):
                        health = service_info['component'].get_health_status()
                        if health.get('health_status') == 'critical':
                            logger.warning(f"⚠️  Service {service_name} is in critical state")
            
            # Check system resources
            if self.config.monitoring.enabled:
                health = self.monitor.get_health_status()
                if health['health_score'] < 50:
                    logger.warning(f"⚠️  System health score is low: {health['health_score']}/100")
            
        except Exception as e:
            logger.error(f"Health check error: {e}")
    
    def analyze_content(self, video_title: str, video_description: str, comments: List[str]) -> Dict[str, Any]:
        """Analyze content using the system"""
        try:
            with self.performance_tracker.track_analysis() as tracker:
                tracker.set_comment_count(len(comments))
                
                # Perform analysis
                result = self.nlp_engine.analyze_video_data(video_title, video_description, comments)
                
                # Update statistics
                self.stats['total_analyses'] += 1
                self.stats['total_comments_processed'] += len(comments)
                
                # Add to analytics
                self.analytics.add_analysis(result)
                
                # Add metadata
                result['system_metadata'] = {
                    'processed_by': 'SentimentAnalysisOrchestrator',
                    'system_uptime_seconds': (datetime.now() - self.start_time).total_seconds(),
                    'total_system_analyses': self.stats['total_analyses'],
                    'environment': self.config.env
                }
                
                return result
                
        except Exception as e:
            logger.error(f"Analysis error: {e}")
            self.stats['errors_handled'] += 1
            raise
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            uptime = (datetime.now() - self.start_time).total_seconds()
            
            # Service statuses
            service_statuses = {}
            for service_name, service_info in self.services.items():
                service_statuses[service_name] = {
                    'status': service_info['status'],
                    'started_at': service_info['started_at'].isoformat(),
                    'uptime_seconds': (datetime.now() - service_info['started_at']).total_seconds()
                }
            
            # System health
            system_health = {}
            if self.config.monitoring.enabled:
                system_health = self.monitor.get_health_status()
            
            # Database stats
            db_stats = {}
            try:
                db_stats = self.database.get_system_stats()
            except:
                pass
            
            return {
                'system_info': {
                    'status': 'running' if self.running else 'stopped',
                    'environment': self.config.env,
                    'uptime_seconds': uptime,
                    'uptime_formatted': self._format_uptime(uptime),
                    'started_at': self.start_time.isoformat()
                },
                'services': service_statuses,
                'statistics': self.stats,
                'health': system_health,
                'database': db_stats,
                'configuration': {
                    'nlp_enabled': True,
                    'streaming_enabled': self.config.streaming.enabled,
                    'monitoring_enabled': self.config.monitoring.enabled,
                    'analytics_enabled': self.config.analytics.enabled
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {'error': str(e)}
    
    def _format_uptime(self, seconds):
        """Format uptime in human readable format"""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        
        if days > 0:
            return f"{days}d {hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def restart_service(self, service_name: str) -> bool:
        """Restart a specific service"""
        if service_name not in self.services:
            logger.error(f"Unknown service: {service_name}")
            return False
        
        try:
            logger.info(f"🔄 Restarting service: {service_name}")
            
            # Stop service
            self._stop_service(service_name)
            
            # Wait a bit
            time.sleep(2)
            
            # Start service again
            if service_name == 'streaming':
                self._start_streaming_server()
            elif service_name == 'dashboard':
                self._start_dashboard()
            elif service_name == 'monitoring':
                self._start_monitoring()
            
            logger.info(f"✅ Service {service_name} restarted")
            self.stats['system_restarts'] += 1
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to restart service {service_name}: {e}")
            return False
    
    def _stop_service(self, service_name: str):
        """Stop a specific service"""
        if service_name in self.services:
            service_info = self.services[service_name]
            service_info['status'] = 'stopped'
            
            # Stop threads if any
            if 'thread' in service_info and service_info['thread'].is_alive():
                # Note: Can't actually stop threads gracefully in Python
                # This is more of a status update
                pass
    
    def shutdown_system(self):
        """Gracefully shutdown the entire system"""
        if not self.running:
            return
        
        logger.info("🛑 Shutting down Sentiment Analysis System...")
        self.running = False
        
        try:
            # Stop all services
            for service_name in list(self.services.keys()):
                self._stop_service(service_name)
            
            # Stop monitoring
            if hasattr(self.monitor, 'stop_monitoring'):
                self.monitor.stop_monitoring()
            
            # Close database connections
            if hasattr(self.database, 'close'):
                self.database.close()
            
            # Final statistics
            uptime = (datetime.now() - self.start_time).total_seconds()
            logger.info(f"📊 Final Statistics:")
            logger.info(f"   Uptime: {self._format_uptime(uptime)}")
            logger.info(f"   Total analyses: {self.stats['total_analyses']}")
            logger.info(f"   Comments processed: {self.stats['total_comments_processed']}")
            logger.info(f"   Errors handled: {self.stats['errors_handled']}")
            logger.info(f"   Restarts: {self.stats['system_restarts']}")
            
            logger.info("✅ System shutdown complete")
            
        except Exception as e:
            logger.error(f"❌ Error during shutdown: {e}")

def create_orchestrator(config_file: str = 'config.ini', environment: str = 'development') -> SentimentAnalysisOrchestrator:
    """Create and configure the orchestrator"""
    return SentimentAnalysisOrchestrator(config_file, environment)

def main():
    """Main function to run the complete system"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Sentiment Analysis System Orchestrator')
    parser.add_argument('--config', default='config.ini', help='Configuration file')
    parser.add_argument('--env', default='development', choices=['development', 'testing', 'production'], help='Environment')
    parser.add_argument('--demo', action='store_true', help='Run quick demo analysis')
    
    args = parser.parse_args()
    
    if args.demo:
        # Quick demo mode
        print("🎯 Running Quick Demo...")
        orchestrator = create_orchestrator(args.config, args.env)
        
        # Demo analysis
        result = orchestrator.analyze_content(
            "My first day in Nairobi 🚖🔥",
            "Trying out local food and matatus, what an adventure!",
            [
                "😂😂 bro you look lost but it's vibes",
                "This city will eat you alive, trust me.",
                "Matatu rides >>> Uber any day",
                "Spam link: www.fakecrypto.com",
                "Karibu Kenya! We love you ❤️"
            ]
        )
        
        print("📊 Demo Analysis Result:")
        print(json.dumps(result, indent=2))
        
        # System status
        status = orchestrator.get_system_status()
        print(f"\n🚥 System Status: {status['system_info']['status']}")
        
    else:
        # Full system mode
        orchestrator = create_orchestrator(args.config, args.env)
        orchestrator.start_system()

if __name__ == '__main__':
    main()
