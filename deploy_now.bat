@echo off
setlocal

REM Dragon Mailer - Deploy (Windows wrapper)
REM Uses deploy_now.ps1 (PuTTY plink/pscp + Docker/Traefik on the server).

set "SCRIPT_DIR=%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%deploy_now.ps1" %*
exit /b %errorlevel%

