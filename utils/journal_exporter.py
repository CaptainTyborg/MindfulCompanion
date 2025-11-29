import json
import pandas as pd
from datetime import datetime
from typing import Dict, List, Optional
import io

class JournalExporter:
    """
    Export mood journal and chat history in various formats
    Supports JSON, CSV, TXT
    """
    
    def __init__(self, mood_tracker):
        self.mood_tracker = mood_tracker
    
    def export_json(self, days: int = 30, include_stats: bool = True) -> str:
        """
        Export journal as JSON
        """
        try:
            mood_df = self.mood_tracker.get_recent_moods(days=days, limit=1000)
            
            if mood_df.empty:
                return json.dumps({"error": "No data to export"}, indent=2)
            
            mood_records = mood_df.to_dict('records')
            
            export_data = {
                "export_date": datetime.now().isoformat(),
                "period_days": days,
                "total_entries": len(mood_records),
                "mood_entries": mood_records
            }
            
            if include_stats:
                stats = self.mood_tracker.get_mood_statistics(days=days)
                trends = self.mood_tracker.get_mood_trends(days=days)
                
                export_data["statistics"] = {
                    "dominant_emotion": stats.get("dominant_emotion"),
                    "average_confidence": stats.get("average_confidence"),
                    "emotion_distribution": stats.get("emotion_distribution"),
                    "sentiment_distribution": stats.get("sentiment_distribution"),
                    "trend": trends.get("trend"),
                    "insights": trends.get("insights", [])
                }
            
            return json.dumps(export_data, indent=2, default=str)
        
        except Exception as e:
            return json.dumps({"error": f"Export failed: {str(e)}"}, indent=2)
    
    def export_csv(self, days: int = 30) -> str:
        """
        Export journal as CSV
        """
        try:
            mood_df = self.mood_tracker.get_recent_moods(days=days, limit=1000)
            
            if mood_df.empty:
                return "No data to export"
            
            csv_buffer = io.StringIO()
            mood_df.to_csv(csv_buffer, index=False)
            return csv_buffer.getvalue()
        
        except Exception as e:
            return f"Export failed: {str(e)}"
    
    def export_text_report(self, days: int = 30) -> str:
        """
        Export as formatted text report
        """
        try:
            mood_df = self.mood_tracker.get_recent_moods(days=days, limit=1000)
            
            if mood_df.empty:
                return "No data to export"
            
            stats = self.mood_tracker.get_mood_statistics(days=days)
            trends = self.mood_tracker.get_mood_trends(days=days)
            
            report = []
            report.append("=" * 60)
            report.append("MINDFUL COMPANION - MOOD JOURNAL REPORT")
            report.append("=" * 60)
            report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"Period: Last {days} days")
            report.append(f"Total Entries: {len(mood_df)}\n")
            
            report.append("-" * 60)
            report.append("SUMMARY STATISTICS")
            report.append("-" * 60)
            report.append(f"Dominant Emotion: {stats.get('dominant_emotion', 'N/A').title()}")
            report.append(f"Average Confidence: {stats.get('average_confidence', 0)}")
            report.append(f"Mood Trend: {trends.get('trend', 'N/A').title()}\n")
            
            report.append("-" * 60)
            report.append("EMOTION DISTRIBUTION")
            report.append("-" * 60)
            emotion_dist = stats.get('emotion_distribution', {})
            for emotion, count in sorted(emotion_dist.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / len(mood_df)) * 100
                report.append(f"{emotion.title():<15} {count:>5} entries  ({percentage:.1f}%)")
            
            report.append("")
            
            report.append("-" * 60)
            report.append("SENTIMENT BREAKDOWN")
            report.append("-" * 60)
            sentiment_dist = stats.get('sentiment_distribution', {})
            for sentiment, count in sentiment_dist.items():
                percentage = (count / len(mood_df)) * 100
                report.append(f"{sentiment.title():<15} {count:>5} entries  ({percentage:.1f}%)")
            
            report.append("")
            
            insights = trends.get('insights', [])
            if insights:
                report.append("-" * 60)
                report.append("PERSONALIZED INSIGHTS")
                report.append("-" * 60)
                for i, insight in enumerate(insights, 1):
                    report.append(f"{i}. {insight}")
                report.append("")
            
            report.append("-" * 60)
            report.append("RECENT MOOD ENTRIES")
            report.append("-" * 60)
            
            for idx, row in mood_df.head(20).iterrows():
                report.append(f"\n[{row['date']} {row['time']}]")
                report.append(f"Emotion: {row['emotion'].title()} | Sentiment: {row['sentiment'].title()}")
                report.append(f"Message: {row.get('message_preview', '')[:80]}...")
            
            report.append("\n" + "=" * 60)
            report.append("END OF REPORT")
            report.append("=" * 60)
            
            return "\n".join(report)
        
        except Exception as e:
            return f"Export failed: {str(e)}"
    
    def export_conversation_log(self, messages: List[Dict]) -> str:
        """
        Export current conversation as text
        """
        if not messages:
            return "No conversation to export"
        
        log = []
        log.append("=" * 60)
        log.append("MINDFUL COMPANION - CONVERSATION LOG")
        log.append("=" * 60)
        log.append(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        for msg in messages:
            role = "You" if msg.get('role') == 'user' else "MindfulCompanion"
            timestamp = msg.get('timestamp', '')
            content = msg.get('content', '')
            
            log.append(f"[{timestamp}] {role}:")
            log.append(content)
            
            if msg.get('role') == 'assistant':
                emotion = msg.get('emotion', 'neutral')
                log.append(f"(Detected emotion: {emotion})")
            
            log.append("")
        
        log.append("=" * 60)
        log.append("END OF CONVERSATION")
        log.append("=" * 60)
        
        return "\n".join(log)
    
    def get_export_filename(self, export_type: str = "json") -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"mindful_companion_journal_{timestamp}.{export_type}"
