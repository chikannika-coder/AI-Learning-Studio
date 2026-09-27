@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\pythonw.exe" (
  start "" ".venv\Scripts\pythonw.exe" "ai_learning_studio.py"
  exit /b 0
)
echo AI Learning Studio has not been installed yet.
echo Starting automatic installer...
call INSTALL_AND_RUN.bat
