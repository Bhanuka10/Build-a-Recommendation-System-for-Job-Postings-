@echo off
REM Startup script for Job Recommendation System Web App (Windows)
REM This script handles all setup and runs the application

echo.
echo ================================================
echo Job Recommendation System - Web Application
echo ================================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python not found. Please install Python 3.7+
    pause
    exit /b 1
)
echo [OK] Python found

REM Check if virtual environment exists
if not exist ".venv" (
    echo.
    echo Creating virtual environment...
    python -m venv .venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat
echo [OK] Virtual environment activated

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt -q
echo [OK] Dependencies installed

REM Test the engine
echo.
echo Testing recommendation engine...
python test_webapp.py
if errorlevel 1 (
    echo.
    echo [X] Engine test failed. Please check configuration.
    pause
    exit /b 1
)

REM Start the application
echo.
echo ================================================
echo Starting web application...
echo ================================================
echo.
echo The application will be available at:
echo   ^> http://localhost:5000
echo.
echo Press Ctrl+C to stop the application
echo.

python app.py
pause
