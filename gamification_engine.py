"""
🎮 ADDICTIVE UI/UX GAMIFICATION SYSTEM
Making the sentiment analysis dashboard irresistibly engaging
"""

import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class GamificationEngine:
    """
    Advanced gamification system to make the dashboard addictive
    """
    
    def __init__(self):
        self.achievements = self._init_achievements()
        self.streak_system = StreakSystem()
        self.points_system = PointsSystem()
        self.challenges = ChallengeSystem()
        self.social_features = SocialFeatures()
        
    def _init_achievements(self) -> List[Dict]:
        """Initialize achievement system"""
        return [
            # Analysis Achievements
            {"id": "first_analysis", "name": "First Steps", "desc": "Analyze your first text", "points": 10, "icon": "🎯", "unlocked": False},
            {"id": "analysis_novice", "name": "Novice Analyzer", "desc": "Complete 10 analyses", "points": 50, "icon": "📊", "unlocked": False},
            {"id": "analysis_expert", "name": "Analysis Expert", "desc": "Complete 100 analyses", "points": 200, "icon": "🧠", "unlocked": False},
            {"id": "analysis_master", "name": "Sentiment Master", "desc": "Complete 1000 analyses", "points": 500, "icon": "🏆", "unlocked": False},
            
            # Accuracy Achievements
            {"id": "accuracy_75", "name": "Sharp Eye", "desc": "Achieve 75% accuracy", "points": 100, "icon": "👁️", "unlocked": False},
            {"id": "accuracy_90", "name": "Perfect Vision", "desc": "Achieve 90% accuracy", "points": 250, "icon": "🎯", "unlocked": False},
            
            # Streak Achievements
            {"id": "streak_7", "name": "Week Warrior", "desc": "Maintain 7-day streak", "points": 150, "icon": "🔥", "unlocked": False},
            {"id": "streak_30", "name": "Monthly Master", "desc": "Maintain 30-day streak", "points": 500, "icon": "🌟", "unlocked": False},
            
            # Feature Exploration
            {"id": "api_explorer", "name": "API Explorer", "desc": "Try all API endpoints", "points": 300, "icon": "🌍", "unlocked": False},
            {"id": "visualization_guru", "name": "Viz Guru", "desc": "Create 50 visualizations", "points": 400, "icon": "📈", "unlocked": False},
            
            # Social Achievements
            {"id": "first_share", "name": "Social Butterfly", "desc": "Share your first analysis", "points": 75, "icon": "🦋", "unlocked": False},
            {"id": "collaboration_king", "name": "Team Player", "desc": "Collaborate on 10 analyses", "points": 200, "icon": "🤝", "unlocked": False},
            
            # Time-based Achievements
            {"id": "night_owl", "name": "Night Owl", "desc": "Analyze after midnight", "points": 50, "icon": "🦉", "unlocked": False},
            {"id": "early_bird", "name": "Early Bird", "desc": "Analyze before 6 AM", "points": 50, "icon": "🐦", "unlocked": False},
            
            # Special Achievements
            {"id": "emoji_master", "name": "Emoji Master", "desc": "Analyze 100 texts with emojis", "points": 150, "icon": "😎", "unlocked": False},
            {"id": "multilingual", "name": "Polyglot", "desc": "Analyze text in 5 languages", "points": 300, "icon": "🌐", "unlocked": False},
        ]

class StreakSystem:
    """Daily streak system to encourage regular usage"""
    
    def __init__(self):
        self.current_streak = 0
        self.best_streak = 0
        self.last_activity = None
        self.streak_rewards = {
            7: {"points": 100, "badge": "🔥", "title": "Week Warrior"},
            14: {"points": 250, "badge": "⚡", "title": "Fortnight Fighter"},
            30: {"points": 500, "badge": "💎", "title": "Monthly Master"},
            60: {"points": 1000, "badge": "👑", "title": "Streak King"},
            100: {"points": 2000, "badge": "🌟", "title": "Centurion"}
        }

class PointsSystem:
    """Comprehensive points and leveling system"""
    
    def __init__(self):
        self.total_points = 0
        self.level = 1
        self.points_to_next_level = 100
        self.level_thresholds = [100, 250, 500, 1000, 2000, 4000, 8000, 15000, 30000, 50000]
        
    def add_points(self, points: int, reason: str) -> Dict:
        """Add points and check for level up"""
        old_level = self.level
        self.total_points += points
        
        # Check for level up
        new_level = self._calculate_level()
        level_up = new_level > old_level
        
        if level_up:
            self.level = new_level
            
        return {
            "points_added": points,
            "total_points": self.total_points,
            "level": self.level,
            "level_up": level_up,
            "reason": reason,
            "points_to_next": self._points_to_next_level()
        }
    
    def _calculate_level(self) -> int:
        """Calculate current level based on points"""
        for i, threshold in enumerate(self.level_thresholds):
            if self.total_points < threshold:
                return i + 1
        return len(self.level_thresholds) + 1

class ChallengeSystem:
    """Daily and weekly challenges"""
    
    def __init__(self):
        self.daily_challenges = self._generate_daily_challenges()
        self.weekly_challenges = self._generate_weekly_challenges()
        
    def _generate_daily_challenges(self) -> List[Dict]:
        """Generate daily challenges"""
        challenges = [
            {"id": "daily_10", "name": "Quick Fire", "desc": "Analyze 10 texts", "target": 10, "reward": 50, "type": "count"},
            {"id": "daily_positive", "name": "Stay Positive", "desc": "Find 5 positive sentiments", "target": 5, "reward": 30, "type": "sentiment"},
            {"id": "daily_api", "name": "Explorer", "desc": "Try 3 different APIs", "target": 3, "reward": 40, "type": "api_usage"},
            {"id": "daily_accuracy", "name": "Precision", "desc": "Achieve 80% accuracy", "target": 80, "reward": 60, "type": "accuracy"},
        ]
        return random.sample(challenges, 2)  # 2 daily challenges

class SocialFeatures:
    """Social engagement features"""
    
    def __init__(self):
        self.leaderboards = {
            "daily": [],
            "weekly": [],
            "monthly": [],
            "all_time": []
        }
        self.sharing_stats = {
            "analyses_shared": 0,
            "likes_received": 0,
            "comments_made": 0
        }

def generate_gamification_ui() -> str:
    """Generate addictive gamification UI components"""
    return """
    <!-- Gamification UI Components -->
    <div class="gamification-overlay">
        <!-- Points & Level Display -->
        <div class="player-stats glass-card">
            <div class="level-display">
                <div class="level-circle">
                    <span class="level-number" id="playerLevel">1</span>
                </div>
                <div class="level-info">
                    <div class="player-name">Sentiment Explorer</div>
                    <div class="xp-bar">
                        <div class="xp-fill" id="xpBar" style="width: 0%"></div>
                        <span class="xp-text" id="xpText">0 / 100 XP</span>
                    </div>
                </div>
            </div>
            
            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value" id="totalPoints">0</div>
                    <div class="stat-label">Points</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="streakCount">0</div>
                    <div class="stat-label">Streak 🔥</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value" id="analysisCount">0</div>
                    <div class="stat-label">Analyses</div>
                </div>
            </div>
        </div>

        <!-- Achievement Notifications -->
        <div id="achievementNotification" class="achievement-popup hidden">
            <div class="achievement-content">
                <div class="achievement-icon">🏆</div>
                <div class="achievement-text">
                    <div class="achievement-title">Achievement Unlocked!</div>
                    <div class="achievement-desc">First Analysis Complete</div>
                </div>
                <div class="achievement-points">+10 XP</div>
            </div>
        </div>

        <!-- Daily Challenges -->
        <div class="challenges-panel glass-card">
            <h3><i class="fas fa-trophy"></i> Daily Challenges</h3>
            <div class="challenges-list" id="dailyChallenges">
                <!-- Populated dynamically -->
            </div>
        </div>

        <!-- Recent Achievements -->
        <div class="achievements-panel glass-card">
            <h3><i class="fas fa-star"></i> Achievements</h3>
            <div class="achievements-grid" id="achievementsGrid">
                <!-- Populated dynamically -->
            </div>
        </div>

        <!-- Leaderboard -->
        <div class="leaderboard-panel glass-card">
            <h3><i class="fas fa-crown"></i> Leaderboard</h3>
            <div class="leaderboard-tabs">
                <button class="tab-btn active" data-period="daily">Daily</button>
                <button class="tab-btn" data-period="weekly">Weekly</button>
                <button class="tab-btn" data-period="all_time">All Time</button>
            </div>
            <div class="leaderboard-list" id="leaderboardList">
                <!-- Populated dynamically -->
            </div>
        </div>
    </div>

    <style>
    /* Gamification Styles */
    .gamification-overlay {
        position: fixed;
        top: 80px;
        right: 20px;
        width: 300px;
        z-index: 1000;
        display: flex;
        flex-direction: column;
        gap: 15px;
        max-height: calc(100vh - 100px);
        overflow-y: auto;
    }

    .player-stats {
        padding: 20px;
        background: linear-gradient(135deg, rgba(147, 51, 234, 0.1), rgba(79, 70, 229, 0.1));
        border: 1px solid rgba(147, 51, 234, 0.3);
    }

    .level-display {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 15px;
    }

    .level-circle {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #9333ea, #4f46e5);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 1.2rem;
        color: white;
        position: relative;
        overflow: hidden;
    }

    .level-circle::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: rotate 2s linear infinite;
    }

    @keyframes rotate {
        to { transform: rotate(360deg); }
    }

    .player-name {
        font-weight: 600;
        font-size: 1.1rem;
        color: var(--text-primary);
    }

    .xp-bar {
        position: relative;
        background: rgba(255, 255, 255, 0.1);
        height: 8px;
        border-radius: 4px;
        margin-top: 5px;
        overflow: hidden;
    }

    .xp-fill {
        height: 100%;
        background: linear-gradient(90deg, #9333ea, #4f46e5);
        border-radius: 4px;
        transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }

    .xp-fill::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        animation: shimmer 2s infinite;
    }

    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    .xp-text {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 0.7rem;
        font-weight: 500;
        color: var(--text-primary);
    }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
        margin-top: 15px;
    }

    .stat-item {
        text-align: center;
        padding: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        transition: all 0.3s ease;
    }

    .stat-item:hover {
        transform: scale(1.05);
        background: rgba(255, 255, 255, 0.1);
    }

    .stat-value {
        font-size: 1.4rem;
        font-weight: bold;
        color: var(--primary);
        margin-bottom: 4px;
    }

    .stat-label {
        font-size: 0.8rem;
        color: var(--text-secondary);
    }

    /* Achievement Popup */
    .achievement-popup {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) scale(0);
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.95), rgba(22, 163, 74, 0.95));
        backdrop-filter: blur(20px);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        z-index: 2000;
        transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    .achievement-popup.show {
        transform: translate(-50%, -50%) scale(1);
        animation: celebrationPulse 0.6s ease;
    }

    @keyframes celebrationPulse {
        0% { transform: translate(-50%, -50%) scale(0); }
        50% { transform: translate(-50%, -50%) scale(1.1); }
        100% { transform: translate(-50%, -50%) scale(1); }
    }

    .achievement-content {
        display: flex;
        align-items: center;
        gap: 15px;
        color: white;
    }

    .achievement-icon {
        font-size: 3rem;
        animation: bounce 1s infinite alternate;
    }

    @keyframes bounce {
        from { transform: translateY(0); }
        to { transform: translateY(-10px); }
    }

    .achievement-title {
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .achievement-desc {
        font-size: 1rem;
        opacity: 0.9;
    }

    .achievement-points {
        font-size: 1.2rem;
        font-weight: bold;
        background: rgba(255, 255, 255, 0.2);
        padding: 8px 12px;
        border-radius: 8px;
    }

    /* Challenges Panel */
    .challenges-panel {
        padding: 15px;
    }

    .challenges-list {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .challenge-item {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 12px;
        border-left: 4px solid var(--primary);
        transition: all 0.3s ease;
    }

    .challenge-item:hover {
        background: rgba(255, 255, 255, 0.1);
        transform: translateX(4px);
    }

    .challenge-name {
        font-weight: 600;
        margin-bottom: 4px;
        color: var(--text-primary);
    }

    .challenge-desc {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-bottom: 8px;
    }

    .challenge-progress {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.8rem;
    }

    .progress-bar-mini {
        flex: 1;
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
        margin: 0 8px;
        overflow: hidden;
    }

    .progress-fill-mini {
        height: 100%;
        background: var(--primary);
        border-radius: 2px;
        transition: width 0.3s ease;
    }

    /* Achievements Panel */
    .achievements-panel {
        padding: 15px;
    }

    .achievements-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 8px;
    }

    .achievement-badge {
        aspect-ratio: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
    }

    .achievement-badge.unlocked {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.2), rgba(22, 163, 74, 0.2));
        border: 1px solid rgba(34, 197, 94, 0.5);
    }

    .achievement-badge.locked {
        opacity: 0.3;
        filter: grayscale(1);
    }

    .achievement-badge:hover:not(.locked) {
        transform: scale(1.1);
        background: rgba(255, 255, 255, 0.1);
    }

    .badge-icon {
        font-size: 1.2rem;
        margin-bottom: 4px;
    }

    .badge-name {
        font-size: 0.7rem;
        text-align: center;
        line-height: 1.2;
    }

    /* Leaderboard Panel */
    .leaderboard-panel {
        padding: 15px;
    }

    .leaderboard-tabs {
        display: flex;
        gap: 8px;
        margin-bottom: 15px;
    }

    .leaderboard-tabs .tab-btn {
        flex: 1;
        padding: 8px 12px;
        background: rgba(255, 255, 255, 0.05);
        border: none;
        border-radius: 6px;
        color: var(--text-secondary);
        font-size: 0.8rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .leaderboard-tabs .tab-btn.active {
        background: var(--primary);
        color: white;
    }

    .leaderboard-list {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .leaderboard-item {
        display: flex;
        align-items: center;
        padding: 10px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        transition: all 0.3s ease;
    }

    .leaderboard-item:hover {
        background: rgba(255, 255, 255, 0.1);
    }

    .rank-number {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        background: var(--primary);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        margin-right: 12px;
    }

    .player-info {
        flex: 1;
    }

    .player-name-leader {
        font-weight: 600;
        font-size: 0.9rem;
    }

    .player-points {
        font-size: 0.8rem;
        color: var(--text-secondary);
    }

    /* Responsive */
    @media (max-width: 1200px) {
        .gamification-overlay {
            position: relative;
            width: 100%;
            top: 0;
            right: 0;
            max-height: none;
            margin-top: 20px;
        }
    }
    </style>
    """

def generate_gamification_javascript() -> str:
    """Generate JavaScript for gamification features"""
    return """
    // Gamification Engine
    class GameEngine {
        constructor() {
            this.player = {
                level: 1,
                points: 0,
                analyses: 0,
                streak: 0,
                achievements: [],
                dailyChallenges: []
            };
            
            this.initializeGameEngine();
        }
        
        initializeGameEngine() {
            this.loadPlayerData();
            this.updateUI();
            this.startStreakCheck();
            this.bindEvents();
        }
        
        // Points & Leveling System
        addPoints(amount, reason) {
            const oldLevel = this.player.level;
            this.player.points += amount;
            
            // Calculate new level
            const newLevel = this.calculateLevel(this.player.points);
            const leveledUp = newLevel > oldLevel;
            
            if (leveledUp) {
                this.player.level = newLevel;
                this.showLevelUpAnimation(newLevel);
            }
            
            this.showPointsAnimation(amount, reason);
            this.updateUI();
            this.savePlayerData();
            
            return { leveledUp, newLevel, points: amount };
        }
        
        calculateLevel(points) {
            const thresholds = [0, 100, 250, 500, 1000, 2000, 4000, 8000, 15000, 30000, 50000];
            for (let i = thresholds.length - 1; i >= 0; i--) {
                if (points >= thresholds[i]) {
                    return i + 1;
                }
            }
            return 1;
        }
        
        // Achievement System
        checkAchievements(action, data = {}) {
            const achievements = [
                {id: 'first_analysis', condition: () => this.player.analyses >= 1, points: 10, name: 'First Steps', icon: '🎯'},
                {id: 'analysis_novice', condition: () => this.player.analyses >= 10, points: 50, name: 'Novice Analyzer', icon: '📊'},
                {id: 'analysis_expert', condition: () => this.player.analyses >= 100, points: 200, name: 'Analysis Expert', icon: '🧠'},
                {id: 'streak_7', condition: () => this.player.streak >= 7, points: 150, name: 'Week Warrior', icon: '🔥'},
                {id: 'night_owl', condition: () => new Date().getHours() >= 0 && new Date().getHours() < 6, points: 50, name: 'Night Owl', icon: '🦉'},
                {id: 'early_bird', condition: () => new Date().getHours() >= 5 && new Date().getHours() < 9, points: 50, name: 'Early Bird', icon: '🐦'}
            ];
            
            achievements.forEach(achievement => {
                if (!this.player.achievements.includes(achievement.id) && achievement.condition()) {
                    this.unlockAchievement(achievement);
                }
            });
        }
        
        unlockAchievement(achievement) {
            this.player.achievements.push(achievement.id);
            this.addPoints(achievement.points, `Achievement: ${achievement.name}`);
            this.showAchievementPopup(achievement);
            this.savePlayerData();
        }
        
        // UI Animations
        showPointsAnimation(points, reason) {
            const pointsEl = document.createElement('div');
            pointsEl.className = 'floating-points';
            pointsEl.textContent = `+${points} XP`;
            pointsEl.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: #10b981;
                font-weight: bold;
                font-size: 1.5rem;
                z-index: 2000;
                pointer-events: none;
                animation: floatUp 2s ease forwards;
            `;
            
            document.body.appendChild(pointsEl);
            setTimeout(() => pointsEl.remove(), 2000);
        }
        
        showLevelUpAnimation(newLevel) {
            const levelUpEl = document.createElement('div');
            levelUpEl.className = 'level-up-popup';
            levelUpEl.innerHTML = `
                <div class="level-up-content">
                    <div class="level-up-icon">🎉</div>
                    <div class="level-up-text">
                        <div class="level-up-title">LEVEL UP!</div>
                        <div class="level-up-level">Level ${newLevel}</div>
                    </div>
                </div>
            `;
            levelUpEl.style.cssText = `
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%) scale(0);
                background: linear-gradient(135deg, rgba(168, 85, 247, 0.95), rgba(139, 69, 193, 0.95));
                backdrop-filter: blur(20px);
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
                z-index: 2000;
                color: white;
                text-align: center;
                animation: levelUpBounce 1s ease forwards;
            `;
            
            document.body.appendChild(levelUpEl);
            setTimeout(() => levelUpEl.remove(), 3000);
        }
        
        showAchievementPopup(achievement) {
            const popup = document.getElementById('achievementNotification');
            if (!popup) return;
            
            popup.querySelector('.achievement-icon').textContent = achievement.icon;
            popup.querySelector('.achievement-title').textContent = 'Achievement Unlocked!';
            popup.querySelector('.achievement-desc').textContent = achievement.name;
            popup.querySelector('.achievement-points').textContent = `+${achievement.points} XP`;
            
            popup.classList.remove('hidden');
            popup.classList.add('show');
            
            setTimeout(() => {
                popup.classList.remove('show');
                popup.classList.add('hidden');
            }, 4000);
        }
        
        // Update UI Elements
        updateUI() {
            // Update level and XP
            const levelEl = document.getElementById('playerLevel');
            const xpBarEl = document.getElementById('xpBar');
            const xpTextEl = document.getElementById('xpText');
            const pointsEl = document.getElementById('totalPoints');
            const streakEl = document.getElementById('streakCount');
            const analysisEl = document.getElementById('analysisCount');
            
            if (levelEl) levelEl.textContent = this.player.level;
            if (pointsEl) pointsEl.textContent = this.player.points.toLocaleString();
            if (streakEl) streakEl.textContent = this.player.streak;
            if (analysisEl) analysisEl.textContent = this.player.analyses;
            
            // Update XP bar
            if (xpBarEl && xpTextEl) {
                const currentLevelPoints = this.getPointsForLevel(this.player.level - 1);
                const nextLevelPoints = this.getPointsForLevel(this.player.level);
                const progress = ((this.player.points - currentLevelPoints) / (nextLevelPoints - currentLevelPoints)) * 100;
                
                xpBarEl.style.width = `${Math.min(progress, 100)}%`;
                xpTextEl.textContent = `${this.player.points - currentLevelPoints} / ${nextLevelPoints - currentLevelPoints} XP`;
            }
        }
        
        getPointsForLevel(level) {
            const thresholds = [0, 100, 250, 500, 1000, 2000, 4000, 8000, 15000, 30000, 50000];
            return thresholds[level] || thresholds[thresholds.length - 1];
        }
        
        // Data Persistence
        savePlayerData() {
            localStorage.setItem('sentimentGameData', JSON.stringify(this.player));
        }
        
        loadPlayerData() {
            const saved = localStorage.getItem('sentimentGameData');
            if (saved) {
                this.player = {...this.player, ...JSON.parse(saved)};
            }
        }
        
        // Event Binding
        bindEvents() {
            // Listen for analysis events
            document.addEventListener('analysisCompleted', (event) => {
                this.player.analyses++;
                this.addPoints(10, 'Text Analysis');
                this.checkAchievements('analysis', event.detail);
            });
            
            // Listen for streak updates
            document.addEventListener('streakUpdated', (event) => {
                this.player.streak = event.detail.streak;
                this.checkAchievements('streak');
            });
        }
        
        // Streak System
        startStreakCheck() {
            const lastActivity = localStorage.getItem('lastActivity');
            const today = new Date().toDateString();
            
            if (lastActivity !== today) {
                const yesterday = new Date(Date.now() - 86400000).toDateString();
                if (lastActivity === yesterday) {
                    this.player.streak++;
                } else if (lastActivity !== today) {
                    this.player.streak = 1;
                }
                localStorage.setItem('lastActivity', today);
                this.savePlayerData();
            }
        }
        
        // Trigger analysis completion
        triggerAnalysis(result) {
            const event = new CustomEvent('analysisCompleted', {
                detail: { result, timestamp: Date.now() }
            });
            document.dispatchEvent(event);
        }
    }
    
    // Initialize Game Engine
    const gameEngine = new GameEngine();
    
    // CSS Animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes floatUp {
            0% {
                opacity: 1;
                transform: translate(-50%, -50%) scale(1);
            }
            100% {
                opacity: 0;
                transform: translate(-50%, -150%) scale(1.2);
            }
        }
        
        @keyframes levelUpBounce {
            0% { transform: translate(-50%, -50%) scale(0); }
            50% { transform: translate(-50%, -50%) scale(1.2); }
            100% { transform: translate(-50%, -50%) scale(1); }
        }
    `;
    document.head.appendChild(style);
    """

if __name__ == "__main__":
    print("🎮 Gamification System Initialized!")
    print("Features: Achievements, Streaks, Points, Levels, Challenges, Leaderboards")