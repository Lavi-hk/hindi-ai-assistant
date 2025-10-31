"""
Main Streamlit Application for Hindi AI Assistant
Integrates STT, Response Generation, TTS, and Face Detection
"""

import streamlit as st
import tempfile
import os
from speech_to_text import HindiSTT
from response_generator import ResponseGenerator
from text_to_speech import HindiTTS
from face_detection import FaceDetector
import cv2
from PIL import Image
import numpy as np


# Configure Streamlit page
st.set_page_config(
    page_title="हिंदी AI सहायक",
    page_icon="🇮🇳",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF6F00;
        color: white;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #E65100;
        transform: scale(1.02);
    }
    .response-box {
        background-color: #E3F2FD;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'stt_initialized' not in st.session_state:
        st.session_state.stt_initialized = False
    if 'use_llm' not in st.session_state:
        st.session_state.use_llm = False


def main():
    """Main application function"""
    
    initialize_session_state()
    
    # Header
    st.markdown('<p class="main-header">🇮🇳 हिंदी AI सहायक</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Hindi-Speaking AI Assistant</p>', unsafe_allow_html=True)
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ सेटिंग्स (Settings)")
        
        # LLM toggle
        use_llm = st.checkbox(
            "🤖 LLM उत्तर (AI-Generated Responses)",
            value=st.session_state.use_llm,
            help="Enable OpenAI for more intelligent responses (requires API key)"
        )
        st.session_state.use_llm = use_llm
        
        # Face detection toggle
        enable_face_detection = st.checkbox(
            "📷 चेहरा पहचान (Face Detection)",
            value=False,
            help="Enable camera for face detection"
        )
        
        st.markdown("---")
        
        # About section
        st.header("ℹ️ परियोजना के बारे में")
        st.markdown("""
        **तकनीकें (Technologies):**
        - Speech-to-Text: Google Speech Recognition
        - Text-to-Speech: gTTS (Google TTS)
        - Face Detection: OpenCV
        - Response: Rule-based + Optional OpenAI
        
        **विशेषताएं (Features):**
        - Hindi speech recognition
        - Natural responses in Hindi
        - Voice output
        - Real-time face detection
        """)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎤 वॉयस इनपुट (Voice Input)")
        
        # Audio file upload
        uploaded_file = st.file_uploader(
            "ऑडियो फ़ाइल अपलोड करें (Upload Audio File)",
            type=['wav', 'mp3', 'ogg', 'm4a'],
            help="Upload a pre-recorded Hindi audio file"
        )
        
        # Microphone input
        st.markdown("**या**")
        use_mic = st.button("🎙️ माइक्रोफोन से बोलें (Use Microphone)")
        
        # Process audio input
        if uploaded_file is not None:
            with st.spinner("🔊 ऑडियो प्रोसेस कर रहे हैं..."):
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    tmp_file_path = tmp_file.name
                
                # Perform STT
                stt = HindiSTT()
                transcribed_text, success = stt.from_audio_file(tmp_file_path)
                
                # Clean up
                os.unlink(tmp_file_path)
                
                # Display result
                if success:
                    st.success(f"✅ Transcription: **{transcribed_text}**")
                    
                    # Generate response
                    with st.spinner("🤔 उत्तर बना रहे हैं..."):
                        generator = ResponseGenerator(use_llm=st.session_state.use_llm)
                        response = generator.generate_response(transcribed_text)
                    
                    # Display and speak response
                    st.markdown('<div class="response-box">', unsafe_allow_html=True)
                    st.markdown(f"**🤖 Assistant:** {response}")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Convert response to speech
                    with st.spinner("🔊 बोल रहे हैं..."):
                        tts = HindiTTS()
                        audio_bytes = tts.speak_streamlit(response)
                        
                        if audio_bytes:
                            st.audio(audio_bytes, format='audio/mp3')
                    
                    # Add to conversation history
                    st.session_state.conversation_history.append({
                        'input': transcribed_text,
                        'output': response
                    })
                else:
                    st.error(f"❌ {transcribed_text}")
        
        if use_mic:
            st.info("🎙️ Please record your speech and upload the file. Microphone input requires additional setup.")
            st.markdown("""
            **नोट:** Live microphone input requires PyAudio installation and proper audio driver setup.
            For testing, please use the audio file upload option.
            """)
        
        # Text input option
        st.markdown("---")
        st.header("✍️ टेक्स्ट इनपुट (Text Input)")
        text_input = st.text_area(
            "यहाँ हिंदी में लिखें (Type in Hindi)",
            placeholder="उदाहरण: नमस्ते, आप कैसे हैं?",
            height=100
        )
        
        if st.button("➡️ उत्तर बनाएं (Generate Response)"):
            if text_input.strip():
                # Generate response
                with st.spinner("🤔 उत्तर बना रहे हैं..."):
                    generator = ResponseGenerator(use_llm=st.session_state.use_llm)
                    response = generator.generate_response(text_input)
                
                # Display response
                st.markdown('<div class="response-box">', unsafe_allow_html=True)
                st.markdown(f"**🤖 Assistant:** {response}")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Convert to speech
                with st.spinner("🔊 बोल रहे हैं..."):
                    tts = HindiTTS()
                    audio_bytes = tts.speak_streamlit(response)
                    
                    if audio_bytes:
                        st.audio(audio_bytes, format='audio/mp3')
                
                # Add to history
                st.session_state.conversation_history.append({
                    'input': text_input,
                    'output': response
                })
            else:
                st.warning("कृपया कुछ टेक्स्ट दर्ज करें।")
        
        # Conversation history
        if st.session_state.conversation_history:
            st.markdown("---")
            st.header("💬 बातचीत इतिहास (Conversation History)")
            for i, conversation in enumerate(reversed(st.session_state.conversation_history[-5:]), 1):
                with st.expander(f"बातचीत #{len(st.session_state.conversation_history) - i + 1}"):
                    st.markdown(f"**आप:** {conversation['input']}")
                    st.markdown(f"**सहायक:** {conversation['output']}")
            
            if st.button("🗑️ इतिहास साफ़ करें (Clear History)"):
                st.session_state.conversation_history = []
                st.rerun()
    
    with col2:
        st.header("📷 चेहरा पहचान (Face Detection)")
        
        if enable_face_detection:
            # Camera placeholder
            camera_placeholder = st.empty()
            
            with st.spinner("📷 कैमरा शुरू कर रहे हैं..."):
                detector = FaceDetector()
                
                if detector.initialize_camera():
                    ret, frame = detector.get_frame()
                    
                    if ret:
                        face_detected, annotated_frame = detector.detect_face(frame)
                        
                        # Display status
                        if face_detected:
                            st.success("✅ **User Detected**")
                        else:
                            st.warning("❌ **No User Detected**")
                        
                        # Convert frame to RGB and display
                        annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                        camera_placeholder.image(annotated_frame_rgb, channels="RGB", use_column_width=True)
                        
                        detector.release_camera()
                    else:
                        st.error("कैमरा से फ्रेम नहीं मिल सका।")
                else:
                    st.error("कैमरा उपलब्ध नहीं है।")
        else:
            st.info("📷 Face detection is disabled. Enable it from settings.")


if __name__ == "__main__":
    main()

