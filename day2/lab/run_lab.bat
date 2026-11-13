@echo off
title ABB AI Lab - keep this window open
cd /d C:\ai-abb\day2\lab
set "PY="
for /d %%D in ("C:\Program Files\Python3*") do if not defined PY if exist "%%D\python.exe" set "PY=%%D\python.exe"
for /d %%D in ("C:\Python3*") do if not defined PY if exist "%%D\python.exe" set "PY=%%D\python.exe"
if not defined PY if exist "%LOCALAPPDATA%\Python\bin\python.exe" set "PY=%LOCALAPPDATA%\Python\bin\python.exe"
if not defined PY if exist "C:\Users\azureuser\AppData\Local\Python\bin\python.exe" set "PY=C:\Users\azureuser\AppData\Local\Python\bin\python.exe"
if not defined PY set "PY=python"
start "" cmd /c "timeout /t 7 >nul & start http://localhost:8501"
"%PY%" -m streamlit run app.py --server.port 8501 --server.headless true --browser.gatherUsageStats false
echo.
echo The lab stopped. Close this window and double-click ABB AI Lab again, or call the trainer.
pause
