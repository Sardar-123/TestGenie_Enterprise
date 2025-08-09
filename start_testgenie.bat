@echo off
echo ============================================
echo    TestGenie Enterprise Startup Script
echo ============================================
echo.

:: Activate virtual environment
echo [1/4] Activating virtual environment...
call .\venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    echo Please run: python -m venv venv
    pause
    exit /b 1
)

:: Check dependencies
echo [2/4] Checking dependencies...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo Installing required dependencies...
    pip install -r requirements_basic.txt
)

:: Create uploads directory
echo [3/4] Setting up directories...
if not exist "uploads" mkdir uploads

:: Start the application
echo [4/4] Starting TestGenie Enterprise...
echo.
echo ============================================
echo   TestGenie Enterprise is starting...
echo ============================================
echo   Open your browser and go to:
echo   http://localhost:5000
echo.
echo   API Endpoints:
echo   - Health Check: http://localhost:5000/api/health
echo   - System Status: http://localhost:5000/api/status
echo   - File Upload: http://localhost:5000/api/upload
echo   - Generate Tests: http://localhost:5000/api/generate-test-cases
echo.
echo   Press Ctrl+C to stop the server
echo ============================================
echo.

python simple_app.py
