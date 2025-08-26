import re
from typing import List, Dict, Set
from textblob import TextBlob

class EmotionDetector:
    """
    Emotion detection system for social media content
    Detects: anger, joy, sadness, excitement, sarcasm, fear, surprise, disgust
    """
    
    def __init__(self):
        self.emotion_lexicon = {
            'anger': {
                'keywords': [
                    'angry', 'mad', 'furious', 'pissed', 'annoyed', 'irritated',
                    'rage', 'hate', 'damn', 'fuck', 'shit', 'stupid', 'idiot',
                    'wtf', 'tf', 'annoying', 'frustrated', 'fed up', 'hasira'
                ],
                'patterns': [r'!{2,}', r'[A-Z]{3,}', r'grrr+', r'ugh+']
            },
            'joy': {
                'keywords': [
                    'happy', 'joy', 'amazing', 'awesome', 'great', 'fantastic',
                    'love', 'excited', 'wonderful', 'brilliant', 'perfect',
                    'yay', 'woohoo', 'haha', 'lol', 'lmao', 'best', 'furaha',
                    'poa', 'sawa', 'nice', 'cool', 'dope', 'fire', 'lit'
                ],
                'patterns': [r'ha+ha+', r'he+he+', r'ya+y+', r'wo+ho+o+']
            },
            'sadness': {
                'keywords': [
                    'sad', 'cry', 'tears', 'depressed', 'down', 'upset',
                    'hurt', 'pain', 'sorry', 'miss', 'lonely', 'heartbroken',
                    'devastated', 'disappointed', 'huzuni', 'machozi'
                ],
                'patterns': [r':\(+', r'T_T', r';\(', r'qq+']
            },
            'excitement': {
                'keywords': [
                    'excited', 'pumped', 'thrilled', 'hyped', 'omg', 'wow',
                    'incredible', 'unbelievable', 'mind-blown', 'epic',
                    'legendary', 'insane', 'crazy good', 'vibes', 'energy'
                ],
                'patterns': [r'!{3,}', r'o+m+g+', r'w+o+w+', r'a+h+']
            },
            'sarcasm': {
                'keywords': [
                    'obviously', 'clearly', 'sure', 'right', 'totally',
                    'definitely', 'of course', 'genius', 'brilliant idea',
                    'great job', 'thanks a lot'
                ],
                'patterns': [r'\.{3,}', r'/s$', r'yeah right', r'sure sure']
            },
            'fear': {
                'keywords': [
                    'scared', 'afraid', 'terrified', 'nervous', 'worried',
                    'anxious', 'panic', 'frightened', 'spooked', 'hofu',
                    'wasiwasi', 'creepy', 'dangerous', 'risky'
                ],
                'patterns': [r'o+h+ no+', r'help+', r'run+']
            },
            'surprise': {
                'keywords': [
                    'surprised', 'shocked', 'unexpected', 'sudden', 'whoa',
                    'what', 'how', 'unbelievable', 'no way', 'really',
                    'seriously', 'wait what'
                ],
                'patterns': [r'wha+t+', r'o+h+', r'no+ way+']
            },
            'disgust': {
                'keywords': [
                    'disgusting', 'gross', 'eww', 'yuck', 'nasty', 'sick',
                    'horrible', 'terrible', 'awful', 'revolting', 'ugh'
                ],
                'patterns': [r'ew+', r'yuck+', r'ugh+', r'bleh+']
            }
        }
        
        # Emoji to emotion mapping
        self.emoji_emotions = {
            '😂': ['joy'], '😭': ['sadness'], '😡': ['anger'], '😍': ['joy'],
            '🤣': ['joy'], '😢': ['sadness'], '😠': ['anger'], '🥰': ['joy'],
            '😤': ['anger'], '😱': ['fear', 'surprise'], '🙄': ['sarcasm'],
            '😬': ['fear'], '🤢': ['disgust'], '🤮': ['disgust'], '😨': ['fear'],
            '😰': ['fear'], '😳': ['surprise'], '🤯': ['surprise', 'excitement'],
            '🔥': ['excitement'], '❤️': ['joy'], '💯': ['excitement'],
            '👏': ['excitement'], '🙌': ['excitement'], '😎': ['joy']
        }
    
    def detect_emotions(self, text: str) -> List[str]:
        """
        Detect emotions in text
        Returns list of detected emotions
        """
        if not text:
            return []
        
        text_lower = text.lower()
        detected_emotions = set()
        
        # Check emoji emotions
        emoji_emotions = self._detect_emoji_emotions(text)
        detected_emotions.update(emoji_emotions)
        
        # Check keyword-based emotions
        for emotion, data in self.emotion_lexicon.items():
            # Check keywords
            for keyword in data['keywords']:
                if keyword in text_lower:
                    detected_emotions.add(emotion)
                    break
            
            # Check patterns
            for pattern in data['patterns']:
                if re.search(pattern, text_lower):
                    detected_emotions.add(emotion)
                    break
        
        # Special sarcasm detection
        if self._detect_sarcasm(text):
            detected_emotions.add('sarcasm')
        
        # If no emotions detected, try sentiment-based fallback
        if not detected_emotions:
            fallback_emotion = self._sentiment_to_emotion_fallback(text)
            if fallback_emotion:
                detected_emotions.add(fallback_emotion)
        
        return list(detected_emotions)
    
    def _detect_emoji_emotions(self, text: str) -> List[str]:
        """Extract emotions from emojis"""
        emotions = []
        for emoji_char, emotion_list in self.emoji_emotions.items():
            if emoji_char in text:
                emotions.extend(emotion_list)
        return emotions
    
    def _detect_sarcasm(self, text: str) -> bool:
        """Advanced sarcasm detection"""
        text_lower = text.lower()
        
        # Check for contradictory sentiment with positive words
        blob = TextBlob(text)
        
        # Look for exaggerated positive words with negative context
        positive_words = ['great', 'amazing', 'fantastic', 'wonderful', 'perfect']
        negative_context = ['but', 'however', 'though', 'unfortunately', 'sadly']
        
        has_positive = any(word in text_lower for word in positive_words)
        has_negative_context = any(word in text_lower for word in negative_context)
        
        # Check for quotation marks around positive words (often sarcastic)
        quoted_positive = bool(re.search(r'["\'](' + '|'.join(positive_words) + r')["\']', text_lower))
        
        # Check for obvious sarcasm markers
        sarcasm_markers = ['/s', 'yeah right', 'sure sure', 'totally believable']
        has_sarcasm_marker = any(marker in text_lower for marker in sarcasm_markers)
        
        return (has_positive and has_negative_context) or quoted_positive or has_sarcasm_marker
    
    def _sentiment_to_emotion_fallback(self, text: str) -> str:
        """Fallback emotion based on sentiment"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.3:
                return 'joy'
            elif polarity < -0.3:
                return 'sadness'
            else:
                return None
        except:
            return None
    
    def get_emotion_intensity(self, text: str, emotion: str) -> float:
        """
        Get intensity score for a specific emotion (0.0 to 1.0)
        """
        if emotion not in self.emotion_lexicon:
            return 0.0
        
        text_lower = text.lower()
        intensity_score = 0.0
        
        # Count keyword matches
        keyword_matches = sum(1 for keyword in self.emotion_lexicon[emotion]['keywords'] 
                            if keyword in text_lower)
        
        # Count pattern matches
        pattern_matches = sum(1 for pattern in self.emotion_lexicon[emotion]['patterns'] 
                            if re.search(pattern, text_lower))
        
        # Calculate base intensity
        total_words = len(text_lower.split())
        if total_words > 0:
            intensity_score = (keyword_matches + pattern_matches) / total_words
        
        # Boost for emoji matches
        emoji_boost = sum(0.2 for emoji_char, emotions in self.emoji_emotions.items() 
                         if emoji_char in text and emotion in emotions)
        
        return min(intensity_score + emoji_boost, 1.0)
