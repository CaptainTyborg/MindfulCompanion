# MindfulCompanion 🧠

An AI-powered mental wellness chatbot built with Streamlit, providing emotional support, mood tracking, multi-language translation, and voice input.

**⚠️ Disclaimer**: Not a replacement for professional mental health care. Crisis resources: 988 (Suicide & Crisis Lifeline)

---

## ✨ Features

- 💬 **AI Chat** - Empathetic conversations powered by Hugging Face LLMs
- 🎤 **Voice Input** - Speech-to-text with Google Speech Recognition
- 🌍 **20+ Languages** - Real-time translation via Google Translate
- 📊 **Mood Tracking** - Log emotions and visualize trends
- 📥 **Journal Export** - Download conversations as JSON/CSV/Text
- 🔒 **Safety First** - Crisis detection & content filtering
- 📈 **Wellness Tips** - Personalized mental health suggestions

---

## 🚀 Quick Start

### Requirements
- Python 3.14+
- Windows/Mac/Linux

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/MindfulCompanion.git
cd MindfulCompanion

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up API key
# Create .env file with:
# HUGGINGFACE_API_KEY=your_key_here

# Run the app
streamlit run app.py
```

Open your browser to: **http://localhost:8502**

---

## 📚 Full Setup Guide

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed instructions including:
- Windows-specific installation
- PyAudio setup for voice input
- Troubleshooting common issues
- Cloud deployment options

---

## 🏗️ Project Structure

```
MindfulCompanion/
├── app.py                    # Main application
├── requirements.txt          # Dependencies
├── .env                      # API keys (not in git)
├── SETUP_GUIDE.md           # Detailed setup instructions
├── backend/                 # Core modules
│   ├── emotion_detector.py
│   ├── llm_handler.py       # Hugging Face integration
│   ├── mood_tracker.py
│   ├── response_generator.py
│   └── safety_filter.py
├── utils/                   # Utilities
│   ├── voice_handler.py     # Speech recognition
│   ├── translator.py        # Multi-language support
│   ├── journal_exporter.py  # Data export
│   └── helpers.py
└── data/                    # Data storage
    ├── mood_logs.csv
    └── wellness_tips.json
```

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit 1.50
- **Backend**: Python 3.14
- **LLM**: Hugging Face Inference API
- **NLP**: NLTK, TextBlob, Transformers
- **Data**: Pandas, Plotly
- **ML**: Scikit-learn
- **Voice**: SpeechRecognition (optional)
- **Translation**: Google Translate (optional)

---

## 📋 Usage

1. **Chat**: Type or speak your feelings
2. **Mood Log**: Your emotional state is tracked automatically
3. **Translate**: Switch languages in the sidebar
4. **Export**: Download your journal anytime
5. **Resources**: Crisis support always available

---

## ⚙️ Configuration

### Environment Variables (.env)
```
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxx
```

### Get API Key
1. Visit https://huggingface.co
2. Sign up or log in
3. Go to Settings → Access Tokens
4. Create a new token
5. Copy and paste into `.env`

---

## 🐛 Troubleshooting

**"Port already in use"**
```bash
streamlit run app.py --server.port 8503
```

**"PyAudio not found"** (Voice input is optional)
- Download wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- Install: `pip install PyAudio-0.2.x-cp314-cp314-win_amd64.whl`
- Or use text input (fallback works automatically)

**"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
```

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for more troubleshooting.

---

## 📖 Documentation

- [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Complete setup & deployment guide
- [requirements.txt](./requirements.txt) - All dependencies with versions

---

## 🎯 Features in Development

- [ ] Multi-turn memory optimization
- [ ] Custom mood categories
- [ ] Dark mode theme
- [ ] Privacy mode (no data logging)
- [ ] API endpoint for third-party integration

---

## 📜 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions welcome! 
1. Fork the repo
2. Create a feature branch
3. Submit a pull request

---

## 💬 Support

- **Issues**: Open a GitHub issue
- **Questions**: Discussions tab
- **Bugs**: Submit detailed bug report

---

## 🙏 Acknowledgments

- Hugging Face for LLM inference
- Streamlit for the beautiful UI framework
- Google Translate API
- NLTK, scikit-learn, and the Python community

---

**Last Updated**: November 29, 2025 | **Version**: 1.0.0
