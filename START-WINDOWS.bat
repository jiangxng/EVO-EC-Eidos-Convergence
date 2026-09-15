@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title 3EC APM Integrated Validation Stack

echo ============================================================
echo  3EC APM Integrated Validation Stack v0.1
echo ============================================================

where git >nul 2>nul || (echo [ERROR] Git is required.& exit /b 1)
where docker >nul 2>nul || (echo [ERROR] Docker Desktop / Docker CLI is required.& exit /b 1)
docker info >nul 2>nul || (echo [ERROR] Docker engine is not running. Start Docker Desktop first.& exit /b 1)

if not exist "workspace\EVO\.git" (
  echo [INFO] Product workspace is missing. Running SETUP-WINDOWS.bat ...
  call SETUP-WINDOWS.bat || exit /b 1
)

echo [1/4] Checking pinned repository versions ...
call STATUS-WINDOWS.bat || exit /b 1

echo.
echo [2/4] Starting deterministic EVO runtime ...
docker compose -p 3ec-apm -f "workspace\EVO\docker-compose.yml" up -d --build || goto :fail

echo.
echo [3/4] Waiting for EVO API health ...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ok=$false; 1..60 | %% { try { $r=Invoke-WebRequest -UseBasicParsing -Uri 'http://127.0.0.1:3000/health' -TimeoutSec 2; if($r.StatusCode -ge 200 -and $r.StatusCode -lt 500){$ok=$true; break} } catch {}; Start-Sleep -Seconds 2 }; if(-not $ok){exit 1}" || goto :healthfail

echo.
echo [4/4] EVO is running.
echo.
echo ============================================================
echo  CURRENT STACK STATUS
echo ============================================================
echo EVO backend: http://127.0.0.1:3000
echo.
echo IMPORTANT:
echo The integrated Eidos enterprise website is NOT yet certified on this
echo branch, so this launcher deliberately does not pretend that a browser
echo UI is available. The next 3EC integration increment will add the
echo Eidos APM website only after the Eidos/EVO public boundary is certified.
echo.
echo Use LOGS-WINDOWS.bat for EVO logs.
echo Use STOP-WINDOWS.bat to stop the current stack.
exit /b 0

:healthfail
echo [ERROR] EVO containers started but API health did not become ready.
echo Run LOGS-WINDOWS.bat and send the output.
exit /b 1

:fail
echo [ERROR] Failed to start the 3EC APM validation stack.
exit /b 1
