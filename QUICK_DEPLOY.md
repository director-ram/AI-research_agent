# 🚀 Quick Deployment Guide

## Option 1: Railway (Recommended - Easiest)

### Backend Deployment:
1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway:**
   ```bash
   railway login
   ```

3. **Deploy Backend:**
   ```bash
   railway init
   railway up
   ```

4. **Add PostgreSQL Database:**
   - Go to Railway dashboard
   - Add PostgreSQL service
   - Connect to your project

5. **Set Environment Variables:**
   - `USE_POSTGRES=true`
   - `POSTGRES_URL=${{Postgres.DATABASE_URL}}`
   - `OPENAI_API_KEY=your_key_here`
   - `ALLOWED_ORIGINS=https://your-frontend-url.vercel.app`

### Frontend Deployment (Vercel):
1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy Frontend:**
   ```bash
   cd frontend
   vercel
   ```

3. **Set Environment Variable:**
   - `NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app`

## Option 2: Render.com (All-in-One)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Production ready deployment"
   git push origin main
   ```

2. **Connect to Render:**
   - Go to render.com
   - Connect your GitHub repository
   - Use the `render.yaml` configuration

3. **Set Environment Variables:**
   - `OPENAI_API_KEY=your_key_here`

## Option 3: Docker Compose (Local)

1. **Run Locally:**
   ```bash
   docker-compose up -d
   ```

2. **Access Application:**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000

## Environment Variables Required:

### Backend:
- `OPENAI_API_KEY` - Your OpenAI API key
- `USE_POSTGRES=true` - Use PostgreSQL
- `POSTGRES_URL` - Database connection string
- `ALLOWED_ORIGINS` - Frontend URL for CORS

### Frontend:
- `NEXT_PUBLIC_API_URL` - Backend API URL

## Quick Test Commands:

```bash
# Test backend
curl https://your-backend-url.railway.app/health

# Test frontend
curl https://your-frontend-url.vercel.app
```

## Troubleshooting:

1. **CORS Issues:** Check `ALLOWED_ORIGINS` matches frontend URL
2. **Database Issues:** Verify `POSTGRES_URL` is correct
3. **API Key Issues:** Ensure `OPENAI_API_KEY` is set correctly
4. **Build Issues:** Check logs in deployment platform

## Support:
- Check `DEPLOYMENT.md` for detailed instructions
- Review logs in your deployment platform
- Ensure all environment variables are set correctly
