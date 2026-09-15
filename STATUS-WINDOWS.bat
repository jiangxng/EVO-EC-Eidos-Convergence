@echo off
setlocal
cd /d "%~dp0"
set "ROOT=%CD%\workspace"
echo ============================================================
echo  3EC APM Validation Stack - Status
echo ============================================================
call :show EVO
call :show Experience-Compiler
call :show eidos
echo.
where docker >nul 2>nul && (docker version --format "Docker: {{.Server.Version}}" 2>nul) || echo Docker: not available/running
where python >nul 2>nul && python --version || echo Python: not found
where node >nul 2>nul && node --version || echo Node: not found
exit /b 0

:show
set "DIR=%ROOT%\%~1"
if not exist "%DIR%\.git" (
  echo %~1: NOT SET UP
  exit /b 0
)
for /f %%H in ('git -C "%DIR%" rev-parse HEAD') do echo %~1: %%H
exit /b 0
