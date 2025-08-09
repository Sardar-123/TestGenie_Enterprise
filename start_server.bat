@echo off
echo 🚀 Starting TestGenie Enterprise Platform
echo ==========================================

echo Activating virtual environment...
call venv\Scripts\activate.bat

@REM echo Installing dependencies if needed...
@REM pip install -q python-dotenv flask openai

echo Starting TestGenie server with SQLite database...
python enterprise_test_platform_sqlite.py
