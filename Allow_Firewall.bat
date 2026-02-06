@echo off
title Allow Dragon Mailer Through Firewall
color 0E

:: Check for admin rights
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  This script requires Administrator privileges.
    echo  Please right-click and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo.
echo  ====================================================
echo       DRAGON MAILER - FIREWALL SETUP
echo  ====================================================
echo.

:: Remove existing rules (if any)
netsh advfirewall firewall delete rule name="Dragon Mailer" >nul 2>&1

:: Add inbound rule for port 8505
netsh advfirewall firewall add rule name="Dragon Mailer" dir=in action=allow protocol=TCP localport=8505

if %errorlevel% equ 0 (
    echo  [OK] Firewall rule added successfully!
    echo.
    echo  Port 8505 is now open for network access.
    echo  Second laptop can now connect to this PC.
) else (
    echo  [!] Failed to add firewall rule.
    echo  Please manually allow port 8505 in Windows Firewall.
)

echo.
pause
