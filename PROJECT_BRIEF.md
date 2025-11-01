# Hindi AI Assistant - Project Brief

## 1. Technologies/APIs Used and Why

### Core Technologies

| Technology | Purpose | Why Chosen |
|------------|---------|------------|
| **Python 3.11** | Programming language | AI ecosystem, extensive libraries, active community |
| **Streamlit** | Web UI framework | Fast prototyping, built-in audio/video widgets, easy cloud deployment |
| **Google Speech Recognition** | Speech-to-Text (STT) | Free tier, excellent Hindi support (hi-IN), easy integration |
| **gTTS (Google Text-to-Speech)** | Text-to-Speech (TTS) | Free, high-quality Hindi voices, simple API, no credentials needed |
| **OpenCV (Headless)** | Face detection | Robust computer vision, mature library, pre-trained models |
| **OpenAI GPT-3.5** | Advanced responses | Intelligent conversational AI, optional for complex queries |

### Why These Choices?

1. **Google APIs for Speech**: Free tier with 50+ requests/day, excellent Hindi accuracy, no authentication complexity
2. **Streamlit**: No frontend skills needed, auto-deployment to cloud, built-in widgets for audio playback
3. **Python 3.11**: Balances modern features with library compatibility (Python 3.13 missing `aifc` for speech_recognition)
4. **OpenCV Headless**: Removes GUI dependencies for cloud deployment while maintaining computer vision capabilities
5. **Hybrid Response System**: Rule-based (fast, free) + optional LLM (intelligent, cost-effective)

### Architecture Decision

**Modular Design**: Separate classes for STT, TTS, Response Generation, and Face Detection
- Easy to test individually
- Replace components without breaking others
- Clear separation of concerns

---

## 2. Setup and Run Instructions

### Local Development

#### Windows (PowerShell)

```powershell
# 1. Clone repository
git clone https://github.com/Lavi-hk/hindi-ai-assistant.git
cd hindi-ai-assistant

# 2. Create virtual environment
python -m venv venv
./venv/Scripts/Activate.ps1

# 3. Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Note: PyAudio requires pipwin on Windows
python -m pip install pipwin
python -m pipwin install pyaudio

# 4. Create sample audio files
python create_sample_audio.py

# 5. Run application
streamlit run app.py
```

Open browser at `http://localhost:8501`

#### Linux/Mac

```bash
# 1-2. Same as above
python -m venv venv
source venv/bin/activate

# 3. Install dependencies (Linux)
sudo apt-get install portaudio19-dev python3-pyaudio
pip install -r requirements.txt

# 4-5. Same as above
python create_sample_audio.py
streamlit run app.py
```

### Cloud Deployment (Streamlit)

1. **Push to GitHub**: Your repo is at `github.com/Lavi-hk/hindi-ai-assistant`
2. **Deploy on Streamlit Cloud**:
   - Go to https://share.streamlit.io
   - Click "New app" → Connect GitHub
   - Select repository and branch (main)
   - Python version: 3.11 (auto-configured via `runtime.txt`)
   - Advanced settings → Secrets (optional): Add `OPENAI_API_KEY` if using LLM mode
   - Click "Deploy"

3. **Access**: Your app will be live at `https://[your-app].streamlit.app`

### Quick Test

After running locally or deploying:

1. **Upload Audio**: Upload `sample_audio/hindi_test.wav`
2. **See Result**: Transcription → Response → Audio playback
3. **Try Text**: Type "नमस्ते, आप कैसे हैं?" in text box
4. **View History**: Scroll to see conversation history

---

## 3. Challenges Faced and How You Solved Them

### Challenge 1: Python 3.13 Compatibility

**Problem**: SpeechRecognition library imports `aifc` module, which was removed in Python 3.13.

**Solution**:
- Created `runtime.txt` with `3.11` to pin Python version
- Python 3.11 has `aifc` and works with all dependencies
- This is a permanent fix for Streamlit Cloud deployments

### Challenge 2: OpenCV Import Error in Cloud

**Problem**: `cv2` native module fails to load in headless environments without proper libraries.

**Solution**:
- Switched to `opencv-python-headless` (no GUI dependencies)
- Implemented lazy import: face detection only loads when user enables it
- Added try-except in `face_detection.py` to gracefully handle missing OpenCV
- Cloud users see friendly error message; doesn't break the app

### Challenge 3: PyGame Compilation on Cloud

**Problem**: PyGame requires SDL2 system libraries, difficult to compile in cloud environments.

**Solution**:
- Removed pygame entirely (not needed for core functionality)
- Streamlit has built-in `st.audio()` widget for playback
- Only `speak_streamlit()` method needed, which uses BytesIO
- Zero dependencies on system audio libraries

### Challenge 4: Dependency Conflict (Streamlit + NumPy)

**Problem**: 
- Streamlit 1.28.0 requires `pillow<11` and `numpy<2`
- Python 3.13 prefers newer versions
- Pyramid of conflicts in dependency resolution

**Solution**:
- Upgraded to Streamlit 1.41.1 (compatible with numpy 2.x)
- Kept Python 3.11 (best compatibility)
- Set `numpy==1.26.4` and `pillow==10.4.0` (proven stable)
- All dependencies now resolve cleanly

### Challenge 5: Hindi Language Handling

**Problem**: Ensuring proper Devanagari script display and phonetic accuracy in speech.

**Solution**:
- Used `hi-IN` language code in Google APIs
- UTF-8 encoding throughout codebase
- Tested with native Hindi speakers
- Hindi-specific error messages for better UX

### Challenge 6: Microphone Input in Cloud

**Problem**: Browser microphone access requires WebRTC and proper setup; Streamlit Cloud has limitations.

**Solution**:
- Primary input: File upload (works everywhere)
- Fallback: Text input (always works)
- Microphone: Optional, documented for local use only
- Clear messaging to users about input methods

### Challenge 7: Cost Management for LLM

**Problem**: OpenAI API costs money per request; could get expensive with high usage.

**Solution**:
- **Hybrid approach**: Rule-based matching first (instant, free)
- LLM fallback only if no rule matches
- Made LLM optional via UI toggle
- Documented token limits (150 tokens per response)
- Estimated cost: ~$0.0002 per complex query

---

## 4. Ideas for Improvement

### Short-term Enhancements (1-2 weeks)

#### 1. Voice Activity Detection (VAD)
- Auto-stop recording when user finishes speaking
- Better microphone experience
- **Implementation**: Use `webrtcvad` library

#### 2. Conversation Memory
- Remember user's name after first mention
- Multi-turn context (e.g., "What about tomorrow?")
- Session-based memory using Streamlit session state
- **Implementation**: Store context in `st.session_state['context']`

#### 3. Error Messages in Hindi
- Currently English for system errors
- Full Hindi localization
- **Implementation**: Error message mapping dictionary

#### 4. Audio Visualization
- Waveform display during playback
- Upload progress bar
- **Implementation**: Use `st.pyplot()` or `plotly` for charts

#### 5. Download Audio
- Save generated audio as MP3
- Share conversation history
- **Implementation**: `st.download_button()` with audio bytes

### Medium-term (1-2 months)

#### 6. Multi-language Support
- Add English as alternative language
- Code-switching (Hindi-English mix)
- **Implementation**: Language detector, separate response rules per language

#### 7. Emotion Detection
- Recognize sentiment from speech/text
- Adjust response tone accordingly
- **Implementation**: Use `textblob` or `vaderSentiment` for sentiment analysis

#### 8. Offline Whisper Model
- Replace Google STT with Whisper (local)
- No internet required for transcription
- **Implementation**: Hugging Face Whisper, quantized model for speed

#### 9. User Profiles
- Multiple users on same instance
- Personalized responses per user
- **Implementation**: Simple JSON-based storage, user authentication

#### 10. Analytics Dashboard
- Track usage statistics
- Most common queries
- **Implementation**: Streamlit's `st.metrics`, Chart components

### Long-term Vision (3-6 months)

#### 11. RAG (Retrieval Augmented Generation)
- Knowledge base integration
- Answer questions from documents
- **Implementation**: Vector database (Pinecone/ChromaDB), embeddings (OpenAI/text-embedding-ada-002)

#### 12. Custom Voice Cloning
- Replace gTTS with user's cloned voice
- More natural speech
- **Implementation**: Coqui TTS, voice cloning APIs

#### 13. Real-time Streaming STT
- Live transcription as user speaks
- WebSocket integration
- **Implementation**: Deepgram/AssemblyAI streaming APIs

#### 14. Multi-modal Input
- Support image uploads (OCR Hindi text)
- Video analysis with face + speech
- **Implementation**: EasyOCR, moviepy for video processing

#### 15. Mobile App
- Native iOS/Android app
- Push notifications
- **Implementation**: React Native or Flutter

#### 16. Scalability & Deployment
- Docker containerization (already in place)
- Kubernetes deployment
- Load balancing for multiple users
- **Implementation**: Docker + K8s manifests, CI/CD with GitHub Actions

#### 17. Advanced Face Detection
- Age/gender estimation
- Emotion recognition from facial expressions
- Multiple people detection
- **Implementation**: MediaPipe or face_recognition library

#### 18. Intent Classification
- Better understanding of user requests
- Slot filling for structured queries
- **Implementation**: Rasa NLU or custom BERT model

#### 19. Security & Privacy
- End-to-end encryption
- Data anonymization
- GDPR compliance
- **Implementation**: Encryption libraries, secure storage

#### 20. Voice Biometrics
- Identify users by voice
- Security enhancements
- **Implementation**: SpeechT5 or similar models

### Quick Wins (Can implement today)

1. **Add more Hindi responses**: Expand rule patterns in `response_generator.py`
2. **Better loading indicators**: Use `st.spinner()` with custom messages
3. **Export conversation**: Add download button for chat history
4. **Keyboard shortcuts**: Enable quick actions
5. **Dark mode**: Theme toggle in Streamlit

---

## Summary

### What Works Well
✅ Full Hindi STT → Response → TTS pipeline  
✅ Cloud deployment on Streamlit  
✅ Modular, maintainable code  
✅ Error handling for edge cases  
✅ Clean UI with bilingual support  

### What Could Be Better
⚠️ Offline capability (requires internet for Google APIs)  
⚠️ Multi-turn conversation context  
⚠️ Advanced features (emotion, voice cloning)  

### Deployment Status
- ✅ GitHub: https://github.com/Lavi-hk/hindi-ai-assistant
- ✅ Streamlit Cloud: Live (auto-deploys from main branch)
- ✅ Docker: Ready for containerized deployment
- ✅ Documentation: Comprehensive README, Architecture, Testing guides

### Next Steps
1. Record demo video (2-5 minutes)
2. Add conversation memory
3. Implement offline Whisper for STT
4. Deploy to production cloud (AWS/GCP)

---

**Built with ❤️ for AI Developer Assessment**  
*Demonstrating end-to-end AI integration, clean code, and production deployment*

