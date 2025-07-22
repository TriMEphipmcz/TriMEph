@echo off
REM ──────────────── Clean up old builds ────────────────
IF EXIST build   rmdir /s /q build
IF EXIST dist    rmdir /s /q dist
IF EXIST TriMEph.spec del /q TriMEph.spec

REM ──────────────── Build the EXE ──────────────────────
python -m PyInstaller ^
  --onefile ^
  --windowed ^
  --icon "resources//Logo.jpg" ^
  --add-data "resources//pozadie.png;." ^
  --add-data "resources//Dokumentacia.pdf;." ^
  --add-data "resources//Logo.jpg;." ^
  TriMEph.py

IF %ERRORLEVEL% NEQ 0 (
  echo.
  echo Build failed!
  pause
  exit /b %ERRORLEVEL%
)

echo.
echo Build succeeded. Executable is in dist\TriMEph.exe
pause
