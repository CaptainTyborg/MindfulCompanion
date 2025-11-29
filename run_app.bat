@echo off
REM Start MindfulCompanion App
echo Starting MindfulCompanion...
cd /d C:\Users\user\Desktop\PLP

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run Streamlit
"C:\Users\user\AppData\Local\Programs\Python\Python314\python.exe" -m streamlit run app.py --logger.level=error

pause
