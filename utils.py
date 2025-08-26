import re
import string
from typing import List, Dict, Tuple
import emoji

class TextPreprocessor:
    """
    Advanced text preprocessing for social media content
    Handles emojis, slang, code-switching, and normalization
    """
    
    def __init__(self):
        # Common social media abbreviations
        self.abbreviations = {
            'lol': 'laugh out loud',
            'lmao': 'laughing my ass off',
            'rofl': 'rolling on floor laughing',
            'omg': 'oh my god',
            'wtf': 'what the fuck',
            'tbh': 'to be honest',
            'imo': 'in my opinion',
            'imho': 'in my humble opinion',
            'fyi': 'for your information',
            'btw': 'by the way',
            'idk': 'i do not know',
            'irl': 'in real life',
            'afaik': 'as far as i know',
            'ttyl': 'talk to you later',
            'brb': 'be right back',
            'gtg': 'got to go',
            'ngl': 'not gonna lie',
            'frfr': 'for real for real',
            'periodt': 'period end of discussion',
            'facts': 'that is true',
            'cap': 'lie false',
            'no cap': 'no lie truth',
            'bet': 'okay sure',
            'say less': 'understood',
            'vibe': 'feeling mood',
            'mood': 'feeling relatable',
            'stan': 'support love',
            'salty': 'bitter angry',
            'shade': 'insult disrespect',
            'tea': 'gossip information',
            'spill': 'tell reveal',
            'lowkey': 'somewhat secretly',
            'highkey': 'obviously clearly',
            'deadass': 'seriously really',
            'sus': 'suspicious weird',
            'simp': 'overly devoted',
            'karen': 'entitled person',
            'ok boomer': 'dismissive response'
        }
        
        # Kenyan/Swahili slang expansions
        self.kenyan_slang = {
            'poa': 'cool good nice',
            'sawa': 'okay good fine',
            'mambo': 'what is up hello',
            'vipi': 'how what',
            'niaje': 'how are you',
            'maze': 'friend buddy',
            'msee': 'person guy',
            'dem': 'girl woman',
            'mzee': 'elder old person',
            'kijana': 'young person youth',
            'buda': 'friend buddy',
            'choma': 'meat barbecue',
            'matatu': 'public transport bus',
            'boda': 'motorcycle taxi',
            'karibu': 'welcome come',
            'asante': 'thank you',
            'pole': 'sorry sympathy',
            'haraka': 'quickly fast',
            'polepole': 'slowly careful',
            'hakuna matata': 'no worries problem',
            'mambo vipi': 'how are things',
            'uko poa': 'you are cool',
            'niko sawa': 'i am fine',
            'si mchezo': 'not joking serious',
            'wacha mchezo': 'stop joking',
            'kuna noma': 'there is trouble',
            'umenishinda': 'you have won defeated me',
            'sasa': 'now what',
            'doh': 'wow expression',
            'jo': 'friend buddy'
        }
    
    def clean_text(self, text: str) -> str:
        """
        Comprehensive text cleaning and normalization
        """
        if not text:
            return ""
        
        # Convert to lowercase for processing
        text = text.lower().strip()
        
        # Handle emojis first (convert to descriptive text)
        text = self._process_emojis(text)
        
        # Expand abbreviations and slang
        text = self._expand_abbreviations(text)
        
        # Clean special characters but preserve sentiment indicators
        text = self._clean_special_chars(text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _process_emojis(self, text: str) -> str:
        """Convert emojis to descriptive text"""
        # Use emoji library to convert emojis to text descriptions
        text_with_emoji_names = emoji.demojize(text, delimiters=(" ", " "))
        
        # Clean up emoji descriptions
        text_with_emoji_names = re.sub(r':', '', text_with_emoji_names)
        text_with_emoji_names = re.sub(r'_', ' ', text_with_emoji_names)
        
        return text_with_emoji_names
    
    def _expand_abbreviations(self, text: str) -> str:
        """Expand common abbreviations and slang"""
        words = text.split()
        expanded_words = []
        
        for word in words:
            # Remove punctuation for matching
            clean_word = word.strip(string.punctuation)
            
            # Check abbreviations
            if clean_word in self.abbreviations:
                expanded_words.append(self.abbreviations[clean_word])
            # Check Kenyan slang
            elif clean_word in self.kenyan_slang:
                expanded_words.append(self.kenyan_slang[clean_word])
            else:
                expanded_words.append(word)
        
        return ' '.join(expanded_words)
    
    def _clean_special_chars(self, text: str) -> str:
        """Clean special characters while preserving sentiment indicators"""
        # Preserve repeated punctuation that indicates emotion
        text = re.sub(r'!{2,}', ' very excited emphasized ', text)
        text = re.sub(r'\?{2,}', ' very confused questioning ', text)
        text = re.sub(r'\.{3,}', ' trailing thought ', text)
        
        # Handle repeated letters (e.g., "sooooo" -> "so very")
        text = re.sub(r'(.)\1{2,}', r'\1 very', text)
        
        # Remove URLs but indicate their presence
        text = re.sub(r'http[s]?://[^\s]+', ' link url ', text)
        text = re.sub(r'www\.[^\s]+', ' website link ', text)
        
        # Handle @ mentions and hashtags
        text = re.sub(r'@\w+', ' mention user ', text)
        text = re.sub(r'#\w+', ' hashtag topic ', text)
        
        # Clean remaining punctuation but keep basic sentence structure
        text = re.sub(r'[^\w\s]', ' ', text)
        
        return text
    
    def extract_features(self, text: str) -> Dict[str, any]:
        """
        Extract linguistic features from text for analysis
        """
        if not text:
            return {
                "word_count": 0,
                "char_count": 0,
                "emoji_count": 0,
                "url_count": 0,
                "caps_ratio": 0.0,
                "exclamation_count": 0,
                "question_count": 0
            }
        
        # Count basic features
        word_count = len(text.split())
        char_count = len(text)
        
        # Count emojis
        emoji_count = len([c for c in text if c in emoji.EMOJI_DATA])
        
        # Count URLs
        url_count = len(re.findall(r'http[s]?://[^\s]+|www\.[^\s]+', text))
        
        # Calculate caps ratio
        caps_chars = sum(1 for c in text if c.isupper())
        caps_ratio = caps_chars / max(char_count, 1)
        
        # Count punctuation
        exclamation_count = text.count('!')
        question_count = text.count('?')
        
        return {
            "word_count": word_count,
            "char_count": char_count,
            "emoji_count": emoji_count,
            "url_count": url_count,
            "caps_ratio": round(caps_ratio, 3),
            "exclamation_count": exclamation_count,
            "question_count": question_count
        }
    
    def detect_language_mix(self, text: str) -> Dict[str, float]:
        """
        Detect code-switching between English and Swahili
        """
        if not text:
            return {"english": 0.0, "swahili": 0.0, "mixed": 0.0}
        
        words = text.lower().split()
        total_words = len(words)
        
        if total_words == 0:
            return {"english": 0.0, "swahili": 0.0, "mixed": 0.0}
        
        # Common English words
        english_words = set([
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
            'after', 'above', 'below', 'between', 'among', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
            'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their'
        ])
        
        # Common Swahili words
        swahili_words = set([
            'na', 'wa', 'ni', 'ya', 'za', 'la', 'cha', 'mwa', 'kwa', 'katika',
            'juu', 'chini', 'mbele', 'nyuma', 'ndani', 'nje', 'mimi', 'wewe',
            'yeye', 'sisi', 'ninyi', 'wao', 'yangu', 'yako', 'yake', 'yetu',
            'yenu', 'yao', 'hii', 'hiyo', 'ile', 'hizi', 'hizo', 'zile'
        ])
        
        english_count = sum(1 for word in words if word in english_words)
        swahili_count = sum(1 for word in words if word in swahili_words)
        
        english_ratio = english_count / total_words
        swahili_ratio = swahili_count / total_words
        mixed_ratio = 1.0 - english_ratio - swahili_ratio
        
        return {
            "english": round(english_ratio, 3),
            "swahili": round(swahili_ratio, 3),
            "mixed": round(mixed_ratio, 3)
        }

class DataValidator:
    """
    Validates input data for the sentiment analysis system
    """
    
    @staticmethod
    def validate_text_input(text: str, max_length: int = 5000) -> Tuple[bool, str]:
        """Validate text input"""
        if not isinstance(text, str):
            return False, "Input must be a string"
        
        if len(text) > max_length:
            return False, f"Text too long. Maximum {max_length} characters allowed"
        
        if not text.strip():
            return False, "Text cannot be empty"
        
        return True, "Valid"
    
    @staticmethod
    def validate_comment_list(comments: List[str], max_count: int = 100) -> Tuple[bool, str]:
        """Validate list of comments"""
        if not isinstance(comments, list):
            return False, "Comments must be a list"
        
        if len(comments) > max_count:
            return False, f"Too many comments. Maximum {max_count} allowed"
        
        if len(comments) == 0:
            return False, "Comment list cannot be empty"
        
        for i, comment in enumerate(comments):
            if not isinstance(comment, str):
                return False, f"Comment at index {i} must be a string"
        
        return True, "Valid"
