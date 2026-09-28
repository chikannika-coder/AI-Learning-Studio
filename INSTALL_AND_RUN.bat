@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title AI Learning Studio V4.7 FIXED - Installer

echo ============================================================
echo   AI Learning Studio V4.7 FIXED
echo   Windows installer / diagnostic launcher
echo ============================================================
echo.

set "PY="
py -3.10 -c "import sys;print(sys.version)" >nul 2>nul && set "PY=py -3.10"
if not defined PY py -3.11 -c "import sys;print(sys.version)" >nul 2>nul && set "PY=py -3.11"
if not defined PY py -3.12 -c "import sys;print(sys.version)" >nul 2>nul && set "PY=py -3.12"
if not defined PY python -c "import sys;print(sys.version)" >nul 2>nul && set "PY=python"

if not defined PY (
  echo [ERROR] Python 3 was not found.
  echo Install Python 3.10 or 3.11 and enable "Add Python to PATH".
  pause
  exit /b 1
)

echo [1/5] Python selected: %PY%
%PY% -c "import sys; print(sys.executable); print(sys.version)"
if errorlevel 1 goto :fatal

echo.
echo [2/5] Checking Tkinter...
%PY% -c "import tkinter; print('Tkinter OK')"
if errorlevel 1 (
  echo [ERROR] Tkinter is missing from this Python installation.
  echo Reinstall Python from python.org with Tcl/Tk support.
  pause
  exit /b 1
)

echo.
echo [3/5] Creating private environment...
if not exist ".venv\Scripts\python.exe" (
  %PY% -m venv .venv
  if errorlevel 1 goto :fatal
) else (
  echo Existing .venv found.
)

echo.
echo [4/5] Installing OPTIONAL packages...
echo The core Studio can open even if an optional package cannot be installed.
".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r requirements.txt
if errorlevel 1 (
  echo [WARNING] Some optional packages failed to install.
  echo Continuing because SymPy, Pillow, OpenCV and pyserial are optional in the app.
)

echo.
echo [5/5] Startup test...
".venv\Scripts\python.exe" -c "import tkinter, pathlib; compile(pathlib.Path('ai_learning_studio.py').read_text(encoding='utf-8'),'ai_learning_studio.py','exec'); print('Program syntax OK')"
if errorlevel 1 goto :fatal

echo.
echo Starting AI Learning Studio V4.7 FIXED...
start "" ".venv\Scripts\pythonw.exe" "%~dp0ai_learning_studio.py"
echo.
echo If the window does not appear, run DIAGNOSE_AND_RUN.bat.
timeout /t 2 /nobreak >nul
exit /b 0

:fatal
echo.
echo [ERROR] Installation/startup preparation failed.
echo Run DIAGNOSE_AND_RUN.bat to see the exact Python error.
pause
exit /b 1
