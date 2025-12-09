import re
from typing import Dict, Tuple
try:
    from textblob import TextBlob
    HAS_TEXTBLOB = True
except Exception:
    HAS_TEXTBLOB = False

import nltk

# Download required NLTK data (run once) if available
try:
    nltk.data.find('tokenizers/punkt')
except Exception:
    try:
        nltk.download('punkt', quiet=True)
    except Exception:
        # If download fails (offline environment), continue without it
        pass

class EmotionDetector:
    """
    Detects emotions from user messages using:
    - Keyword matching
    - Sentiment analysis (TextBlob)
    - Context awareness
    """
    
    def __init__(self):
        # Emotion keyword dictionaries
        self.emotion_keywords = {
            "sad": [
                "sad", "depressed", "down", "unhappy", "miserable", "crying",
                "tears", "hopeless", "lonely", "empty", "hurt", "pain",
                "grief", "loss", "heartbroken", "devastated"
            ],
            "anxious": [
                "anxious", "worried", "nervous", "stress", "panic", "fear",
                "scared", "overwhelmed", "tense", "restless", "uneasy",
                "terrified", "afraid", "concern", "dread"
            ],
            "angry": [
                "angry", "mad", "furious", "annoyed", "irritated", "frustrated",
                "rage", "upset", "hate", "pissed", "infuriated", "resentful"
            ],
            "happy": [
                "happy", "joy", "excited", "great", "wonderful", "amazing",
                "love", "grateful", "blessed", "content", "cheerful",
                "delighted", "pleased", "glad", "fantastic"
            ],
            "fearful": [
                "fear", "scared", "afraid", "terrified", "frightened",
                "horror", "panic", "dread", "phobia", "nightmare"
            ],
            "confused": [
                "confused", "lost", "unsure", "don't know", "uncertain",
                "puzzled", "mixed", "conflicted"
            ]
        }
        
        # Intensity modifiers
        self.intensity_words = {
            "high": ["very", "extremely", "incredibly", "so", "really", "absolutely"],
            "low": ["a bit", "slightly", "somewhat", "kind of", "sort of"]
        }
    
    def detect_emotion(self, text: str) -> Dict[str, any]:
        """
        Analyze text and return emotion data
        
        Returns:
            Dict containing:
            - primary_emotion: Main detected emotion
            - confidence: Confidence score (0-1)
            - sentiment: Positive/Negative/Neutral
            - intensity: low/medium/high
        """
        
        text_lower = text.lower()
        
        # Calculate sentiment using TextBlob if available, otherwise use a lightweight fallback
        if HAS_TEXTBLOB:
            try:
                blob = TextBlob(text)
                polarity = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
                subjectivity = blob.sentiment.subjectivity  # 0 (objective) to 1 (subjective)
            except Exception:
                polarity = 0.0
                subjectivity = 0.0
        else:
            # Fallback: simple polarity score based on keyword matching
            positive_words = [
                "happy", "joy", "good", "great", "wonderful", "amazing", "love",
                "glad", "fantastic", "pleased", "excited", "grateful"
            ]
            negative_words = [
                "sad", "depressed", "bad", "terrible", "awful", "hate", "angry",
                "miserable", "lonely", "upset", "anxious", "worried"
            ]

            text_lower = text.lower()
            pos_count = sum(1 for w in positive_words if w in text_lower)
            neg_count = sum(1 for w in negative_words if w in text_lower)

            if pos_count + neg_count == 0:
                polarity = 0.0
            else:
                polarity = (pos_count - neg_count) / max(1, pos_count + neg_count)

            subjectivity = 0.0
        
        # Count keyword matches for each emotion
        emotion_scores = {}
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                emotion_scores[emotion] = score
        
        # Determine primary emotion
        if emotion_scores:
            primary_emotion = max(emotion_scores, key=emotion_scores.get)
            confidence = min(emotion_scores[primary_emotion] * 0.25, 1.0)
        else:
            # Use sentiment as fallback
            if polarity > 0.3:
                primary_emotion = "happy"
                confidence = polarity
            elif polarity < -0.3:
                primary_emotion = "sad"
                confidence = abs(polarity)
            else:
                primary_emotion = "neutral"
                confidence = 0.5
        
        # Determine intensity
        intensity = self._calculate_intensity(text_lower, subjectivity)
        
        # Determine sentiment category
        if polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "primary_emotion": primary_emotion,
            "confidence": round(confidence, 2),
            "sentiment": sentiment,
            "intensity": intensity,
            "polarity": round(float(polarity), 2),
            "subjectivity": round(float(subjectivity), 2)
        }
    
    def _calculate_intensity(self, text: str, subjectivity: float) -> str:
        """Calculate emotional intensity"""
        
        # Check for intensity modifiers
        high_count = sum(1 for word in self.intensity_words["high"] if word in text)
        low_count = sum(1 for word in self.intensity_words["low"] if word in text)
        
        # Check for capitalization and exclamation marks
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        exclamation_count = text.count('!')
        
        # Calculate intensity score
        intensity_score = (
            high_count * 2 +
            exclamation_count * 1.5 +
            caps_ratio * 10 +
            subjectivity * 2 -
            low_count * 2
        )
        
        if intensity_score > 5:
            return "high"
        elif intensity_score > 2:
            return "medium"
        else:
            return "low"
    
    def get_emotion_emoji(self, emotion: str) -> str:
        """Return emoji for emotion"""
        emoji_map = {
            "sad": "😢",
            "anxious": "😰",
            "angry": "😠",
            "happy": "😊",
            "fearful": "😨",
            "confused": "😕",
            "neutral": "😐"
        }
        return emoji_map.get(emotion, "💭")
    
    def get_emotion_color(self, emotion: str) -> str:
        """Return color code for emotion (for UI)"""
        color_map = {
            "sad": "#6B8E23",
            "anxious": "#FF8C00",
            "angry": "#DC143C",
            "happy": "#32CD32",
            "fearful": "#9370DB",
            "confused": "#4682B4",
            "neutral": "#808080"
        }
        return color_map.get(emotion, "#808080")
