@echo off
setlocal EnableExtensions
cd /d "%~dp0"
if not exist "workspace\EVO\docker-compose.yml" (
  echo [ERROR] EVO workspace is missing. Run SETUP-WINDOWS.bat first.
  exit /b 1
)
echo ============================================================
echo  3EC APM - EVO Runtime Status
echo ============================================================
docker compose -p 3ec-apm -f "workspace\EVO\docker-compose.yml" ps
echo.
echo ============================================================
echo  Recent logs (last 200 lines)
echo ============================================================
docker compose -p 3ec-apm -f "workspace\EVO\docker-compose.yml" logs --tail=200
