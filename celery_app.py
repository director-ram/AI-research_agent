"""
Celery application for background job processing
"""
from celery import Celery
from config import settings

# Create Celery instance
celery_app = Celery(
    "ai_research_agent",
    broker=f"redis://localhost:6379/0",
    backend=f"redis://localhost:6379/0",
    include=["tasks"]
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes
    task_soft_time_limit=240,  # 4 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=50,
)

# Optional configuration for better performance
celery_app.conf.update(
    result_expires=3600,  # Results expire after 1 hour
    task_always_eager=False,  # Set to True for testing
    task_eager_propagates=True,
)
