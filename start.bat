@echo off
cd /d "%~dp0"

echo ================================
echo   Storyboard Studio
echo ================================
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo Python 3 is required. Please install it from https://python.org
    pause
    exit /b 1
)

python --version

if not exist "venv" (
    echo Setting up virtual environment...
    python -m venv venv
)

call venv\Scripts\activate

echo Installing dependencies...
pip install -q -r requirements.txt

if not exist ".env" (
    echo.
    echo No .env file found. Creating one...
    set /p api_key="Enter your Anthropic API key: "
    echo ANTHROPIC_API_KEY=%api_key%> .env
    echo .env created.
)

if not exist "data" mkdir data

echo.
echo Starting server at http://localhost:5000
echo Press Ctrl+C to stop.
echo.
python app.py
pause
