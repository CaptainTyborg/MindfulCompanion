import pandas as pd
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

class MoodTracker:
    """
    Tracks user mood over time using CSV storage
    Provides analytics and visualizations
    """
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.mood_file = os.path.join(data_dir, "mood_logs.csv")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize CSV if it doesn't exist
        if not os.path.exists(self.mood_file):
            self._create_mood_file()
    
    def _create_mood_file(self):
        """Create initial mood log CSV"""
        df = pd.DataFrame(columns=[
            "timestamp",
            "date",
            "time",
            "emotion",
            "confidence",
            "sentiment",
            "intensity",
            "message_preview",
            "session_id"
        ])
        df.to_csv(self.mood_file, index=False)
    
    def log_mood(self, 
                 emotion: str,
                 confidence: float,
                 sentiment: str,
                 intensity: str,
                 message: str,
                 session_id: str = "default") -> bool:
        """
        Log a mood entry
        
        Args:
            emotion: Primary detected emotion
            confidence: Detection confidence (0-1)
            sentiment: positive/negative/neutral
            intensity: low/medium/high
            message: User message (truncated preview)
            session_id: Session identifier
        
        Returns:
            Success status
        """
        
        try:
            now = datetime.now()
            
            # Create new entry
            new_entry = {
                "timestamp": now.isoformat(),
                "date": now.strftime("%Y-%m-%d"),
                "time": now.strftime("%H:%M:%S"),
                "emotion": emotion,
                "confidence": confidence,
                "sentiment": sentiment,
                "intensity": intensity,
                "message_preview": message[:100] if message else "",
                "session_id": session_id
            }
            
            # Append to CSV
            df = pd.read_csv(self.mood_file)
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv(self.mood_file, index=False)
            
            return True
            
        except Exception as e:
            print(f"Error logging mood: {e}")
            return False
    
    def get_recent_moods(self, days: int = 7, limit: int = 50) -> pd.DataFrame:
        """Get recent mood entries"""
        
        try:
            df = pd.read_csv(self.mood_file)
            
            if df.empty:
                return df
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Filter by date range
            cutoff_date = datetime.now() - timedelta(days=days)
            df = df[df['timestamp'] >= cutoff_date]
            
            # Sort by timestamp descending
            df = df.sort_values('timestamp', ascending=False)
            
            # Limit results
            return df.head(limit)
            
        except Exception as e:
            print(f"Error retrieving moods: {e}")
            return pd.DataFrame()
    
    def get_mood_statistics(self, days: int = 7) -> Dict[str, any]:
        """
        Calculate mood statistics for a time period
        
        Returns:
            Dict with statistics and insights
        """
        
        df = self.get_recent_moods(days=days, limit=1000)
        
        if df.empty:
            return {
                "total_entries": 0,
                "dominant_emotion": "neutral",
                "average_confidence": 0,
                "sentiment_distribution": {},
                "emotion_distribution": {},
                "intensity_distribution": {}
            }
        
        # Calculate statistics
        stats = {
            "total_entries": len(df),
            "dominant_emotion": df['emotion'].mode()[0] if not df['emotion'].empty else "neutral",
            "average_confidence": round(df['confidence'].mean(), 2),
            "sentiment_distribution": df['sentiment'].value_counts().to_dict(),
            "emotion_distribution": df['emotion'].value_counts().to_dict(),
            "intensity_distribution": df['intensity'].value_counts().to_dict(),
            "date_range": {
                "start": df['timestamp'].min().strftime("%Y-%m-%d"),
                "end": df['timestamp'].max().strftime("%Y-%m-%d")
            }
        }
        
        return stats
    
    def get_mood_trends(self, days: int = 7) -> Dict[str, any]:
        """
        Analyze mood trends over time
        
        Returns:
            Dict with trend analysis
        """
        
        df = self.get_recent_moods(days=days, limit=1000)
        
        if df.empty:
            return {"trend": "insufficient_data", "insights": []}
        
        # Group by date
        daily_moods = df.groupby('date')['emotion'].agg(lambda x: x.mode()[0] if not x.empty else 'neutral')
        daily_sentiment = df.groupby('date')['sentiment'].agg(lambda x: x.mode()[0] if not x.empty else 'neutral')
        
        # Calculate trend
        positive_days = sum(1 for s in daily_sentiment if s == 'positive')
        negative_days = sum(1 for s in daily_sentiment if s == 'negative')
        
        if positive_days > negative_days:
            trend = "improving"
            trend_message = "Your mood seems to be improving!"
        elif negative_days > positive_days:
            trend = "declining"
            trend_message = "You might be going through a tough period."
        else:
            trend = "stable"
            trend_message = "Your mood has been relatively stable."
        
        # Generate insights
        insights = self._generate_insights(df)
        
        return {
            "trend": trend,
            "trend_message": trend_message,
            "daily_moods": daily_moods.to_dict(),
            "insights": insights
        }
    
    def _generate_insights(self, df: pd.DataFrame) -> List[str]:
        """Generate personalized insights from mood data"""
        
        insights = []
        
        # Most common emotion
        most_common = df['emotion'].mode()[0] if not df['emotion'].empty else None
        if most_common:
            insights.append(f"You've been feeling {most_common} most often lately.")
        
        # Time patterns
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        morning = df[df['hour'] < 12]
        evening = df[df['hour'] >= 18]
        
        if not morning.empty and not evening.empty:
            morning_sentiment = morning['sentiment'].mode()[0]
            evening_sentiment = evening['sentiment'].mode()[0]
            
            if morning_sentiment == 'positive' and evening_sentiment == 'negative':
                insights.append("You tend to feel better in the morning.")
            elif evening_sentiment == 'positive' and morning_sentiment == 'negative':
                insights.append("Your mood improves as the day goes on.")
        
        # Intensity patterns
        high_intensity = len(df[df['intensity'] == 'high'])
        if high_intensity > len(df) * 0.5:
            insights.append("You've been experiencing strong emotions. Remember to take breaks.")
        
        return insights
    
    def export_mood_data(self, format: str = "json") -> Optional[str]:
        """Export mood data in various formats"""
        
        df = self.get_recent_moods(days=30, limit=1000)
        
        if df.empty:
            return None
        
        try:
            if format == "json":
                return df.to_json(orient='records', date_format='iso')
            elif format == "csv":
                return df.to_csv(index=False)
            else:
                return None
        except Exception as e:
            print(f"Error exporting data: {e}")
            return None
    
    def clear_old_data(self, days: int = 90):
        """Delete mood logs older than specified days"""
        
        try:
            df = pd.read_csv(self.mood_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            cutoff_date = datetime.now() - timedelta(days=days)
            df = df[df['timestamp'] >= cutoff_date]
            
            df.to_csv(self.mood_file, index=False)
            return True
            
        except Exception as e:
            print(f"Error clearing old data: {e}")
            return False
