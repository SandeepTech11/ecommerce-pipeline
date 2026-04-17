@echo off
echo ================================================
echo   Real-Time E-Commerce Pipeline - Windows Setup
echo ================================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
pip install -r requirements.txt

echo.
echo [2/3] Generating initial data...
python run_pipeline.py --mode batch --batch-size 100

echo.
echo [3/3] Starting dashboard...
echo       Open http://localhost:5000 in your browser
echo       Press Ctrl+C to stop
echo.
python dashboard\app.py

pause
