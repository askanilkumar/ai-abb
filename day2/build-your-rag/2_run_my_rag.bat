@echo off
REM Step 3 - starts your app and opens it in the browser. Keep this black window open while you use the app.
cd /d "%USERPROFILE%\Desktop\my-rag"
start "" cmd /c "timeout /t 6 >/dev/null & start http://localhost:8601"
python -m streamlit run app.py --server.port 8601 --server.headless true --browser.gatherUsageStats false
echo.
echo The app stopped. If you see a red error above, copy it and paste it into Abby with the "fix it" prompt.
pause
