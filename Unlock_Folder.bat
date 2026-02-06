@echo off
setlocal EnableDelayedExpansion
title Dragon Mailer - Unlock Folder
color 0E
cd /d "%~dp0"

echo.
echo  ====================================================
echo       DRAGON MAILER - FOLDER UNLOCK
echo  ====================================================
echo.

:: Use PowerShell to mask password input
for /f "delims=" %%p in ('powershell -Command "$p = Read-Host '  Enter password' -AsSecureString; [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($p))"') do set "pass=%%p"

if "!pass!"=="SoftWork1@" (
    echo.
    echo  [OK] Password accepted!
    
    :: Unhide all files and folders in the directory
    attrib -h -s "%~dp0*.*" >nul 2>&1
    attrib -h -s "%~dp0config" /D >nul 2>&1
    attrib -h -s "%~dp0azure" /D >nul 2>&1
    attrib -h -s "%~dp0images" /D >nul 2>&1
    attrib -h -s "%~dp0utils" /D >nul 2>&1
    attrib -h -s "%~dp0docs" /D >nul 2>&1
    attrib -h -s "%~dp0Scripts" /D >nul 2>&1
    
    echo  Folder contents are now visible.
    echo.
    echo  Run Lock_Folder.bat when done to hide again.
) else (
    echo.
    echo  [X] Invalid password!
)

echo.
pause
endlocal
