# AI Research Agent - Deployment Guide

## Production Deployment

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Database Configuration
USE_POSTGRES=true
POSTGRES_URL=postgresql://username:password@localhost:5432/research_agent

# AI API Keys
OPENAI_API_KEY=your_openai_api_key_here

# CORS Configuration
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Server Configuration
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=INFO
```

### Docker Deployment

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

2. **For production with custom domain:**
   ```bash
   # Update docker-compose.yml with your domain
   ALLOWED_ORIGINS=https://yourdomain.com
   docker-compose up -d
   ```

### Manual Deployment

#### Backend (FastAPI)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL database:**
   ```bash
   createdb research_agent
   ```

3. **Run migrations:**
   ```bash
   # Database tables will be created automatically on first run
   ```

4. **Start the server:**
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

#### Frontend (Next.js)

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Build for production:**
   ```bash
   npm run build
   ```

3. **Start the server:**
   ```bash
   npm start
   ```

### Cloud Deployment

#### Render.com

1. **Backend:**
   - Connect your GitHub repository
   - Set environment variables
   - Use PostgreSQL addon
   - Deploy with Docker

2. **Frontend:**
   - Connect your GitHub repository
   - Set `NEXT_PUBLIC_API_URL` to your backend URL
   - Deploy as static site

#### Railway

1. **Backend:**
   - Connect repository
   - Add PostgreSQL service
   - Set environment variables
   - Deploy

2. **Frontend:**
   - Connect repository
   - Set environment variables
   - Deploy

### Security Considerations

1. **Environment Variables:**
   - Never commit `.env` files
   - Use secure secret management
   - Rotate API keys regularly

2. **CORS:**
   - Configure `ALLOWED_ORIGINS` for your domain
   - Remove development URLs in production

3. **Database:**
   - Use strong passwords
   - Enable SSL connections
   - Regular backups

4. **API Keys:**
   - Store securely
   - Monitor usage
   - Set rate limits

### Monitoring

1. **Health Checks:**
   - Backend: `GET /health`
   - Frontend: `GET /`

2. **Logging:**
   - Application logs in `/var/log`
   - Database logs
   - Error tracking

3. **Performance:**
   - Monitor response times
   - Database query performance
   - Memory usage

### Troubleshooting

1. **Database Connection Issues:**
   - Check connection string
   - Verify database is running
   - Check firewall settings

2. **CORS Issues:**
   - Verify `ALLOWED_ORIGINS` configuration
   - Check frontend URL

3. **API Key Issues:**
   - Verify key is valid
   - Check rate limits
   - Monitor usage

### Scaling

1. **Horizontal Scaling:**
   - Use load balancer
   - Multiple backend instances
   - Database read replicas

2. **Vertical Scaling:**
   - Increase server resources
   - Optimize database queries
   - Cache frequently accessed data
