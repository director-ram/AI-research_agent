#!/usr/bin/env python3
"""
Startup script for the AI Research Agent
"""
import uvicorn
import sys
import os
from pathlib import Path

def main():
    """Main entry point for the application"""
    print("🔍 Starting AI Research Agent...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ Error: main.py not found. Please run from the project root directory.")
        sys.exit(1)
    
    # Check for required files
    required_files = ["agent.py", "models.py", "database.py", "web_search.py", "analysis.py", "logger.py", "config.py"]
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"❌ Error: Missing required files: {', '.join(missing_files)}")
        sys.exit(1)
    
    print("✅ All required files found")
    print("🚀 Starting server on http://localhost:8000")
    print("📖 API documentation available at http://localhost:8000/docs")
    print("=" * 50)
    
    try:
        # Start the server
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down AI Research Agent...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
