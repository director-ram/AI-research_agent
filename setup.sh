#!/bin/bash

echo "🤖 AI Research Agent - Linux/Mac Setup"
echo "======================================"

echo ""
echo "Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.11+ from https://www.python.org/downloads/"
    exit 1
fi
echo "✅ Python found"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 18+ from https://nodejs.org/"
    exit 1
fi
echo "✅ Node.js found"

# Check Git
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Please install Git from https://git-scm.com/"
    exit 1
fi
echo "✅ Git found"

echo ""
echo "Setting up backend..."

# Create virtual environment
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

echo "✅ Backend setup complete"

echo ""
echo "Setting up frontend..."

# Install Node.js dependencies
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install Node.js dependencies"
    exit 1
fi

# Build frontend
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Failed to build frontend"
    exit 1
fi

cd ..
echo "✅ Frontend setup complete"

echo ""
echo "Creating environment file..."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    cat > .env << EOF
# AI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
USE_POSTGRES=false
DATABASE_URL=sqlite:///./data/research_agent.db

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Server Configuration
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
EOF
    echo "✅ Environment file created"
else
    echo "✅ Environment file already exists"
fi

echo ""
echo "Creating data directory..."
mkdir -p data
echo "✅ Data directory created"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your OpenAI API key (optional)"
echo "2. Run: python main.py (in one terminal)"
echo "3. Run: cd frontend && npm run dev (in another terminal)"
echo "4. Open: http://localhost:3000"
echo ""
echo "Or use Docker: docker-compose up -d"
echo ""
