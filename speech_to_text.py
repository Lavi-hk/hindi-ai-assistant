"""
Speech-to-Text Module for Hindi Language
Supports both pre-recorded audio files and live microphone input
"""

import speech_recognition as sr
import wave
from pydub import AudioSegment
import os
from typing import Optional, Tuple


class HindiSTT:
    """
    Speech-to-Text handler for Hindi language using Google Speech Recognition API
    """
    
    def __init__(self):
        """Initialize the recognizer"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
    def from_audio_file(self, audio_path: str) -> Tuple[Optional[str], bool]:
        """
        Convert Hindi speech from audio file to text
        
        Args:
            audio_path: Path to audio file (MP3/WAV/OGG/M4A)
            
        Returns:
            Tuple of (transcribed_text, success_flag)
        """
        try:
            # Convert audio to WAV if needed
            audio_file = self._convert_to_wav(audio_path)
            
            # Read audio file
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
                
            # Recognize speech using Google's API (supports Hindi)
            text = self.recognizer.recognize_google(audio, language='hi-IN')
            
            # Clean up temporary file if created
            if audio_file != audio_path and os.path.exists(audio_file):
                os.remove(audio_file)
                
            return text, True
            
        except sr.UnknownValueError:
            return "क्षमा करें, मैं समझ नहीं पाया। कृपया फिर से बोलें।", False
        except sr.RequestError as e:
            return f"क्षमा करें, सेवा उपलब्ध नहीं है: {str(e)}", False
        except Exception as e:
            return f"त्रुटि: {str(e)}", False
    
    def from_microphone(self, duration: int = 5) -> Tuple[Optional[str], bool]:
        """
        Convert Hindi speech from live microphone input to text
        
        Args:
            duration: Recording duration in seconds (default: 5)
            
        Returns:
            Tuple of (transcribed_text, success_flag)
        """
        try:
            with self.microphone as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("बोलिए... (Speak...)")
                
                # Record audio
                audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
                
            # Recognize speech using Google's API
            text = self.recognizer.recognize_google(audio, language='hi-IN')
            return text, True
            
        except sr.WaitTimeoutError:
            return "क्षमा करें, कोई ऑडियो दर्ज नहीं हुआ।", False
        except sr.UnknownValueError:
            return "क्षमा करें, मैं समझ नहीं पाया। कृपया फिर से बोलें।", False
        except sr.RequestError as e:
            return f"क्षमा करें, सेवा उपलब्ध नहीं है: {str(e)}", False
        except Exception as e:
            return f"त्रुटि: {str(e)}", False
    
    def _convert_to_wav(self, audio_path: str) -> str:
        """
        Convert audio file to WAV format if needed
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Path to WAV file
        """
        if audio_path.lower().endswith('.wav'):
            return audio_path
        
        try:
            # Load audio file
            audio = AudioSegment.from_file(audio_path)
            
            # Convert to WAV
            wav_path = audio_path.rsplit('.', 1)[0] + '_temp.wav'
            audio.export(wav_path, format='wav')
            
            return wav_path
        except Exception as e:
            print(f"Audio conversion error: {e}")
            return audio_path  # Return original path if conversion fails


def test_stt_from_file():
    """Test function for file-based STT"""
    stt = HindiSTT()
    audio_path = "sample_audio/hindi_test.wav"
    
    if os.path.exists(audio_path):
        text, success = stt.from_audio_file(audio_path)
        print(f"Transcribed: {text}")
        print(f"Success: {success}")
    else:
        print("Sample audio file not found")


if __name__ == "__main__":
    test_stt_from_file()

