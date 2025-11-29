import re
from typing import Dict, Tuple

class SafetyFilter:
    """
    Ensures chatbot responses are safe and appropriate.
    - Detects crisis situations
    - Prevents medical advice
    - Filters inappropriate content
    """
    
    def __init__(self):
        # Crisis keywords that require immediate professional help
        self.crisis_keywords = [
            "suicide", "suicidal", "kill myself", "end my life", "die",
            "self harm", "cutting", "overdose", "hurt myself",
            "want to die", "better off dead", "no reason to live"
        ]
        
        # Medical/diagnostic terms to avoid
        self.medical_keywords = [
            "diagnose", "diagnosis", "prescribe", "prescription", "medication",
            "disorder", "condition", "treatment plan", "therapy", "cure",
            "illness", "disease", "syndrome", "clinical"
        ]
        
        # Prohibited response patterns
        self.prohibited_phrases = [
            "you have", "you are diagnosed", "you suffer from",
            "i diagnose", "you need medication", "take these pills",
            "you should stop taking", "this is definitely"
        ]
    
    def check_crisis(self, text: str) -> Dict[str, any]:
        """
        Check if user message indicates crisis situation
        
        Returns:
            Dict with is_crisis flag and suggested response
        """
        
        text_lower = text.lower()
        
        # Check for crisis keywords
        crisis_detected = any(keyword in text_lower for keyword in self.crisis_keywords)
        
        if crisis_detected:
            return {
                "is_crisis": True,
                "severity": "high",
                "message": self._get_crisis_response()
            }
        
        return {
            "is_crisis": False,
            "severity": "none",
            "message": None
        }
    
    def _get_crisis_response(self) -> str:
        """Return crisis intervention message"""
        return """I'm concerned about what you've shared. Please know that you don't have to face this alone.

**If you're in immediate danger, please:**
• Call emergency services (911 in US)
• Go to your nearest emergency room
• Call a crisis hotline:
  - National Suicide Prevention Lifeline: 988
  - Crisis Text Line: Text HOME to 741741
  - International: findahelpline.com

You deserve support from trained professionals who can help you through this. I'm here to listen, but I'm not equipped to handle crisis situations. Please reach out to one of the resources above."""
    
    def filter_response(self, response: str, user_message: str) -> Tuple[str, bool]:
        """
        Filter bot response to ensure safety
        
        Returns:
            Tuple of (filtered_response, is_safe)
        """
        
        response_lower = response.lower()
        
        # Check if response contains medical advice
        contains_medical = any(keyword in response_lower for keyword in self.medical_keywords)
        contains_prohibited = any(phrase in response_lower for phrase in self.prohibited_phrases)
        
        if contains_medical or contains_prohibited:
            # Replace with safe response
            safe_response = self._get_safe_alternative()
            return safe_response, False
        
        # Add disclaimer if discussing mental health
        if self._is_mental_health_topic(response_lower):
            response = self._add_disclaimer(response)
        
        return response, True
    
    def _is_mental_health_topic(self, text: str) -> bool:
        """Check if response discusses mental health topics"""
        mental_health_terms = [
            "depression", "anxiety", "mental health", "therapy",
            "counseling", "psychologist", "psychiatrist"
        ]
        return any(term in text for term in mental_health_terms)
    
    def _add_disclaimer(self, response: str) -> str:
        """Add appropriate disclaimer to response"""
        disclaimer = "\n\n*Remember: I'm here for support, but I'm not a therapist or medical professional.*"
        if disclaimer not in response:
            return response + disclaimer
        return response
    
    def _get_safe_alternative(self) -> str:
        """Return safe alternative response"""
        return """I want to support you, but I'm not qualified to provide medical advice or diagnosis. 

If you're experiencing mental health concerns, I encourage you to:
• Speak with a healthcare provider
• Contact a mental health professional
• Call a helpline for guidance

I'm here to listen and provide general emotional support. How are you feeling right now?"""
    
    def validate_user_input(self, text: str) -> Dict[str, any]:
        """
        Validate user input for safety concerns
        
        Returns:
            Dict with validation status and suggestions
        """
        
        if not text or len(text.strip()) < 2:
            return {
                "valid": False,
                "reason": "empty",
                "suggestion": "Please share what's on your mind."
            }
        
        # Check for spam/gibberish
        if len(set(text)) < 3 or text.count(text[0]) > len(text) * 0.7:
            return {
                "valid": False,
                "reason": "gibberish",
                "suggestion": "I'm having trouble understanding. Could you rephrase that?"
            }
        
        # Check message length
        if len(text) > 1000:
            return {
                "valid": True,
                "reason": "long",
                "suggestion": "That's a lot to process! Let's break it down together."
            }
        
        return {
            "valid": True,
            "reason": "ok",
            "suggestion": None
        }
    
    def sanitize_output(self, text: str) -> str:
        """Remove potentially harmful content from output"""
        
        # Remove any URLs (to prevent phishing)
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '[link removed]', text)
        
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[email removed]', text)
        
        # Remove phone numbers
        text = re.sub(r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', '[phone removed]', text)
        
        return text
