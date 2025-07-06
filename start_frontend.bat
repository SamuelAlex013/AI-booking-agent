@echo off
echo 🎨 Starting Streamlit Frontend...
echo.

cd /d "f:\college\projects\AI-booking-agent"

echo Make sure the backend is running on http://127.0.0.1:8000
echo.

echo 🌟 Starting Streamlit app...
echo Visit: http://localhost:8501 to use the chat interface
echo.
F:\college\projects\AI-booking-agent\venv\Scripts\streamlit.exe run frontend/app.py

pause
