# GitHub Upload Instructions

This guide walks you through uploading MindfulCompanion to GitHub.

---

## Step 1: Install Git

If you don't have Git installed:

1. Download Git for Windows: https://git-scm.com/download/win
2. Run the installer with default settings
3. Restart PowerShell/Command Prompt

Verify installation:
```powershell
git --version
```

---

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `MindfulCompanion`
3. Description: "AI-powered mental wellness chatbot with voice input and multi-language support"
4. Choose **Public** or **Private** (your preference)
5. Do NOT initialize with README (we already have one)
6. Click **Create repository**

After creation, you'll see instructions. Copy your repository URL (e.g., `https://github.com/yourusername/MindfulCompanion.git`)

---

## Step 3: Initialize Git & Upload

Run these commands in PowerShell from the project directory:

```powershell
# Navigate to project
cd "C:\Users\YourUsername\Desktop\PLP"

# Initialize git repository
git init

# Configure your identity
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add all files (respects .gitignore)
git add .

# Create initial commit
git commit -m "Initial commit: MindfulCompanion v1.0"

# Add remote repository (replace with your URL)
git remote add origin https://github.com/yourusername/MindfulCompanion.git

# Rename branch to main (GitHub default)
git branch -M main

# Push to GitHub
git push -u origin main
```

You'll be prompted for authentication:
- **Username**: Your GitHub username
- **Password**: Use a Personal Access Token (see below)

---

## Step 4: Create Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click **Generate new token** → **Generate new token (classic)**
3. Set name: `MindfulCompanion Upload`
4. Select scopes: Check `repo` (full control of private repositories)
5. Click **Generate token**
6. **Copy the token immediately** (you won't see it again!)
7. Use this token as your password when pushing to Git

---

## Step 5: Verify Upload

1. Go to https://github.com/yourusername/MindfulCompanion
2. Verify files are present:
   - ✅ `app.py`
   - ✅ `requirements.txt`
   - ✅ `README.md`
   - ✅ `SETUP_GUIDE.md`
   - ✅ `LICENSE`
   - ✅ `backend/` folder
   - ✅ `utils/` folder
   - ✅ `data/` folder
   - ✅ `.gitignore`

3. Check `.gitignore` is working (these should NOT appear):
   - ❌ `.venv/`
   - ❌ `__pycache__/`
   - ❌ `.env`
   - ❌ `mood_logs.csv`

---

## Step 6: Update Repository Settings (Optional)

### Add Topics
1. Go to your repo → **About** (gear icon)
2. Add topics: `python`, `streamlit`, `chatbot`, `mental-health`, `ai`, `nlp`

### Enable Discussions
1. Settings → **Discussions** → Enable

### Add CI/CD (Advanced)
1. Create `.github/workflows/tests.yml` for automated testing

---

## Step 7: Future Updates

To push changes after initial upload:

```powershell
# Make changes to files

# Stage changes
git add .

# Commit with message
git commit -m "Description of changes"

# Push to GitHub
git push origin main
```

---

## Troubleshooting

### "fatal: not a git repository"
```powershell
cd "C:\Users\YourUsername\Desktop\PLP"
git init
```

### "fatal: The current branch main has no upstream branch"
```powershell
git push -u origin main
```

### "Authentication failed"
- Use Personal Access Token instead of password
- Generate at: https://github.com/settings/tokens
- Use as password when Git prompts

### ".gitignore not working"
```powershell
# Remove cached files
git rm -r --cached .

# Re-add everything (respecting .gitignore)
git add .

git commit -m "Remove cached files"
git push
```

### Large file warning
If you see warnings about large files:
1. Check `.gitignore` includes `__pycache__/`, `.venv/`
2. Don't commit `mood_logs.csv` (should be in .gitignore)
3. Use `git lfs` for files > 100MB

---

## Share Your Project

Once uploaded, you can share:
- **GitHub URL**: `https://github.com/yourusername/MindfulCompanion`
- **Share button**: Click "Share" in GitHub UI
- **Create Release**: Go to Releases → Create new release

---

## Enable GitHub Pages (Optional)

Deploy your README as a website:

1. Settings → **Pages**
2. Source: **Deploy from a branch**
3. Select: **main** branch, **/ (root)** folder
4. Your site: `https://yourusername.github.io/MindfulCompanion`

---

## Next Steps

- ✅ Upload to GitHub
- ⬜ Get feedback from community
- ⬜ Consider issues/pull requests
- ⬜ Add badges (build status, downloads, etc.)
- ⬜ Set up GitHub Actions for automation

---

**Happy sharing!** 🚀
