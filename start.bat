@echo off
echo 🚀 Starting AI Research Agent
echo ============================

echo.
echo Starting backend...
start "Backend" cmd /k "call venv\Scripts\activate.bat && python main.py"

echo.
echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Starting frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ✅ Both services starting...
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause >nul
