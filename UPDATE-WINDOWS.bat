@echo off
setlocal
cd /d "%~dp0"
echo [INFO] Updating product repositories to the exact commits pinned by this integration candidate.
call SETUP-WINDOWS.bat
exit /b %ERRORLEVEL%
