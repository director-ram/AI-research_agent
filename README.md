# 🤖 AI Research Agent

An intelligent research assistant that uses AI to analyze topics, gather information from multiple sources, and generate comprehensive research reports with real-time progress tracking.

## ✨ Features

- **🔍 Intelligent Research**: AI-powered topic analysis and information gathering
- **📊 Real-time Progress**: Live updates during research with detailed workflow steps
- **📝 Comprehensive Reports**: Generated summaries, keywords, and structured insights
- **💾 Persistent Storage**: Research history saved for future reference
- **📄 Export Options**: Download research as PDF or DOCX documents
- **🎨 Modern UI**: Beautiful, responsive interface built with Next.js
- **⚡ Fast Performance**: Optimized for speed and reliability

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** - [Download here](https://www.python.org/downloads/)
- **Node.js 18+** - [Download here](https://nodejs.org/)
- **Git** - [Download here](https://git-scm.com/)

### Option 1: One-Click Setup (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-research-agent.git
   cd ai-research-agent
   ```

2. **Run the setup script:**
   ```bash
   # Windows
   setup.bat
   
   # Mac/Linux
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Start the application:**
   ```bash
   # Start both backend and frontend
   docker-compose up -d
   ```

4. **Open your browser:**
   - Go to `http://localhost:3000`
   - Start researching! 🎉

### Option 2: Manual Setup

#### Step 1: Backend Setup

1. **Navigate to project directory:**
   ```bash
   cd ai-research-agent
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
   echo "USE_POSTGRES=false" >> .env
   echo "DATABASE_URL=sqlite:///./data/research_agent.db" >> .env
   ```

5. **Start the backend:**
   ```bash
   python main.py
   ```
   - Backend will run on `http://localhost:8000`
   - You'll see: `Uvicorn running on http://0.0.0.0:8000`

#### Step 2: Frontend Setup

1. **Open a new terminal and navigate to frontend:**
   ```bash
   cd ai-research-agent/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the frontend:**
   ```bash
   npm run dev
   ```
   - Frontend will run on `http://localhost:3000`
   - You'll see: `Ready - started server on 0.0.0.0:3000`

#### Step 3: Verify Setup

1. **Check backend health:**
   - Open `http://localhost:8000/health`
   - Should show: `{"status":"healthy","timestamp":"..."}`

2. **Check frontend:**
   - Open `http://localhost:3000`
   - Should see the AI Research Agent interface

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# AI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Database Configuration
USE_POSTGRES=false
DATABASE_URL=sqlite:///./data/research_agent.db

# For PostgreSQL (optional)
# USE_POSTGRES=true
# POSTGRES_URL=postgresql://username:password@localhost:5432/research_agent

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Server Configuration
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```

### Getting OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Copy the key and add it to your `.env` file

**Note:** The app works without OpenAI API key using local AI models, but OpenAI provides better results.

## 📖 How to Use

### 1. Start a Research

1. **Enter your research topic** in the input field
2. **Click "Start Research"**
3. **Watch the progress** in real-time:
   - Progress bar shows completion percentage
   - Step details show what's happening
   - Current step is highlighted

### 2. Monitor Progress

The research goes through 5 steps:
1. **Input Parsing** - Understanding your topic
2. **Data Gathering** - Collecting information from web sources
3. **Processing** - Analyzing and summarizing content
4. **Result Persistence** - Saving to database
5. **Frontend Preparation** - Making results available

### 3. View Results

Once complete, you can:
- **View detailed results** with AI-generated summary
- **See key terms and concepts** extracted
- **Browse source articles** with working links
- **Download as PDF or DOCX** for offline use

### 4. Manage Research History

- **View all past research** in the history section
- **Click any research** to see full details
- **Delete individual research** or clear all
- **Refresh the list** manually if needed

## 🐳 Docker Deployment

### Using Docker Compose (Easiest)

1. **Make sure Docker is installed:**
   - [Docker Desktop](https://www.docker.com/products/docker-desktop/)

2. **Run the application:**
   ```bash
   docker-compose up -d
   ```

3. **Access the application:**
   - Frontend: `http://localhost:3000`
   - Backend: `http://localhost:8000`

4. **Stop the application:**
   ```bash
   docker-compose down
   ```

### Using Docker (Manual)

1. **Build backend image:**
   ```bash
   docker build -t ai-research-backend .
   ```

2. **Run backend:**
   ```bash
   docker run -p 8000:8000 --env-file .env ai-research-backend
   ```

3. **Build and run frontend:**
   ```bash
   cd frontend
   docker build -t ai-research-frontend .
   docker run -p 3000:3000 ai-research-frontend
   ```

## ☁️ Cloud Deployment

### Deploy to Railway (Recommended)

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Deploy backend:**
   ```bash
   railway init
   railway up
   ```

4. **Add PostgreSQL database:**
   - Go to Railway dashboard
   - Add PostgreSQL service
   - Connect to your project

5. **Deploy frontend to Vercel:**
   ```bash
   cd frontend
   npx vercel
   ```

### Deploy to Render.com

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Deploy to production"
   git push origin main
   ```

2. **Connect to Render:**
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository
   - Use the `render.yaml` configuration

## 🛠️ Development

### Project Structure

```
ai-research-agent/
├── main.py                 # FastAPI backend server
├── agent.py               # AI research agent logic
├── analysis.py            # AI analysis and summarization
├── database.py            # Database operations
├── models.py              # Data models
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── Dockerfile             # Backend Docker configuration
├── docker-compose.yml     # Full stack Docker setup
├── frontend/              # Next.js frontend
│   ├── src/
│   │   ├── app/           # Main application pages
│   │   ├── components/    # React components
│   │   └── types/         # TypeScript type definitions
│   ├── package.json       # Node.js dependencies
│   └── Dockerfile         # Frontend Docker configuration
└── README.md              # This file
```

### Running in Development Mode

1. **Backend (Terminal 1):**
   ```bash
   python main.py
   ```

2. **Frontend (Terminal 2):**
   ```bash
   cd frontend
   npm run dev
   ```

### Making Changes

1. **Backend changes:** Restart the Python server
2. **Frontend changes:** Hot reload automatically updates
3. **Database changes:** May require restart

## 🔍 Troubleshooting

### Common Issues

#### Backend Won't Start
- **Check Python version:** `python --version` (should be 3.11+)
- **Check dependencies:** `pip install -r requirements.txt`
- **Check port:** Make sure port 8000 is available
- **Check logs:** Look for error messages in terminal

#### Frontend Won't Start
- **Check Node.js version:** `node --version` (should be 18+)
- **Check dependencies:** `npm install`
- **Check port:** Make sure port 3000 is available
- **Clear cache:** `npm run build` then `npm start`

#### Database Issues
- **Check file permissions:** Make sure the app can write to the data directory
- **Check SQLite:** Database file should be created automatically
- **Check PostgreSQL:** Verify connection string is correct

#### AI Features Not Working
- **Check API key:** Verify OpenAI API key is set correctly
- **Check internet:** AI models need internet connection
- **Check logs:** Look for error messages in terminal

### Getting Help

1. **Check the logs** in your terminal for error messages
2. **Verify environment variables** are set correctly
3. **Check the health endpoints:**
   - Backend: `http://localhost:8000/health`
   - Frontend: `http://localhost:3000`
4. **Restart the services** if needed

## 📚 API Documentation

Once running, visit:
- **Backend API:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/health`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m "Add feature"`
6. Push: `git push origin feature-name`
7. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **OpenAI** for AI capabilities
- **Hugging Face** for local AI models
- **FastAPI** for the backend framework
- **Next.js** for the frontend framework
- **Tailwind CSS** for styling

---

**Happy Researching! 🚀**

If you encounter any issues, please check the troubleshooting section or create an issue on GitHub.