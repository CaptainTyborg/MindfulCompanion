# Deployment Guide for MindfulCompanion

## Option 1: Streamlit Cloud (Recommended - Free & Easy)

### Prerequisites
- GitHub account (✅ already have it)
- Streamlit Cloud account (free)

### Steps

1. **Create Streamlit Cloud Account**
   - Go to https://streamlit.io/cloud
   - Click "Sign up" and authenticate with GitHub
   - Grant repository access

2. **Deploy Your App**
   - In Streamlit Cloud dashboard, click "New app"
   - Select:
     - Repository: `CaptainTyborg/MindfulCompanion`
     - Branch: `main`
     - Main file path: `app.py`
   - Click "Deploy"

3. **Add Secrets**
   - In your deployed app, go to **Settings** (⚙️ gear icon)
   - Click **Secrets**
   - Add your Hugging Face API key:
     ```
     HUGGINGFACE_API_KEY = "your_actual_hf_token_here"
     ```
   - Click **Save**

4. **Done!**
   - Your app will be live at: `https://mindfulcompanion.streamlit.app` (or similar)
   - It will auto-update whenever you push to GitHub

### Cost
- **Free tier**: Up to 3 deployments, 1GB storage, limited compute
- **Pro tier**: $5/month for more resources

---

## Option 2: Heroku (Requires Credit Card)

### Steps

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create mindfulcompanion
   ```

4. **Add Config Vars (secrets)**
   ```bash
   heroku config:set HUGGINGFACE_API_KEY="your_token_here"
   ```

5. **Create Procfile**
   ```
   web: streamlit run app.py
   ```

6. **Deploy**
   ```bash
   git push heroku main
   ```

---

## Option 3: Railway.app (Easy Alternative)

1. Go to https://railway.app
2. Create account & login
3. Click "New Project" → "Deploy from GitHub"
4. Select your repo
5. Add environment variables in dashboard
6. Deploy

---

## Option 4: Docker + Any Cloud (AWS, Google Cloud, Azure)

### Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build & Push
```bash
docker build -t mindfulcompanion:latest .
docker push your-registry/mindfulcompanion:latest
```

---

## Environment Variables Required

For any deployment, set these:

| Variable | Description | Where to Find |
|----------|-------------|---------------|
| `HUGGINGFACE_API_KEY` | Hugging Face API token | https://huggingface.co/settings/tokens |

---

## Testing Before Deployment

Run locally first:
```bash
cd C:\Users\user\Desktop\PLP
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Visit: http://localhost:8501

---

## Monitoring

### Streamlit Cloud
- Dashboard shows app status, logs, and usage
- Auto-restarts on errors
- Analytics available

### Logs
- Streamlit Cloud: Logs tab in dashboard
- Heroku: `heroku logs --tail`
- Docker: `docker logs container_id`

---

## Troubleshooting

### "ModuleNotFoundError"
- Ensure all packages in `requirements.txt` are listed
- Run: `pip freeze > requirements.txt` to regenerate

### "HUGGINGFACE_API_KEY not found"
- Add the secret in your platform's settings (not in code)
- Don't commit `.env` file (use `.gitignore`)

### App timeout
- Reduce LLM model size or use smaller model
- Increase timeout in platform settings

### Voice input not working
- Streamlit Cloud doesn't support microphone input
- App gracefully falls back to text input
- This is expected behavior

---

## Next Steps

1. ✅ Choose your deployment platform (Streamlit Cloud recommended)
2. ⬜ Set up account on chosen platform
3. ⬜ Deploy your repository
4. ⬜ Add secrets/environment variables
5. ⬜ Test the deployed app
6. ⬜ Share your live URL!

---

## Quick Links

- **Streamlit Cloud**: https://streamlit.io/cloud
- **Railway**: https://railway.app
- **Heroku**: https://www.heroku.com
- **Docker Hub**: https://hub.docker.com
- **AWS**: https://aws.amazon.com
- **Google Cloud**: https://cloud.google.com
- **Azure**: https://azure.microsoft.com

**Your GitHub repo is ready to deploy!** 🚀
