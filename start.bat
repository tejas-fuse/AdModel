@echo off
REM AdModel Startup Script for Windows

echo 🎨 Starting AdModel - AI Virtual Model Creator
echo ==============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -q -r requirements.txt

REM Create necessary directories
if not exist "uploads" mkdir uploads
if not exist "saved_models" mkdir saved_models

REM Start the server
echo.
echo 🚀 Starting AdModel server...
echo 📍 Access the application at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
