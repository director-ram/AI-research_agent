"""
Configuration settings for the AI Research Agent
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API Keys
    openai_api_key: Optional[str] = None
    serpapi_key: Optional[str] = None
    newsapi_key: Optional[str] = None
    
    # Database
    database_url: str = "sqlite:///./research_agent.db"
    postgres_url: Optional[str] = None
    use_postgres: bool = False
    
    # Agent Settings
    max_research_steps: int = 5
    max_web_searches: int = 3
    research_timeout: int = 300  # 5 minutes
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "agent.log"
    
    # Redis (for Celery)
    redis_url: str = "redis://localhost:6379/0"
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields in .env file

settings = Settings()
