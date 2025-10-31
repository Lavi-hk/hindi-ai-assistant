# Quick Start Guide - Hindi AI Assistant

Get up and running in 5 minutes! ⚡

## 🚀 Fastest Setup

### Step 1: Install Python
Ensure Python 3.8+ is installed:
```bash
python --version
```

### Step 2: Install Dependencies
```bash
pip install streamlit speechrecognition gtts opencv-python pygame pydub
```

**Windows PyAudio Fix:**
```bash
pip install pipwin
pipwin install pyaudio
```

### Step 3: Create Sample Audio
```bash
python create_sample_audio.py
```

### Step 4: Run the App
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

## 📝 First Test

1. **Upload Audio**: Click "Browse files" → select `sample_audio/hindi_test.wav`
2. **See Magic**: Transcription → Response → Audio output
3. **Try Text**: Type "नमस्ते, आप कैसे हैं?" and click "Generate Response"

## 🎯 That's It!

You're ready to use the Hindi AI Assistant!

---

## 🆘 Troubleshooting

### Audio Issues
- **Windows**: Install Visual C++ Build Tools
- **Mac**: `brew install portaudio`
- **Linux**: `sudo apt-get install portaudio19-dev`

### Import Errors
```bash
pip install --upgrade -r requirements.txt
```

### Streamlit Issues
```bash
pip install --upgrade streamlit
```

## 📚 Next Steps

- Read full [README.md](README.md) for architecture details
- Check [DEMO_INSTRUCTIONS.md](DEMO_INSTRUCTIONS.md) for demo prep
- Explore the code in individual modules

---

**Need Help?** Open an issue or check the documentation.

