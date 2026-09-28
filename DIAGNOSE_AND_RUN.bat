@echo off
setlocal
cd /d "%~dp0"
title AI Learning Studio V4.7 - Diagnostics
echo ============================================================
echo AI Learning Studio V4.7 diagnostics
echo ============================================================
echo Folder: %CD%
echo.
if exist ".venv\Scripts\python.exe" (
  set "PY=.venv\Scripts\python.exe"
) else (
  set "PY=python"
)
echo Python:
"%PY%" -c "import sys; print(sys.executable); print(sys.version)"
echo.
echo Tkinter:
"%PY%" -c "import tkinter; print('Tkinter OK', tkinter.TkVersion)"
echo.
echo Optional modules:
"%PY%" -c "mods=['sympy','PIL','cv2','serial']; import importlib.util; [print(m, 'OK' if importlib.util.find_spec(m) else 'optional/not installed') for m in mods]"
echo.
echo Starting in CONSOLE MODE. Keep this window open.
echo Any traceback will be visible below.
echo ============================================================
"%PY%" "ai_learning_studio.py"
echo.
echo Program exited with code %errorlevel%.
pause
