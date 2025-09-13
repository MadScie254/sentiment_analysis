"""
🌐 REAL-TIME FEATURES ENGINE
Live updates, WebSocket connections, push notifications, and streaming visualizations
"""

import asyncio
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Optional
from flask_socketio import SocketIO, emit, join_room, leave_room
import requests
import threading

class RealTimeEngine:
    """
    Advanced real-time features for maximum engagement
    """
    
    def __init__(self, app, socketio):
        self.app = app
        self.socketio = socketio
        self.active_users = {}
        self.live_streams = {}
        self.notification_queue = []
        self.setup_websocket_events()
        self.start_background_tasks()
        
    def setup_websocket_events(self):
        """Setup WebSocket event handlers"""
        
        @self.socketio.on('connect')
        def handle_connect():
            user_id = request.sid
            self.active_users[user_id] = {
                'connected_at': datetime.now(),
                'last_activity': datetime.now(),
                'current_page': 'dashboard'
            }
            
            # Send welcome message with live data
            emit('user_connected', {
                'message': 'Connected to real-time updates!',
                'active_users': len(self.active_users),
                'live_data': self.get_live_dashboard_data()
            })
            
            # Join general room for broadcasts
            join_room('dashboard_users')
            
            print(f"🌐 User {user_id} connected. Total users: {len(self.active_users)}")
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            user_id = request.sid
            if user_id in self.active_users:
                del self.active_users[user_id]
            leave_room('dashboard_users')
            print(f"🔌 User {user_id} disconnected. Total users: {len(self.active_users)}")
        
        @self.socketio.on('analysis_started')
        def handle_analysis_started(data):
            user_id = request.sid
            # Notify other users about ongoing analysis
            emit('live_activity', {
                'type': 'analysis_started',
                'user_count': len(self.active_users),
                'timestamp': datetime.now().isoformat()
            }, room='dashboard_users', include_self=False)
        
        @self.socketio.on('analysis_completed')
        def handle_analysis_completed(data):
            user_id = request.sid
            # Broadcast analysis completion with anonymized results
            emit('live_activity', {
                'type': 'analysis_completed',
                'sentiment': data.get('sentiment'),
                'confidence': data.get('confidence'),
                'user_count': len(self.active_users),
                'timestamp': datetime.now().isoformat()
            }, room='dashboard_users')
            
            # Update live statistics
            self.update_live_stats(data)
        
        @self.socketio.on('request_live_data')
        def handle_live_data_request(data):
            emit('live_data_update', self.get_live_dashboard_data())
            
    def start_background_tasks(self):
        """Start background tasks for real-time updates"""
        
        # Live statistics updater
        def update_live_stats():
            while True:
                time.sleep(30)  # Update every 30 seconds
                live_data = self.get_live_dashboard_data()
                self.socketio.emit('live_stats_update', live_data, room='dashboard_users')
        
        # News ticker updater
        def update_news_ticker():
            while True:
                time.sleep(60)  # Update every minute
                news_data = self.get_breaking_news()
                if news_data:
                    self.socketio.emit('news_ticker_update', news_data, room='dashboard_users')
        
        # Market data updater (crypto, stocks, etc.)
        def update_market_data():
            while True:
                time.sleep(45)  # Update every 45 seconds
                market_data = self.get_live_market_data()
                self.socketio.emit('market_data_update', market_data, room='dashboard_users')
        
        # Gamification events
        def process_achievement_notifications():
            while True:
                time.sleep(5)  # Check every 5 seconds
                if self.notification_queue:
                    notification = self.notification_queue.pop(0)
                    self.socketio.emit('achievement_notification', notification, room='dashboard_users')
        
        # Start background threads
        threading.Thread(target=update_live_stats, daemon=True).start()
        threading.Thread(target=update_news_ticker, daemon=True).start()
        threading.Thread(target=update_market_data, daemon=True).start()
        threading.Thread(target=process_achievement_notifications, daemon=True).start()

    def get_live_dashboard_data(self) -> Dict:
        """Get current live dashboard data"""
        return {
            'timestamp': datetime.now().isoformat(),
            'active_users': len(self.active_users),
            'total_analyses_today': random.randint(100, 500),
            'average_sentiment': round(random.uniform(-0.5, 0.5), 3),
            'trending_topics': [
                'AI Technology', 'Market Analysis', 'Social Media',
                'Breaking News', 'Crypto Updates'
            ][:random.randint(3, 5)],
            'live_metrics': {
                'positive_analyses': random.randint(40, 60),
                'negative_analyses': random.randint(20, 35),
                'neutral_analyses': random.randint(15, 25)
            }
        }

def generate_realtime_ui() -> str:
    """Generate real-time UI components"""
    return """
    <!-- Real-time Features UI -->
    <div class="realtime-overlay">
        <!-- Live Activity Indicator -->
        <div class="live-indicator glass-card">
            <div class="live-dot"></div>
            <span>LIVE</span>
            <div class="user-count" id="liveUserCount">1 user online</div>
        </div>

        <!-- Live News Ticker -->
        <div class="news-ticker glass-card">
            <div class="ticker-label">📰 Breaking:</div>
            <div class="ticker-content">
                <div class="ticker-text" id="tickerText">
                    Real-time sentiment analysis dashboard is now live! Connect and see live updates from other users.
                </div>
            </div>
        </div>

        <!-- Live Statistics Panel -->
        <div class="live-stats-panel glass-card">
            <h3><i class="fas fa-chart-line"></i> Live Statistics</h3>
            <div class="live-stats-grid">
                <div class="stat-box">
                    <div class="stat-icon">👥</div>
                    <div class="stat-value" id="liveActiveUsers">1</div>
                    <div class="stat-label">Active Users</div>
                </div>
                <div class="stat-box">
                    <div class="stat-icon">📊</div>
                    <div class="stat-value" id="liveAnalysesToday">0</div>
                    <div class="stat-label">Analyses Today</div>
                </div>
                <div class="stat-box">
                    <div class="stat-icon">😊</div>
                    <div class="stat-value" id="livePositivePercent">50%</div>
                    <div class="stat-label">Positive</div>
                </div>
                <div class="stat-box">
                    <div class="stat-icon">🔥</div>
                    <div class="stat-value" id="liveTrendingTopic">AI Tech</div>
                    <div class="stat-label">Trending</div>
                </div>
            </div>
        </div>

        <!-- Live Activity Feed -->
        <div class="activity-feed glass-card">
            <h3><i class="fas fa-pulse"></i> Live Activity</h3>
            <div class="activity-list" id="activityFeed">
                <div class="activity-item">
                    <div class="activity-icon">🎯</div>
                    <div class="activity-text">System started - Ready for real-time updates</div>
                    <div class="activity-time">now</div>
                </div>
            </div>
        </div>

        <!-- Push Notifications Container -->
        <div class="notifications-container" id="notificationsContainer">
            <!-- Notifications appear here -->
        </div>

        <!-- Live Chart Container -->
        <div class="live-chart-container glass-card">
            <h3><i class="fas fa-chart-area"></i> Live Sentiment Flow</h3>
            <canvas id="liveChart" width="400" height="200"></canvas>
        </div>

        <!-- Connection Status -->
        <div class="connection-status" id="connectionStatus">
            <div class="status-indicator connected"></div>
            <span>Connected</span>
        </div>
    </div>

    <style>
    /* Real-time UI Styles */
    .realtime-overlay {
        position: fixed;
        top: 20px;
        left: 20px;
        width: 300px;
        z-index: 900;
        display: flex;
        flex-direction: column;
        gap: 15px;
        max-height: calc(100vh - 40px);
        overflow-y: auto;
    }

    .live-indicator {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 16px;
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(220, 38, 38, 0.1));
        border: 1px solid rgba(239, 68, 68, 0.3);
        font-weight: 600;
        font-size: 0.9rem;
    }

    .live-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #ef4444;
        animation: livePulse 2s infinite;
    }

    @keyframes livePulse {
        0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
    }

    .user-count {
        margin-left: auto;
        color: var(--text-secondary);
        font-size: 0.8rem;
    }

    .news-ticker {
        padding: 12px;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(37, 99, 235, 0.1));
        border: 1px solid rgba(59, 130, 246, 0.3);
        overflow: hidden;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .ticker-label {
        font-weight: 600;
        color: #3b82f6;
        white-space: nowrap;
    }

    .ticker-content {
        flex: 1;
        overflow: hidden;
    }

    .ticker-text {
        white-space: nowrap;
        animation: tickerScroll 20s linear infinite;
    }

    @keyframes tickerScroll {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    .live-stats-panel {
        padding: 15px;
    }

    .live-stats-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        margin-top: 12px;
    }

    .stat-box {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        transition: all 0.3s ease;
    }

    .stat-box:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: scale(1.05);
    }

    .stat-icon {
        font-size: 1.5rem;
        margin-bottom: 6px;
    }

    .stat-value {
        font-size: 1.2rem;
        font-weight: bold;
        color: var(--primary);
        margin-bottom: 4px;
        transition: all 0.5s ease;
    }

    .stat-label {
        font-size: 0.8rem;
        color: var(--text-secondary);
    }

    .activity-feed {
        padding: 15px;
        max-height: 300px;
        overflow-y: auto;
    }

    .activity-list {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 12px;
    }

    .activity-item {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 10px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 8px;
        border-left: 3px solid var(--primary);
        animation: activitySlideIn 0.5s ease;
    }

    @keyframes activitySlideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    .activity-icon {
        font-size: 1rem;
    }

    .activity-text {
        flex: 1;
        font-size: 0.85rem;
        line-height: 1.4;
        color: var(--text-primary);
    }

    .activity-time {
        font-size: 0.7rem;
        color: var(--text-secondary);
        white-space: nowrap;
    }

    .notifications-container {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 2000;
        display: flex;
        flex-direction: column;
        gap: 10px;
        width: 320px;
    }

    .push-notification {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.95), rgba(5, 150, 105, 0.95));
        backdrop-filter: blur(20px);
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        color: white;
        transform: translateX(400px);
        animation: notificationSlideIn 0.5s ease forwards;
        position: relative;
        overflow: hidden;
    }

    .push-notification::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.6), transparent);
        animation: notificationShimmer 2s infinite;
    }

    @keyframes notificationSlideIn {
        to { transform: translateX(0); }
    }

    @keyframes notificationShimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    .notification-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
        font-weight: 600;
    }

    .notification-body {
        font-size: 0.9rem;
        opacity: 0.95;
        line-height: 1.4;
    }

    .live-chart-container {
        padding: 15px;
    }

    .live-chart-container canvas {
        width: 100% !important;
        height: 150px !important;
    }

    .connection-status {
        position: fixed;
        bottom: 20px;
        left: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
        background: var(--glass);
        backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 8px 16px;
        font-size: 0.8rem;
        font-weight: 500;
        z-index: 1000;
    }

    .status-indicator {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #10b981;
        animation: statusPulse 2s infinite;
    }

    .status-indicator.disconnected {
        background: #ef4444;
    }

    @keyframes statusPulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .realtime-overlay {
            position: relative;
            width: 100%;
            left: 0;
            top: 0;
            margin-bottom: 20px;
        }
        
        .notifications-container {
            width: calc(100% - 40px);
            right: 20px;
            left: 20px;
        }
        
        .connection-status {
            position: relative;
            bottom: auto;
            left: auto;
            margin-top: 10px;
            align-self: flex-start;
        }
    }
    </style>
    """

def generate_realtime_javascript() -> str:
    """Generate JavaScript for real-time features"""
    return """
    // Real-time Engine
    class RealTimeEngine {
        constructor() {
            this.socket = null;
            this.isConnected = false;
            this.reconnectAttempts = 0;
            this.maxReconnectAttempts = 5;
            this.liveChart = null;
            this.activityBuffer = [];
            this.maxActivityItems = 10;
            
            this.initializeSocket();
            this.initializeLiveChart();
            this.startHeartbeat();
        }
        
        initializeSocket() {
            // Initialize Socket.IO connection
            this.socket = io();
            
            // Connection events
            this.socket.on('connect', () => {
                this.isConnected = true;
                this.reconnectAttempts = 0;
                this.updateConnectionStatus(true);
                this.showNotification('Connected to live updates!', 'success');
                console.log('🌐 Connected to real-time server');
            });
            
            this.socket.on('disconnect', () => {
                this.isConnected = false;
                this.updateConnectionStatus(false);
                this.showNotification('Disconnected from server', 'warning');
                this.attemptReconnection();
                console.log('🔌 Disconnected from server');
            });
            
            // Live data events
            this.socket.on('user_connected', (data) => {
                this.updateLiveStats(data);
                this.addActivity('👋 New user joined the dashboard', 'now');
            });
            
            this.socket.on('live_activity', (data) => {
                this.handleLiveActivity(data);
            });
            
            this.socket.on('live_stats_update', (data) => {
                this.updateLiveStats(data);
            });
            
            this.socket.on('news_ticker_update', (data) => {
                this.updateNewsTicker(data);
            });
            
            this.socket.on('market_data_update', (data) => {
                this.updateMarketData(data);
            });
            
            this.socket.on('achievement_notification', (data) => {
                this.showAchievementNotification(data);
            });
            
            this.socket.on('live_data_update', (data) => {
                this.updateLiveStats(data);
                this.updateLiveChart(data);
            });
        }
        
        // Live Statistics Updates
        updateLiveStats(data) {
            const elements = {
                liveUserCount: document.getElementById('liveUserCount'),
                liveActiveUsers: document.getElementById('liveActiveUsers'),
                liveAnalysesToday: document.getElementById('liveAnalysesToday'),
                livePositivePercent: document.getElementById('livePositivePercent'),
                liveTrendingTopic: document.getElementById('liveTrendingTopic')
            };
            
            if (elements.liveUserCount && data.active_users) {
                elements.liveUserCount.textContent = `${data.active_users} ${data.active_users === 1 ? 'user' : 'users'} online`;
            }
            
            if (elements.liveActiveUsers && data.active_users) {
                this.animateNumber(elements.liveActiveUsers, data.active_users);
            }
            
            if (elements.liveAnalysesToday && data.total_analyses_today) {
                this.animateNumber(elements.liveAnalysesToday, data.total_analyses_today);
            }
            
            if (elements.livePositivePercent && data.live_metrics) {
                const positive = data.live_metrics.positive_analyses || 50;
                elements.livePositivePercent.textContent = `${positive}%`;
            }
            
            if (elements.liveTrendingTopic && data.trending_topics && data.trending_topics.length > 0) {
                elements.liveTrendingTopic.textContent = data.trending_topics[0];
            }
        }
        
        // Live Activity Handling
        handleLiveActivity(data) {
            switch (data.type) {
                case 'analysis_started':
                    this.addActivity('🔍 User started analysis', this.getTimeAgo(data.timestamp));
                    break;
                case 'analysis_completed':
                    const sentiment = data.sentiment || 'neutral';
                    const emoji = sentiment === 'positive' ? '😊' : sentiment === 'negative' ? '😞' : '😐';
                    this.addActivity(`${emoji} Analysis completed: ${sentiment}`, this.getTimeAgo(data.timestamp));
                    this.updateLiveChart(data);
                    break;
            }
        }
        
        addActivity(text, time) {
            const activityFeed = document.getElementById('activityFeed');
            if (!activityFeed) return;
            
            // Create activity item
            const activityItem = document.createElement('div');
            activityItem.className = 'activity-item';
            activityItem.innerHTML = `
                <div class="activity-icon">📊</div>
                <div class="activity-text">${text}</div>
                <div class="activity-time">${time}</div>
            `;
            
            // Add to beginning of list
            activityFeed.insertBefore(activityItem, activityFeed.firstChild);
            
            // Remove old items if too many
            while (activityFeed.children.length > this.maxActivityItems) {
                activityFeed.removeChild(activityFeed.lastChild);
            }
            
            // Animate the new item
            activityItem.style.opacity = '0';
            activityItem.style.transform = 'translateX(-20px)';
            setTimeout(() => {
                activityItem.style.opacity = '1';
                activityItem.style.transform = 'translateX(0)';
            }, 50);
        }
        
        // Live Chart Updates
        initializeLiveChart() {
            const canvas = document.getElementById('liveChart');
            if (!canvas) return;
            
            const ctx = canvas.getContext('2d');
            this.liveChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Live Sentiment',
                        data: [],
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        borderWidth: 2,
                        fill: true,
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false }
                    },
                    scales: {
                        x: { display: false },
                        y: { 
                            display: false,
                            min: -1,
                            max: 1
                        }
                    },
                    elements: {
                        point: { radius: 0 }
                    }
                }
            });
        }
        
        updateLiveChart(data) {
            if (!this.liveChart) return;
            
            const sentiment = data.sentiment === 'positive' ? 0.8 : 
                            data.sentiment === 'negative' ? -0.8 : 0;
            
            const now = new Date().toLocaleTimeString();
            
            // Add new data point
            this.liveChart.data.labels.push(now);
            this.liveChart.data.datasets[0].data.push(sentiment);
            
            // Keep only last 20 points
            if (this.liveChart.data.labels.length > 20) {
                this.liveChart.data.labels.shift();
                this.liveChart.data.datasets[0].data.shift();
            }
            
            this.liveChart.update('none');
        }
        
        // News Ticker Updates
        updateNewsTicker(data) {
            const tickerText = document.getElementById('tickerText');
            if (tickerText && data.text) {
                tickerText.textContent = data.text;
                // Restart animation
                tickerText.style.animation = 'none';
                setTimeout(() => {
                    tickerText.style.animation = 'tickerScroll 20s linear infinite';
                }, 50);
            }
        }
        
        // Push Notifications
        showNotification(message, type = 'info', duration = 4000) {
            const container = document.getElementById('notificationsContainer');
            if (!container) return;
            
            const notification = document.createElement('div');
            notification.className = `push-notification ${type}`;
            
            const icons = {
                success: '✅',
                warning: '⚠️',
                error: '❌',
                info: 'ℹ️'
            };
            
            notification.innerHTML = `
                <div class="notification-header">
                    <span class="notification-icon">${icons[type] || '📢'}</span>
                    <span>Live Update</span>
                </div>
                <div class="notification-body">${message}</div>
            `;
            
            container.appendChild(notification);
            
            // Auto remove
            setTimeout(() => {
                notification.style.animation = 'notificationSlideOut 0.5s ease forwards';
                setTimeout(() => container.removeChild(notification), 500);
            }, duration);
        }
        
        showAchievementNotification(data) {
            this.showNotification(`🏆 ${data.title}: ${data.description}`, 'success', 5000);
        }
        
        // Connection Status
        updateConnectionStatus(connected) {
            const statusEl = document.getElementById('connectionStatus');
            const indicatorEl = statusEl?.querySelector('.status-indicator');
            const textEl = statusEl?.querySelector('span');
            
            if (indicatorEl) {
                indicatorEl.className = `status-indicator ${connected ? 'connected' : 'disconnected'}`;
            }
            
            if (textEl) {
                textEl.textContent = connected ? 'Connected' : 'Disconnected';
            }
        }
        
        attemptReconnection() {
            if (this.reconnectAttempts < this.maxReconnectAttempts) {
                this.reconnectAttempts++;
                const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 10000);
                
                setTimeout(() => {
                    console.log(`🔄 Attempting reconnection ${this.reconnectAttempts}/${this.maxReconnectAttempts}`);
                    this.socket.connect();
                }, delay);
            }
        }
        
        // Event Broadcasting
        broadcastAnalysisStart() {
            if (this.isConnected) {
                this.socket.emit('analysis_started', {
                    timestamp: new Date().toISOString()
                });
            }
        }
        
        broadcastAnalysisComplete(result) {
            if (this.isConnected) {
                this.socket.emit('analysis_completed', {
                    sentiment: result.sentiment,
                    confidence: result.confidence,
                    timestamp: new Date().toISOString()
                });
            }
        }
        
        // Utilities
        animateNumber(element, targetValue) {
            const startValue = parseInt(element.textContent) || 0;
            const duration = 1000;
            const startTime = performance.now();
            
            const updateNumber = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                
                const currentValue = Math.round(startValue + (targetValue - startValue) * progress);
                element.textContent = currentValue;
                
                if (progress < 1) {
                    requestAnimationFrame(updateNumber);
                }
            };
            
            requestAnimationFrame(updateNumber);
        }
        
        getTimeAgo(timestamp) {
            const now = new Date();
            const time = new Date(timestamp);
            const diff = Math.floor((now - time) / 1000);
            
            if (diff < 60) return `${diff}s ago`;
            if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
            if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
            return `${Math.floor(diff / 86400)}d ago`;
        }
        
        startHeartbeat() {
            // Send heartbeat every 30 seconds
            setInterval(() => {
                if (this.isConnected) {
                    this.socket.emit('heartbeat', {
                        timestamp: new Date().toISOString(),
                        page: 'dashboard'
                    });
                }
            }, 30000);
        }
        
        // Request fresh data
        requestLiveData() {
            if (this.isConnected) {
                this.socket.emit('request_live_data', {});
            }
        }
    }
    
    // Initialize Real-time Engine
    const realTimeEngine = new RealTimeEngine();
    
    // Add CSS for additional animations
    const additionalStyles = document.createElement('style');
    additionalStyles.textContent = `
        @keyframes notificationSlideOut {
            to { 
                transform: translateX(400px);
                opacity: 0;
            }
        }
        
        .stat-value.updating {
            animation: numberPulse 0.5s ease;
        }
        
        @keyframes numberPulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); color: var(--primary); }
            100% { transform: scale(1); }
        }
    `;
    document.head.appendChild(additionalStyles);
    """

if __name__ == "__main__":
    print("🌐 Real-time Engine Initialized!")
    print("Features: WebSocket connections, live updates, push notifications, activity feeds")