@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "ROOT=%CD%\workspace"
if not exist "%ROOT%" mkdir "%ROOT%"

where git >nul 2>nul || (echo [ERROR] Git is required.& exit /b 1)

echo ============================================================
echo  3EC APM Validation Stack - Repository Setup
echo ============================================================
echo Workspace: %ROOT%
echo.

call :sync EVO https://github.com/jiangxng/EVO.git evo/enterprise-package-v0.1 ce7240191455e1691fff84d032483f28ed3df469 || exit /b 1
call :sync Experience-Compiler https://github.com/jiangxng/Experience-Compiler.git sprint0-visible-advisory fc2be5d6f24facbcf0e4090d7920a5eed45fd758 || exit /b 1
call :sync eidos https://github.com/jiangxng/eidos.git main 52f8923ab2b4ee833ae5b05623bfd180f554570a || exit /b 1

echo.
echo [PASS] All three product repositories are pinned to stack.lock.json commits.
echo Next: run STATUS-WINDOWS.bat, then TEST-WINDOWS.bat.
exit /b 0

:sync
set "NAME=%~1"
set "URL=%~2"
set "BRANCH=%~3"
set "SHA=%~4"
set "DIR=%ROOT%\%NAME%"
echo [SYNC] %NAME%  branch=%BRANCH%  commit=%SHA%
if not exist "%DIR%\.git" (
  git clone --no-checkout "%URL%" "%DIR%" || exit /b 1
)
git -C "%DIR%" fetch --prune origin || exit /b 1
git -C "%DIR%" fetch origin "%BRANCH%" || exit /b 1
git -C "%DIR%" cat-file -e "%SHA%^{commit}" 2>nul || git -C "%DIR%" fetch origin "%SHA%" || exit /b 1
git -C "%DIR%" checkout --detach "%SHA%" || exit /b 1
for /f %%H in ('git -C "%DIR%" rev-parse HEAD') do set "ACTUAL=%%H"
if /I not "%ACTUAL%"=="%SHA%" (
  echo [ERROR] %NAME% expected %SHA% but got %ACTUAL%
  exit /b 1
)
exit /b 0
