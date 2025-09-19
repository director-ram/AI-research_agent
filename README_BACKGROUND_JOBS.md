# AI Research Agent - Background Job System

## 🚀 **Enhanced Backend with Background Job Processing**

This implementation now includes a complete background job system using **Celery** with **Redis** as the message broker, following your exact requirements.

## ✅ **Backend Requirements Implemented**

### **FastAPI Backend (Python)**
- ✅ **FastAPI** with async support
- ✅ **Background Job System**: Celery with Redis
- ✅ **Database**: SQLite (default) + PostgreSQL support
- ✅ **Persistence**: Complete workflow logs and structured results

### **API Endpoints**
- ✅ `POST /research` → Submit new topic, trigger background workflow
- ✅ `GET /research` → List all research topics
- ✅ `GET /research/{id}` → Get logs and results
- ✅ `GET /research/{id}/status` → Get real-time job status

### **Background Job System**
- ✅ **Celery** for distributed task processing
- ✅ **Redis** as message broker and result backend
- ✅ **Job Status Tracking**: Real-time progress monitoring
- ✅ **Error Handling**: Comprehensive failure management
- ✅ **Scalability**: Multiple worker support

### **Database Support**
- ✅ **SQLite**: Default for development
- ✅ **PostgreSQL**: Production-ready with Docker support
- ✅ **Migrations**: Alembic for schema management
- ✅ **Persistence**: Complete research history and logs

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React/Next.js │    │   FastAPI Server │    │   Celery Worker │
│   Frontend      │◄──►│   (Port 8000)    │◄──►│   (Background)  │
│   (Port 3000)   │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   PostgreSQL/    │    │     Redis       │
                       │   SQLite DB      │    │   (Message      │
                       │   (Persistence)  │    │    Broker)      │
                       └──────────────────┘    └─────────────────┘
```

## 🚀 **Quick Start**

### **Option 1: Development Setup**

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Redis** (Required for Celery)
   ```bash
   # Windows (if Redis installed)
   redis-server
   
   # Or use Docker
   docker run -d -p 6379:6379 redis:7-alpine
   ```

3. **Start Celery Worker**
   ```bash
   celery -A celery_app worker --loglevel=info --concurrency=2
   ```

4. **Start FastAPI Server**
   ```bash
   python main.py
   ```

5. **Start Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### **Option 2: Docker Compose (Recommended)**

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### **Option 3: Automated Startup**

```bash
# Start all services automatically
python start_services.py
```

## 📊 **Job Processing Flow**

### **1. Job Submission**
```python
# POST /research
{
  "topic": "Artificial Intelligence in Healthcare"
}

# Response
{
  "research_id": "uuid-here",
  "status": "PENDING",
  "message": "Research started successfully in background"
}
```

### **2. Real-time Status Monitoring**
```python
# GET /research/{id}/status
{
  "research_id": "uuid-here",
  "status": "IN_PROGRESS",
  "message": "Step 3: Processing - Analyzing articles...",
  "progress": {
    "current": 3,
    "total": 5
  }
}
```

### **3. Job Completion**
```python
# GET /research/{id}
{
  "research_id": "uuid-here",
  "topic": "Artificial Intelligence in Healthcare",
  "status": "completed",
  "workflow_steps": [...],
  "results": {
    "processed_articles": [...],
    "top_keywords": [...],
    "total_articles_processed": 5
  }
}
```

## 🔧 **Configuration**

### **Environment Variables**
```env
# Database
DATABASE_URL=sqlite:///./research_agent.db
POSTGRES_URL=postgresql://user:pass@localhost:5432/research_agent
USE_POSTGRES=false

# Redis
REDIS_URL=redis://localhost:6379/0

# APIs (Optional)
OPENAI_API_KEY=your_key_here
NEWSAPI_KEY=your_key_here
SERPAPI_KEY=your_key_here
```

### **Celery Configuration**
- **Broker**: Redis
- **Result Backend**: Redis
- **Concurrency**: 2 workers (configurable)
- **Task Time Limit**: 5 minutes
- **Soft Time Limit**: 4 minutes

## 📈 **Monitoring & Management**

### **Celery Flower (Web UI)**
```bash
# Start Flower monitoring
celery -A celery_app flower --port=5555

# Access: http://localhost:5555
```

### **Health Checks**
```bash
# API Health
curl http://localhost:8000/health

# Celery Health
curl http://localhost:8000/celery/health
```

## 🐳 **Docker Services**

| Service | Port | Description |
|---------|------|-------------|
| FastAPI | 8000 | Main API server |
| Frontend | 3000 | React/Next.js UI |
| Redis | 6379 | Message broker |
| PostgreSQL | 5432 | Database |
| Celery Flower | 5555 | Job monitoring |

## 🔍 **API Documentation**

### **Research Endpoints**

#### **Start Research**
```http
POST /research
Content-Type: application/json

{
  "topic": "Machine Learning Trends"
}
```

#### **Get Job Status**
```http
GET /research/{research_id}/status
```

#### **Get Research Results**
```http
GET /research/{research_id}
```

#### **List All Research**
```http
GET /research
```

### **Job Status Values**
- `PENDING` - Job queued, waiting to start
- `IN_PROGRESS` - Job running (with progress info)
- `COMPLETED` - Job finished successfully
- `FAILED` - Job failed with error details

## 🚀 **Production Deployment**

### **Scaling Workers**
```bash
# Start multiple workers
celery -A celery_app worker --loglevel=info --concurrency=4 --hostname=worker1@%h
celery -A celery_app worker --loglevel=info --concurrency=4 --hostname=worker2@%h
```

### **Load Balancing**
- Multiple Celery workers can process jobs in parallel
- Redis handles job distribution
- FastAPI can handle multiple concurrent requests

### **Monitoring**
- Use Celery Flower for job monitoring
- Redis monitoring for queue health
- Database monitoring for persistence

## 🎯 **Key Features**

### **Background Processing**
- ✅ Non-blocking API responses
- ✅ Real-time job status updates
- ✅ Scalable worker architecture
- ✅ Job failure handling and retry

### **Data Persistence**
- ✅ Complete workflow logs
- ✅ Structured research results
- ✅ Job metadata and timestamps
- ✅ Error tracking and debugging

### **Production Ready**
- ✅ Docker containerization
- ✅ Health checks and monitoring
- ✅ Error handling and logging
- ✅ Scalable architecture

## 🔧 **Troubleshooting**

### **Common Issues**

1. **Redis Connection Error**
   ```bash
   # Check if Redis is running
   redis-cli ping
   # Should return: PONG
   ```

2. **Celery Worker Not Starting**
   ```bash
   # Check Redis connection
   celery -A celery_app inspect ping
   ```

3. **Database Connection Issues**
   ```bash
   # Check database URL
   echo $DATABASE_URL
   ```

### **Logs**
```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f api
docker-compose logs -f celery-worker
```

## 🎉 **Success Metrics**

✅ **Background Job System**: Celery + Redis implemented  
✅ **API Endpoints**: All required endpoints working  
✅ **Database Persistence**: SQLite + PostgreSQL support  
✅ **Real-time Status**: Job progress monitoring  
✅ **Scalability**: Multiple worker support  
✅ **Production Ready**: Docker + monitoring  
✅ **Error Handling**: Comprehensive failure management  
✅ **Documentation**: Complete setup and usage guides  

The system now fully meets your backend requirements with a robust background job processing system! 🚀
