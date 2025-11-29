from typing import Dict, List, Optional
from backend.llm_handler import LLMHandler
from backend.emotion_detector import EmotionDetector
from backend.safety_filter import SafetyFilter
from utils.prompts import PromptBuilder

class ResponseGenerator:
    """
    Main controller for generating safe, supportive responses
    Coordinates all backend components
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.llm = LLMHandler(api_key)
        self.emotion_detector = EmotionDetector()
        self.safety_filter = SafetyFilter()
        self.prompt_builder = PromptBuilder()
        self.conversation_history = []
    
    def generate(self, 
                 user_message: str,
                 conversation_context: Optional[List[Dict]] = None) -> Dict[str, any]:
        """
        Generate complete response with emotion analysis and safety checks
        
        Args:
            user_message: User's input text
            conversation_context: Previous conversation turns
        
        Returns:
            Dict containing response, emotion data, and metadata
        """
        
        # Step 1: Validate input
        validation = self.safety_filter.validate_user_input(user_message)
        if not validation["valid"]:
            return self._create_response_object(
                response=validation["suggestion"],
                emotion_data={"primary_emotion": "neutral", "confidence": 1.0},
                is_safe=True,
                metadata={"validation_failed": True}
            )
        
        # Step 2: Check for crisis
        crisis_check = self.safety_filter.check_crisis(user_message)
        if crisis_check["is_crisis"]:
            return self._create_response_object(
                response=crisis_check["message"],
                emotion_data={"primary_emotion": "fearful", "confidence": 1.0},
                is_safe=True,
                metadata={"is_crisis": True}
            )
        
        # Step 3: Detect emotion
        emotion_data = self.emotion_detector.detect_emotion(user_message)
        
        # Step 4: Build context-aware prompt
        prompt = self.prompt_builder.build_prompt(
            user_message=user_message,
            emotion=emotion_data["primary_emotion"],
            conversation_history=conversation_context or self.conversation_history
        )
        
        # Step 5: Generate response using LLM
        raw_response = self.llm.generate_response(
            prompt=prompt,
            emotion=emotion_data["primary_emotion"]
        )
        
        # Step 6: Safety filter
        filtered_response, is_safe = self.safety_filter.filter_response(
            raw_response, 
            user_message
        )
        
        # Step 7: Sanitize output
        final_response = self.safety_filter.sanitize_output(filtered_response)
        
        # Step 8: Update conversation history
        self._update_history(user_message, final_response)
        
        # Step 9: Return complete response object
        return self._create_response_object(
            response=final_response,
            emotion_data=emotion_data,
            is_safe=is_safe,
            metadata={
                "model_used": self.llm.current_model,
                "prompt_length": len(prompt)
            }
        )
    
    def _create_response_object(self,
                                response: str,
                                emotion_data: Dict,
                                is_safe: bool,
                                metadata: Dict) -> Dict[str, any]:
        """Create standardized response object"""
        return {
            "response": response,
            "emotion": emotion_data.get("primary_emotion", "neutral"),
            "emotion_confidence": emotion_data.get("confidence", 0.5),
            "sentiment": emotion_data.get("sentiment", "neutral"),
            "intensity": emotion_data.get("intensity", "medium"),
            "emoji": self.emotion_detector.get_emotion_emoji(
                emotion_data.get("primary_emotion", "neutral")
            ),
            "color": self.emotion_detector.get_emotion_color(
                emotion_data.get("primary_emotion", "neutral")
            ),
            "is_safe": is_safe,
            "metadata": metadata
        }
    
    def _update_history(self, user_msg: str, bot_msg: str, max_history: int = 10):
        """Update conversation history with size limit"""
        self.conversation_history.append({
            "role": "user",
            "content": user_msg
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": bot_msg
        })
        
        # Keep only recent history
        if len(self.conversation_history) > max_history * 2:
            self.conversation_history = self.conversation_history[-(max_history * 2):]
    
    def get_conversation_summary(self) -> Dict[str, any]:
        """Generate summary of conversation"""
        if not self.conversation_history:
            return {"message_count": 0, "dominant_emotion": "neutral"}
        
        user_messages = [msg["content"] for msg in self.conversation_history if msg["role"] == "user"]
        
        # Analyze overall emotional tone
        emotions = [self.emotion_detector.detect_emotion(msg)["primary_emotion"] 
                   for msg in user_messages]
        
        from collections import Counter
        emotion_counts = Counter(emotions)
        dominant_emotion = emotion_counts.most_common(1)[0][0] if emotions else "neutral"
        
        return {
            "message_count": len(user_messages),
            "dominant_emotion": dominant_emotion,
            "emotion_distribution": dict(emotion_counts)
        }
    
    def reset_conversation(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_suggestions(self, emotion: str) -> List[str]:
        """Get quick response suggestions based on emotion"""
        suggestions = {
            "sad": [
                "Tell me more about what's bothering you",
                "What usually helps when you feel this way?",
                "I'm here to listen"
            ],
            "anxious": [
                "Let's try a breathing exercise",
                "What's making you feel anxious?",
                "How can I support you right now?"
            ],
            "angry": [
                "Tell me what happened",
                "What triggered these feelings?",
                "Take your time to express yourself"
            ],
            "happy": [
                "That's wonderful! Tell me more",
                "What made your day better?",
                "I'm glad to hear that!"
            ],
            "neutral": [
                "How are you feeling today?",
                "What's on your mind?",
                "Tell me about your day"
            ]
        }
        
        return suggestions.get(emotion, suggestions["neutral"])
