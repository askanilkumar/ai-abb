@echo off
REM Trainer demo - AskIT advanced RAG (production-style RAG)
cd /d "%~dp0"
start "" cmd /c "timeout /t 8 >nul & start http://localhost:8502"
python -m streamlit run app.py --server.port 8502 --server.headless true --browser.gatherUsageStats false
pause
