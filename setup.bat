@echo off
echo 🤖 AI Research Agent - Windows Setup
echo ====================================

echo.
echo Checking prerequisites...

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.11+ from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo ✅ Python found

:: Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not found. Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)
echo ✅ Node.js found

:: Check Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git not found. Please install Git from https://git-scm.com/
    pause
    exit /b 1
)
echo ✅ Git found

echo.
echo Setting up backend...

:: Create virtual environment
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install Python dependencies
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✅ Backend setup complete

echo.
echo Setting up frontend...

:: Install Node.js dependencies
cd frontend
npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
)

:: Build frontend
npm run build
if %errorlevel% neq 0 (
    echo ❌ Failed to build frontend
    pause
    exit /b 1
)

cd ..
echo ✅ Frontend setup complete

echo.
echo Creating environment file...

:: Create .env file if it doesn't exist
if not exist .env (
    echo # AI Configuration > .env
    echo OPENAI_API_KEY=your_openai_api_key_here >> .env
    echo. >> .env
    echo # Database Configuration >> .env
    echo USE_POSTGRES=false >> .env
    echo DATABASE_URL=sqlite:///./data/research_agent.db >> .env
    echo. >> .env
    echo # CORS Configuration >> .env
    echo ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000 >> .env
    echo. >> .env
    echo # Server Configuration >> .env
    echo HOST=0.0.0.0 >> .env
    echo PORT=8000 >> .env
    echo LOG_LEVEL=INFO >> .env
    echo ✅ Environment file created
) else (
    echo ✅ Environment file already exists
)

echo.
echo Creating data directory...
if not exist data mkdir data
echo ✅ Data directory created

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Edit .env file and add your OpenAI API key (optional)
echo 2. Run: python main.py (in one terminal)
echo 3. Run: cd frontend && npm run dev (in another terminal)
echo 4. Open: http://localhost:3000
echo.
echo Or use Docker: docker-compose up -d
echo.
pause
