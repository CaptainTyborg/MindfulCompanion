import speech_recognition as sr
from typing import Optional, Tuple
import streamlit as st

class VoiceHandler:
    """
    Handles voice input and speech recognition
    Uses Google Speech Recognition API (free)
    """
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000  # Adjust for ambient noise
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 1.0  # Seconds of silence before stopping
    
    def listen(self, language: str = "en-US", timeout: int = 10) -> Tuple[bool, Optional[str], str]:
        """
        Listen to microphone and convert speech to text
        
        Args:
            language: Language code (e.g., 'en-US', 'es-ES', 'fr-FR')
            timeout: Maximum seconds to wait for speech
        
        Returns:
            Tuple of (success, text, message)
        """
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                st.info("🎤 Adjusting for background noise... Please wait.")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                
                st.info("🎤 Listening... Speak now!")
                
                # Listen for audio
                try:
                    audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=30)
                except sr.WaitTimeoutError:
                    return False, None, "⏱️ No speech detected. Please try again."
                
                st.info("🔄 Processing your speech...")
                
                # Recognize speech using Google Speech Recognition
                try:
                    text = self.recognizer.recognize_google(audio, language=language)
                    return True, text, f"✅ Heard: '{text}'"
                
                except sr.UnknownValueError:
                    return False, None, "❌ Could not understand audio. Please speak clearly and try again."
                
                except sr.RequestError as e:
                    return False, None, f"❌ Speech recognition service error: {e}"
        
        except OSError as e:
            error_msg = str(e)
            if "Could not find PyAudio" in error_msg or "PyAudio" in error_msg:
                return False, None, ("❌ PyAudio not installed. Voice input unavailable on this system.\n"
                                    "To enable: Download PyAudio wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio "
                                    "and install with pip. For now, use text input.")
            return False, None, f"❌ Microphone error: {e}. Please check your microphone connection."
        
        except Exception as e:
            error_msg = str(e)
            if "PyAudio" in error_msg:
                return False, None, ("❌ PyAudio not installed. Voice input unavailable on this system.\n"
                                    "To enable: Download PyAudio wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio "
                                    "and install with pip. For now, use text input.")
            return False, None, f"❌ Unexpected error: {e}"
    
    def is_microphone_available(self) -> bool:
        """Check if microphone is available"""
        try:
            mic_list = sr.Microphone.list_microphone_names()
            return len(mic_list) > 0
        except Exception:
            return False
    
    def get_available_microphones(self) -> list:
        """Get list of available microphones"""
        try:
            return sr.Microphone.list_microphone_names()
        except Exception:
            return []
    
    def test_microphone(self) -> Tuple[bool, str]:
        """Test microphone functionality"""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                return True, "✅ Microphone is working!"
        except OSError as e:
            if "Could not find PyAudio" in str(e):
                return False, ("❌ PyAudio not installed. On Windows, install via:\n"
                             "1. Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio\n"
                             "2. Run: pip install <downloaded_file>.whl\n"
                             "Voice input will use fallback text mode.")
            return False, f"❌ No microphone detected. Please connect a microphone. ({e})"
        except Exception as e:
            error_msg = str(e)
            if "PyAudio" in error_msg:
                return False, ("❌ PyAudio not installed. On Windows, install via:\n"
                             "1. Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio\n"
                             "2. Run: pip install <downloaded_file>.whl\n"
                             "Voice input will use fallback text mode.")
            return False, f"❌ Microphone test failed: {e}"


def voice_to_text(language: str = "en-US") -> Optional[str]:
    """
    Convenience function for voice input
    
    Args:
        language: Language code for speech recognition
    
    Returns:
        Recognized text or None if failed
    """
    handler = VoiceHandler()
    success, text, message = handler.listen(language=language)
    
    if success:
        st.success(message)
        return text
    else:
        st.error(message)
        return None

# Language codes for speech recognition
SUPPORTED_LANGUAGES = {
    "English (US)": "en-US",
    "English (UK)": "en-GB",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "German": "de-DE",
    "Italian": "it-IT",
    "Portuguese": "pt-PT",
    "Dutch": "nl-NL",
    "Russian": "ru-RU",
    "Chinese (Mandarin)": "zh-CN",
    "Japanese": "ja-JP",
    "Korean": "ko-KR",
    "Arabic": "ar-SA",
    "Hindi": "hi-IN"
}
