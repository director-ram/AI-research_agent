"""
Celery tasks for background research processing
"""
import asyncio
import uuid
import time
from datetime import datetime
from celery import current_task
from celery_app import celery_app
from agent import AIResearchAgent
from models import ResearchRequest, ResearchStatus
from database import db_manager
from logger import AgentLogger

logger = AgentLogger()

@celery_app.task(bind=True, name="process_research_task")
def process_research_task(self, topic: str, research_id: str):
    """
    Background task to process research using the 5-step workflow
    """
    try:
        # Update task status
        self.update_state(
            state="PROGRESS",
            meta={
                "current": 0,
                "total": 5,
                "status": "Starting research workflow...",
                "research_id": research_id
            }
        )
        
        # Create research request
        request = ResearchRequest(
            topic=topic,
            research_id=research_id,
            status=ResearchStatus.IN_PROGRESS,
            created_at=datetime.utcnow(),
            steps=[],
            trace_log=[]
        )
        
        # Save initial request
        db_manager.save_research_request(request)
        
        # Initialize agent
        agent = AIResearchAgent()
        
        # Step 1: Input Parsing
        self.update_state(
            state="PROGRESS",
            meta={
                "current": 1,
                "total": 5,
                "status": "Step 1: Input Parsing - Validating topic...",
                "research_id": research_id
            }
        )
        
        request = asyncio.run(agent._step1_input_parsing(request))
        
        # Step 2: Data Gathering
        self.update_state(
            state="PROGRESS",
            meta={
                "current": 2,
                "total": 5,
                "status": "Step 2: Data Gathering - Fetching articles...",
                "research_id": research_id
            }
        )
        
        request = asyncio.run(agent._step2_data_gathering(request))
        
        # Step 3: Processing
        self.update_state(
            state="PROGRESS",
            meta={
                "current": 3,
                "total": 5,
                "status": "Step 3: Processing - Analyzing articles...",
                "research_id": research_id
            }
        )
        
        request = asyncio.run(agent._step3_processing(request))
        
        # Step 4: Result Persistence
        self.update_state(
            state="PROGRESS",
            meta={
                "current": 4,
                "total": 5,
                "status": "Step 4: Result Persistence - Saving results...",
                "research_id": research_id
            }
        )
        
        request = asyncio.run(agent._step4_result_persistence(request))
        
        # Step 5: Return to Frontend
        self.update_state(
            state="PROGRESS",
            meta={
                "current": 5,
                "total": 5,
                "status": "Step 5: Return to Frontend - Preparing results...",
                "research_id": research_id
            }
        )
        
        request = asyncio.run(agent._step5_return_to_frontend(request))
        
        # Mark as completed
        request.status = ResearchStatus.COMPLETED
        request.completed_at = datetime.utcnow()
        db_manager.save_research_request(request)
        
        # Final success state
        self.update_state(
            state="SUCCESS",
            meta={
                "current": 5,
                "total": 5,
                "status": "Research completed successfully!",
                "research_id": research_id,
                "result": {
                    "research_id": research_id,
                    "topic": topic,
                    "status": "completed",
                    "completed_at": request.completed_at.isoformat(),
                    "articles_processed": len(request.final_result.get("processed_articles", [])),
                    "keywords_found": len(request.final_result.get("top_keywords", [])),
                    "steps_completed": len(request.steps)
                }
            }
        )
        
        logger.log(f"Research task completed successfully for topic: {topic}", research_id)
        
        return {
            "research_id": research_id,
            "topic": topic,
            "status": "completed",
            "completed_at": request.completed_at.isoformat(),
            "articles_processed": len(request.final_result.get("processed_articles", [])),
            "keywords_found": len(request.final_result.get("top_keywords", [])),
            "steps_completed": len(request.steps)
        }
        
    except Exception as e:
        # Mark as failed
        error_msg = str(e)
        logger.log(f"Research task failed for topic: {topic}. Error: {error_msg}", research_id)
        
        # Update request status
        try:
            request.status = ResearchStatus.FAILED
            request.completed_at = datetime.utcnow()
            request.trace_log.append(f"TASK ERROR: {error_msg}")
            db_manager.save_research_request(request)
        except:
            pass
        
        # Update task state
        self.update_state(
            state="FAILURE",
            meta={
                "current": 0,
                "total": 5,
                "status": f"Research failed: {error_msg}",
                "research_id": research_id,
                "error": error_msg
            }
        )
        
        raise e

@celery_app.task(name="health_check_task")
def health_check_task():
    """
    Health check task for Celery worker
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "worker": "ai_research_agent"
    }
