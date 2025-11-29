from typing import List, Dict, Optional

class PromptBuilder:
    """
    Builds context-aware prompts for the LLM
    Ensures supportive, safe, non-clinical responses
    """
    
    def __init__(self):
        self.system_prompt = """You are a compassionate mental wellness companion. Your role is to:

- Listen actively and validate emotions
- Provide supportive, non-judgmental responses
- Offer general wellness tips and coping strategies
- Encourage self-care and healthy habits
- NEVER diagnose or provide medical advice
- NEVER claim to be a therapist or medical professional
- Redirect to professional help when appropriate

Guidelines:
- Keep responses warm, empathetic, and concise (2-4 sentences)
- Use "I understand", "That sounds difficult", "Your feelings are valid"
- Ask thoughtful follow-up questions
- Suggest healthy coping mechanisms
- Avoid clinical language
- Be authentic and human

If someone is in crisis, immediately suggest professional crisis resources."""
    
    def build_prompt(self,
                    user_message: str,
                    emotion: str = "neutral",
                    conversation_history: Optional[List[Dict]] = None) -> str:
        """
        Build complete prompt with context
        
        Args:
            user_message: Current user message
            emotion: Detected emotion
            conversation_history: Previous conversation
        
        Returns:
            Complete prompt string
        """
        
        # Start with system prompt
        prompt_parts = [self.system_prompt]
        
        # Add emotion context
        emotion_context = self._get_emotion_context(emotion)
        prompt_parts.append(f"\nCurrent user emotion: {emotion}\n{emotion_context}")
        
        # Add conversation history (if available)
        if conversation_history:
            history_text = self._format_history(conversation_history)
            prompt_parts.append(f"\nConversation history:\n{history_text}")
        
        # Add current user message
        prompt_parts.append(f"\nUser: {user_message}\n\nRespond with empathy and support:")
        
        return "\n".join(prompt_parts)
    
    def _get_emotion_context(self, emotion: str) -> str:
        """Get context-specific guidance for each emotion"""
        
        emotion_guidance = {
            "sad": """The user is feeling sad. Acknowledge their pain, validate their feelings, 
            and gently encourage them without dismissing their emotions. Suggest small, 
            manageable self-care activities.""",
            
            "anxious": """The user is feeling anxious. Help them feel grounded. Suggest 
            breathing exercises or grounding techniques. Remind them this feeling is temporary.""",
            
            "angry": """The user is feeling angry. Validate that anger is a normal emotion. 
            Help them identify what triggered it. Suggest healthy ways to process these feelings.""",
            
            "happy": """The user is feeling happy! Celebrate with them. Ask what contributed 
            to these positive feelings. Encourage them to savor this moment.""",
            
            "fearful": """The user is feeling fearful. Provide reassurance. Help them feel 
            safe. Break down their fears into manageable pieces. Remind them of their strength.""",
            
            "confused": """The user is feeling confused. Help them organize their thoughts. 
            Ask clarifying questions. Break things down step by step.""",
            
            "neutral": """Engage warmly and naturally. Ask open-ended questions to understand 
            how they're really feeling."""
        }
        
        return emotion_guidance.get(emotion, emotion_guidance["neutral"])
    
    def _format_history(self, history: List[Dict], max_turns: int = 3) -> str:
        """Format conversation history for context"""
        
        # Keep only recent turns
        recent_history = history[-(max_turns * 2):] if len(history) > max_turns * 2 else history
        
        formatted = []
        for msg in recent_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            content = msg["content"][:200]  # Truncate long messages
            formatted.append(f"{role}: {content}")
        
        return "\n".join(formatted)
    
    def build_wellness_tip_prompt(self, category: str = "general") -> str:
        """Build prompt for generating wellness tips"""
        
        return f"""Generate a brief, actionable wellness tip for {category}. 
        Keep it positive, practical, and under 50 words.
        
        Tip:"""
    
    def build_reflection_prompt(self, mood_data: Dict) -> str:
        """Build prompt for end-of-day reflection"""
        
        dominant_emotion = mood_data.get("dominant_emotion", "neutral")
        
        return f"""The user has been feeling mostly {dominant_emotion} today. 
        Generate a brief, supportive end-of-day reflection message that:
        - Acknowledges their emotional journey today
        - Offers gentle encouragement
        - Suggests one small thing for tomorrow
        
        Keep it under 100 words and warm in tone.
        
        Reflection:"""
