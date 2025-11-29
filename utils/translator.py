from googletrans import Translator, LANGUAGES
from typing import Optional, Dict
import streamlit as st

class TranslationHandler:
    """
    Handles multi-language translation using Google Translate
    Supports 100+ languages
    """
    
    def __init__(self):
        self.translator = Translator()
        self.available_languages = LANGUAGES
        
        # Popular language mappings
        self.popular_languages = {
            "English": "en",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Italian": "it",
            "Portuguese": "pt",
            "Dutch": "nl",
            "Russian": "ru",
            "Chinese (Simplified)": "zh-cn",
            "Japanese": "ja",
            "Korean": "ko",
            "Arabic": "ar",
            "Hindi": "hi",
            "Turkish": "tr",
            "Polish": "pl",
            "Swedish": "sv",
            "Norwegian": "no",
            "Danish": "da",
            "Finnish": "fi",
            "Greek": "el"
        }
    
    def translate(self, text: str, dest_lang: str = "es", src_lang: str = "en") -> Optional[str]:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            dest_lang: Destination language code (e.g., 'es', 'fr')
            src_lang: Source language code (default: 'en', or 'auto' for auto-detect)
        
        Returns:
            Translated text or None if failed
        """
        try:
            if not text or len(text.strip()) == 0:
                return None
            
            # Translate
            result = self.translator.translate(text, dest=dest_lang, src=src_lang)
            return result.text
        
        except Exception as e:
            print(f"Translation error: {e}")
            return None
    
    def detect_language(self, text: str) -> Optional[Dict]:
        """
        Detect the language of given text
        
        Returns:
            Dict with 'lang' code and 'confidence' or None
        """
        try:
            detection = self.translator.detect(text)
            return {
                "lang": detection.lang,
                "confidence": detection.confidence,
                "language_name": LANGUAGES.get(detection.lang, "Unknown")
            }
        except Exception as e:
            print(f"Language detection error: {e}")
            return None
    
    def translate_conversation(self, 
                              user_message: str, 
                              bot_response: str,
                              user_lang: str = "en",
                              bot_lang: str = "es") -> Dict[str, str]:
        """
        Translate both user and bot messages
        
        Returns:
            Dict with translated messages
        """
        try:
            # Translate user message to English (if not already)
            if user_lang != "en":
                user_in_english = self.translate(user_message, dest_lang="en", src_lang=user_lang)
            else:
                user_in_english = user_message
            
            # Translate bot response to user's language
            if bot_lang != user_lang:
                bot_translated = self.translate(bot_response, dest_lang=user_lang, src_lang="en")
            else:
                bot_translated = bot_response
            
            return {
                "user_original": user_message,
                "user_english": user_in_english,
                "bot_english": bot_response,
                "bot_translated": bot_translated
            }
        
        except Exception as e:
            print(f"Conversation translation error: {e}")
            return {
                "user_original": user_message,
                "user_english": user_message,
                "bot_english": bot_response,
                "bot_translated": bot_response
            }
    
    def get_language_name(self, lang_code: str) -> str:
        """Get full language name from code"""
        return LANGUAGES.get(lang_code, lang_code.upper())
    
    def get_popular_languages(self) -> Dict[str, str]:
        """Get popular languages for UI selection"""
        return self.popular_languages

# Convenience function
def translate_text(text: str, to_language: str = "es") -> str:
    """
    Simple translation function
    
    Args:
        text: Text to translate
        to_language: Target language code
    
    Returns:
        Translated text
    """
    handler = TranslationHandler()
    translated = handler.translate(text, dest_lang=to_language)
    return translated if translated else text

# Language emoji mapping for UI
LANGUAGE_EMOJIS = {
    "en": "🇺🇸",
    "es": "🇪🇸",
    "fr": "🇫🇷",
    "de": "🇩🇪",
    "it": "🇮🇹",
    "pt": "🇵🇹",
    "nl": "🇳🇱",
    "ru": "🇷🇺",
    "zh-cn": "🇨🇳",
    "ja": "🇯🇵",
    "ko": "🇰🇷",
    "ar": "🇸🇦",
    "hi": "🇮🇳",
    "tr": "🇹🇷"
}
