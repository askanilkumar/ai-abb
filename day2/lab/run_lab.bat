@echo off
title ABB AI Lab - keep this window open
cd /d C:\ai-abb\day2\lab
start "" cmd /c "timeout /t 7 >nul & start http://localhost:8501"
python -m streamlit run app.py --server.port 8501 --server.headless true --browser.gatherUsageStats false
echo.
echo The lab stopped. Close this window and double-click ABB AI Lab again, or call the trainer.
pause
