@echo off
echo Starting AI Research Agent Development Environment
echo ================================================

echo.
echo 1. Starting Backend Server...
start "Backend Server" cmd /k "py main.py"

echo.
echo 2. Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo 3. Starting Frontend Server...
cd frontend
start "Frontend Server" cmd /k "npm run dev"

echo.
echo 4. Services started!
echo    Backend: http://localhost:8000
echo    Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause > nul
