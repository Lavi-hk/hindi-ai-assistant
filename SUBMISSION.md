# Submission Guide

Use this to submit your Hindi AI Assistant assessment.

## 1) Prepare Repository

- Create a new GitHub repository (public or private): `hindi-ai-assistant`
- Initialize and push code

```bash
# In project root
git init
git add .
git commit -m "feat: Hindi AI Assistant initial implementation"
# Replace with your repo URL
git branch -M main
git remote add origin https://github.com/<your-username>/hindi-ai-assistant.git
git push -u origin main
```

## 2) Include Required Items

- Working code (already included)
- `README.md` with setup and usage (done)
- Sample audio (create via `python create_sample_audio.py`)
- Short demo video (2–5 mins)
- Brief documentation (approach, tech choices, challenges, improvements)
  - Covered in `README.md`, `PROJECT_SUMMARY.md`, `ARCHITECTURE.md`

## 3) Record Demo Video (2–5 mins)

Suggested outline:
- 10s: Title slide (project name, your name)
- 30s: What it does (STT → Response → TTS, optional Face Detection)
- 60–120s: Live walkthrough
  - Upload `sample_audio/hindi_test.wav` → show transcription and audio response
  - Type a query in Hindi → show response and audio
  - Toggle Face Detection → show detection
  - Toggle LLM (if you set API key) → ask a complex question
- 30s: Architecture quick overview (show `ARCHITECTURE.md` diagram)
- 20s: Challenges and improvements (from README)
- 10s: Closing

Tips:
- Use OBS or built-in recorder
- Ensure mic/speaker levels are good
- Keep it concise and smooth

## 4) Share Submission Links

Provide:
- GitHub Repo URL
- Demo Video URL (YouTube unlisted/Drive link)
- Optional: ZIP of repo (if required)

## 5) Quick Local Run (Windows PowerShell)

```powershell
# Create venv
python -m venv venv

# Activate
./venv/Scripts/Activate.ps1

# Install dependencies (PyAudio optional for mic)
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# If you need microphone input (optional)
# Install PyAudio via pipwin (prebuilt wheel)
python -m pip install pipwin
python -m pipwin install pyaudio

# Create sample audio (for upload testing)
python create_sample_audio.py

# Run app
streamlit run app.py
```

Notes:
- If PyAudio fails, you can use file upload and text input paths (microphone optional).
- Allow camera permissions in browser for Face Detection.

## 6) Checklist Before Submission

- [ ] App runs locally (`streamlit run app.py`)
- [ ] Audio upload path works end-to-end (STT → Response → TTS)
- [ ] Text input path works end-to-end
- [ ] Face detection shows user status
- [ ] README accurate and complete
- [ ] Demo video recorded and uploaded
- [ ] Repo pushed to GitHub

Good luck! 🚀
