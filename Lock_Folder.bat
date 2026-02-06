@echo off
title Dragon Mailer - Lock Folder
color 0C
cd /d "%~dp0"

echo.
echo  ====================================================
echo       DRAGON MAILER - FOLDER LOCK
echo  ====================================================
echo.
echo  Locking folder contents...

:: Hide all sensitive files and folders (but keep lock/unlock visible)
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
attrib +h +s "*.txt" >nul 2>&1
attrib +h +s "*.css" >nul 2>&1
attrib +h +s "*.js" >nul 2>&1
attrib +h +s "*.sh" >nul 2>&1
attrib +h +s "Dockerfile" >nul 2>&1

:: Keep these visible
attrib -h -s "DragonMailer.bat" >nul 2>&1
attrib -h -s "Install.bat" >nul 2>&1
attrib -h -s "Lock_Folder.bat" >nul 2>&1
attrib -h -s "Unlock_Folder.bat" >nul 2>&1
attrib -h -s "Allow_Firewall.bat" >nul 2>&1
attrib -h -s "NETWORK_SETUP.txt" >nul 2>&1

echo.
echo  [OK] Folder is now LOCKED!
echo.
echo  Visible files: DragonMailer.bat, Lock/Unlock scripts
echo  Hidden files: app.py, config, azure, etc.
echo.
echo  Enter password in Unlock_Folder.bat to see all files.
echo.
pause
