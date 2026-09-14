@echo off
setlocal
cd /d "%~dp0"
title EVO x EC x Eidos Architecture Convergence v0.2

echo ============================================================
echo EVO x EC x Eidos Architecture Convergence v0.2
echo APM runnable reference validation
echo ============================================================
echo.
set "PYEXE="
py -3.12 -c "import sys; assert sys.version_info[:2] == (3,12)" >nul 2>&1
if not errorlevel 1 set "PYEXE=py -3.12"
if not defined PYEXE (
  py -3.13 -c "import sys; assert sys.version_info[:2] == (3,13)" >nul 2>&1
  if not errorlevel 1 set "PYEXE=py -3.13"
)
if not defined PYEXE (
  echo [ERROR] Python 3.12 or 3.13 was not found.
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" (
  echo [0/6] Creating .venv ...
  %PYEXE% -m venv .venv
  if errorlevel 1 goto :fail
) else (
  echo [0/6] Existing .venv found.
)
set "PYTHONPATH=%CD%\src;%CD%\vendor\ec-v1.0.1\src"
set "VPY=%CD%\.venv\Scripts\python.exe"
echo [1/6] Doctor ...
"%VPY%" -m convergence doctor || goto :fail
echo [2/6] Contracts ...
"%VPY%" -m convergence validate-contracts || goto :fail
echo [3/6] Tests ...
"%VPY%" -m unittest discover -s tests -v || goto :fail
echo [4/6] APM E2E ...
"%VPY%" -m convergence e2e || goto :fail
echo [5/6] Enterprise Function Pack backup/install ...
"%VPY%" -m convergence function-pack-smoke || goto :fail
echo [6/6] Two-EC knowledge merge ...
"%VPY%" -m convergence knowledge-merge-smoke || goto :fail
echo.
echo ============================================================
echo ARCHITECTURE CONVERGENCE v0.2: PASS
echo ============================================================
echo Outputs: runtime-output\
pause
exit /b 0
:fail
echo.
echo ============================================================
echo ARCHITECTURE CONVERGENCE v0.2: FAILED
echo ============================================================
pause
exit /b 1
