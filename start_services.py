#!/usr/bin/env python3
"""
Startup script for all services
"""
import subprocess
import sys
import time
import os
from pathlib import Path

def start_redis():
    """Start Redis server"""
    print("🔴 Starting Redis server...")
    try:
        # Try to start Redis (Windows)
        subprocess.Popen(["redis-server"], shell=True)
        time.sleep(2)
        print("✅ Redis server started")
        return True
    except Exception as e:
        print(f"❌ Failed to start Redis: {e}")
        print("Please install Redis or start it manually")
        return False

def start_celery_worker():
    """Start Celery worker"""
    print("🔄 Starting Celery worker...")
    try:
        subprocess.Popen([
            sys.executable, "-m", "celery", 
            "-A", "celery_app", 
            "worker", 
            "--loglevel=info",
            "--concurrency=2"
        ])
        time.sleep(3)
        print("✅ Celery worker started")
        return True
    except Exception as e:
        print(f"❌ Failed to start Celery worker: {e}")
        return False

def start_fastapi():
    """Start FastAPI server"""
    print("🚀 Starting FastAPI server...")
    try:
        subprocess.Popen([
            sys.executable, "main.py"
        ])
        time.sleep(3)
        print("✅ FastAPI server started")
        return True
    except Exception as e:
        print(f"❌ Failed to start FastAPI: {e}")
        return False

def main():
    """Main startup function"""
    print("🚀 Starting AI Research Agent Services")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ Error: main.py not found. Please run from the project root directory.")
        sys.exit(1)
    
    # Start services
    services_started = []
    
    if start_redis():
        services_started.append("Redis")
    
    if start_celery_worker():
        services_started.append("Celery Worker")
    
    if start_fastapi():
        services_started.append("FastAPI Server")
    
    print("\n" + "=" * 50)
    print("🎉 Services started successfully!")
    print(f"✅ Started: {', '.join(services_started)}")
    print("\n📋 Service URLs:")
    print("   FastAPI Server: http://localhost:8000")
    print("   API Documentation: http://localhost:8000/docs")
    print("   Health Check: http://localhost:8000/health")
    print("\n💡 Next steps:")
    print("   1. Start the frontend: cd frontend && npm run dev")
    print("   2. Open http://localhost:3000 in your browser")
    print("   3. Submit a research topic to test the system")
    print("\n🛑 To stop services: Press Ctrl+C")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down services...")
        sys.exit(0)

if __name__ == "__main__":
    main()
