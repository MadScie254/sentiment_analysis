"""
Real-time monitoring and alerting system for sentiment analysis
Provides system health monitoring, performance metrics, and alerting
"""

import time
import threading
import psutil
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Callable, Optional
from collections import deque, defaultdict
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import logging
from dataclasses import dataclass
import statistics

@dataclass
class Alert:
    """Alert data structure"""
    alert_id: str
    severity: str  # critical, warning, info
    title: str
    message: str
    source: str
    timestamp: datetime
    resolved: bool = False
    resolution_time: Optional[datetime] = None

class SystemMonitor:
    """
    Real-time system monitoring for sentiment analysis API
    """
    
    def __init__(self):
        self.metrics = defaultdict(deque)
        self.alerts = []
        self.thresholds = {
            'cpu_usage': 80.0,
            'memory_usage': 85.0,
            'response_time': 5.0,
            'error_rate': 0.05,
            'queue_size': 100
        }
        self.monitoring = False
        self.monitor_thread = None
        self.start_time = datetime.now()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def start_monitoring(self, interval: int = 30):
        """Start real-time monitoring"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop, 
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        self.logger.info("System monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        self.logger.info("System monitoring stopped")
    
    def _monitoring_loop(self, interval: int):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                # Collect system metrics
                self._collect_system_metrics()
                
                # Check thresholds and generate alerts
                self._check_thresholds()
                
                # Clean old metrics (keep last 100 measurements)
                self._cleanup_old_metrics()
                
                time.sleep(interval)
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(interval)
    
    def _collect_system_metrics(self):
        """Collect system performance metrics"""
        timestamp = datetime.now()
        
        # CPU and Memory metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Network metrics
        network = psutil.net_io_counters()
        
        # Store metrics
        self.metrics['cpu_usage'].append((timestamp, cpu_percent))
        self.metrics['memory_usage'].append((timestamp, memory.percent))
        self.metrics['memory_available_gb'].append((timestamp, memory.available / (1024**3)))
        self.metrics['disk_usage'].append((timestamp, disk.percent))
        self.metrics['network_bytes_sent'].append((timestamp, network.bytes_sent))
        self.metrics['network_bytes_recv'].append((timestamp, network.bytes_recv))
        
        # Process-specific metrics
        try:
            process = psutil.Process()
            process_memory = process.memory_info()
            process_cpu = process.cpu_percent()
            
            self.metrics['process_memory_mb'].append((timestamp, process_memory.rss / (1024**2)))
            self.metrics['process_cpu'].append((timestamp, process_cpu))
            
        except psutil.NoSuchProcess:
            pass
    
    def record_api_request(self, endpoint: str, response_time: float, status_code: int):
        """Record API request metrics"""
        timestamp = datetime.now()
        
        self.metrics['response_times'].append((timestamp, response_time))
        self.metrics['request_count'].append((timestamp, 1))
        
        # Track errors (status codes >= 400)
        if status_code >= 400:
            self.metrics['error_count'].append((timestamp, 1))
        
        # Track by endpoint
        endpoint_key = f'endpoint_{endpoint.replace("/", "_")}'
        self.metrics[endpoint_key].append((timestamp, response_time))
    
    def record_analysis_metrics(self, analysis_time: float, comment_count: int, success: bool):
        """Record sentiment analysis performance metrics"""
        timestamp = datetime.now()
        
        self.metrics['analysis_time'].append((timestamp, analysis_time))
        self.metrics['comments_processed'].append((timestamp, comment_count))
        
        if not success:
            self.metrics['analysis_failures'].append((timestamp, 1))
    
    def _check_thresholds(self):
        """Check metrics against thresholds and generate alerts"""
        # Check CPU usage
        if self.metrics['cpu_usage']:
            recent_cpu = [value for _, value in list(self.metrics['cpu_usage'])[-5:]]
            avg_cpu = statistics.mean(recent_cpu)
            
            if avg_cpu > self.thresholds['cpu_usage']:
                self._create_alert(
                    severity="warning",
                    title="High CPU Usage",
                    message=f"CPU usage is {avg_cpu:.1f}% (threshold: {self.thresholds['cpu_usage']}%)",
                    source="SystemMonitor"
                )
        
        # Check memory usage
        if self.metrics['memory_usage']:
            recent_memory = [value for _, value in list(self.metrics['memory_usage'])[-5:]]
            avg_memory = statistics.mean(recent_memory)
            
            if avg_memory > self.thresholds['memory_usage']:
                self._create_alert(
                    severity="warning",
                    title="High Memory Usage",
                    message=f"Memory usage is {avg_memory:.1f}% (threshold: {self.thresholds['memory_usage']}%)",
                    source="SystemMonitor"
                )
        
        # Check response times
        if self.metrics['response_times']:
            recent_times = [value for _, value in list(self.metrics['response_times'])[-10:]]
            avg_response_time = statistics.mean(recent_times)
            
            if avg_response_time > self.thresholds['response_time']:
                self._create_alert(
                    severity="warning",
                    title="Slow Response Time",
                    message=f"Average response time is {avg_response_time:.2f}s (threshold: {self.thresholds['response_time']}s)",
                    source="APIMonitor"
                )
        
        # Check error rate
        if self.metrics['request_count'] and self.metrics['error_count']:
            recent_requests = len([1 for _, _ in list(self.metrics['request_count'])[-50:]])
            recent_errors = len([1 for _, _ in list(self.metrics['error_count'])[-50:]])
            
            if recent_requests > 0:
                error_rate = recent_errors / recent_requests
                
                if error_rate > self.thresholds['error_rate']:
                    self._create_alert(
                        severity="critical",
                        title="High Error Rate",
                        message=f"Error rate is {error_rate:.2%} (threshold: {self.thresholds['error_rate']:.2%})",
                        source="APIMonitor"
                    )
    
    def _create_alert(self, severity: str, title: str, message: str, source: str):
        """Create a new alert"""
        # Check if similar alert already exists and is unresolved
        for alert in self.alerts:
            if (alert.title == title and alert.source == source and 
                not alert.resolved and 
                (datetime.now() - alert.timestamp).total_seconds() < 300):  # 5 minutes
                return  # Don't duplicate recent alerts
        
        alert = Alert(
            alert_id=f"{int(time.time())}_{len(self.alerts)}",
            severity=severity,
            title=title,
            message=message,
            source=source,
            timestamp=datetime.now()
        )
        
        self.alerts.append(alert)
        self.logger.warning(f"ALERT [{severity.upper()}] {title}: {message}")
        
        # Trigger notification
        self._send_notification(alert)
    
    def _send_notification(self, alert: Alert):
        """Send alert notification (placeholder for actual notification system)"""
        # This would integrate with your notification system
        # For now, just log the alert
        notification_data = {
            "alert_id": alert.alert_id,
            "severity": alert.severity,
            "title": alert.title,
            "message": alert.message,
            "source": alert.source,
            "timestamp": alert.timestamp.isoformat()
        }
        
        # In production, you might send to Slack, email, or other services
        self.logger.info(f"Notification sent: {json.dumps(notification_data)}")
    
    def _cleanup_old_metrics(self):
        """Remove old metrics to prevent memory bloat"""
        max_metrics = 100
        
        for metric_name, metric_data in self.metrics.items():
            while len(metric_data) > max_metrics:
                metric_data.popleft()
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current system metrics snapshot"""
        current_time = datetime.now()
        
        # Get latest values
        latest_metrics = {}
        for metric_name, metric_data in self.metrics.items():
            if metric_data:
                latest_metrics[metric_name] = metric_data[-1][1]
        
        # Calculate uptime
        uptime = current_time - self.start_time
        
        # Get recent averages
        recent_averages = {}
        for metric_name, metric_data in self.metrics.items():
            if metric_data and len(metric_data) >= 5:
                recent_values = [value for _, value in list(metric_data)[-5:]]
                recent_averages[f"{metric_name}_avg_5"] = statistics.mean(recent_values)
        
        return {
            "timestamp": current_time.isoformat(),
            "uptime_seconds": uptime.total_seconds(),
            "latest_metrics": latest_metrics,
            "recent_averages": recent_averages,
            "active_alerts": len([a for a in self.alerts if not a.resolved]),
            "total_alerts": len(self.alerts)
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall system health status"""
        # Determine health based on recent alerts and metrics
        critical_alerts = len([a for a in self.alerts[-10:] if a.severity == "critical" and not a.resolved])
        warning_alerts = len([a for a in self.alerts[-10:] if a.severity == "warning" and not a.resolved])
        
        if critical_alerts > 0:
            health_status = "critical"
            health_score = 0
        elif warning_alerts > 2:
            health_status = "warning"
            health_score = 50
        elif warning_alerts > 0:
            health_status = "degraded"
            health_score = 75
        else:
            health_status = "healthy"
            health_score = 100
        
        # Get recent performance metrics
        recent_metrics = {}
        if self.metrics['cpu_usage']:
            recent_cpu = [value for _, value in list(self.metrics['cpu_usage'])[-5:]]
            recent_metrics['avg_cpu_usage'] = statistics.mean(recent_cpu)
        
        if self.metrics['memory_usage']:
            recent_memory = [value for _, value in list(self.metrics['memory_usage'])[-5:]]
            recent_metrics['avg_memory_usage'] = statistics.mean(recent_memory)
        
        if self.metrics['response_times']:
            recent_times = [value for _, value in list(self.metrics['response_times'])[-10:]]
            recent_metrics['avg_response_time'] = statistics.mean(recent_times)
        
        return {
            "health_status": health_status,
            "health_score": health_score,
            "critical_alerts": critical_alerts,
            "warning_alerts": warning_alerts,
            "recent_performance": recent_metrics,
            "monitoring_active": self.monitoring,
            "last_check": datetime.now().isoformat()
        }
    
    def get_alerts(self, severity: str = None, resolved: bool = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get alerts with optional filtering"""
        filtered_alerts = self.alerts
        
        if severity:
            filtered_alerts = [a for a in filtered_alerts if a.severity == severity]
        
        if resolved is not None:
            filtered_alerts = [a for a in filtered_alerts if a.resolved == resolved]
        
        # Sort by timestamp (newest first) and limit
        filtered_alerts = sorted(filtered_alerts, key=lambda x: x.timestamp, reverse=True)[:limit]
        
        return [
            {
                "alert_id": alert.alert_id,
                "severity": alert.severity,
                "title": alert.title,
                "message": alert.message,
                "source": alert.source,
                "timestamp": alert.timestamp.isoformat(),
                "resolved": alert.resolved,
                "resolution_time": alert.resolution_time.isoformat() if alert.resolution_time else None
            }
            for alert in filtered_alerts
        ]
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Mark an alert as resolved"""
        for alert in self.alerts:
            if alert.alert_id == alert_id and not alert.resolved:
                alert.resolved = True
                alert.resolution_time = datetime.now()
                self.logger.info(f"Alert {alert_id} resolved")
                return True
        return False
    
    def get_performance_report(self, hours_back: int = 24) -> Dict[str, Any]:
        """Generate performance report for specified time period"""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        report = {
            "report_period_hours": hours_back,
            "generated_at": datetime.now().isoformat()
        }
        
        # Analyze CPU usage
        cpu_data = [(ts, val) for ts, val in self.metrics['cpu_usage'] if ts >= cutoff_time]
        if cpu_data:
            cpu_values = [val for _, val in cpu_data]
            report['cpu_stats'] = {
                "average": statistics.mean(cpu_values),
                "maximum": max(cpu_values),
                "minimum": min(cpu_values),
                "data_points": len(cpu_values)
            }
        
        # Analyze memory usage
        memory_data = [(ts, val) for ts, val in self.metrics['memory_usage'] if ts >= cutoff_time]
        if memory_data:
            memory_values = [val for _, val in memory_data]
            report['memory_stats'] = {
                "average": statistics.mean(memory_values),
                "maximum": max(memory_values),
                "minimum": min(memory_values),
                "data_points": len(memory_values)
            }
        
        # Analyze response times
        response_data = [(ts, val) for ts, val in self.metrics['response_times'] if ts >= cutoff_time]
        if response_data:
            response_values = [val for _, val in response_data]
            report['response_time_stats'] = {
                "average": statistics.mean(response_values),
                "maximum": max(response_values),
                "minimum": min(response_values),
                "median": statistics.median(response_values),
                "p95": sorted(response_values)[int(len(response_values) * 0.95)] if len(response_values) > 20 else max(response_values),
                "total_requests": len(response_values)
            }
        
        # Count alerts in period
        period_alerts = [a for a in self.alerts if a.timestamp >= cutoff_time]
        report['alerts_summary'] = {
            "total_alerts": len(period_alerts),
            "critical": len([a for a in period_alerts if a.severity == "critical"]),
            "warning": len([a for a in period_alerts if a.severity == "warning"]),
            "info": len([a for a in period_alerts if a.severity == "info"])
        }
        
        return report
    
    def export_metrics(self, filename: str, hours_back: int = 24) -> bool:
        """Export metrics to file"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours_back)
            
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "period_hours": hours_back,
                "metrics": {}
            }
            
            # Export all metrics within time period
            for metric_name, metric_data in self.metrics.items():
                period_data = [(ts.isoformat(), val) for ts, val in metric_data if ts >= cutoff_time]
                export_data["metrics"][metric_name] = period_data
            
            # Export alerts
            period_alerts = [a for a in self.alerts if a.timestamp >= cutoff_time]
            export_data["alerts"] = [
                {
                    "alert_id": alert.alert_id,
                    "severity": alert.severity,
                    "title": alert.title,
                    "message": alert.message,
                    "source": alert.source,
                    "timestamp": alert.timestamp.isoformat(),
                    "resolved": alert.resolved
                }
                for alert in period_alerts
            ]
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export metrics: {e}")
            return False

class PerformanceTracker:
    """
    Lightweight performance tracking decorator and context manager
    """
    
    def __init__(self, monitor: SystemMonitor):
        self.monitor = monitor
    
    def track_api_call(self, endpoint: str):
        """Decorator to track API call performance"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = time.time()
                status_code = 200
                
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    status_code = 500
                    raise
                finally:
                    response_time = time.time() - start_time
                    self.monitor.record_api_request(endpoint, response_time, status_code)
            
            return wrapper
        return decorator
    
    def track_analysis(self):
        """Context manager to track analysis performance"""
        return AnalysisTracker(self.monitor)

class AnalysisTracker:
    """Context manager for tracking analysis performance"""
    
    def __init__(self, monitor: SystemMonitor):
        self.monitor = monitor
        self.start_time = None
        self.comment_count = 0
        self.success = True
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            analysis_time = time.time() - self.start_time
            self.success = exc_type is None
            self.monitor.record_analysis_metrics(analysis_time, self.comment_count, self.success)
    
    def set_comment_count(self, count: int):
        """Set the number of comments being processed"""
        self.comment_count = count
