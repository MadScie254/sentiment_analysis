@echo off
echo 🚀 Starting Immersive Sentiment Analysis Dashboard...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python detected
echo.

REM Install dependencies if needed
echo 📦 Installing dependencies...
pip install -r requirements_awesome.txt

if errorlevel 1 (
    echo ⚠️  Some packages failed to install, trying with basic requirements...
    pip install flask flask-cors python-dotenv requests pandas numpy transformers torch textblob vadersentiment feedparser sqlalchemy
)

echo.
echo 🔧 Setting up environment...

REM Create .env if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env 2>nul
)

echo.
echo 🌟 Starting the awesome dashboard...
echo 📱 Dashboard will be available at: http://localhost:5003
echo 🔧 Press Ctrl+C to stop the server
echo.

python awesome_dashboard.py

pause
