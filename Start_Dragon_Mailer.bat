@echo off
title Dragon Mailer - Glass Edition
echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║      DRAGON MAILER - Glass Edition           ║
echo  ║       Email and SMS Messaging App            ║
echo  ╚══════════════════════════════════════════════╝
echo.
echo Starting Dragon Mailer...
echo.

cd /d "%~dp0"

:: Check if streamlit is installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing Streamlit...
    pip install streamlit
)

:: Start the application
python -m streamlit run app.py --server.port 8505

pause
