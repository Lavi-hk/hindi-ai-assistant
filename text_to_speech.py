"""
Text-to-Speech Module for Hindi Language
Converts Hindi text to speech audio
"""

from gtts import gTTS
import os
import tempfile
from typing import Optional
from io import BytesIO


class HindiTTS:
    """
    Text-to-Speech handler for Hindi using Google TTS (gTTS)
    """
    
    def __init__(self):
        """Initialize TTS; playback handled by caller (e.g., Streamlit)."""
        self.temp_dir = tempfile.gettempdir()
    
    def speak(self, text: str, save_file: Optional[str] = None) -> bool:
        """
        Convert Hindi text to speech and play it
        
        Args:
            text: Hindi text to convert
            save_file: Optional path to save the audio file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create gTTS object with Hindi language
            tts = gTTS(text=text, lang='hi', slow=False)
            
            # Save to temporary file
            temp_file = os.path.join(self.temp_dir, 'hindi_tts_temp.mp3')
            tts.save(temp_file)
            
            # Optionally save to specified file
            if save_file:
                tts.save(save_file)
            
            # Caller is responsible for playback; we just save.
            # Clean up temporary file
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            return True
            
        except Exception as e:
            print(f"TTS Error: {e}")
            return False
    
    def speak_streamlit(self, text: str) -> bytes:
        """
        Generate audio bytes for Streamlit audio player
        
        Args:
            text: Hindi text to convert
            
        Returns:
            Audio bytes
        """
        try:
            # Create gTTS object
            tts = gTTS(text=text, lang='hi', slow=False)
            
            # Save to BytesIO buffer
            audio_buffer = BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            return audio_buffer.read()
            
        except Exception as e:
            print(f"TTS Error: {e}")
            return b''
    
    # Local playback helper removed to keep cloud build lightweight


def test_tts():
    """Test function for TTS"""
    tts = HindiTTS()
    
    test_texts = [
        "नमस्ते! मैं एक हिंदी बोलने वाली AI सहायक हूं।",
        "आपकी क्या मदद कर सकता हूं?",
        "धन्यवाद! जल्द ही मिलते हैं।"
    ]
    
    for text in test_texts:
        print(f"\nSpeaking: {text}")
        _ = tts.speak_streamlit(text)
        import time
        time.sleep(2)


if __name__ == "__main__":
    test_tts()

