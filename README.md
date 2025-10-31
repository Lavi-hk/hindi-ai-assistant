# 🇮🇳 हिंदी AI सहायक (Hindi AI Assistant)

A comprehensive Hindi-speaking AI assistant with speech-to-text, intelligent response generation, text-to-speech, and face detection capabilities.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Challenges & Solutions](#challenges--solutions)
- [Future Improvements](#future-improvements)
- [Demo Video](#demo-video)
- [License](#license)

---

## 🎯 Overview

This project demonstrates a fully functional Hindi-speaking AI assistant that integrates multiple AI components:

- **Speech Recognition** (STT): Converts Hindi speech to text
- **Response Generation**: Intelligent Hindi responses (rule-based + optional LLM)
- **Text-to-Speech** (TTS): Converts Hindi text to natural speech
- **Face Detection**: Real-time webcam-based face detection

Built as a technical assessment for an AI Developer role, showcasing integration skills, clean code practices, and comprehensive documentation.

---

## ✨ Features

### Core Capabilities

1. **Speech-to-Text (STT)**
   - Supports pre-recorded audio files (WAV, MP3, OGG, M4A)
   - Live microphone input capability
   - Google Speech Recognition API for Hindi (hi-IN)
   - Automatic audio format conversion

2. **Response Generation**
   - Rule-based Hindi responses for common queries
   - Optional OpenAI GPT integration for complex questions
   - Context-aware responses
   - Conversational flow handling

3. **Text-to-Speech (TTS)**
   - Google Text-to-Speech (gTTS) for Hindi
   - Natural voice output
   - Audio playback integration
   - Streamlit-compatible audio generation

4. **Face Detection**
   - Real-time webcam face detection
   - OpenCV Haar Cascade classifier
   - Visual feedback with bounding boxes
   - User presence detection

5. **User Interface**
   - Modern Streamlit web interface
   - Bilingual (Hindi/English) UI
   - Conversation history
   - Audio visualization
   - Responsive design

---

## 🛠 Technologies Used

### Core Libraries

| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| **Streamlit** | Web UI Framework | Rapid development, easy deployment, built-in audio/video support |
| **SpeechRecognition** | STT Engine | Well-documented, supports Google API (Hindi), easy integration |
| **gTTS** | TTS Engine | Free, high-quality Hindi TTS, simple API |
| **OpenCV** | Face Detection | Robust detection, real-time performance, mature library |
| **PyGame** | Audio Playback | Lightweight, cross-platform audio handling |
| **OpenAI** | LLM (Optional) | Advanced responses, GPT-3.5 integration |

### Language Support
- **Primary Language**: Hindi (Devanagari script)
- **Input Methods**: Audio, Text
- **Output Formats**: Text, Audio

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Internet connection (for Google APIs)
- Microphone (optional, for live input)
- Webcam (optional, for face detection)

### Step-by-Step Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd hindi-ai-assistant
```

2. **Create virtual environment** (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

**Note:** If you encounter issues with `pyaudio` installation:

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

**Mac:**
```bash
brew install portaudio
pip install pyaudio
```

4. **Environment Configuration** (Optional)
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key if using LLM features
```

5. **Verify Installation**
```bash
python -c "import streamlit, speech_recognition, gtts, cv2; print('All dependencies installed successfully!')"
```

---

## 🚀 Usage

### Running the Application

Launch the Streamlit app:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the Assistant

#### 1. **Audio File Input**
- Click "Browse files" to upload a Hindi audio file
- Supported formats: WAV, MP3, OGG, M4A
- Wait for transcription and response

#### 2. **Text Input**
- Type your query in Hindi in the text box
- Click "Generate Response"
- Listen to the audio response

#### 3. **Face Detection**
- Enable "Face Detection" in sidebar
- Grant camera permissions
- View real-time face detection

#### 4. **LLM Mode**
- Toggle "LLM Responses" in sidebar
- Requires OpenAI API key in `.env`
- Generates more intelligent responses

---

## 🏗 Architecture

### Project Structure

```
hindi-ai-assistant/
│
├── app.py                      # Main Streamlit application
├── speech_to_text.py          # STT module
├── response_generator.py      # Response generation
├── text_to_speech.py          # TTS module
├── face_detection.py          # Face detection
├── requirements.txt           # Dependencies
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── README.md                 # Documentation
│
└── sample_audio/             # Test audio files
    ├── hindi_test.wav
    └── ...
```

### Module Design

**1. Speech-to-Text (`speech_to_text.py`)**
```python
HindiSTT
├── from_audio_file()      # File input
└── from_microphone()      # Live input
```

**2. Response Generation (`response_generator.py`)**
```python
ResponseGenerator
├── generate_response()    # Main method
├── _match_rule()         # Rule-based matching
└── _get_llm_response()   # LLM integration
```

**3. Text-to-Speech (`text_to_speech.py`)**
```python
HindiTTS
├── speak()               # Play audio
└── speak_streamlit()     # Return audio bytes
```

**4. Face Detection (`face_detection.py`)**
```python
FaceDetector
├── initialize_camera()
├── detect_face()
└── release_camera()
```

### Flow Diagram

```
User Input → STT → Text → Response Generator → Response → TTS → Audio Output
                ↓
         Conversation History
                ↓
         Face Detection (Optional)
```

---

## 📚 API Reference

### Speech-to-Text

```python
from speech_to_text import HindiSTT

stt = HindiSTT()

# From audio file
text, success = stt.from_audio_file("audio.wav")

# From microphone
text, success = stt.from_microphone(duration=5)
```

### Response Generation

```python
from response_generator import ResponseGenerator

generator = ResponseGenerator(use_llm=True)

response = generator.generate_response("नमस्ते, आप कैसे हैं?")
```

### Text-to-Speech

```python
from text_to_speech import HindiTTS

tts = HindiTTS()

tts.speak("नमस्ते! मैं ठीक हूं।")

# For Streamlit
audio_bytes = tts.speak_streamlit("नमस्ते! मैं ठीक हूं।")
```

### Face Detection

```python
from face_detection import FaceDetector

detector = FaceDetector()
detector.initialize_camera()

ret, frame = detector.get_frame()
face_detected, annotated_frame = detector.detect_face(frame)

detector.release_camera()
```

---

## 🤔 Challenges & Solutions

### Challenge 1: Hindi Language Support

**Problem:** Ensuring proper Devanagari script handling and correct phonetics.

**Solution:** 
- Used Google Speech Recognition with `hi-IN` language code
- Tested with multiple Hindi audio samples
- Implemented UTF-8 encoding throughout
- Added Hindi-specific error messages

### Challenge 2: Audio Format Compatibility

**Problem:** Supporting multiple audio formats while SpeechRecognition only accepts WAV.

**Solution:**
- Used `pydub` for format conversion
- Implemented automatic WAV conversion
- Temporary file cleanup after processing

### Challenge 3: Real-time Integration

**Problem:** Integrating STT, TTS, and face detection smoothly.

**Solution:**
- Modular design with separate classes
- Async operations where possible
- Progress indicators in UI
- Clean resource management

### Challenge 4: LLM Cost & Latency

**Problem:** OpenAI API costs and slower response times.

**Solution:**
- Hybrid approach: rule-based first, LLM fallback
- Made LLM optional (toggle in UI)
- Cached common responses
- Set reasonable token limits

### Challenge 5: Cross-platform Audio

**Problem:** Audio playback working differently on Windows/Mac/Linux.

**Solution:**
- Used pygame for cross-platform compatibility
- Provided platform-specific installation notes
- Streamlit audio widget as fallback

---

## 🔮 Future Improvements

### Short-term Enhancements

1. **Voice Activity Detection (VAD)**
   - Auto-stop recording when user finishes speaking
   - Better microphone handling

2. **Conversation Memory**
   - Multi-turn conversation context
   - Remember user preferences/name
   - Session-based memory

3. **More Language Support**
   - Add English as alternative
   - Code-switching support (Hindi-English mix)

4. **Enhanced Face Detection**
   - Emotion detection
   - User recognition
   - Engagement tracking

### Long-term Vision

1. **Advanced STT**
   - Whisper model integration
   - Offline capability
   - Domain-specific adaptation

2. **Better TTS**
   - Coqui TTS for high-quality voices
   - Custom voice cloning
   - Emotion-aware speech

3. **Conversational AI**
   - RAG (Retrieval Augmented Generation)
   - Knowledge base integration
   - Skill-based architecture

4. **Deployment**
   - Cloud deployment (Heroku, AWS, GCP)
   - Docker containerization
   - CI/CD pipeline

5. **Analytics**
   - Usage tracking
   - Performance metrics
   - User feedback collection

---

## 🎬 Demo Video

Watch the demo video to see the Hindi AI Assistant in action:

**Demo Link:** [YouTube/Vimeo/Demo URL]

**Features Demonstrated:**
1. Audio file upload and transcription
2. Text input and response generation
3. Text-to-speech output
4. Face detection with webcam
5. Conversation history
6. LLM-powered responses

---

## 📝 Sample Interactions

### Example 1: Greeting
```
User: "नमस्ते, आप कैसे हैं?"
Assistant: "नमस्ते! मैं ठीक हूं, धन्यवाद! आप कैसे हैं?"
```

### Example 2: Name Question
```
User: "मेरा नाम क्या है?"
Assistant: "मेरा नाम हिंदी AI सहायक है। आप मुझे कुछ भी पूछ सकते हैं।"
```

### Example 3: Weather Query
```
User: "आज मौसम कैसा है?"
Assistant: "क्षमा करें, मैं मौसम के बारे में जानकारी नहीं दे सकता।"
```

### Example 4: Capabilities
```
User: "आप क्या कर सकते हैं?"
Assistant: "मैं हिंदी में बात कर सकता हूं, प्रश्नों का उत्तर दे सकता हूं, 
और आपकी मदद कर सकता हूं।"
```

---

## 🧪 Testing

### Unit Tests

Test individual components:
```bash
# Test STT
python speech_to_text.py

# Test TTS
python text_to_speech.py

# Test Response Generator
python response_generator.py

# Test Face Detection
python face_detection.py
```

### Integration Test

Run the full application:
```bash
streamlit run app.py
```

Upload `sample_audio/hindi_test.wav` and verify the workflow.

---

## 📧 Support & Contact

For questions, issues, or contributions:

- **Repository:** [GitHub Link]
- **Issues:** [Issues Link]
- **Email:** [Your Email]

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Google Speech Recognition API
- gTTS (Google Text-to-Speech)
- OpenAI for GPT models
- OpenCV community
- Streamlit team

---

## ✅ Checklist

- [x] Speech-to-Text (Hindi) ✓
- [x] Response Generation ✓
- [x] Text-to-Speech (Hindi) ✓
- [x] Face Detection ✓
- [x] Modern UI ✓
- [x] Error Handling ✓
- [x] Documentation ✓
- [x] Sample Audio Files ✓
- [ ] Demo Video (To be recorded)

---

**Made with ❤️ for AI Developer Assessment**

*"Building bridges between human communication and artificial intelligence in Hindi"*

