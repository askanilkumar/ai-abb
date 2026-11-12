@echo off
REM Step 1 - makes your own folder (safe from course updates) and opens an empty app.py in Notepad
set MY=%USERPROFILE%\Desktop\my-rag
if not exist "%MY%" mkdir "%MY%"
copy /Y "%~dp0Axion_HR_Policy.pdf" "%MY%\" >nul
copy /Y "%~dp02_run_my_rag.bat" "%MY%\" >nul
if not exist "%MY%\app.py" type nul > "%MY%\app.py"
start "" notepad "%MY%\app.py"
start "" explorer "%MY%"
