@echo off
REM ============================================
REM ETT Olfactometer S — Python Environment Setup
REM ============================================
REM Run this once to create the virtual environment
REM and install all dependencies.
REM
REM Usage: double-click this file, or from Command Prompt:
REM     setup.bat
REM
REM After setup, activate the environment with:
REM     ett-venv\Scripts\activate
REM ============================================

echo.
echo ETT Olfactometer S - Python Environment Setup
echo ================================================
echo.

REM Check Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found on PATH.
    echo Install Python 3.10+ from python.org and ensure
    echo "Add Python to PATH" is checked during install.
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
python -m venv ett-venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    pause
    exit /b 1
)

echo [2/4] Activating environment...
call ett-venv\Scripts\activate.bat

echo [3/4] Upgrading pip...
python -m pip install --upgrade pip --quiet

echo [4/4] Installing pythonnet...
pip install pythonnet --quiet
if errorlevel 1 (
    echo ERROR: Failed to install pythonnet.
    pause
    exit /b 1
)

echo.
echo Verifying installation...
python -c "import clr; print('  clr module:', clr.__file__)"
if errorlevel 1 (
    echo.
    echo WARNING: clr import failed. You may have a conflicting 'clr' package.
    echo Try:  pip uninstall clr  then  pip install pythonnet
    pause
    exit /b 1
)

echo.
echo ================================================
echo Setup complete!
echo.
echo To use this environment in a new terminal:
echo     cd %CD%
echo     ett-venv\Scripts\activate
echo     python ett_smoketest.py
echo ================================================
echo.
pause