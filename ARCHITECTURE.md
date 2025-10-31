# Architecture Documentation

## System Overview

The Hindi AI Assistant is built with a modular, extensible architecture that separates concerns and enables easy maintenance and enhancement.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Streamlit Web Interface                       │
│                         (app.py)                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
┌───────▼────────┐                   ┌──────────▼─────────┐
│   User Input   │                   │   User Interface   │
│   (Audio/Text) │                   │   (Display/Output) │
└───────┬────────┘                   └──────────┬─────────┘
        │                                       │
        └───────────────────┬───────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
┌───────▼────────┐                  ┌───────────▼─────────┐
│   Hindi STT    │                  │  Response Generator │
│ (speech_to_    │                  │  (response_gener-   │
│  text.py)      │                  │   ator.py)          │
└────────────────┘                  └───────────┬─────────┘
                                                │
                                        ┌───────┴────────┐
                                        │                │
                                ┌───────▼─────┐  ┌──────▼──────────┐
                                │ Rule-Based  │  │   OpenAI LLM    │
                                │  Responses  │  │  (Optional)     │
                                └─────────────┘  └─────────────────┘
                                        │                │
                                        └───────┬────────┘
                                                │
                                        ┌───────▼─────────┐
                                        │   Hindi TTS     │
                                        │ (text_to_       │
                                        │  speech.py)     │
                                        └─────────────────┘
```

## Component Details

### 1. Speech-to-Text Module (`speech_to_text.py`)

**Purpose:** Convert Hindi speech to text

**Key Classes:**
- `HindiSTT`: Main STT handler

**Methods:**
- `from_audio_file(audio_path)`: Process pre-recorded audio
- `from_microphone(duration)`: Real-time microphone input
- `_convert_to_wav(audio_path)`: Format conversion

**Technology:**
- Google Speech Recognition API
- Supports Hindi (hi-IN) language code
- Automatic audio format conversion via pydub

**Flow:**
```
Audio Input → Format Check → Convert to WAV → Google API → Text Output
```

### 2. Response Generation Module (`response_generator.py`)

**Purpose:** Generate intelligent Hindi responses

**Key Classes:**
- `ResponseGenerator`: Main response handler

**Methods:**
- `generate_response(user_input)`: Main entry point
- `_match_rule(user_input)`: Rule-based matching
- `_get_llm_response(user_input)`: LLM fallback

**Features:**
- Pattern-based matching
- Category-based responses
- Optional OpenAI GPT integration
- Fallback to default responses

**Flow:**
```
User Input → Pattern Match → Rule-Based Response
                    ↓ (if no match)
              LLM Fallback → OpenAI Response
```

**Response Categories:**
- Greetings
- Name questions
- Weather queries
- Time queries
- Capabilities
- Thank you
- Farewell
- Unknown queries

### 3. Text-to-Speech Module (`text_to_speech.py`)

**Purpose:** Convert Hindi text to speech

**Key Classes:**
- `HindiTTS`: Main TTS handler

**Methods:**
- `speak(text, save_file)`: Generate and play audio
- `speak_streamlit(text)`: Return audio bytes for Streamlit
- `_play_audio(file_path)`: Playback using pygame

**Technology:**
- Google TTS (gTTS)
- Hindi language (hi) support
- pygame for audio playback

**Flow:**
```
Text Input → gTTS → MP3 Generation → Playback/Return Audio
```

### 4. Face Detection Module (`face_detection.py`)

**Purpose:** Real-time face detection using webcam

**Key Classes:**
- `FaceDetector`: Face detection handler

**Methods:**
- `initialize_camera(camera_index)`: Setup webcam
- `detect_face(frame)`: Process frame and detect faces
- `get_frame()`: Capture frame from camera
- `release_camera()`: Clean up resources

**Technology:**
- OpenCV Haar Cascade classifier
- Real-time video processing
- Bounding box visualization

**Flow:**
```
Camera → Frame Capture → Grayscale → Face Detection → Visual Feedback
```

### 5. Main Application (`app.py`)

**Purpose:** Streamlit-based web interface

**Key Features:**
- Audio file upload
- Text input
- Microphone input support
- Face detection toggle
- LLM mode toggle
- Conversation history
- Audio playback
- Bilingual UI (Hindi/English)

**UI Components:**
- File uploader
- Text area
- Audio player
- Camera viewer
- History panel
- Settings sidebar

**State Management:**
- Session state for conversation history
- User preferences
- Module initialization flags

## Data Flow

### Complete Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. User Input                                                   │
│    - Audio file upload OR                                       │
│    - Text input                                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. Speech-to-Text (if audio)                                    │
│    - Format conversion                                           │
│    - Google API call                                             │
│    - Transcription display                                       │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. Response Generation                                          │
│    - Pattern matching                                            │
│    - LLM (optional)                                              │
│    - Response text                                               │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. Text-to-Speech                                               │
│    - Audio generation                                            │
│    - Playback                                                    │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. Display & History                                            │
│    - Show response                                               │
│    - Store in history                                            │
│    - Audio player                                                │
└─────────────────────────────────────────────────────────────────┘
```

### Parallel Processing

```
Face Detection (Optional)
┌─────────────────────────┐
│ Camera → OpenCV → UI    │
└─────────────────────────┘
```

## Design Patterns

### 1. Singleton-like Pattern
- Each module has a single instance
- Shared across app lifecycle

### 2. Strategy Pattern
- Rule-based vs LLM responses
- Different strategies for different scenarios

### 3. Factory Pattern
- Audio format conversion
- Response generation

### 4. Observer Pattern
- Session state management
- UI updates based on state

## Error Handling

### Graceful Degradation
- STT failure → Show error message
- LLM failure → Fallback to rule-based
- TTS failure → Show text only
- Camera failure → Disable face detection

### Error Types
1. **Network Errors**: Google API unavailable
2. **Format Errors**: Unsupported audio formats
3. **Permission Errors**: Camera/microphone access
4. **API Errors**: Missing API keys
5. **Resource Errors**: Memory/CPU issues

## Performance Considerations

### Latency Breakdown
- STT: 2-3 seconds
- Rule-based response: <0.5 seconds
- LLM response: 3-5 seconds
- TTS: 1-2 seconds
- **Total**: 5-10 seconds

### Optimization Strategies
1. **Caching**: Audio files, responses
2. **Async**: Parallel operations where possible
3. **Lazy Loading**: Load models on demand
4. **Connection Pooling**: Reuse API connections

## Security Considerations

1. **API Keys**: Environment variables, never hardcode
2. **File Upload**: Validate file types and sizes
3. **Camera**: User consent for access
4. **Data Privacy**: No permanent storage
5. **Sanitization**: Input validation

## Scalability

### Current Limitations
- Single user
- Local processing
- No database
- No authentication

### Future Scaling
- Multi-user support
- Cloud deployment
- Database for history
- User authentication
- Load balancing
- CDN for audio files

## Extensibility Points

1. **New Languages**: Add language codes to STT/TTS
2. **New Responses**: Add to rule patterns
3. **New Features**: Add new modules
4. **New Integrations**: Connect external APIs
5. **New UI**: Customize Streamlit components

## Testing Strategy

### Unit Tests
- Test each module independently
- Mock external dependencies

### Integration Tests
- Test full workflow
- Real API calls (test environment)

### User Acceptance Tests
- Test with real users
- Collect feedback

## Deployment Architecture

### Development
```
Local Machine → Streamlit Server → Local Browser
```

### Production (Future)
```
Cloud VM → Docker → Load Balancer → Users
        ↓
     Database
        ↓
   External APIs
```

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|------------|---------|
| UI | Streamlit | Web interface |
| STT | Google Speech API | Speech recognition |
| NLU | Rule-based + OpenAI | Response generation |
| TTS | Google TTS | Text-to-speech |
| Vision | OpenCV | Face detection |
| Audio | pydub, pygame | Audio processing |
| Infrastructure | Python | Backend logic |

## API Integration

### Google Services
- Speech Recognition (free tier)
- Text-to-Speech (free tier)
- Rate limiting: ~50 requests/day

### OpenAI
- GPT-3.5-turbo (pay-per-use)
- Optional integration
- Cost optimization: hybrid approach

## Future Enhancements

1. **Offline Mode**: Local models
2. **Multi-turn**: Conversation context
3. **Emotion Detection**: Sentiment analysis
4. **Voice Cloning**: Custom voices
5. **Knowledge Base**: RAG implementation
6. **Analytics**: Usage tracking
7. **Mobile App**: React Native
8. **WebSocket**: Real-time streaming

---

**Architecture designed for:**
- Maintainability
- Extensibility  
- Performance
- User Experience

