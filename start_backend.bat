@echo off
echo 🚀 Starting AI Booking Agent Backend...
echo.

cd /d "f:\college\projects\AI-booking-agent"

echo 📦 Installing/updating dependencies...
F:\college\projects\AI-booking-agent\venv\Scripts\pip.exe install -r requirements.txt > nul 2>&1

echo.
echo 🧪 Testing core components...
F:\college\projects\AI-booking-agent\venv\Scripts\python.exe test_optimized.py

echo.
echo 🌐 Starting backend server...
echo ✅ Backend will be available at: http://127.0.0.1:8000
echo 📚 API Documentation: http://127.0.0.1:8000/docs
echo.
echo ⚠️  Keep this window open while using the application!
echo 🎨 To start the frontend, run: start_frontend.bat
echo.
F:\college\projects\AI-booking-agent\venv\Scripts\python.exe -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
