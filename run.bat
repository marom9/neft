@echo off
title Energy ^& Logistics Dashboard

echo.
echo  [1/2] Installing / verifying dependencies...
python -m pip install -r requirements.txt --quiet --disable-pip-version-check
if errorlevel 1 (
    echo  ERROR: pip install failed. Check internet connection.
    pause
    exit /b 1
)

echo  [2/2] Starting dashboard at http://localhost:8501
echo  Press Ctrl+C in this window to stop.
echo.

python -m streamlit run app.py --server.headless false --browser.gatherUsageStats false

pause
