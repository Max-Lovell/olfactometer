@echo off
REM ============================================
REM ETT Olfactometer S — Python Environment Setup
REM ============================================
REM Requires the Python Launcher (py.exe), which is included
REM with any recent Python install from python.org.
REM
REM Usage: double-click this file, or run from Command Prompt.
REM After setup, activate the environment with:
REM     ett-venv\Scripts\activate
REM ============================================

echo.
echo ETT Olfactometer S - Python Environment Setup
echo ================================================
echo.

REM --- Check py launcher is available ---
py --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python Launcher (py.exe) not found.
    echo Install any Python from https://www.python.org/downloads/
    echo and make sure "Add Python to PATH" is checked.
    pause
    exit /b 1
)

REM --- Ensure Python 3.12 is available, install if not ---
py -3.12 --version >nul 2>&1
if errorlevel 1 (
    echo Python 3.12 not found. Installing via py launcher...
    py install 3.12
    if errorlevel 1 (
        echo ERROR: Failed to install Python 3.12.
        pause
        exit /b 1
    )
)
for /f "tokens=2 delims= " %%v in ('py -3.12 --version 2^>^&1') do echo Found Python %%v - OK
echo.

REM --- Remove old venv if present ---
if exist ett-venv (
    echo Removing old virtual environment...
    rmdir /s /q ett-venv
)

REM --- Create venv ---
echo [1/3] Creating virtual environment...
py -3.12 -m venv ett-venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment.
    pause
    exit /b 1
)

REM --- Activate and install ---
echo [2/3] Activating environment...
call ett-venv\Scripts\activate.bat

echo [3/3] Installing pythonnet...
pip install --upgrade pip --quiet
pip install pythonnet --quiet
if errorlevel 1 (
    echo ERROR: Failed to install pythonnet.
    pause
    exit /b 1
)

REM --- Verify ---
echo.
echo Verifying installation...
python -c "import clr; print('  pythonnet OK')"
if errorlevel 1 (
    echo WARNING: pythonnet import failed. Try: pip uninstall clr ^& pip install pythonnet
    pause
    exit /b 1
)

echo.
echo ================================================
echo Setup complete!
echo.
echo To use in a new terminal:
echo     cd %CD%
echo     ett-venv\Scripts\activate
echo     python ett_smoketest.py
echo ================================================
echo.
pause