"""
Enhanced Modern UI Components and Styling System
Advanced CSS generation with smooth animations, stable charts, and modern design patterns
"""

from typing import Dict, Any, List
import json

class ModernUIGenerator:
    """Generate modern, minimalist UI components with advanced styling and stable chart handling"""
    
    def __init__(self):
        self.color_palette = {
            'primary': '#6366f1',
            'secondary': '#8b5cf6', 
            'accent': '#06b6d4',
            'success': '#10b981',
            'warning': '#f59e0b',
            'error': '#ef4444',
            'neutral': '#6b7280',
            'background': '#0f172a',
            'surface': '#1e293b',
            'glass': 'rgba(255, 255, 255, 0.1)',
            'glass_border': 'rgba(255, 255, 255, 0.2)',
            'text_primary': '#f8fafc',
            'text_secondary': '#cbd5e1',
            'text_muted': '#64748b'
        }
        
        self.animations = {
            'fast': '0.15s',
            'normal': '0.3s', 
            'slow': '0.5s',
            'ease': 'cubic-bezier(0.4, 0, 0.2, 1)',
            'bounce': 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
            'elastic': 'cubic-bezier(0.175, 0.885, 0.32, 1.275)'
        }
    
    def generate_stable_chart_styles(self) -> str:
        """Generate CSS for stable, non-resizing charts"""
        return """
        /* Stable Chart Container Styles */
        .chart-container {
            position: relative;
            width: 100%;
            height: 400px; /* Fixed height prevents growth */
            overflow: hidden;
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: var(--border-radius);
            padding: 1rem;
        }
        
        .chart-container canvas {
            max-width: 100% !important;
            max-height: 100% !important;
            width: auto !important;
            height: auto !important;
        }
        
        /* Mini chart styles */
        .chart-mini {
            height: 120px !important;
            width: 100%;
            position: relative;
            overflow: hidden;
        }
        
        .chart-mini canvas {
            max-height: 100px !important;
        }
        
        /* Prevent chart resize on scroll */
        .chart-wrapper {
            position: relative;
            height: 100%;
            width: 100%;
        }
        
        /* Word cloud container */
        .word-cloud-container {
            height: 400px !important;
            width: 100%;
            overflow: hidden;
            position: relative;
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: var(--border-radius);
        }
        
        .word-cloud-container svg {
            width: 100% !important;
            height: 100% !important;
            max-width: 100%;
            max-height: 100%;
        }
        """
    
    def generate_pagination_styles(self) -> str:
        """Generate styles for pagination components"""
        return """
        /* Pagination Styles */
        .pagination-container {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.5rem;
            margin: 2rem 0;
            padding: 1rem;
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: var(--border-radius);
        }
        
        .pagination-btn {
            background: var(--glass);
            border: 1px solid var(--glass-border);
            color: var(--text-primary);
            padding: 0.5rem 1rem;
            border-radius: var(--border-radius);
            cursor: pointer;
            transition: all var(--transition-normal) var(--ease);
            min-width: 40px;
            text-align: center;
        }
        
        .pagination-btn:hover:not(:disabled) {
            background: var(--primary);
            border-color: var(--primary);
            transform: translateY(-1px);
        }
        
        .pagination-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .pagination-btn.active {
            background: var(--primary);
            border-color: var(--primary);
            font-weight: 600;
        }
        
        .pagination-info {
            color: var(--text-secondary);
            font-size: 0.875rem;
            margin: 0 1rem;
        }
        
        .load-more-btn {
            background: linear-gradient(135deg, var(--primary), var(--accent));
            border: none;
            color: white;
            padding: 0.75rem 2rem;
            border-radius: var(--border-radius);
            cursor: pointer;
            font-weight: 600;
            transition: all var(--transition-normal) var(--ease);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin: 1rem auto;
        }
        
        .load-more-btn:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        
        .load-more-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        """
    
    def generate_media_panel_styles(self) -> str:
        """Generate styles for media metadata panel"""
        return """
        /* Media Panel Styles */
        .media-panel {
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            margin-bottom: 1rem;
        }
        
        .media-input-group {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }
        
        .media-input-toggle {
            display: flex;
            background: var(--glass);
            border-radius: var(--border-radius);
            padding: 0.25rem;
            margin-bottom: 1rem;
        }
        
        .media-toggle-btn {
            flex: 1;
            background: transparent;
            border: none;
            color: var(--text-secondary);
            padding: 0.5rem 1rem;
            border-radius: calc(var(--border-radius) - 0.25rem);
            cursor: pointer;
            transition: all var(--transition-normal) var(--ease);
        }
        
        .media-toggle-btn.active {
            background: var(--primary);
            color: white;
        }
        
        .url-input-container,
        .file-input-container {
            display: none;
        }
        
        .url-input-container.active,
        .file-input-container.active {
            display: block;
        }
        
        .media-url-input {
            width: 100%;
            background: var(--glass);
            border: 1px solid var(--glass-border);
            color: var(--text-primary);
            padding: 0.75rem;
            border-radius: var(--border-radius);
            font-size: 1rem;
        }
        
        .media-url-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        }
        
        .file-drop-zone {
            border: 2px dashed var(--glass-border);
            border-radius: var(--border-radius);
            padding: 2rem;
            text-align: center;
            transition: all var(--transition-normal) var(--ease);
            cursor: pointer;
        }
        
        .file-drop-zone:hover,
        .file-drop-zone.dragover {
            border-color: var(--primary);
            background: rgba(99, 102, 241, 0.05);
        }
        
        .metadata-card {
            background: var(--surface);
            border: 1px solid var(--glass-border);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            margin-top: 1rem;
        }
        
        .metadata-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--glass-border);
        }
        
        .metadata-title {
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .metadata-platform {
            background: var(--primary);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.75rem;
            font-weight: 500;
        }
        
        .metadata-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 1rem;
        }
        
        .metadata-item {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }
        
        .metadata-label {
            font-size: 0.75rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 500;
        }
        
        .metadata-value {
            color: var(--text-primary);
            font-weight: 500;
        }
        
        .metadata-thumbnail {
            max-width: 200px;
            border-radius: var(--border-radius);
            border: 1px solid var(--glass-border);
        }
        
        .copy-json-btn {
            background: var(--glass);
            border: 1px solid var(--glass-border);
            color: var(--text-primary);
            padding: 0.5rem 1rem;
            border-radius: var(--border-radius);
            cursor: pointer;
            transition: all var(--transition-normal) var(--ease);
            font-size: 0.875rem;
        }
        
        .copy-json-btn:hover {
            background: var(--primary);
            border-color: var(--primary);
        }
        
        .raw-metadata {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--glass-border);
            border-radius: var(--border-radius);
            padding: 1rem;
            max-height: 300px;
            overflow-y: auto;
            font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
            font-size: 0.875rem;
            line-height: 1.4;
            color: var(--text-secondary);
            white-space: pre-wrap;
            word-break: break-word;
        }
        """
    
    def generate_tab_styles(self) -> str:
        """Generate enhanced tab styles"""
        return """
        /* Enhanced Tab Styles */
        .tab-container {
            background: var(--glass);
            border: 1px solid var(--glass-border);
            border-radius: var(--border-radius);
            overflow: hidden;
            margin: 2rem 0;
        }
        
        .tab-nav {
            display: flex;
            background: var(--surface);
            border-bottom: 1px solid var(--glass-border);
            overflow-x: auto;
            scrollbar-width: none;
        }
        
        .tab-nav::-webkit-scrollbar {
            display: none;
        }
        
        .tab-btn {
            flex: 1;
            min-width: max-content;
            background: transparent;
            border: none;
            color: var(--text-secondary);
            padding: 1rem 1.5rem;
            cursor: pointer;
            transition: all var(--transition-normal) var(--ease);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 500;
            white-space: nowrap;
            position: relative;
        }
        
        .tab-btn::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: var(--primary);
            transform: scaleX(0);
            transition: transform var(--transition-normal) var(--ease);
        }
        
        .tab-btn:hover {
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.05);
        }
        
        .tab-btn.active {
            color: var(--primary);
            background: rgba(99, 102, 241, 0.1);
        }
        
        .tab-btn.active::after {
            transform: scaleX(1);
        }
        
        .tab-content {
            padding: 2rem;
            min-height: 400px;
        }
        
        .tab-pane {
            display: none;
            animation: fadeInUp var(--transition-normal) var(--ease);
        }
        
        .tab-pane.active {
            display: block;
        }
        """
    
    def generate_base_styles(self) -> str:
        """Generate base CSS styles with modern design system"""
        return f"""
        /* Modern CSS Variables */
        :root {{
            --primary: {self.color_palette['primary']};
            --secondary: {self.color_palette['secondary']};
            --accent: {self.color_palette['accent']};
            --success: {self.color_palette['success']};
            --warning: {self.color_palette['warning']};
            --error: {self.color_palette['error']};
            --neutral: {self.color_palette['neutral']};
            --background: {self.color_palette['background']};
            --surface: {self.color_palette['surface']};
            --glass: {self.color_palette['glass']};
            --glass-border: {self.color_palette['glass_border']};
            --text-primary: {self.color_palette['text_primary']};
            --text-secondary: {self.color_palette['text_secondary']};
            --text-muted: {self.color_palette['text_muted']};
            
            --transition-fast: {self.animations['fast']};
            --transition-normal: {self.animations['normal']};
            --transition-slow: {self.animations['slow']};
            --ease: {self.animations['ease']};
            --bounce: {self.animations['bounce']};
            --elastic: {self.animations['elastic']};
            
            --border-radius: 12px;
            --border-radius-lg: 16px;
            --border-radius-xl: 20px;
            --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.12);
            --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.15);
            --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.2);
            --shadow-xl: 0 20px 40px rgba(0, 0, 0, 0.25);
        }}
        
        /* Reset and Base */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        html {{
            scroll-behavior: smooth;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%);
            color: var(--text-primary);
            line-height: 1.6;
            font-size: 16px;
            overflow-x: hidden;
            min-height: 100vh;
        }}
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {{
            font-weight: 600;
            letter-spacing: -0.025em;
            line-height: 1.2;
        }}
        
        h1 {{ font-size: 2.5rem; }}
        h2 {{ font-size: 2rem; }}
        h3 {{ font-size: 1.5rem; }}
        h4 {{ font-size: 1.25rem; }}
        h5 {{ font-size: 1.125rem; }}
        h6 {{ font-size: 1rem; }}
        
        p {{ 
            color: var(--text-secondary);
            margin-bottom: 1rem;
        }}
        
        /* Modern Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: rgba(0, 0, 0, 0.1);
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--glass-border);
            border-radius: 4px;
            transition: background var(--transition-normal) var(--ease);
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: rgba(255, 255, 255, 0.3);
        }}
        """
    
    def generate_glass_components(self) -> str:
        """Generate glassmorphism components"""
        return """
        /* Glass Container */
        .glass-container {
            background: var(--glass);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow-lg);
            position: relative;
            overflow: hidden;
        }
        
        .glass-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        }
        
        /* Glass Card */
        .glass-card {
            background: var(--glass);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            box-shadow: var(--shadow-md);
            transition: all var(--transition-normal) var(--ease);
            position: relative;
            overflow: hidden;
        }
        
        .glass-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
            border-color: rgba(255, 255, 255, 0.3);
        }
        
        .glass-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left var(--transition-slow) var(--ease);
        }
        
        .glass-card:hover::after {
            left: 100%;
        }
        
        /* Glass Button */
        .glass-btn {
            background: var(--glass);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: var(--border-radius);
            padding: 0.75rem 1.5rem;
            color: var(--text-primary);
            font-weight: 500;
            cursor: pointer;
            transition: all var(--transition-normal) var(--ease);
            position: relative;
            overflow: hidden;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .glass-btn:hover {
            transform: translateY(-1px);
            background: rgba(255, 255, 255, 0.15);
            border-color: rgba(255, 255, 255, 0.3);
            box-shadow: var(--shadow-md);
        }
        
        .glass-btn:active {
            transform: translateY(0);
        }
        
        .glass-btn.primary {
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            border: none;
        }
        
        .glass-btn.primary:hover {
            background: linear-gradient(135deg, 
                color-mix(in srgb, var(--primary) 80%, white), 
                color-mix(in srgb, var(--secondary) 80%, white));
        }
        """
    
    def generate_modern_animations(self) -> str:
        """Generate smooth modern animations"""
        return """
        /* Fade In Animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInLeft {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes fadeInRight {
            from {
                opacity: 0;
                transform: translateX(20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes scaleIn {
            from {
                opacity: 0;
                transform: scale(0.8);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
            }
            to {
                transform: translateX(0);
            }
        }
        
        @keyframes slideInLeft {
            from {
                transform: translateX(-100%);
            }
            to {
                transform: translateX(0);
            }
        }
        
        @keyframes bounce {
            0%, 20%, 53%, 80%, 100% {
                transform: translate3d(0, 0, 0);
            }
            40%, 43% {
                transform: translate3d(0, -8px, 0);
            }
            70% {
                transform: translate3d(0, -4px, 0);
            }
            90% {
                transform: translate3d(0, -2px, 0);
            }
        }
        
        @keyframes pulse {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.05);
            }
            100% {
                transform: scale(1);
            }
        }
        
        @keyframes shimmer {
            0% {
                background-position: -200% 0;
            }
            100% {
                background-position: 200% 0;
            }
        }
        
        @keyframes float {
            0%, 100% {
                transform: translateY(0px);
            }
            50% {
                transform: translateY(-6px);
            }
        }
        
        /* Animation Classes */
        .animate-fade-in-up {
            animation: fadeInUp var(--transition-slow) var(--ease) forwards;
        }
        
        .animate-fade-in-down {
            animation: fadeInDown var(--transition-slow) var(--ease) forwards;
        }
        
        .animate-fade-in-left {
            animation: fadeInLeft var(--transition-slow) var(--ease) forwards;
        }
        
        .animate-fade-in-right {
            animation: fadeInRight var(--transition-slow) var(--ease) forwards;
        }
        
        .animate-scale-in {
            animation: scaleIn var(--transition-normal) var(--elastic) forwards;
        }
        
        .animate-bounce {
            animation: bounce 1s var(--ease);
        }
        
        .animate-pulse {
            animation: pulse 2s infinite;
        }
        
        .animate-float {
            animation: float 3s ease-in-out infinite;
        }
        
        /* Staggered Animations */
        .stagger-fade-in > * {
            opacity: 0;
            animation: fadeInUp var(--transition-slow) var(--ease) forwards;
        }
        
        .stagger-fade-in > *:nth-child(1) { animation-delay: 0.1s; }
        .stagger-fade-in > *:nth-child(2) { animation-delay: 0.2s; }
        .stagger-fade-in > *:nth-child(3) { animation-delay: 0.3s; }
        .stagger-fade-in > *:nth-child(4) { animation-delay: 0.4s; }
        .stagger-fade-in > *:nth-child(5) { animation-delay: 0.5s; }
        .stagger-fade-in > *:nth-child(6) { animation-delay: 0.6s; }
        """
    
    def generate_interactive_components(self) -> str:
        """Generate interactive UI components"""
        return """
        /* Modern Tab System */
        .tab-container {
            background: var(--glass);
            backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border);
            border-radius: var(--border-radius-lg);
            overflow: hidden;
        }
        
        .tab-nav {
            display: flex;
            background: rgba(0, 0, 0, 0.2);
            border-bottom: 1px solid var(--glass-border);
        }
        
        .tab-btn {
            flex: 1;
            padding: 1rem 1.5rem;
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-weight: 500;
            cursor: pointer;
            transition: all var(--transition-normal) var(--ease);
            position: relative;
        }
        
        .tab-btn:hover {
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.05);
        }
        
        .tab-btn.active {
            color: var(--primary);
            background: rgba(99, 102, 241, 0.1);
        }
        
        .tab-btn.active::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--primary);
            border-radius: 3px 3px 0 0;
        }
        
        .tab-content {
            padding: 2rem;
            min-height: 300px;
        }
        
        .tab-pane {
            display: none;
            animation: fadeInUp var(--transition-normal) var(--ease);
        }
        
        .tab-pane.active {
            display: block;
        }
        
        /* Modern Cards */
        .metric-card {
            background: var(--glass);
            backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            transition: all var(--transition-normal) var(--ease);
            position: relative;
            overflow: hidden;
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-xl);
        }
        
        .metric-card .metric-icon {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
        }
        
        .metric-card .metric-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }
        
        .metric-card .metric-label {
            color: var(--text-secondary);
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        /* Progress Bars */
        .progress-bar {
            width: 100%;
            height: 8px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 4px;
            overflow: hidden;
            position: relative;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            border-radius: 4px;
            transition: width var(--transition-slow) var(--ease);
            position: relative;
        }
        
        .progress-fill::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            animation: shimmer 2s infinite;
        }
        
        /* Loading States */
        .skeleton {
            background: linear-gradient(90deg, 
                rgba(255, 255, 255, 0.1) 0%, 
                rgba(255, 255, 255, 0.2) 50%, 
                rgba(255, 255, 255, 0.1) 100%);
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
            border-radius: var(--border-radius);
        }
        
        .loading-spinner {
            width: 40px;
            height: 40px;
            border: 3px solid rgba(255, 255, 255, 0.1);
            border-top: 3px solid var(--primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Notification Styles */
        .notification {
            background: var(--glass);
            backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: var(--border-radius);
            padding: 1rem 1.5rem;
            margin-bottom: 1rem;
            position: relative;
            overflow: hidden;
            animation: slideInRight var(--transition-normal) var(--ease);
        }
        
        .notification.success {
            border-left: 4px solid var(--success);
        }
        
        .notification.warning {
            border-left: 4px solid var(--warning);
        }
        
        .notification.error {
            border-left: 4px solid var(--error);
        }
        
        .notification.info {
            border-left: 4px solid var(--accent);
        }
        """
    
    def generate_responsive_layout(self) -> str:
        """Generate responsive layout system"""
        return """
        /* Container System */
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1rem;
        }
        
        .container-fluid {
            width: 100%;
            padding: 0 1rem;
        }
        
        /* Grid System */
        .grid {
            display: grid;
            gap: 1.5rem;
        }
        
        .grid-cols-1 { grid-template-columns: repeat(1, 1fr); }
        .grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
        .grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
        .grid-cols-4 { grid-template-columns: repeat(4, 1fr); }
        
        /* Flexbox Utilities */
        .flex { display: flex; }
        .flex-col { flex-direction: column; }
        .flex-wrap { flex-wrap: wrap; }
        .items-center { align-items: center; }
        .items-start { align-items: flex-start; }
        .items-end { align-items: flex-end; }
        .justify-center { justify-content: center; }
        .justify-between { justify-content: space-between; }
        .justify-around { justify-content: space-around; }
        .gap-1 { gap: 0.25rem; }
        .gap-2 { gap: 0.5rem; }
        .gap-3 { gap: 0.75rem; }
        .gap-4 { gap: 1rem; }
        .gap-6 { gap: 1.5rem; }
        .gap-8 { gap: 2rem; }
        
        /* Spacing */
        .p-1 { padding: 0.25rem; }
        .p-2 { padding: 0.5rem; }
        .p-3 { padding: 0.75rem; }
        .p-4 { padding: 1rem; }
        .p-6 { padding: 1.5rem; }
        .p-8 { padding: 2rem; }
        
        .m-1 { margin: 0.25rem; }
        .m-2 { margin: 0.5rem; }
        .m-3 { margin: 0.75rem; }
        .m-4 { margin: 1rem; }
        .m-6 { margin: 1.5rem; }
        .m-8 { margin: 2rem; }
        
        .mb-2 { margin-bottom: 0.5rem; }
        .mb-4 { margin-bottom: 1rem; }
        .mb-6 { margin-bottom: 1.5rem; }
        .mt-2 { margin-top: 0.5rem; }
        .mt-4 { margin-top: 1rem; }
        .mt-6 { margin-top: 1.5rem; }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .container {
                padding: 0 0.5rem;
            }
            
            .grid-cols-2,
            .grid-cols-3,
            .grid-cols-4 {
                grid-template-columns: 1fr;
            }
            
            .tab-nav {
                flex-direction: column;
            }
            
            .metric-card {
                padding: 1rem;
            }
            
            h1 { font-size: 2rem; }
            h2 { font-size: 1.5rem; }
        }
        
        @media (max-width: 480px) {
            .container {
                padding: 0 0.25rem;
            }
            
            .glass-card {
                padding: 1rem;
            }
            
            .tab-content {
                padding: 1rem;
            }
        }
        
        /* Utility Classes */
        .text-center { text-align: center; }
        .text-left { text-align: left; }
        .text-right { text-align: right; }
        
        .font-bold { font-weight: 700; }
        .font-semibold { font-weight: 600; }
        .font-medium { font-weight: 500; }
        
        .text-sm { font-size: 0.875rem; }
        .text-lg { font-size: 1.125rem; }
        .text-xl { font-size: 1.25rem; }
        .text-2xl { font-size: 1.5rem; }
        
        .opacity-50 { opacity: 0.5; }
        .opacity-75 { opacity: 0.75; }
        
        .cursor-pointer { cursor: pointer; }
        .cursor-not-allowed { cursor: not-allowed; }
        
        .select-none { user-select: none; }
        
        .hidden { display: none; }
        .block { display: block; }
        .inline-block { display: inline-block; }
        
        .relative { position: relative; }
        .absolute { position: absolute; }
        .fixed { position: fixed; }
        
        .w-full { width: 100%; }
        .h-full { height: 100%; }
        .min-h-screen { min-height: 100vh; }
        """
    
    def generate_chart_styles(self) -> str:
        """Generate styles for charts and data visualization"""
        return """
        /* Chart Container */
        .chart-container {
            background: var(--glass);
            backdrop-filter: blur(16px);
            border: 1px solid var(--glass-border);
            border-radius: var(--border-radius-lg);
            padding: 1.5rem;
            margin-bottom: 2rem;
            position: relative;
        }
        
        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        
        .chart-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .chart-subtitle {
            font-size: 0.875rem;
            color: var(--text-secondary);
            margin-top: 0.25rem;
        }
        
        .chart-canvas {
            max-height: 400px;
            position: relative;
        }
        
        /* Legend Styles */
        .chart-legend {
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-top: 1rem;
            justify-content: center;
        }
        
        .legend-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
            color: var(--text-secondary);
        }
        
        .legend-color {
            width: 12px;
            height: 12px;
            border-radius: 2px;
        }
        
        /* Data Table */
        .data-table {
            width: 100%;
            border-collapse: collapse;
            background: var(--glass);
            backdrop-filter: blur(16px);
            border-radius: var(--border-radius);
            overflow: hidden;
            border: 1px solid var(--glass-border);
        }
        
        .data-table th {
            background: rgba(0, 0, 0, 0.2);
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            color: var(--text-primary);
            border-bottom: 1px solid var(--glass-border);
        }
        
        .data-table td {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            color: var(--text-secondary);
            transition: background var(--transition-fast) var(--ease);
        }
        
        .data-table tr:hover td {
            background: rgba(255, 255, 255, 0.05);
        }
        
        .data-table tr:last-child td {
            border-bottom: none;
        }
        """
    
    def generate_complete_css(self) -> str:
        """Generate complete CSS with all components including stable charts and pagination"""
        return (
            self.generate_base_styles() +
            self.generate_stable_chart_styles() +
            self.generate_pagination_styles() +
            self.generate_media_panel_styles() +
            self.generate_tab_styles() +
            self.generate_glass_components() +
            self.generate_modern_animations() +
            self.generate_interactive_components() +
            self.generate_responsive_layout() +
            self.generate_chart_styles()
        )
    
    def generate_javascript_animations(self) -> str:
        """Generate JavaScript for advanced animations"""
        return """
        // Advanced Animation Controller
        class AnimationController {
            constructor() {
                this.observers = new Map();
                this.initializeObservers();
            }
            
            initializeObservers() {
                // Intersection Observer for scroll animations
                this.intersectionObserver = new IntersectionObserver(
                    (entries) => this.handleIntersection(entries),
                    { threshold: 0.1, rootMargin: '50px' }
                );
                
                // Start observing elements
                this.observeElements();
            }
            
            observeElements() {
                // Observe elements with animation classes
                document.querySelectorAll('[data-animate]').forEach(el => {
                    this.intersectionObserver.observe(el);
                });
            }
            
            handleIntersection(entries) {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const element = entry.target;
                        const animationType = element.dataset.animate;
                        this.triggerAnimation(element, animationType);
                        this.intersectionObserver.unobserve(element);
                    }
                });
            }
            
            triggerAnimation(element, type) {
                switch (type) {
                    case 'fade-up':
                        element.classList.add('animate-fade-in-up');
                        break;
                    case 'fade-down':
                        element.classList.add('animate-fade-in-down');
                        break;
                    case 'fade-left':
                        element.classList.add('animate-fade-in-left');
                        break;
                    case 'fade-right':
                        element.classList.add('animate-fade-in-right');
                        break;
                    case 'scale':
                        element.classList.add('animate-scale-in');
                        break;
                    case 'bounce':
                        element.classList.add('animate-bounce');
                        break;
                    default:
                        element.classList.add('animate-fade-in-up');
                }
            }
            
            // Stagger animation for multiple elements
            staggerAnimation(selector, delay = 100) {
                const elements = document.querySelectorAll(selector);
                elements.forEach((el, index) => {
                    setTimeout(() => {
                        el.classList.add('animate-fade-in-up');
                    }, index * delay);
                });
            }
            
            // Parallax effect
            initParallax() {
                window.addEventListener('scroll', () => {
                    const scrolled = window.pageYOffset;
                    const parallaxElements = document.querySelectorAll('[data-parallax]');
                    
                    parallaxElements.forEach(el => {
                        const speed = el.dataset.parallax || 0.5;
                        const yPos = -(scrolled * speed);
                        el.style.transform = `translateY(${yPos}px)`;
                    });
                });
            }
            
            // Smooth transitions for dynamic content
            fadeInContent(element, duration = 300) {
                element.style.opacity = '0';
                element.style.transform = 'translateY(20px)';
                element.style.transition = `all ${duration}ms cubic-bezier(0.4, 0, 0.2, 1)`;
                
                requestAnimationFrame(() => {
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                });
            }
            
            // Loading animation
            showLoading(container) {
                container.innerHTML = `
                    <div class="flex items-center justify-center p-8">
                        <div class="loading-spinner"></div>
                        <span class="ml-3 text-secondary">Loading...</span>
                    </div>
                `;
            }
            
            // Success animation
            showSuccess(message, duration = 3000) {
                const notification = document.createElement('div');
                notification.className = 'notification success fixed top-4 right-4 z-50';
                notification.innerHTML = `
                    <div class="flex items-center gap-3">
                        <i class="fas fa-check-circle text-success"></i>
                        <span>${message}</span>
                    </div>
                `;
                
                document.body.appendChild(notification);
                
                setTimeout(() => {
                    notification.style.animation = 'slideInLeft 0.3s ease forwards';
                    setTimeout(() => notification.remove(), 300);
                }, duration);
            }
            
            // Error animation
            showError(message, duration = 5000) {
                const notification = document.createElement('div');
                notification.className = 'notification error fixed top-4 right-4 z-50';
                notification.innerHTML = `
                    <div class="flex items-center gap-3">
                        <i class="fas fa-exclamation-circle text-error"></i>
                        <span>${message}</span>
                    </div>
                `;
                
                document.body.appendChild(notification);
                
                setTimeout(() => {
                    notification.style.animation = 'slideInLeft 0.3s ease forwards';
                    setTimeout(() => notification.remove(), 300);
                }, duration);
            }
            
            // Morphing number animation
            animateNumber(element, start, end, duration = 1000) {
                const startTime = performance.now();
                const difference = end - start;
                
                const updateNumber = (currentTime) => {
                    const elapsed = currentTime - startTime;
                    const progress = Math.min(elapsed / duration, 1);
                    
                    // Easing function
                    const easeOutQuart = 1 - Math.pow(1 - progress, 4);
                    const current = start + (difference * easeOutQuart);
                    
                    element.textContent = Math.round(current).toLocaleString();
                    
                    if (progress < 1) {
                        requestAnimationFrame(updateNumber);
                    }
                };
                
                requestAnimationFrame(updateNumber);
            }
            
            // Progress bar animation
            animateProgress(element, targetPercent, duration = 1000) {
                const progressFill = element.querySelector('.progress-fill');
                if (!progressFill) return;
                
                progressFill.style.width = '0%';
                
                requestAnimationFrame(() => {
                    progressFill.style.transition = `width ${duration}ms cubic-bezier(0.4, 0, 0.2, 1)`;
                    progressFill.style.width = `${targetPercent}%`;
                });
            }
        }
        
        // Initialize animation controller
        const animationController = new AnimationController();
        
        // Initialize when DOM is loaded
        document.addEventListener('DOMContentLoaded', () => {
            animationController.initParallax();
            
            // Add smooth scrolling to anchor links
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function (e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                });
            });
        });
        
        // Export for global use
        window.animationController = animationController;
        """

# Global UI generator instance
ui_generator = ModernUIGenerator()
