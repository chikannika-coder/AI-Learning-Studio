@echo off
setlocal
cd /d "%~dp0"
title AI Learning Studio v5.9 • Windows Edition - Automatic Installer

echo ============================================================
echo   AI Learning Studio v5.9 • Windows Edition - Automatic Install and Run
echo ============================================================
echo.

where py >nul 2>nul
if %errorlevel%==0 (
  set "PY=py -3"
) else (
  where python >nul 2>nul
  if errorlevel 1 (
    echo [ERROR] Python 3 was not found.
    echo Please install Python 3.10 or newer from python.org
    echo During setup, enable "Add Python to PATH".
    pause
    exit /b 1
  )
  set "PY=python"
)

if not exist ".venv\Scripts\python.exe" (
  echo [1/4] Creating private Python environment...
  %PY% -m venv .venv
  if errorlevel 1 goto :fail
) else (
  echo [1/4] Python environment already exists.
)

echo [2/4] Updating pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip

echo [3/4] Installing required packages...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :fail

echo [4/4] Starting AI Learning Studio...
start "" ".venv\Scripts\pythonw.exe" "ai_learning_studio.py"
exit /b 0

:fail
echo.
echo [ERROR] Installation did not complete.
echo Check your internet connection and Python installation.
pause
exit /b 1
