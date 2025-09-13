"""
🎨 VISUAL EXPERIENCE ENGINE
Advanced animations, dynamic themes, interactive visualizations, and micro-interactions
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional
import colorsys

class VisualExperienceEngine:
    """
    Advanced visual system for creating addictive user experiences
    """
    
    def __init__(self):
        self.theme_engine = ThemeEngine()
        self.animation_engine = AnimationEngine()
        self.interaction_engine = InteractionEngine()
        self.particle_system = ParticleSystem()
        
    def get_theme_config(self, theme_name: str = 'dynamic') -> Dict:
        """Get complete theme configuration"""
        return self.theme_engine.get_theme(theme_name)
    
    def get_animation_presets(self) -> Dict:
        """Get animation presets for different elements"""
        return self.animation_engine.get_presets()
    
    def generate_particle_effect(self, effect_type: str) -> Dict:
        """Generate particle effect configuration"""
        return self.particle_system.create_effect(effect_type)

class ThemeEngine:
    """Dynamic theme system with intelligent color generation"""
    
    def __init__(self):
        self.themes = self._initialize_themes()
        self.current_theme = 'dynamic'
        
    def _initialize_themes(self) -> Dict:
        """Initialize all available themes"""
        return {
            'dynamic': self._create_dynamic_theme(),
            'cyberpunk': self._create_cyberpunk_theme(),
            'nature': self._create_nature_theme(),
            'space': self._create_space_theme(),
            'ocean': self._create_ocean_theme(),
            'sunset': self._create_sunset_theme(),
            'minimal': self._create_minimal_theme(),
            'retro': self._create_retro_theme()
        }
    
    def get_theme(self, theme_name: str) -> Dict:
        """Get theme configuration"""
        return self.themes.get(theme_name, self.themes['dynamic'])
    
    def _create_dynamic_theme(self) -> Dict:
        """Dynamic theme that changes based on time/usage"""
        hour = datetime.now().hour
        
        # Morning (6-12): Fresh blues and greens
        if 6 <= hour < 12:
            primary = '#3b82f6'  # Blue
            secondary = '#10b981'  # Green
            accent = '#f59e0b'  # Amber
        # Afternoon (12-18): Warm oranges and yellows
        elif 12 <= hour < 18:
            primary = '#f97316'  # Orange
            secondary = '#eab308'  # Yellow
            accent = '#dc2626'  # Red
        # Evening (18-22): Purples and pinks
        elif 18 <= hour < 22:
            primary = '#8b5cf6'  # Violet
            secondary = '#ec4899'  # Pink
            accent = '#6366f1'  # Indigo
        # Night (22-6): Deep blues and purples
        else:
            primary = '#1e1b4b'  # Deep indigo
            secondary = '#312e81'  # Deep purple
            accent = '#3730a3'  # Deep violet
            
        return {
            'name': 'dynamic',
            'colors': {
                'primary': primary,
                'secondary': secondary,
                'accent': accent,
                'background': 'linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95))',
                'surface': 'rgba(255, 255, 255, 0.05)',
                'glass': 'rgba(255, 255, 255, 0.1)',
                'border': 'rgba(255, 255, 255, 0.1)',
                'text_primary': '#f1f5f9',
                'text_secondary': '#94a3b8',
                'success': '#10b981',
                'warning': '#f59e0b',
                'error': '#ef4444',
                'info': '#3b82f6'
            },
            'effects': {
                'blur': '20px',
                'glow': '0 0 20px rgba(59, 130, 246, 0.3)',
                'shadow': '0 8px 32px rgba(0, 0, 0, 0.3)',
                'border_radius': '16px',
                'transition': 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
            },
            'animations': {
                'hover_scale': 'scale(1.05)',
                'click_scale': 'scale(0.95)',
                'float': 'translateY(-2px)',
                'pulse': 'scale(1.02)'
            }
        }
    
    def _create_cyberpunk_theme(self) -> Dict:
        """High-tech cyberpunk theme"""
        return {
            'name': 'cyberpunk',
            'colors': {
                'primary': '#00ffff',  # Cyan
                'secondary': '#ff00ff',  # Magenta
                'accent': '#ffff00',  # Yellow
                'background': 'linear-gradient(135deg, #0a0a0a, #1a0033)',
                'surface': 'rgba(0, 255, 255, 0.05)',
                'glass': 'rgba(0, 255, 255, 0.1)',
                'border': 'rgba(0, 255, 255, 0.3)',
                'text_primary': '#00ffff',
                'text_secondary': '#ff00ff',
                'success': '#00ff00',
                'warning': '#ffff00',
                'error': '#ff0040',
                'info': '#0080ff'
            },
            'effects': {
                'blur': '10px',
                'glow': '0 0 30px rgba(0, 255, 255, 0.5)',
                'shadow': '0 0 50px rgba(255, 0, 255, 0.3)',
                'border_radius': '4px',
                'transition': 'all 0.2s ease'
            },
            'animations': {
                'hover_scale': 'scale(1.1)',
                'click_scale': 'scale(0.9)',
                'float': 'translateY(-4px)',
                'pulse': 'scale(1.05)'
            }
        }
    
    def _create_nature_theme(self) -> Dict:
        """Organic nature-inspired theme"""
        return {
            'name': 'nature',
            'colors': {
                'primary': '#22c55e',  # Green
                'secondary': '#84cc16',  # Lime
                'accent': '#eab308',  # Amber
                'background': 'linear-gradient(135deg, #064e3b, #1e3a1e)',
                'surface': 'rgba(34, 197, 94, 0.1)',
                'glass': 'rgba(255, 255, 255, 0.1)',
                'border': 'rgba(34, 197, 94, 0.3)',
                'text_primary': '#f0fdf4',
                'text_secondary': '#86efac',
                'success': '#16a34a',
                'warning': '#ca8a04',
                'error': '#dc2626',
                'info': '#0891b2'
            },
            'effects': {
                'blur': '15px',
                'glow': '0 0 25px rgba(34, 197, 94, 0.4)',
                'shadow': '0 8px 25px rgba(0, 0, 0, 0.3)',
                'border_radius': '20px',
                'transition': 'all 0.4s cubic-bezier(0.23, 1, 0.32, 1)'
            }
        }
    
    def _create_space_theme(self) -> Dict:
        """Cosmic space theme"""
        return {
            'name': 'space',
            'colors': {
                'primary': '#6366f1',  # Indigo
                'secondary': '#8b5cf6',  # Violet
                'accent': '#f59e0b',  # Amber (stars)
                'background': 'linear-gradient(135deg, #000000, #1e1b4b)',
                'surface': 'rgba(99, 102, 241, 0.1)',
                'glass': 'rgba(255, 255, 255, 0.05)',
                'border': 'rgba(99, 102, 241, 0.3)',
                'text_primary': '#e2e8f0',
                'text_secondary': '#a5b4fc',
                'success': '#10b981',
                'warning': '#f59e0b',
                'error': '#ef4444',
                'info': '#3b82f6'
            },
            'effects': {
                'blur': '25px',
                'glow': '0 0 40px rgba(99, 102, 241, 0.6)',
                'shadow': '0 20px 40px rgba(0, 0, 0, 0.5)',
                'border_radius': '12px',
                'transition': 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)'
            }
        }
    
    def _create_ocean_theme(self) -> Dict:
        """Deep ocean theme"""
        return {
            'name': 'ocean',
            'colors': {
                'primary': '#0ea5e9',  # Sky
                'secondary': '#06b6d4',  # Cyan
                'accent': '#10b981',  # Emerald
                'background': 'linear-gradient(135deg, #0c4a6e, #164e63)',
                'surface': 'rgba(14, 165, 233, 0.1)',
                'glass': 'rgba(255, 255, 255, 0.1)',
                'border': 'rgba(14, 165, 233, 0.3)',
                'text_primary': '#e0f2fe',
                'text_secondary': '#7dd3fc',
                'success': '#10b981',
                'warning': '#f59e0b',
                'error': '#ef4444',
                'info': '#0ea5e9'
            }
        }
    
    def _create_sunset_theme(self) -> Dict:
        """Warm sunset theme"""
        return {
            'name': 'sunset',
            'colors': {
                'primary': '#f97316',  # Orange
                'secondary': '#ec4899',  # Pink
                'accent': '#eab308',  # Yellow
                'background': 'linear-gradient(135deg, #7c2d12, #991b1b)',
                'surface': 'rgba(249, 115, 22, 0.1)',
                'glass': 'rgba(255, 255, 255, 0.1)',
                'border': 'rgba(249, 115, 22, 0.3)',
                'text_primary': '#fef2f2',
                'text_secondary': '#fdba74',
                'success': '#16a34a',
                'warning': '#ca8a04',
                'error': '#dc2626',
                'info': '#0891b2'
            }
        }
    
    def _create_minimal_theme(self) -> Dict:
        """Clean minimal theme"""
        return {
            'name': 'minimal',
            'colors': {
                'primary': '#374151',  # Gray
                'secondary': '#6b7280',  # Gray
                'accent': '#3b82f6',  # Blue
                'background': 'linear-gradient(135deg, #f9fafb, #f3f4f6)',
                'surface': 'rgba(255, 255, 255, 0.8)',
                'glass': 'rgba(255, 255, 255, 0.9)',
                'border': 'rgba(0, 0, 0, 0.1)',
                'text_primary': '#111827',
                'text_secondary': '#6b7280',
                'success': '#10b981',
                'warning': '#f59e0b',
                'error': '#ef4444',
                'info': '#3b82f6'
            }
        }
    
    def _create_retro_theme(self) -> Dict:
        """80s retro theme"""
        return {
            'name': 'retro',
            'colors': {
                'primary': '#ff0080',  # Hot Pink
                'secondary': '#00ffff',  # Cyan
                'accent': '#ffff00',  # Yellow
                'background': 'linear-gradient(135deg, #2d1b69, #11001e)',
                'surface': 'rgba(255, 0, 128, 0.1)',
                'glass': 'rgba(255, 255, 255, 0.05)',
                'border': 'rgba(255, 0, 128, 0.3)',
                'text_primary': '#ffffff',
                'text_secondary': '#ff80ff',
                'success': '#00ff00',
                'warning': '#ffff00',
                'error': '#ff4040',
                'info': '#00ffff'
            }
        }

class AnimationEngine:
    """Advanced animation system with physics-based effects"""
    
    def __init__(self):
        self.presets = self._create_animation_presets()
    
    def get_presets(self) -> Dict:
        """Get all animation presets"""
        return self.presets
    
    def _create_animation_presets(self) -> Dict:
        """Create comprehensive animation library"""
        return {
            'entrance': {
                'fadeInUp': {
                    'keyframes': {
                        '0%': {'opacity': '0', 'transform': 'translateY(20px)'},
                        '100%': {'opacity': '1', 'transform': 'translateY(0)'}
                    },
                    'duration': '0.6s',
                    'timing': 'cubic-bezier(0.4, 0, 0.2, 1)'
                },
                'slideInRight': {
                    'keyframes': {
                        '0%': {'opacity': '0', 'transform': 'translateX(100px)'},
                        '100%': {'opacity': '1', 'transform': 'translateX(0)'}
                    },
                    'duration': '0.5s',
                    'timing': 'cubic-bezier(0.23, 1, 0.32, 1)'
                },
                'scaleIn': {
                    'keyframes': {
                        '0%': {'opacity': '0', 'transform': 'scale(0.5)'},
                        '100%': {'opacity': '1', 'transform': 'scale(1)'}
                    },
                    'duration': '0.4s',
                    'timing': 'cubic-bezier(0.175, 0.885, 0.32, 1.275)'
                },
                'bounceIn': {
                    'keyframes': {
                        '0%': {'opacity': '0', 'transform': 'scale(0.3)'},
                        '50%': {'opacity': '1', 'transform': 'scale(1.1)'},
                        '100%': {'opacity': '1', 'transform': 'scale(1)'}
                    },
                    'duration': '0.8s',
                    'timing': 'cubic-bezier(0.68, -0.55, 0.265, 1.55)'
                }
            },
            'hover': {
                'lift': {
                    'transform': 'translateY(-4px)',
                    'box-shadow': '0 12px 40px rgba(0, 0, 0, 0.15)',
                    'transition': 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
                },
                'glow': {
                    'box-shadow': '0 0 20px currentColor',
                    'transform': 'scale(1.02)',
                    'transition': 'all 0.3s ease'
                },
                'tilt': {
                    'transform': 'perspective(1000px) rotateX(5deg) rotateY(10deg)',
                    'transition': 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
                },
                'shine': {
                    'position': 'relative',
                    'overflow': 'hidden',
                    'background': 'linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%)',
                    'background-size': '200% 200%',
                    'animation': 'shine 2s infinite'
                }
            },
            'click': {
                'ripple': {
                    'position': 'relative',
                    'overflow': 'hidden',
                    'transform': 'scale(0.98)',
                    'transition': 'transform 0.1s ease'
                },
                'bounce': {
                    'animation': 'clickBounce 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55)'
                },
                'pulse': {
                    'animation': 'clickPulse 0.4s ease-out'
                }
            },
            'loading': {
                'spin': {
                    'animation': 'spin 1s linear infinite'
                },
                'pulse': {
                    'animation': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite'
                },
                'bounce': {
                    'animation': 'bounce 1s infinite'
                },
                'wave': {
                    'animation': 'wave 1.5s ease-in-out infinite'
                }
            },
            'micro': {
                'heartbeat': {
                    'animation': 'heartbeat 1.5s ease-in-out infinite both'
                },
                'wobble': {
                    'animation': 'wobble 0.5s ease-in-out'
                },
                'flash': {
                    'animation': 'flash 0.5s ease-in-out'
                },
                'rubberBand': {
                    'animation': 'rubberBand 0.8s ease-in-out'
                }
            }
        }

class InteractionEngine:
    """Advanced interaction and micro-interaction system"""
    
    def __init__(self):
        self.gestures = self._initialize_gestures()
        self.feedback_system = FeedbackSystem()
        
    def _initialize_gestures(self) -> Dict:
        """Initialize gesture recognition patterns"""
        return {
            'swipe_right': {'threshold': 50, 'direction': 'horizontal'},
            'swipe_left': {'threshold': 50, 'direction': 'horizontal'},
            'swipe_up': {'threshold': 50, 'direction': 'vertical'},
            'swipe_down': {'threshold': 50, 'direction': 'vertical'},
            'pinch': {'threshold': 10, 'type': 'multi-touch'},
            'long_press': {'duration': 500, 'type': 'time-based'}
        }

class FeedbackSystem:
    """Haptic and visual feedback system"""
    
    def __init__(self):
        self.feedback_types = {
            'success': {'color': '#10b981', 'intensity': 'medium'},
            'error': {'color': '#ef4444', 'intensity': 'strong'},
            'warning': {'color': '#f59e0b', 'intensity': 'light'},
            'info': {'color': '#3b82f6', 'intensity': 'light'}
        }

class ParticleSystem:
    """Dynamic particle effects system"""
    
    def __init__(self):
        self.effects = {
            'celebration': self._create_celebration_effect(),
            'sparkle': self._create_sparkle_effect(),
            'smoke': self._create_smoke_effect(),
            'fire': self._create_fire_effect(),
            'stars': self._create_stars_effect()
        }
    
    def create_effect(self, effect_type: str) -> Dict:
        """Create particle effect configuration"""
        return self.effects.get(effect_type, self.effects['sparkle'])
    
    def _create_celebration_effect(self) -> Dict:
        """Celebration confetti effect"""
        return {
            'particle_count': 50,
            'colors': ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57'],
            'shapes': ['circle', 'square', 'triangle'],
            'physics': {
                'gravity': 0.5,
                'initial_velocity': {'min': 5, 'max': 15},
                'spread': 60,
                'life': {'min': 1000, 'max': 3000}
            }
        }
    
    def _create_sparkle_effect(self) -> Dict:
        """Magical sparkle effect"""
        return {
            'particle_count': 20,
            'colors': ['#ffffff', '#f0f9ff', '#dbeafe'],
            'shapes': ['star', 'circle'],
            'physics': {
                'gravity': -0.1,
                'initial_velocity': {'min': 1, 'max': 3},
                'spread': 30,
                'life': {'min': 500, 'max': 1500}
            }
        }
    
    def _create_smoke_effect(self) -> Dict:
        """Smooth smoke effect"""
        return {
            'particle_count': 15,
            'colors': ['rgba(255,255,255,0.1)', 'rgba(200,200,200,0.2)'],
            'shapes': ['circle'],
            'physics': {
                'gravity': -0.2,
                'initial_velocity': {'min': 0.5, 'max': 2},
                'spread': 45,
                'life': {'min': 2000, 'max': 4000}
            }
        }
    
    def _create_fire_effect(self) -> Dict:
        """Dynamic fire effect"""
        return {
            'particle_count': 30,
            'colors': ['#ff4500', '#ff6347', '#ffa500', '#ffff00'],
            'shapes': ['circle'],
            'physics': {
                'gravity': -0.3,
                'initial_velocity': {'min': 2, 'max': 6},
                'spread': 20,
                'life': {'min': 800, 'max': 2000}
            }
        }
    
    def _create_stars_effect(self) -> Dict:
        """Twinkling stars effect"""
        return {
            'particle_count': 100,
            'colors': ['#ffffff', '#ffd700', '#87ceeb'],
            'shapes': ['star'],
            'physics': {
                'gravity': 0,
                'initial_velocity': {'min': 0, 'max': 0.5},
                'spread': 360,
                'life': {'min': 3000, 'max': 8000}
            }
        }

def generate_visual_experience_ui() -> str:
    """Generate complete visual experience UI system"""
    return """
    <!-- Visual Experience Engine UI -->
    <div class="visual-experience-system">
        <!-- Theme Selector -->
        <div class="theme-selector glass-card">
            <h4><i class="fas fa-palette"></i> Visual Themes</h4>
            <div class="theme-grid">
                <div class="theme-option" data-theme="dynamic">
                    <div class="theme-preview dynamic-preview"></div>
                    <span>Dynamic</span>
                </div>
                <div class="theme-option" data-theme="cyberpunk">
                    <div class="theme-preview cyberpunk-preview"></div>
                    <span>Cyberpunk</span>
                </div>
                <div class="theme-option" data-theme="nature">
                    <div class="theme-preview nature-preview"></div>
                    <span>Nature</span>
                </div>
                <div class="theme-option" data-theme="space">
                    <div class="theme-preview space-preview"></div>
                    <span>Space</span>
                </div>
                <div class="theme-option" data-theme="ocean">
                    <div class="theme-preview ocean-preview"></div>
                    <span>Ocean</span>
                </div>
                <div class="theme-option" data-theme="sunset">
                    <div class="theme-preview sunset-preview"></div>
                    <span>Sunset</span>
                </div>
                <div class="theme-option" data-theme="minimal">
                    <div class="theme-preview minimal-preview"></div>
                    <span>Minimal</span>
                </div>
                <div class="theme-option" data-theme="retro">
                    <div class="theme-preview retro-preview"></div>
                    <span>Retro</span>
                </div>
            </div>
        </div>

        <!-- Animation Controls -->
        <div class="animation-controls glass-card">
            <h4><i class="fas fa-magic"></i> Animation Settings</h4>
            <div class="control-group">
                <label>Animation Speed</label>
                <input type="range" id="animationSpeed" min="0.1" max="2" step="0.1" value="1">
                <span id="speedValue">1x</span>
            </div>
            <div class="control-group">
                <label class="checkbox-label">
                    <input type="checkbox" id="reducedMotion">
                    <span class="checkmark"></span>
                    Reduce Motion
                </label>
            </div>
            <div class="control-group">
                <label class="checkbox-label">
                    <input type="checkbox" id="particleEffects" checked>
                    <span class="checkmark"></span>
                    Particle Effects
                </label>
            </div>
            <div class="control-group">
                <label class="checkbox-label">
                    <input type="checkbox" id="soundEffects">
                    <span class="checkmark"></span>
                    Sound Effects
                </label>
            </div>
        </div>

        <!-- Visual Effects Playground -->
        <div class="effects-playground glass-card">
            <h4><i class="fas fa-sparkles"></i> Effects Demo</h4>
            <div class="effect-buttons">
                <button class="effect-btn" data-effect="celebration">
                    🎉 Celebration
                </button>
                <button class="effect-btn" data-effect="sparkle">
                    ✨ Sparkle
                </button>
                <button class="effect-btn" data-effect="fire">
                    🔥 Fire
                </button>
                <button class="effect-btn" data-effect="stars">
                    ⭐ Stars
                </button>
            </div>
            <div class="effect-canvas" id="effectCanvas">
                <!-- Particle effects render here -->
            </div>
        </div>
    </div>

    <!-- Particle Effect Canvas -->
    <canvas id="particleCanvas" style="position: fixed; top: 0; left: 0; pointer-events: none; z-index: 9999;"></canvas>

    <style>
    /* Visual Experience System Styles */
    .visual-experience-system {
        position: fixed;
        top: 20px;
        left: 20px;
        width: 280px;
        z-index: 970;
        display: flex;
        flex-direction: column;
        gap: 15px;
        max-height: calc(100vh - 40px);
        overflow-y: auto;
    }

    .theme-selector, .animation-controls, .effects-playground {
        padding: 20px;
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(var(--glass-blur));
        border-radius: var(--glass-radius);
    }

    .theme-selector h4, .animation-controls h4, .effects-playground h4 {
        margin: 0 0 15px 0;
        font-size: 1rem;
        color: var(--text-primary);
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .theme-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
    }

    .theme-option {
        cursor: pointer;
        text-align: center;
        padding: 12px;
        border-radius: 12px;
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }

    .theme-option:hover {
        background: rgba(255, 255, 255, 0.05);
        transform: scale(1.05);
    }

    .theme-option.active {
        border-color: var(--primary);
        background: rgba(var(--primary-rgb), 0.1);
    }

    .theme-preview {
        width: 100%;
        height: 40px;
        border-radius: 8px;
        margin-bottom: 8px;
        position: relative;
        overflow: hidden;
    }

    .theme-preview::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(2px);
        border-radius: inherit;
    }

    .dynamic-preview { background: linear-gradient(135deg, #3b82f6, #8b5cf6); }
    .cyberpunk-preview { background: linear-gradient(135deg, #00ffff, #ff00ff); }
    .nature-preview { background: linear-gradient(135deg, #22c55e, #84cc16); }
    .space-preview { background: linear-gradient(135deg, #6366f1, #1e1b4b); }
    .ocean-preview { background: linear-gradient(135deg, #0ea5e9, #06b6d4); }
    .sunset-preview { background: linear-gradient(135deg, #f97316, #ec4899); }
    .minimal-preview { background: linear-gradient(135deg, #f9fafb, #374151); }
    .retro-preview { background: linear-gradient(135deg, #ff0080, #00ffff); }

    .theme-option span {
        font-size: 0.8rem;
        color: var(--text-secondary);
        font-weight: 500;
    }

    .control-group {
        margin-bottom: 15px;
    }

    .control-group label:not(.checkbox-label) {
        display: block;
        font-size: 0.85rem;
        color: var(--text-primary);
        margin-bottom: 6px;
        font-weight: 500;
    }

    .control-group input[type="range"] {
        width: 100%;
        background: transparent;
        appearance: none;
        height: 6px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 3px;
        outline: none;
    }

    .control-group input[type="range"]::-webkit-slider-thumb {
        appearance: none;
        width: 18px;
        height: 18px;
        background: var(--primary);
        border-radius: 50%;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .control-group input[type="range"]::-webkit-slider-thumb:hover {
        transform: scale(1.2);
        box-shadow: 0 0 10px var(--primary);
    }

    #speedValue {
        float: right;
        font-size: 0.8rem;
        color: var(--primary);
        font-weight: 600;
    }

    .checkbox-label {
        display: flex;
        align-items: center;
        gap: 10px;
        cursor: pointer;
        color: var(--text-primary);
        font-size: 0.85rem;
    }

    .checkbox-label input[type="checkbox"] {
        display: none;
    }

    .checkmark {
        width: 18px;
        height: 18px;
        border: 2px solid var(--glass-border);
        border-radius: 4px;
        position: relative;
        transition: all 0.3s ease;
    }

    .checkbox-label input[type="checkbox"]:checked + .checkmark {
        background: var(--primary);
        border-color: var(--primary);
    }

    .checkbox-label input[type="checkbox"]:checked + .checkmark::after {
        content: '✓';
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        color: white;
        font-size: 0.8rem;
        font-weight: bold;
    }

    .effect-buttons {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
        margin-bottom: 15px;
    }

    .effect-btn {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid var(--glass-border);
        color: var(--text-primary);
        padding: 10px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 0.8rem;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
    }

    .effect-btn:hover {
        background: var(--primary);
        color: white;
        transform: scale(1.05);
    }

    .effect-canvas {
        height: 100px;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 8px;
        position: relative;
        overflow: hidden;
        border: 1px solid var(--glass-border);
    }

    /* Advanced CSS Animations */
    @keyframes shine {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }

    @keyframes heartbeat {
        0%, 50%, 100% { transform: scale(1); }
        25%, 75% { transform: scale(1.1); }
    }

    @keyframes wobble {
        0% { transform: rotate(0deg); }
        15% { transform: rotate(-5deg); }
        30% { transform: rotate(3deg); }
        45% { transform: rotate(-3deg); }
        60% { transform: rotate(2deg); }
        75% { transform: rotate(-1deg); }
        100% { transform: rotate(0deg); }
    }

    @keyframes flash {
        0%, 50%, 100% { opacity: 1; }
        25%, 75% { opacity: 0.3; }
    }

    @keyframes rubberBand {
        0% { transform: scale(1); }
        30% { transform: scaleX(1.25) scaleY(0.75); }
        40% { transform: scaleX(0.75) scaleY(1.25); }
        50% { transform: scaleX(1.15) scaleY(0.85); }
        65% { transform: scaleX(0.95) scaleY(1.05); }
        75% { transform: scaleX(1.05) scaleY(0.95); }
        100% { transform: scale(1); }
    }

    @keyframes clickBounce {
        0% { transform: scale(1); }
        50% { transform: scale(0.8); }
        100% { transform: scale(1); }
    }

    @keyframes clickPulse {
        0% { box-shadow: 0 0 0 0 rgba(var(--primary-rgb), 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(var(--primary-rgb), 0); }
        100% { box-shadow: 0 0 0 0 rgba(var(--primary-rgb), 0); }
    }

    @keyframes wave {
        0%, 60%, 100% { transform: initial; }
        30% { transform: translateY(-15px); }
    }

    /* Responsive */
    @media (max-width: 1400px) {
        .visual-experience-system {
            position: relative;
            width: 100%;
            left: 0;
            margin-bottom: 20px;
        }
    }
    </style>

    <script>
    // Visual Experience Engine JavaScript
    class VisualExperienceEngine {
        constructor() {
            this.currentTheme = 'dynamic';
            this.animationSpeed = 1;
            this.particleEffectsEnabled = true;
            this.soundEffectsEnabled = false;
            this.reducedMotion = false;
            
            this.particleSystem = new ParticleSystem();
            this.themeSystem = new ThemeSystem();
            
            this.initializeVisualSystem();
        }
        
        initializeVisualSystem() {
            this.setupThemeSelector();
            this.setupAnimationControls();
            this.setupEffectButtons();
            this.setupParticleSystem();
            this.applyInitialTheme();
        }
        
        setupThemeSelector() {
            const themeOptions = document.querySelectorAll('.theme-option');
            themeOptions.forEach(option => {
                option.addEventListener('click', () => {
                    const theme = option.dataset.theme;
                    this.switchTheme(theme);
                });
            });
        }
        
        switchTheme(themeName) {
            this.currentTheme = themeName;
            this.themeSystem.applyTheme(themeName);
            
            // Update active state
            document.querySelectorAll('.theme-option').forEach(opt => {
                opt.classList.remove('active');
            });
            document.querySelector(`[data-theme="${themeName}"]`).classList.add('active');
            
            // Trigger theme change effect
            if (this.particleEffectsEnabled) {
                this.particleSystem.createEffect('sparkle', { x: window.innerWidth / 2, y: window.innerHeight / 2 });
            }
        }
        
        setupAnimationControls() {
            const speedSlider = document.getElementById('animationSpeed');
            const speedValue = document.getElementById('speedValue');
            const reducedMotionCheckbox = document.getElementById('reducedMotion');
            const particleEffectsCheckbox = document.getElementById('particleEffects');
            const soundEffectsCheckbox = document.getElementById('soundEffects');
            
            speedSlider.addEventListener('input', (e) => {
                this.animationSpeed = parseFloat(e.target.value);
                speedValue.textContent = `${this.animationSpeed}x`;
                this.updateAnimationSpeed();
            });
            
            reducedMotionCheckbox.addEventListener('change', (e) => {
                this.reducedMotion = e.target.checked;
                this.updateMotionSettings();
            });
            
            particleEffectsCheckbox.addEventListener('change', (e) => {
                this.particleEffectsEnabled = e.target.checked;
            });
            
            soundEffectsCheckbox.addEventListener('change', (e) => {
                this.soundEffectsEnabled = e.target.checked;
            });
        }
        
        updateAnimationSpeed() {
            const root = document.documentElement;
            root.style.setProperty('--animation-speed', `${1 / this.animationSpeed}s`);
        }
        
        updateMotionSettings() {
            const root = document.documentElement;
            if (this.reducedMotion) {
                root.style.setProperty('--transition-duration', '0.1s');
                root.style.setProperty('--animation-duration', '0.2s');
            } else {
                root.style.setProperty('--transition-duration', '0.3s');
                root.style.setProperty('--animation-duration', '0.6s');
            }
        }
        
        setupEffectButtons() {
            const effectButtons = document.querySelectorAll('.effect-btn');
            effectButtons.forEach(btn => {
                btn.addEventListener('click', () => {
                    const effect = btn.dataset.effect;
                    this.triggerEffect(effect, btn);
                });
            });
        }
        
        triggerEffect(effectType, element) {
            if (!this.particleEffectsEnabled) return;
            
            const rect = element.getBoundingClientRect();
            const x = rect.left + rect.width / 2;
            const y = rect.top + rect.height / 2;
            
            this.particleSystem.createEffect(effectType, { x, y });
            
            // Add button feedback
            element.style.transform = 'scale(0.95)';
            setTimeout(() => {
                element.style.transform = '';
            }, 150);
        }
        
        setupParticleSystem() {
            this.particleSystem.initialize();
        }
        
        applyInitialTheme() {
            this.themeSystem.applyTheme(this.currentTheme);
            document.querySelector(`[data-theme="${this.currentTheme}"]`).classList.add('active');
        }
    }
    
    class ParticleSystem {
        constructor() {
            this.canvas = null;
            this.ctx = null;
            this.particles = [];
            this.animationId = null;
        }
        
        initialize() {
            this.canvas = document.getElementById('particleCanvas');
            this.ctx = this.canvas.getContext('2d');
            this.resizeCanvas();
            
            window.addEventListener('resize', () => this.resizeCanvas());
            this.startAnimation();
        }
        
        resizeCanvas() {
            this.canvas.width = window.innerWidth;
            this.canvas.height = window.innerHeight;
        }
        
        createEffect(type, position) {
            const effects = {
                celebration: () => this.createCelebrationParticles(position),
                sparkle: () => this.createSparkleParticles(position),
                fire: () => this.createFireParticles(position),
                stars: () => this.createStarParticles(position)
            };
            
            const effect = effects[type];
            if (effect) {
                effect();
            }
        }
        
        createCelebrationParticles(position) {
            const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57'];
            
            for (let i = 0; i < 30; i++) {
                this.particles.push({
                    x: position.x,
                    y: position.y,
                    vx: (Math.random() - 0.5) * 15,
                    vy: Math.random() * -10 - 5,
                    gravity: 0.3,
                    life: 1,
                    maxLife: Math.random() * 100 + 50,
                    color: colors[Math.floor(Math.random() * colors.length)],
                    size: Math.random() * 5 + 2,
                    type: 'confetti'
                });
            }
        }
        
        createSparkleParticles(position) {
            for (let i = 0; i < 15; i++) {
                this.particles.push({
                    x: position.x + (Math.random() - 0.5) * 50,
                    y: position.y + (Math.random() - 0.5) * 50,
                    vx: (Math.random() - 0.5) * 3,
                    vy: (Math.random() - 0.5) * 3,
                    gravity: -0.05,
                    life: 1,
                    maxLife: Math.random() * 60 + 30,
                    color: '#ffffff',
                    size: Math.random() * 3 + 1,
                    type: 'sparkle'
                });
            }
        }
        
        createFireParticles(position) {
            const colors = ['#ff4500', '#ff6347', '#ffa500', '#ffff00'];
            
            for (let i = 0; i < 20; i++) {
                this.particles.push({
                    x: position.x + (Math.random() - 0.5) * 20,
                    y: position.y,
                    vx: (Math.random() - 0.5) * 4,
                    vy: Math.random() * -8 - 2,
                    gravity: -0.1,
                    life: 1,
                    maxLife: Math.random() * 40 + 20,
                    color: colors[Math.floor(Math.random() * colors.length)],
                    size: Math.random() * 6 + 2,
                    type: 'fire'
                });
            }
        }
        
        createStarParticles(position) {
            for (let i = 0; i < 25; i++) {
                this.particles.push({
                    x: position.x + (Math.random() - 0.5) * 100,
                    y: position.y + (Math.random() - 0.5) * 100,
                    vx: (Math.random() - 0.5) * 2,
                    vy: (Math.random() - 0.5) * 2,
                    gravity: 0,
                    life: 1,
                    maxLife: Math.random() * 120 + 60,
                    color: '#ffd700',
                    size: Math.random() * 4 + 1,
                    type: 'star'
                });
            }
        }
        
        updateParticles() {
            this.particles = this.particles.filter(particle => {
                particle.x += particle.vx;
                particle.y += particle.vy;
                particle.vy += particle.gravity;
                particle.life -= 1/particle.maxLife;
                
                return particle.life > 0;
            });
        }
        
        drawParticles() {
            this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
            
            this.particles.forEach(particle => {
                this.ctx.save();
                this.ctx.globalAlpha = particle.life;
                this.ctx.fillStyle = particle.color;
                
                if (particle.type === 'star') {
                    this.drawStar(particle);
                } else if (particle.type === 'sparkle') {
                    this.drawSparkle(particle);
                } else {
                    this.ctx.beginPath();
                    this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
                    this.ctx.fill();
                }
                
                this.ctx.restore();
            });
        }
        
        drawStar(particle) {
            const { x, y, size } = particle;
            this.ctx.beginPath();
            for (let i = 0; i < 5; i++) {
                const angle = (i * 144 - 90) * Math.PI / 180;
                const x1 = x + Math.cos(angle) * size;
                const y1 = y + Math.sin(angle) * size;
                if (i === 0) this.ctx.moveTo(x1, y1);
                else this.ctx.lineTo(x1, y1);
            }
            this.ctx.closePath();
            this.ctx.fill();
        }
        
        drawSparkle(particle) {
            const { x, y, size } = particle;
            this.ctx.beginPath();
            this.ctx.moveTo(x, y - size);
            this.ctx.lineTo(x + size/3, y - size/3);
            this.ctx.lineTo(x + size, y);
            this.ctx.lineTo(x + size/3, y + size/3);
            this.ctx.lineTo(x, y + size);
            this.ctx.lineTo(x - size/3, y + size/3);
            this.ctx.lineTo(x - size, y);
            this.ctx.lineTo(x - size/3, y - size/3);
            this.ctx.closePath();
            this.ctx.fill();
        }
        
        startAnimation() {
            const animate = () => {
                this.updateParticles();
                this.drawParticles();
                this.animationId = requestAnimationFrame(animate);
            };
            animate();
        }
    }
    
    class ThemeSystem {
        constructor() {
            this.themes = this.initializeThemes();
        }
        
        initializeThemes() {
            return {
                dynamic: {
                    '--primary': '#3b82f6',
                    '--secondary': '#10b981',
                    '--accent': '#f59e0b',
                    '--primary-rgb': '59, 130, 246'
                },
                cyberpunk: {
                    '--primary': '#00ffff',
                    '--secondary': '#ff00ff',
                    '--accent': '#ffff00',
                    '--primary-rgb': '0, 255, 255'
                },
                nature: {
                    '--primary': '#22c55e',
                    '--secondary': '#84cc16',
                    '--accent': '#eab308',
                    '--primary-rgb': '34, 197, 94'
                },
                space: {
                    '--primary': '#6366f1',
                    '--secondary': '#8b5cf6',
                    '--accent': '#f59e0b',
                    '--primary-rgb': '99, 102, 241'
                },
                ocean: {
                    '--primary': '#0ea5e9',
                    '--secondary': '#06b6d4',
                    '--accent': '#10b981',
                    '--primary-rgb': '14, 165, 233'
                },
                sunset: {
                    '--primary': '#f97316',
                    '--secondary': '#ec4899',
                    '--accent': '#eab308',
                    '--primary-rgb': '249, 115, 22'
                },
                minimal: {
                    '--primary': '#374151',
                    '--secondary': '#6b7280',
                    '--accent': '#3b82f6',
                    '--primary-rgb': '55, 65, 81'
                },
                retro: {
                    '--primary': '#ff0080',
                    '--secondary': '#00ffff',
                    '--accent': '#ffff00',
                    '--primary-rgb': '255, 0, 128'
                }
            };
        }
        
        applyTheme(themeName) {
            const theme = this.themes[themeName];
            if (!theme) return;
            
            const root = document.documentElement;
            Object.entries(theme).forEach(([property, value]) => {
                root.style.setProperty(property, value);
            });
            
            // Add theme class to body
            document.body.className = document.body.className.replace(/theme-\w+/g, '');
            document.body.classList.add(`theme-${themeName}`);
        }
    }
    
    // Initialize the visual experience engine
    const visualExperienceEngine = new VisualExperienceEngine();
    </script>
    """

if __name__ == "__main__":
    print("🎨 Visual Experience Engine Initialized!")
    print("Features: Dynamic themes, advanced animations, particle effects, micro-interactions")