# MindfulCompanion - Installation & Setup Guide

## 🧠 About MindfulCompanion

MindfulCompanion is an AI-powered mental wellness chatbot that provides emotional support, active listening, mood tracking, and wellness tips. It uses natural language processing and machine learning to understand emotions and deliver contextual responses.

**⚠️ Disclaimer**: This is NOT a replacement for professional mental health care. If you're in crisis, please contact:
- **988 Suicide & Crisis Lifeline** (US)
- **Crisis Text Line**: Text HOME to 741741
- **Emergency**: Call 911

---

## 🚀 Quick Start (Windows)

### Prerequisites
- Python 3.14+ installed
- 2+ GB free disk space
- Internet connection

### Installation Steps

1. **Clone or download the project**
   ```powershell
   cd C:\Users\YourUsername\Desktop\PLP
   ```

2. **Create virtual environment** (if not already created)
   ```powershell
   C:\Users\YourUsername\AppData\Local\Programs\Python\Python314\python.exe -m venv .venv
   ```

3. **Activate virtual environment**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Configure Hugging Face API key**
   - Create a `.env` file in the project root:
   ```
   HUGGINGFACE_API_KEY=your_api_key_here
   ```
   - Get your key from: https://huggingface.co/settings/tokens

6. **Run the app**
   ```powershell
   streamlit run app.py
   ```

The app will open at: `http://localhost:8502`

---

## 📦 Dependencies

### Core Requirements
- `streamlit==1.50.0` - Web UI framework
- `python-dotenv==1.2.1` - Environment variable management
- `requests==2.32.5` - HTTP requests
- `nltk==3.9.2` - Natural language processing
- `scikit-learn==1.7.2` - Machine learning
- `pandas==2.3.3` - Data manipulation
- `transformers==4.57.3` - NLP models
- `huggingface_hub==1.1.6` - LLM integration
- `plotly==5.18.0` - Data visualization
- `textblob==0.17.1` - Sentiment analysis

### Optional (Voice Input)
- `SpeechRecognition==3.14.4` - Speech-to-text
- `PyAudio` - Microphone access (platform-specific)

### Optional (Translation)
- `googletrans==4.0.2` - Multi-language translation

---

## 🎤 Voice Input Setup (Windows)

### Option 1: Install PyAudio via Wheel (Recommended)

1. Download the appropriate wheel for your Python version:
   - **Python 3.14**: `PyAudio-0.2.x-cp314-cp314-win_amd64.whl`
   - Visit: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

2. Install the wheel:
   ```powershell
   .\.venv\Scripts\pip.exe install C:\path\to\PyAudio-0.2.x-cp314-cp314-win_amd64.whl
   ```

3. Test the microphone:
   - Open the app
   - Go to sidebar → Voice Input → Click "🔊 Test Microphone"
   - Allow microphone access when prompted

### Option 2: Use Text Input (No Setup Required)
- If PyAudio is not installed, voice features gracefully fall back to text input
- Click the 🎤 button → You'll see instructions to install PyAudio
- For now, type your message in the chat box

---

## 🌍 Translation Support

The app supports 20+ languages via Google Translate:
- English, Spanish, French, German, Italian, Portuguese
- Dutch, Russian, Chinese, Japanese, Korean
- Arabic, Hindi, Turkish, Polish, Swedish, Norwegian, Danish, Finnish, Greek

Select your language from the sidebar to see responses translated automatically.

---

## 📊 Features

### 💬 Chat Interface
- Real-time conversation with AI wellness companion
- Emotion detection & mood tracking
- Context-aware responses using LLM

### 🎤 Voice Input (Optional)
- Convert speech to text via Google Speech Recognition
- Automatic language detection
- Microphone test utility

### 🌍 Multi-Language Support
- 20+ languages supported
- Auto-detect language from user input
- Translate conversations in real-time

### 📈 Mood Tracking
- Log emotional state after each chat
- Track mood trends over time
- Visualize mood statistics

### 📥 Journal Export
- Export mood logs as JSON, CSV, or text
- Download conversation history
- Generate mood reports

### 🔒 Safety Features
- Crisis detection & resources
- Inappropriate content filtering
- Conversation privacy (local storage)

---

## 📁 Project Structure

```
PLP/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env                        # API keys (not in git)
├── .gitignore                  # Git ignore patterns
├── README.md                   # This file
│
├── backend/
│   ├── __init__.py
│   ├── emotion_detector.py     # Emotion analysis
│   ├── llm_handler.py          # LLM integration (Hugging Face)
│   ├── mood_tracker.py         # Mood logging & stats
│   ├── response_generator.py   # Response orchestration
│   └── safety_filter.py        # Content filtering
│
├── utils/
│   ├── __init__.py
│   ├── helpers.py              # Utility functions
│   ├── journal_exporter.py     # Export journal data
│   ├── translator.py           # Translation handler
│   └── voice_handler.py        # Voice input handler
│
├── data/
│   ├── mood_logs.csv           # Mood tracking database
│   └── wellness_tips.json      # Wellness tips database
│
└── .streamlit/
    └── config.toml             # Streamlit configuration
```

---

## 🔧 Configuration

### Environment Variables (.env)
```
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxx
```

### Streamlit Config (.streamlit/config.toml)
- Theme: Light/Dark mode
- Page layout: Wide/Centered
- Max upload size: 200 MB

---

## 🐛 Troubleshooting

### Issue: "No module named 'streamlit'"
**Solution**: Ensure virtual environment is activated
```powershell
.\.venv\Scripts\Activate.ps1
pip install streamlit
```

### Issue: "ModuleNotFoundError: No module named 'pyaudio'"
**Solution**: Voice input is optional
- Install PyAudio using the wheel method above, OR
- Use text input (feature gracefully degrades)

### Issue: "ModuleNotFoundError: No module named 'regex'"
**Solution**: Install regex
```powershell
.\.venv\Scripts\pip.exe install regex
```

### Issue: LLM responses are generic/fallback
**Solution**: Check Hugging Face API key
```powershell
# Verify key in .env file
type .env
```

### Issue: Port 8502 already in use
**Solution**: Use a different port
```powershell
streamlit run app.py --server.port 8503
```

---

## 🚀 Deployment

### Local Network Access
App is accessible on your network at: `http://10.236.26.52:8502`

### Cloud Deployment (Streamlit Cloud)
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your GitHub repository
4. Deploy with one click

### Docker Deployment
```dockerfile
FROM python:3.14
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

---

## 📝 Usage Tips

1. **Emotion Detection**: Be specific with your feelings for better responses
2. **Mood Tracking**: Log your mood regularly to see patterns
3. **Export Data**: Download your journal monthly for backup
4. **Multiple Languages**: Switch languages anytime in the sidebar
5. **Crisis Resources**: Resources are always available in the sidebar

---

## 📄 License

MIT License - Feel free to use, modify, and distribute this project.

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📞 Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check existing documentation
- Review the troubleshooting section above

---

**Last Updated**: November 29, 2025  
**Version**: 1.0.0

