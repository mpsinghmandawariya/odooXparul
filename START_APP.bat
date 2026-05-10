@echo off
echo ========================================
echo    TRAVELOOP - Starting Application
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Checking Python installation...
python --version
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)
echo.

echo [2/3] Verifying app configuration...
python test_app.py
if errorlevel 1 (
    echo [ERROR] App configuration failed
    pause
    exit /b 1
)
echo.

echo [3/3] Starting Flask server...
echo.
echo ========================================
echo   Server will start at:
echo   http://127.0.0.1:5000
echo.
echo   Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause
