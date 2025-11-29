# MindfulCompanion Startup Script
Write-Host "Starting MindfulCompanion..." -ForegroundColor Green
cd C:\Users\user\Desktop\PLP

# Activate venv
& ".\venv\Scripts\Activate.ps1"

# Run Streamlit
& "C:\Users\user\AppData\Local\Programs\Python\Python314\python.exe" -m streamlit run app.py --logger.level=error
