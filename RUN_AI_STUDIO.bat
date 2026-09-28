@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\pythonw.exe" (
  start "" ".venv\Scripts\pythonw.exe" "%~dp0ai_learning_studio.py"
  exit /b 0
)
call INSTALL_AND_RUN.bat
