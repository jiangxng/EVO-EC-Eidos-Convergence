@echo off
setlocal EnableExtensions
cd /d "%~dp0"
if not exist "workspace\EVO\docker-compose.yml" (
  echo [INFO] EVO workspace is not installed. Nothing to stop.
  exit /b 0
)
echo [STOP] 3EC APM validation stack ...
docker compose -p 3ec-apm -f "workspace\EVO\docker-compose.yml" down
if errorlevel 1 exit /b 1
echo [PASS] Stack stopped. Persistent PostgreSQL volume was retained.
