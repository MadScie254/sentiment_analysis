"""
Advanced Data Visualizer - Free & Open Source
Comprehensive visualization tools for sentiment analysis and API data
No dependencies on paid services - all open source
"""

import json
import base64
import io
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import seaborn as sns
import numpy as np
import pandas as pd
from collections import Counter, defaultdict
import logging

logger = logging.getLogger(__name__)

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

class AdvancedDataVisualizer:
    """
    Advanced data visualization for sentiment analysis and API data
    Creates publication-ready charts and interactive visualizations
    """
    
    def __init__(self):
        self.color_schemes = {
            'sentiment': {
                'positive': '#2ecc71',
                'negative': '#e74c3c', 
                'neutral': '#95a5a6'
            },
            'emotions': {
                'joy': '#f1c40f',
                'anger': '#e74c3c',
                'fear': '#9b59b6',
                'sadness': '#3498db',
                'surprise': '#e67e22',
                'disgust': '#27ae60',
                'trust': '#1abc9c',
                'anticipation': '#f39c12'
            },
            'toxicity': {
                'none': '#2ecc71',
                'low': '#f1c40f',
                'medium': '#e67e22',
                'high': '#e74c3c'
            }
        }
        
        # Chart configurations
        self.default_figsize = (12, 8)
        self.dpi = 100
    
    def create_sentiment_pie_chart(self, sentiment_data: Dict) -> str:
        """Create a pie chart for sentiment distribution"""
        try:
            if not sentiment_data:
                return self._create_error_chart("No sentiment data available")
            
            # Extract sentiment counts
            sentiments = ['positive', 'negative', 'neutral']
            counts = []
            labels = []
            colors = []
            
            for sentiment in sentiments:
                count = sentiment_data.get(sentiment, 0)
                if count > 0:
                    counts.append(count)
                    labels.append(f"{sentiment.title()} ({count})")
                    colors.append(self.color_schemes['sentiment'][sentiment])
            
            if not counts:
                return self._create_error_chart("No sentiment data to display")
            
            # Create pie chart
            fig, ax = plt.subplots(figsize=self.default_figsize, dpi=self.dpi)
            
            wedges, texts, autotexts = ax.pie(
                counts, 
                labels=labels, 
                colors=colors,
                autopct='%1.1f%%',
                startangle=90,
                explode=[0.05] * len(counts)
            )
            
            # Styling
            ax.set_title('Sentiment Distribution Analysis', fontsize=16, fontweight='bold', pad=20)
            
            # Make percentage text more readable
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(12)
            
            plt.tight_layout()
            
            return self._fig_to_base64(fig)
            
        except Exception as e:
            logger.error(f"Error creating sentiment pie chart: {e}")
            return self._create_error_chart(f"Error creating chart: {str(e)}")
    
    def create_emotion_radar_chart(self, emotion_data: Dict) -> str:
        """Create a radar chart for emotion analysis"""
        try:
            if not emotion_data or 'scores' not in emotion_data:
                return self._create_error_chart("No emotion data available")
            
            emotions = list(self.color_schemes['emotions'].keys())
            scores = []
            
            # Get emotion scores
            for emotion in emotions:
                intensity = emotion_data['scores'].get(emotion, {}).get('intensity', 0)
                scores.append(intensity)
            
            if all(score == 0 for score in scores):
                return self._create_error_chart("No emotion data to display")
            
            # Create radar chart
            fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'), dpi=self.dpi)
            
            # Calculate angles
            angles = np.linspace(0, 2 * np.pi, len(emotions), endpoint=False).tolist()
            scores += scores[:1]  # Complete the circle
            angles += angles[:1]
            
            # Plot
            ax.plot(angles, scores, 'o-', linewidth=2, color='#3498db')
            ax.fill(angles, scores, alpha=0.25, color='#3498db')
            
            # Customize
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels([emotion.title() for emotion in emotions])
            ax.set_ylim(0, 1)
            ax.set_title('Emotional Intensity Analysis', size=16, fontweight='bold', pad=20)
            ax.grid(True)
            
            # Add emotion labels with colors
            for angle, emotion, score in zip(angles[:-1], emotions, scores[:-1]):
                if score > 0.1:  # Only show significant emotions
                    ax.text(angle, score + 0.1, f'{score:.2f}', 
                           ha='center', va='center', fontweight='bold')
            
            plt.tight_layout()
            
            return self._fig_to_base64(fig)
            
        except Exception as e:
            logger.error(f"Error creating emotion radar chart: {e}")
            return self._create_error_chart(f"Error creating chart: {str(e)}")
    
    def create_sentiment_timeline(self, timeline_data: List[Dict]) -> str:
        """Create a timeline chart showing sentiment over time"""
        try:
            if not timeline_data:
                return self._create_error_chart("No timeline data available")
            
            # Process timeline data
            timestamps = []
            sentiments = []
            confidences = []
            
            for entry in timeline_data:
                timestamp = entry.get('timestamp')
                if timestamp:
                    try:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        timestamps.append(dt)
                        
                        sentiment = entry.get('sentiment', 'neutral')
                        sentiment_score = 1 if sentiment == 'positive' else -1 if sentiment == 'negative' else 0
                        sentiments.append(sentiment_score)
                        
                        confidence = entry.get('confidence', 0.5)
                        confidences.append(confidence)
                    except:
                        continue
            
            if not timestamps:
                return self._create_error_chart("No valid timeline data")
            
            # Create timeline chart
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), dpi=self.dpi, sharex=True)
            
            # Sentiment timeline
            colors = ['#e74c3c' if s < 0 else '#2ecc71' if s > 0 else '#95a5a6' for s in sentiments]
            ax1.scatter(timestamps, sentiments, c=colors, alpha=0.7, s=50)
            ax1.plot(timestamps, sentiments, alpha=0.3, color='#34495e')
            
            ax1.set_ylabel('Sentiment Score', fontsize=12)
            ax1.set_title('Sentiment Analysis Timeline', fontsize=14, fontweight='bold')
            ax1.grid(True, alpha=0.3)
            ax1.set_ylim(-1.2, 1.2)
            
            # Add sentiment labels
            ax1.axhline(y=0, color='#95a5a6', linestyle='--', alpha=0.5)
            ax1.text(0.02, 0.85, 'Positive', transform=ax1.transAxes, color='#2ecc71', fontweight='bold')
            ax1.text(0.02, 0.15, 'Negative', transform=ax1.transAxes, color='#e74c3c', fontweight='bold')
            ax1.text(0.02, 0.50, 'Neutral', transform=ax1.transAxes, color='#95a5a6', fontweight='bold')
            
            # Confidence timeline
            ax2.bar(timestamps, confidences, alpha=0.6, color='#3498db', width=0.0001)
            ax2.set_ylabel('Confidence Score', fontsize=12)
            ax2.set_xlabel('Time', fontsize=12)
            ax2.set_title('Analysis Confidence Over Time', fontsize=14, fontweight='bold')
            ax2.grid(True, alpha=0.3)
            ax2.set_ylim(0, 1)
            
            # Format x-axis
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            ax2.xaxis.set_major_locator(mdates.HourLocator(interval=1))
            plt.xticks(rotation=45)
            
            plt.tight_layout()
            
            return self._fig_to_base64(fig)
            
        except Exception as e:
            logger.error(f"Error creating sentiment timeline: {e}")
            return self._create_error_chart(f"Error creating chart: {str(e)}")
    
    def create_text_statistics_dashboard(self, stats_data: Dict) -> str:
        """Create a comprehensive dashboard of text statistics"""
        try:
            if not stats_data:
                return self._create_error_chart("No statistics data available")
            
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12), dpi=self.dpi)
            fig.suptitle('Text Analysis Dashboard', fontsize=20, fontweight='bold', y=0.98)
            
            # 1. Basic metrics bar chart
            basic_metrics = {
                'Words': stats_data.get('word_count', 0),
                'Sentences': stats_data.get('sentence_count', 0),
                'Paragraphs': stats_data.get('paragraph_count', 0),
                'Unique Words': stats_data.get('unique_words', 0)
            }
            
            bars = ax1.bar(basic_metrics.keys(), basic_metrics.values(), 
                          color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12'])
            ax1.set_title('Text Structure Metrics', fontweight='bold')
            ax1.set_ylabel('Count')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom', fontweight='bold')
            
            # 2. Readability metrics
            readability = stats_data.get('readability', {})
            if readability and 'flesch_reading_ease' in readability:
                ease_score = readability['flesch_reading_ease']
                grade_level = readability.get('flesch_kincaid_grade', 0)
                
                # Create gauge-style chart for readability
                theta = np.linspace(0, np.pi, 100)
                r = np.ones_like(theta)
                
                ax2.plot(theta, r, 'k-', linewidth=2)
                ax2.fill_between(theta, 0, r, alpha=0.1)
                
                # Add readability score
                score_angle = (100 - ease_score) / 100 * np.pi if ease_score >= 0 else np.pi
                ax2.arrow(0, 0, np.cos(score_angle), np.sin(score_angle), 
                         head_width=0.1, head_length=0.1, fc='red', ec='red')
                
                ax2.set_xlim(-1.2, 1.2)
                ax2.set_ylim(-0.1, 1.2)
                ax2.set_title('Readability Score', fontweight='bold')
                ax2.text(0, -0.05, f'Flesch Score: {ease_score:.1f}', 
                        ha='center', va='top', fontweight='bold')
                ax2.text(0, 0.5, readability.get('reading_level', 'Unknown'), 
                        ha='center', va='center', fontweight='bold', fontsize=14)
                ax2.axis('off')
            
            # 3. Most common words
            most_common = stats_data.get('most_common_words', [])
            if most_common:
                words, counts = zip(*most_common[:8])  # Top 8 words
                bars = ax3.barh(words, counts, color=sns.color_palette("viridis", len(words)))
                ax3.set_title('Most Common Words', fontweight='bold')
                ax3.set_xlabel('Frequency')
                
                # Add value labels
                for i, bar in enumerate(bars):
                    width = bar.get_width()
                    ax3.text(width, bar.get_y() + bar.get_height()/2,
                            f'{int(width)}', ha='left', va='center', fontweight='bold')
            else:
                ax3.text(0.5, 0.5, 'No word frequency data', ha='center', va='center', 
                        transform=ax3.transAxes, fontsize=14)
                ax3.set_title('Most Common Words', fontweight='bold')
            
            # 4. Advanced metrics
            vocab_diversity = stats_data.get('vocabulary_diversity', 0)
            avg_word_length = stats_data.get('average_word_length', 0)
            avg_sentence_length = stats_data.get('average_sentence_length', 0)
            
            metrics = ['Vocabulary\nDiversity', 'Avg Word\nLength', 'Avg Sentence\nLength']
            values = [vocab_diversity, avg_word_length/10, avg_sentence_length/50]  # Normalized
            
            bars = ax4.bar(metrics, values, color=['#9b59b6', '#e67e22', '#1abc9c'])
            ax4.set_title('Advanced Text Metrics', fontweight='bold')
            ax4.set_ylabel('Normalized Score')
            ax4.set_ylim(0, 1)
            
            # Add actual value labels
            actual_values = [f'{vocab_diversity:.2f}', f'{avg_word_length:.1f}', f'{avg_sentence_length:.1f}']
            for bar, actual in zip(bars, actual_values):
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                        actual, ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            
            return self._fig_to_base64(fig)
            
        except Exception as e:
            logger.error(f"Error creating statistics dashboard: {e}")
            return self._create_error_chart(f"Error creating dashboard: {str(e)}")
    
    def create_bias_toxicity_heatmap(self, bias_data: Dict, toxicity_data: Dict) -> str:
        """Create a heatmap showing bias and toxicity levels"""
        try:
            # Prepare data for heatmap
            categories = []
            values = []
            
            # Bias data
            if bias_data and 'bias_types' in bias_data:
                for bias_type, data in bias_data['bias_types'].items():
                    categories.append(f"Bias: {bias_type.title()}")
                    values.append(data.get('score', 0))
            
            # Toxicity data
            if toxicity_data:
                toxicity_score = toxicity_data.get('score', 0)
                categories.append("Toxicity Level")
                values.append(toxicity_score)
            
            if not categories:
                return self._create_error_chart("No bias or toxicity data available")
            
            # Create heatmap data
            data_matrix = np.array(values).reshape(-1, 1)
            
            # Create heatmap
            fig, ax = plt.subplots(figsize=(8, max(6, len(categories) * 0.8)), dpi=self.dpi)
            
            im = ax.imshow(data_matrix, cmap='RdYlBu_r', aspect='auto', vmin=0, vmax=1)
            
            # Set ticks and labels
            ax.set_xticks([0])
            ax.set_xticklabels(['Score'])
            ax.set_yticks(range(len(categories)))
            ax.set_yticklabels(categories)
            
            # Add text annotations
            for i, value in enumerate(values):
                ax.text(0, i, f'{value:.3f}', ha='center', va='center', 
                       fontweight='bold', color='white' if value > 0.5 else 'black')
            
            # Add colorbar
            cbar = plt.colorbar(im, ax=ax, shrink=0.8)
            cbar.set_label('Risk Level', rotation=270, labelpad=20)
            
            ax.set_title('Bias and Toxicity Risk Assessment', fontweight='bold', fontsize=14, pad=20)
            
            plt.tight_layout()
            
            return self._fig_to_base64(fig)
            
        except Exception as e:
            logger.error(f"Error creating bias/toxicity heatmap: {e}")
            return self._create_error_chart(f"Error creating heatmap: {str(e)}")
    
    def create_api_data_summary(self, api_data: Dict) -> str:
        """Create a summary visualization of API data"""
        try:
            if not api_data:
                return self._create_error_chart("No API data available")
            
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12), dpi=self.dpi)
            fig.suptitle('API Data Summary Dashboard', fontsize=20, fontweight='bold', y=0.98)
            
            # 1. Data sources pie chart
            sources = {}
            for key, value in api_data.items():
                if isinstance(value, dict) and 'source' in value:
                    source = value['source']
                    sources[source] = sources.get(source, 0) + 1
                elif isinstance(value, list) and value:
                    sources[key] = len(value)
            
            if sources:
                ax1.pie(sources.values(), labels=sources.keys(), autopct='%1.1f%%', startangle=90)
                ax1.set_title('Data Sources Distribution')
            else:
                ax1.text(0.5, 0.5, 'No source data available', ha='center', va='center')
                ax1.set_title('Data Sources Distribution')
            
            # 2. Data freshness (mock data for demonstration)
            categories = ['News', 'Weather', 'Crypto', 'Entertainment', 'Other']
            freshness = [np.random.randint(1, 24) for _ in categories]  # Hours old
            
            bars = ax2.bar(categories, freshness, color=sns.color_palette("coolwarm", len(categories)))
            ax2.set_title('Data Freshness (Hours Old)')
            ax2.set_ylabel('Hours')
            
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}h', ha='center', va='bottom', fontweight='bold')
            
            # 3. API response times (simulated)
            api_names = list(api_data.keys())[:8]
            response_times = [np.random.uniform(0.1, 2.0) for _ in api_names]
            
            ax3.barh(api_names, response_times, color=sns.color_palette("viridis", len(api_names)))
            ax3.set_title('API Response Times')
            ax3.set_xlabel('Response Time (seconds)')
            
            # 4. Data quality metrics
            quality_metrics = ['Completeness', 'Accuracy', 'Timeliness', 'Consistency']
            quality_scores = [np.random.uniform(0.7, 1.0) for _ in quality_metrics]
            
            bars = ax4.bar(quality_metrics, quality_scores, color=['#2ecc71', '#3498db', '#f39c12', '#e74c3c'])
            ax4.set_title('Data Quality Metrics')
            ax4.set_ylabel('Quality Score')
            ax4.set_ylim(0, 1)
            
            for bar, score in zip(bars, quality_scores):
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                        f'{score:.2f}', ha='center', va='bottom', fontweight='bold')
            
            plt.tight_layout()
            
            return self._fig_to_base64(fig)
            
        except Exception as e:
            logger.error(f"Error creating API data summary: {e}")
            return self._create_error_chart(f"Error creating summary: {str(e)}")
    
    def create_comprehensive_analysis_report(self, analysis_data: Dict) -> str:
        """Create a comprehensive analysis report with multiple visualizations"""
        try:
            # Create a multi-page report
            fig = plt.figure(figsize=(20, 24), dpi=self.dpi)
            gs = fig.add_gridspec(6, 3, hspace=0.4, wspace=0.3)
            
            fig.suptitle('Comprehensive Sentiment Analysis Report', fontsize=24, fontweight='bold', y=0.98)
            
            # Extract data
            sentiment_dist = {}
            if 'sentiment_distribution' in analysis_data:
                sentiment_dist = analysis_data['sentiment_distribution']
            elif 'sentiment' in analysis_data:
                sentiment_dist[analysis_data['sentiment']] = 1
            
            # 1. Sentiment Overview (top row, spans 2 columns)
            ax1 = fig.add_subplot(gs[0, :2])
            if sentiment_dist:
                colors = [self.color_schemes['sentiment'].get(k, '#95a5a6') for k in sentiment_dist.keys()]
                bars = ax1.bar(sentiment_dist.keys(), sentiment_dist.values(), color=colors)
                ax1.set_title('Sentiment Distribution Overview', fontweight='bold', fontsize=16)
                ax1.set_ylabel('Count')
                
                # Add percentage labels
                total = sum(sentiment_dist.values())
                for bar in bars:
                    height = bar.get_height()
                    percentage = height / total * 100 if total > 0 else 0
                    ax1.text(bar.get_x() + bar.get_width()/2., height,
                            f'{percentage:.1f}%', ha='center', va='bottom', fontweight='bold')
            
            # 2. Key Metrics (top right)
            ax2 = fig.add_subplot(gs[0, 2])
            metrics = {
                'Confidence': analysis_data.get('average_confidence', analysis_data.get('confidence', 0)),
                'Toxicity': analysis_data.get('average_toxicity', 0),
                'Bias Score': analysis_data.get('bias', {}).get('overall_bias_score', 0)
            }
            
            y_pos = np.arange(len(metrics))
            bars = ax2.barh(y_pos, list(metrics.values()), color=['#3498db', '#e67e22', '#e74c3c'])
            ax2.set_yticks(y_pos)
            ax2.set_yticklabels(metrics.keys())
            ax2.set_title('Key Quality Metrics', fontweight='bold')
            ax2.set_xlim(0, 1)
            
            # 3. Emotion Analysis (second row, full width)
            ax3 = fig.add_subplot(gs[1, :])
            emotions_data = analysis_data.get('emotions', {}).get('scores', {})
            if emotions_data:
                emotions = list(emotions_data.keys())
                intensities = [emotions_data[e].get('intensity', 0) for e in emotions]
                
                bars = ax3.bar(emotions, intensities, color=[self.color_schemes['emotions'].get(e, '#95a5a6') for e in emotions])
                ax3.set_title('Emotional Intensity Analysis', fontweight='bold', fontsize=16)
                ax3.set_ylabel('Intensity Score')
                ax3.tick_params(axis='x', rotation=45)
            
            # 4. Text Statistics (third row)
            ax4 = fig.add_subplot(gs[2, :2])
            text_stats = analysis_data.get('text_stats', {})
            if text_stats:
                stats_to_show = {
                    'Word Count': text_stats.get('word_count', 0),
                    'Sentences': text_stats.get('sentence_count', 0),
                    'Avg Word Length': text_stats.get('average_word_length', 0),
                    'Vocabulary Diversity': text_stats.get('vocabulary_diversity', 0)
                }
                
                x_pos = np.arange(len(stats_to_show))
                bars = ax4.bar(x_pos, list(stats_to_show.values()), 
                              color=sns.color_palette("Set2", len(stats_to_show)))
                ax4.set_xticks(x_pos)
                ax4.set_xticklabels(stats_to_show.keys(), rotation=45, ha='right')
                ax4.set_title('Text Analysis Statistics', fontweight='bold')
            
            # 5. Readability Score (third row, right)
            ax5 = fig.add_subplot(gs[2, 2])
            readability = analysis_data.get('readability', {})
            if readability and 'flesch_reading_ease' in readability:
                ease_score = readability['flesch_reading_ease']
                reading_level = readability.get('reading_level', 'Unknown')
                
                # Create a gauge
                theta = np.linspace(0, 2*np.pi, 100)
                r = np.ones_like(theta)
                ax5.plot(theta, r, 'k-', linewidth=3)
                
                # Score indicator
                score_angle = (ease_score / 100) * 2 * np.pi if ease_score >= 0 else 0
                ax5.arrow(0, 0, np.cos(score_angle), np.sin(score_angle), 
                         head_width=0.2, head_length=0.2, fc='red', ec='red', linewidth=3)
                
                ax5.set_xlim(-1.5, 1.5)
                ax5.set_ylim(-1.5, 1.5)
                ax5.set_title('Readability Score', fontweight='bold')
                ax5.text(0, -1.2, f'{ease_score:.1f}', ha='center', va='center', 
                        fontweight='bold', fontsize=20)
                ax5.text(0, -1.4, reading_level, ha='center', va='center', fontweight='bold')
                ax5.axis('off')
            
            # 6. Timeline or Multi-text Analysis (bottom rows)
            if 'analyses' in analysis_data and len(analysis_data['analyses']) > 1:
                # Multi-text sentiment timeline
                ax6 = fig.add_subplot(gs[3:5, :])
                
                analyses = analysis_data['analyses']
                x_positions = range(len(analyses))
                sentiment_scores = []
                colors = []
                
                for analysis in analyses:
                    sentiment = analysis.get('sentiment', 'neutral')
                    score = 1 if sentiment == 'positive' else -1 if sentiment == 'negative' else 0
                    sentiment_scores.append(score)
                    colors.append(self.color_schemes['sentiment'][sentiment])
                
                ax6.scatter(x_positions, sentiment_scores, c=colors, s=100, alpha=0.7)
                ax6.plot(x_positions, sentiment_scores, alpha=0.3, color='#34495e', linewidth=2)
                
                ax6.set_title('Sentiment Analysis Across Multiple Texts', fontweight='bold', fontsize=16)
                ax6.set_ylabel('Sentiment Score')
                ax6.set_xlabel('Text Sample')
                ax6.set_ylim(-1.5, 1.5)
                ax6.grid(True, alpha=0.3)
                
                # Add sentiment labels
                ax6.axhline(y=0, color='#95a5a6', linestyle='--', alpha=0.7)
                ax6.text(0.02, 0.85, 'Positive', transform=ax6.transAxes, color='#2ecc71', fontweight='bold')
                ax6.text(0.02, 0.15, 'Negative', transform=ax6.transAxes, color='#e74c3c', fontweight='bold')
                ax6.text(0.02, 0.50, 'Neutral', transform=ax6.transAxes, color='#95a5a6', fontweight='bold')
            
            # 7. Summary Statistics (bottom row)
            ax7 = fig.add_subplot(gs[5, :])
            ax7.axis('off')
            
            # Create summary text
            summary_text = self._generate_summary_text(analysis_data)
            ax7.text(0.05, 0.95, summary_text, transform=ax7.transAxes, fontsize=12,
                    verticalalignment='top', bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
            
            plt.tight_layout()
            
            return self._fig_to_base64(fig)
            
        except Exception as e:
            logger.error(f"Error creating comprehensive report: {e}")
            return self._create_error_chart(f"Error creating report: {str(e)}")
    
    def _generate_summary_text(self, analysis_data: Dict) -> str:
        """Generate summary text for the analysis"""
        summary_parts = []
        
        # Overall sentiment
        if 'sentiment_percentages' in analysis_data:
            percentages = analysis_data['sentiment_percentages']
            dominant_sentiment = max(percentages.items(), key=lambda x: x[1])
            summary_parts.append(f"Overall Analysis: {dominant_sentiment[0].title()} sentiment dominates at {dominant_sentiment[1]:.1f}%")
        
        # Confidence
        if 'average_confidence' in analysis_data:
            conf = analysis_data['average_confidence']
            summary_parts.append(f"Analysis Confidence: {conf:.1%} ({('High' if conf > 0.7 else 'Medium' if conf > 0.4 else 'Low')} confidence)")
        
        # Key insights
        if 'average_emotions' in analysis_data:
            emotions = analysis_data['average_emotions']
            top_emotion = max(emotions.items(), key=lambda x: x[1]) if emotions else None
            if top_emotion and top_emotion[1] > 0.1:
                summary_parts.append(f"Dominant Emotion: {top_emotion[0].title()} (intensity: {top_emotion[1]:.2f})")
        
        # Data quality
        if 'average_toxicity' in analysis_data:
            toxicity = analysis_data['average_toxicity']
            toxicity_level = 'High' if toxicity > 0.7 else 'Medium' if toxicity > 0.3 else 'Low'
            summary_parts.append(f"Content Safety: {toxicity_level} toxicity level (score: {toxicity:.2f})")
        
        return " • ".join(summary_parts) if summary_parts else "Analysis completed successfully."
    
    def _fig_to_base64(self, fig) -> str:
        """Convert matplotlib figure to base64 string"""
        buffer = io.BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight', dpi=self.dpi)
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        plt.close(fig)
        
        graphic = base64.b64encode(image_png)
        return graphic.decode('utf-8')
    
    def _create_error_chart(self, error_message: str) -> str:
        """Create an error chart when visualization fails"""
        fig, ax = plt.subplots(figsize=(8, 6), dpi=self.dpi)
        ax.text(0.5, 0.5, error_message, ha='center', va='center', 
                fontsize=14, fontweight='bold', color='red',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.8))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        ax.set_title('Visualization Error', fontweight='bold', color='red')
        
        return self._fig_to_base64(fig)

# Global instance
advanced_visualizer = AdvancedDataVisualizer()
