@echo off
title Dragon Mailer
cd /d "%~dp0"
color 0B

:: Try multiple Python paths
set PYTHON=
if exist "C:\Program Files\Microsoft SDKs\Azure\CLI2\python.exe" (
    set PYTHON="C:\Program Files\Microsoft SDKs\Azure\CLI2\python.exe"
    goto :found_python
)
where python >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON=python
    goto :found_python
)
if exist "C:\Python314\python.exe" (
    set PYTHON="C:\Python314\python.exe"
    goto :found_python
)
if exist "C:\Python311\python.exe" (
    set PYTHON="C:\Python311\python.exe"
    goto :found_python
)
if exist "C:\Python310\python.exe" (
    set PYTHON="C:\Python310\python.exe"
    goto :found_python
)

echo Python not found! Please install Python 3.10+
pause
exit /b 1

:found_python

:: Check/install Streamlit
%PYTHON% -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    %PYTHON% -m pip install streamlit pillow --quiet
)

:: Get local IP for network access
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    for /f "tokens=1" %%b in ("%%a") do set LOCAL_IP=%%b
)

:: Start the app
cls
echo.
echo  ____                              __  __       _ _           
echo ^|  _ \ _ __ __ _  __ _  ___  _ __ ^|  \/  ^| __ _(_) ^| ___ _ __ 
echo ^| ^| ^| ^| '__/ _` ^|/ _` ^|/ _ \^| '_ \^| ^|\/^| ^|/ _` ^| ^| ^|/ _ \ '__^|
echo ^| ^|_^| ^| ^| ^| (_^| ^| (_^| ^| (_) ^| ^| ^| ^| ^|  ^| ^| (_^| ^| ^| ^|  __/ ^|   
echo ^|____/^|_^|  \__,_^|\__, ^|\___/^|_^| ^|_^|_^|  ^|_^|\__,_^|_^|_^|\___^|_^|   
echo                  ^|___/                                        
echo.
echo  Starting Dragon Mailer...
echo.
echo  LOCAL ACCESS:   http://localhost:8505
echo  NETWORK ACCESS: http://%LOCAL_IP%:8505
echo.
echo  (Second laptop can use the NETWORK ACCESS URL)
echo.
echo  Press Ctrl+C to stop the server
echo.

timeout /t 2 >nul
start "" "http://localhost:8505"
%PYTHON% -m streamlit run app.py --server.address 0.0.0.0 --server.port 8505 --server.headless true
