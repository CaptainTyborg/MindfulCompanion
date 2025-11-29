import json
import os
import random
from datetime import datetime
from typing import List, Dict

def load_wellness_tips(filepath: str = "data/wellness_tips.json") -> List[str]:
    """Load wellness tips from JSON file"""
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("tips", [])
    except Exception as e:
        print(f"Error loading wellness tips: {e}")
    
    # Return default tips if file not found
    return get_default_wellness_tips()

def get_default_wellness_tips() -> List[str]:
    """Return default wellness tips"""
    
    return [
        "💧 Remember to stay hydrated! Drink a glass of water right now.",
        "🌅 Start your day with 5 minutes of stretching or light movement.",
        "📵 Take a 10-minute break from screens every hour.",
        "🌬️ Practice deep breathing: Inhale for 4, hold for 4, exhale for 6.",
        "📝 Write down 3 things you're grateful for today.",
        "🚶 Take a short walk outside, even just 5 minutes helps.",
        "😴 Aim for 7-9 hours of sleep tonight.",
        "🍎 Eat something nourishing today that makes you feel good.",
        "🤝 Reach out to a friend or loved one today.",
        "🎵 Listen to your favorite uplifting song.",
        "🧘 Try a 5-minute meditation or mindfulness exercise.",
        "📚 Read something that inspires or relaxes you.",
        "🎨 Do something creative, even if just for a few minutes.",
        "🌱 Spend time with nature, even looking at plants helps.",
        "💪 Celebrate one small win from today.",
        "🛁 Take a relaxing bath or shower.",
        "📖 Journal about your feelings for 10 minutes.",
        "🎯 Set one small, achievable goal for tomorrow.",
        "☀️ Get some sunlight exposure during the day.",
        "🧹 Tidy up one small space in your environment."
    ]

def save_wellness_tips(tips: List[str], filepath: str = "data/wellness_tips.json"):
    """Save wellness tips to JSON file"""
    
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump({"tips": tips}, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving wellness tips: {e}")
        return False

def get_daily_wellness_tip() -> str:
    """Get a random wellness tip"""
    
    tips = load_wellness_tips()
    return random.choice(tips) if tips else "Take a deep breath and be kind to yourself today."

def get_time_based_greeting() -> str:
    """Get greeting based on time of day"""
    
    hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return "Good morning! 🌅"
    elif 12 <= hour < 17:
        return "Good afternoon! ☀️"
    elif 17 <= hour < 22:
        return "Good evening! 🌆"
    else:
        return "Hello! 🌙"

def format_timestamp(dt: datetime = None) -> str:
    """Format timestamp for display"""
    
    if dt is None:
        dt = datetime.now()
    
    return dt.strftime("%I:%M %p")

def generate_session_id() -> str:
    """Generate unique session ID"""
    
    return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to max length"""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def get_emotion_suggestion(emotion: str) -> str:
    """Get activity suggestion based on emotion"""
    
    suggestions = {
        "sad": "Consider going for a walk or calling a friend. Sometimes movement and connection help.",
        "anxious": "Try a 5-minute breathing exercise. Focus on slow, deep breaths.",
        "angry": "Physical activity might help. Consider going for a run or doing some stretching.",
        "happy": "Enjoy this feeling! Maybe share your joy with someone you care about.",
        "fearful": "Ground yourself by naming 5 things you can see, 4 you can touch, 3 you can hear.",
        "confused": "Write down your thoughts. Sometimes seeing them on paper helps clarify things.",
        "neutral": "Check in with yourself. How are you really feeling right now?"
    }
    
    return suggestions.get(emotion, suggestions["neutral"])

def create_mood_emoji_scale() -> List[Dict[str, str]]:
    """Create emoji mood scale for user selection"""
    
    return [
        {"emoji": "😢", "label": "Very Sad", "value": "very_sad"},
        {"emoji": "😔", "label": "Sad", "value": "sad"},
        {"emoji": "😐", "label": "Neutral", "value": "neutral"},
        {"emoji": "🙂", "label": "Good", "value": "good"},
        {"emoji": "😊", "label": "Very Good", "value": "very_good"}
    ]

def validate_api_key(key: str, key_type: str = "huggingface") -> bool:
    """Basic validation for API keys"""
    
    if not key or len(key) < 10:
        return False
    
    if key_type == "huggingface":
        return key.startswith("hf_")
    
    return True

def format_mood_chart_data(mood_stats: Dict) -> Dict:
    """Format mood data for chart display"""
    
    emotion_dist = mood_stats.get("emotion_distribution", {})
    
    return {
        "labels": list(emotion_dist.keys()),
        "values": list(emotion_dist.values()),
        "colors": [get_emotion_color(e) for e in emotion_dist.keys()]
    }

def get_emotion_color(emotion: str) -> str:
    """Get color for emotion (for charts)"""
    
    colors = {
        "sad": "#6B8E23",
        "anxious": "#FF8C00",
        "angry": "#DC143C",
        "happy": "#32CD32",
        "fearful": "#9370DB",
        "confused": "#4682B4",
        "neutral": "#808080"
    }
    
    return colors.get(emotion, "#808080")

def estimate_reading_time(text: str, wpm: int = 200) -> str:
    """Estimate reading time for text"""
    
    word_count = len(text.split())
    minutes = max(1, round(word_count / wpm))
    
    return f"{minutes} min read"

# Initialize wellness tips file on first import
if not os.path.exists("data/wellness_tips.json"):
    save_wellness_tips(get_default_wellness_tips())
