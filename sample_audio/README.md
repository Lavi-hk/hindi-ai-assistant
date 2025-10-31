# Sample Audio Files

This directory contains sample Hindi audio files for testing the STT functionality.

## Creating Test Audio

### Option 1: Using gTTS (Recommended)

```python
from gtts import gTTS

# Create audio file
tts = gTTS(text="नमस्ते, आप कैसे हैं? मेरा नाम राहुल है।", lang='hi')
tts.save('hindi_test.wav')
```

### Option 2: Using Online Tools

1. Visit [Google Translate](https://translate.google.com/)
2. Enter text in Hindi
3. Click the speaker icon
4. Right-click and "Save audio as..." to download

### Option 3: Record Your Own

Record yourself speaking in Hindi using:
- Windows Voice Recorder
- Mac QuickTime
- Android/iOS Voice Recorder
- Audacity

## Test Phrases

Here are some test phrases you can record:

1. **Greeting:** "नमस्ते, आप कैसे हैं?"
2. **Name Question:** "मेरा नाम क्या है?"
3. **Weather:** "आज मौसम कैसा है?"
4. **Capabilities:** "आप क्या कर सकते हैं?"
5. **Thank You:** "धन्यवाद, आपका बहुत धन्यवाद"

## File Formats Supported

- WAV (recommended)
- MP3
- OGG
- M4A

## Notes

- Audio should be in Hindi language
- Clarity is important for better transcription
- Duration: 1-10 seconds recommended
- Sample rate: 16kHz recommended

