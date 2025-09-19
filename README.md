# AI Research Agent

An intelligent AI-powered research agent that accepts topics from users, runs comprehensive research workflows, and returns structured results with explainable traces. This system demonstrates how AI agents work in production environments with planning, execution, persistence, and transparency.

## Features

- **Intelligent Planning**: AI-driven research strategy planning based on topic analysis
- **Web Search Integration**: Automated web search with result processing and relevance scoring
- **Analysis & Synthesis**: AI-powered analysis of research results with key findings extraction
- **Persistent Storage**: SQLite database for storing research history and results
- **Explainable Traces**: Complete audit trail of agent decisions and actions
- **Web Interface**: Modern, responsive web UI for topic input and result visualization
- **RESTful API**: Full API for integration with other systems
- **Real-time Status**: Live updates on research progress

## Architecture

The system follows a production-ready AI agent architecture:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Interface │    │   FastAPI Server │    │  AI Research    │
│                 │◄──►│                  │◄──►│     Agent       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   Database       │    │  Web Search     │
                       │   (SQLite)       │    │  Service        │
                       └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │  Analysis       │
                                               │  Service        │
                                               └─────────────────┘
```

## Quick Start

### 1. Installation

```bash
# Clone or download the project
cd ai-research-agent

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy the environment example and configure:

```bash
cp env_example.txt .env
# Edit .env with your API keys (optional for demo mode)
```

### 3. Run the Application

```bash
# Start the server
python main.py

# Or with uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Access the Interface

Open your browser and go to: `http://localhost:8000`

## Usage

### Web Interface

1. Enter a research topic in the input field
2. Click "Start Research"
3. Watch the real-time progress updates
4. View the comprehensive research results with:
   - Executive summary
   - Key findings
   - Source citations
   - Confidence scores
   - Complete trace logs

### API Usage

#### Start Research
```bash
curl -X POST "http://localhost:8000/research" \
     -H "Content-Type: application/json" \
     -d '{"topic": "Artificial Intelligence in Healthcare"}'
```

#### Get Research Results
```bash
curl "http://localhost:8000/research/{research_id}"
```

#### Get All Research
```bash
curl "http://localhost:8000/research"
```

## How It Works

### 1. Planning Phase
- Analyzes the research topic
- Generates research questions and search queries
- Plans the research strategy

### 2. Execution Phase
- Performs web searches using multiple queries
- Processes and scores search results
- Extracts relevant information

### 3. Analysis Phase
- Synthesizes information from multiple sources
- Identifies key findings and trends
- Generates comprehensive summaries

### 4. Validation Phase
- Validates result completeness and quality
- Calculates confidence scores
- Ensures research standards are met

### 5. Persistence
- Stores all research data in SQLite database
- Maintains complete audit trail
- Enables research history retrieval

## Key Components

### Core Agent (`agent.py`)
- Main orchestration logic
- Step-by-step execution
- Error handling and recovery
- Progress tracking

### Web Search (`web_search.py`)
- Search query execution
- Result processing and scoring
- Source diversity analysis
- Mock and real API support

### Analysis (`analysis.py`)
- Content analysis and synthesis
- Key findings extraction
- Confidence scoring
- Summary generation

### Database (`database.py`)
- SQLite integration
- Research request storage
- Step tracking
- Query optimization

### Logging (`logger.py`)
- Comprehensive logging system
- Trace generation
- Debug information
- Performance metrics

## Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| `MAX_RESEARCH_STEPS` | Maximum research steps | 5 |
| `MAX_WEB_SEARCHES` | Maximum web searches | 3 |
| `RESEARCH_TIMEOUT` | Research timeout (seconds) | 300 |
| `LOG_LEVEL` | Logging level | INFO |
| `DATABASE_URL` | Database connection | sqlite:///./research_agent.db |

## Testing

Run the test suite:

```bash
# Run all tests
pytest test_agent.py -v

# Run with coverage
pytest test_agent.py --cov=agent --cov-report=html
```

## Production Deployment

### Environment Variables
- `OPENAI_API_KEY`: For real AI analysis (optional)
- `SERPAPI_KEY`: For real web search (optional)
- `DATABASE_URL`: Database connection string
- `LOG_LEVEL`: Logging level

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Scaling Considerations
- Use PostgreSQL for production database
- Implement Redis for caching
- Add load balancing for multiple instances
- Set up monitoring and alerting

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Create an issue in the repository
- Check the logs in `agent.log`
- Review the API documentation at `/docs`

---

**Note**: This is a demonstration system. For production use, integrate with real APIs and implement additional security measures.
