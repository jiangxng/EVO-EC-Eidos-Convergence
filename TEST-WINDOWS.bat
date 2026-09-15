@echo off
setlocal EnableExtensions
cd /d "%~dp0"
set "ROOT=%CD%\workspace"
set "FAILED=0"

echo ============================================================
echo  3EC APM Validation Stack - Local Certification
 echo ============================================================

if not exist "%ROOT%\EVO\.git" (echo [ERROR] Run SETUP-WINDOWS.bat first.& exit /b 1)
if not exist "%ROOT%\Experience-Compiler\.git" (echo [ERROR] Run SETUP-WINDOWS.bat first.& exit /b 1)
if not exist "%ROOT%\eidos\.git" (echo [ERROR] Run SETUP-WINDOWS.bat first.& exit /b 1)

where python >nul 2>nul || (echo [ERROR] Python 3.12+ is required.& exit /b 1)
where node >nul 2>nul || (echo [ERROR] Node 20+ is required.& exit /b 1)
where npm >nul 2>nul || (echo [ERROR] npm is required.& exit /b 1)

echo.
echo [1/3] EC tests
pushd "%ROOT%\Experience-Compiler"
set "PYTHONPATH=%CD%\src"
python -m unittest discover -s tests -v || set "FAILED=1"
popd

echo.
echo [2/3] Eidos build/test
pushd "%ROOT%\eidos"
call npm ci || set "FAILED=1"
call npm test || set "FAILED=1"
call npm run build || set "FAILED=1"
popd

echo.
echo [3/3] EVO container/runtime tests
pushd "%ROOT%\EVO"
if exist docker-compose.yml (
  where docker >nul 2>nul || (echo [ERROR] Docker is required for EVO validation.& set "FAILED=1")
  if "%FAILED%"=="0" docker compose build || set "FAILED=1"
) else (
  echo [WARN] EVO docker-compose.yml not found at repository root; product-owned CI remains authoritative.
)
popd

echo.
if "%FAILED%"=="0" (
  echo [PASS] Local repository-level validation completed.
  echo [NOTE] This does NOT yet certify the browser-visible APM integrated website.
  exit /b 0
)
echo [FAIL] One or more validations failed.
exit /b 1
