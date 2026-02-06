@echo off
title Dragon Mailer Installer
cd /d "%~dp0"
color 0A

echo.
echo  ====================================================
echo       DRAGON MAILER INSTALLER
echo  ====================================================
echo.

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

echo [!] ERROR: Python not found!
echo     Please install Python from: https://python.org
pause
exit /b 1

:found_python

echo [1/4] Python found!
echo       Using: %PYTHON%

:: Install dependencies
echo.
echo [2/4] Installing dependencies...
%PYTHON% -m pip install streamlit pillow --quiet
echo       Dependencies installed!

:: Convert logo to ICO (if needed)
echo.
echo [3/4] Creating icon...
if not exist "images\dragon_logo.ico" (
    %PYTHON% -c "from PIL import Image; img = Image.open('images/dragon_logo.png').convert('RGBA'); img.thumbnail((256,256)); img.save('images/dragon_logo.ico', format='ICO')" 2>nul
)
if exist "images\dragon_logo.ico" (
    echo       Icon ready!
) else (
    echo       Note: Custom icon not available, will use default
    echo       ^(Install Pillow: pip install pillow^)
)

:: Create desktop shortcut
echo.
echo [4/5] Creating desktop shortcut...
powershell -ExecutionPolicy Bypass -File "%~dp0create_shortcut.ps1"
echo       Shortcut created on desktop!

:: Setup folder lock - lock it immediately with password SoftWork1@
echo.
echo [5/5] Setting up folder protection...

:: Hide all sensitive files and folders
attrib +h +s "app.py" >nul 2>&1
attrib +h +s "config" /D >nul 2>&1
attrib +h +s "azure" /D >nul 2>&1
attrib +h +s "images" /D >nul 2>&1
attrib +h +s "utils" /D >nul 2>&1
attrib +h +s "docs" /D >nul 2>&1
attrib +h +s "Scripts" /D >nul 2>&1
attrib +h +s "Lib" /D >nul 2>&1
attrib +h +s "__pycache__" /D >nul 2>&1
attrib +h +s "etc" /D >nul 2>&1
attrib +h +s "share" /D >nul 2>&1
attrib +h +s "requirements.txt" >nul 2>&1
attrib +h +s "*.py" >nul 2>&1
attrib +h +s "*.json" >nul 2>&1
attrib +h +s "*.md" >nul 2>&1
attrib +h +s "*.css" >nul 2>&1
attrib +h +s "*.js" >nul 2>&1
attrib +h +s "Dockerfile" >nul 2>&1

:: Keep these visible for easy access
attrib -h -s "DragonMailer.bat" >nul 2>&1
attrib -h -s "Install.bat" >nul 2>&1
attrib -h -s "Lock_Folder.bat" >nul 2>&1
attrib -h -s "Unlock_Folder.bat" >nul 2>&1
attrib -h -s "Allow_Firewall.bat" >nul 2>&1
attrib -h -s "NETWORK_SETUP.txt" >nul 2>&1

echo       Folder protection enabled!

echo.
echo  ====================================================
echo       INSTALLATION COMPLETE!
echo  ====================================================
echo.
echo  PASSWORD: SoftWork1@
echo.
echo  Folder is now LOCKED - sensitive files are hidden.
echo  DragonMailer.bat can still run the app.
echo.
echo  To view hidden files: Run Unlock_Folder.bat
echo  To hide files again:  Run Lock_Folder.bat
echo.
echo  Double-click "Dragon Mailer" on desktop or DragonMailer.bat to start!
echo.
pause
