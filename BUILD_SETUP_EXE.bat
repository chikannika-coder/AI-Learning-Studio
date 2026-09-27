@echo off
setlocal
cd /d "%~dp0"
title Build AI Learning Studio v5.9 Setup.exe
echo ============================================================
echo AI Learning Studio v5.9 - Windows EXE / Setup Builder
echo ============================================================
echo.

where py >nul 2>nul
if %errorlevel%==0 (set "PY=py -3") else (set "PY=python")

if not exist ".buildvenv\Scripts\python.exe" (
  echo [1/6] Creating build environment...
  %PY% -m venv .buildvenv || goto :fail
)
echo [2/6] Installing build dependencies...
".buildvenv\Scripts\python.exe" -m pip install --upgrade pip
".buildvenv\Scripts\python.exe" -m pip install pyinstaller sympy Pillow opencv-python pyserial || goto :fail

echo [3/6] Building standalone Windows EXE...
".buildvenv\Scripts\pyinstaller.exe" --clean --noconfirm AI_Learning_Studio.spec || goto :fail

echo [4/6] EXE built: dist\AI_Learning_Studio_v59.exe

echo [5/6] Looking for Inno Setup...
set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" (
  echo.
  echo [NOTICE] Inno Setup 6 is not installed.
  echo The standalone EXE is ready in dist\AI_Learning_Studio_v59.exe
  echo To also create Setup.exe, install Inno Setup 6 and run this file again.
  goto :done
)

echo [6/6] Building Setup.exe with Desktop shortcut...
"%ISCC%" AI_Learning_Studio_v59.iss || goto :fail
echo Setup created in installer\AI_Learning_Studio_v59_Setup.exe

:done
echo.
echo BUILD COMPLETE
pause
exit /b 0

:fail
echo.
echo BUILD FAILED. Review the message above.
pause
exit /b 1
