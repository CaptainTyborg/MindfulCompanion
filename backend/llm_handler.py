import os
import requests
import time
from typing import Dict, Optional

try:
    from huggingface_hub import InferenceClient
    HAS_HF_CLIENT = True
except ImportError:
    HAS_HF_CLIENT = False

class LLMHandler:
    """
    Handles interactions with free LLM APIs.
    Primary: Hugging Face Inference API
    Fallback: Local response generation
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        
        # Try to use Hugging Face InferenceClient if available
        if HAS_HF_CLIENT and self.api_key:
            self.client = InferenceClient(api_key=self.api_key)
            self.use_client = True
        else:
            self.client = None
            self.use_client = False
        
        # Models for text generation
        self.models = {
            "primary": "mistralai/Mistral-7B-Instruct-v0.1",
            "fallback": "gpt2",
        }
        
        self.current_model = self.models["primary"]
    
    def generate_response(self, 
                         prompt: str, 
                         emotion: str = "neutral",
                         max_length: int = 150,
                         temperature: float = 0.7) -> str:
        """
        Generate supportive response using free LLM API
        
        Args:
            prompt: The conversation prompt
            emotion: Detected emotion (for context)
            max_length: Maximum response length
            temperature: Response creativity (0-1)
        
        Returns:
            Generated response string
        """
        
        if not self.api_key or not self.use_client:
            return self._fallback_response(emotion, prompt)
        
        try:
            # Use InferenceClient for text generation
            response_text = self.client.text_generation(
                prompt=prompt,
                model=self.current_model,
                max_new_tokens=150,
                temperature=0.7,
                top_p=0.9,
            )
            
            if response_text:
                return self._clean_response(response_text)
                
            return self._fallback_response(emotion, prompt)
            
        except Exception as e:
            print(f"LLM API Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return self._fallback_response(emotion, prompt)
    
    def _clean_response(self, text: str) -> str:
        """Clean and format the generated response"""
        text = text.strip()
        
        # Remove incomplete sentences at the end
        if text and text[-1] not in '.!?':
            last_punct = max(
                text.rfind('.'),
                text.rfind('!'),
                text.rfind('?')
            )
            if last_punct > 0:
                text = text[:last_punct + 1]
        
        return text
    
    def _fallback_response(self, emotion: str, user_message: str = "") -> str:
        """
        Enhanced fallback responses when API is unavailable
        Emotion-based supportive messages with keyword matching
        """
        # Advanced fallback responses based on emotion
        fallback_responses = {
            "sad": [
                "I hear you, and it's completely okay to feel this way right now.",
                "These difficult emotions are temporary, even though they feel heavy.",
                "You're stronger than you realize. Let's take this one moment at a time.",
                "What you're feeling is valid. Would it help to talk about what's troubling you?",
                "Sometimes we all need support. I'm here to listen without judgment."
            ],
            "anxious": [
                "Anxiety can feel overwhelming, but remember: you've handled difficult moments before.",
                "Try this: breathe in for 4 counts, hold for 4, breathe out for 6. Let's slow things down.",
                "What's one small thing you could control right now? Sometimes focusing helps.",
                "Your worries are real, but not everything you worry about will happen.",
                "Grounding yourself might help. What's one thing you can see, hear, or feel right now?"
            ],
            "angry": [
                "Your anger is valid. Strong feelings mean something matters to you.",
                "Before acting on this feeling, pause. What do you really need right now?",
                "It's okay to be frustrated. Let's explore what's really bothering you.",
                "Anger often masks another emotion. Can you dig deeper into what you're feeling?",
                "Taking a break might help. What usually calms you down?"
            ],
            "happy": [
                "That's wonderful! I'm genuinely glad you're experiencing these positive feelings.",
                "This is beautiful to hear. What's making you feel so good right now?",
                "Let's celebrate this moment with you! What's contributing most?",
                "Savor this feeling! These good moments are important and worth recognizing.",
                "Your joy is contagious. Keep embracing these positive moments!"
            ],
            "neutral": [
                "I'm here and listening. What's on your mind today?",
                "How are you truly feeling beneath the surface?",
                "I'm interested in what you have to share. What brings you here?",
                "Take your time. I'm ready to listen to whatever you want to express.",
                "Tell me more. What would be most helpful to talk about right now?"
            ],
            "fearful": [
                "Fear is natural, but you're safe right now in this moment.",
                "What you're afraid of feels real, and that's okay. Let's face it together.",
                "You're braver than you believe. What specifically is scaring you?",
                "Fear often shrinks when we talk about it. I'm here to listen.",
                "Remember: you've overcome challenges before. This is just one more."
            ]
        }
        
        import random
        
        # Get responses for this emotion
        responses = fallback_responses.get(emotion, fallback_responses["neutral"])
        base_response = random.choice(responses)
        
        # Add contextual elements if message contains keywords
        context_additions = {
            "sleep|tired|exhausted": " Getting quality sleep could really help you right now.",
            "work|job|boss|colleague": " Work stress is real. Remember, you deserve breaks and boundaries.",
            "relationship|friend|family|love": " Relationships matter. Communication is often the first step.",
            "health|sick|pain|hurt": " Your wellbeing is important. Take care of yourself first.",
            "money|financial|broke|debt": " Financial stress is significant. But you have more control than you think.",
            "future|tomorrow|worry|what if": " Focus on today. Tomorrow will take care of itself."
        }
        
        # Check if any keywords match
        user_message_lower = user_message.lower()
        for keywords, addition in context_additions.items():
            if any(keyword in user_message_lower for keyword in keywords.split("|")):
                base_response = base_response.rstrip(".!?") + "." + addition
                break
        
        return base_response
    
    def switch_model(self, model_type: str = "primary"):
        """Switch between available models"""
        if model_type in self.models:
            self.current_model = self.models[model_type]
            return True
        return False
