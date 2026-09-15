@echo off
setlocal EnableExtensions
cd /d "%~dp0"
if not exist "workspace\EVO\docker-compose.yml" (
  echo [ERROR] EVO workspace is missing. Run SETUP-WINDOWS.bat first.
  exit /b 1
)
echo ============================================================
echo  WARNING: RESET APM DEMO
echo ============================================================
echo This deletes the local 3ec-apm PostgreSQL Docker volume and all
echo local demo/runtime data for this validation stack.
echo.
set /p CONFIRM=Type RESET to continue: 
if /I not "%CONFIRM%"=="RESET" (
  echo [CANCELLED] No data was changed.
  exit /b 0
)
docker compose -p 3ec-apm -f "workspace\EVO\docker-compose.yml" down -v || exit /b 1
echo [PASS] Demo data removed. Starting a clean seeded EVO runtime ...
call START-WINDOWS.bat
