"""
Database setup and operations for the AI Research Agent
"""
from sqlalchemy import create_engine, Column, String, DateTime, Text, Float, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Optional, List
from models import ResearchRequest, ResearchStep, ResearchStatus
from config import settings
import os

Base = declarative_base()

class ResearchRequestDB(Base):
    __tablename__ = "research_requests"
    
    research_id = Column(String, primary_key=True)
    topic = Column(String, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    final_result = Column(JSON, nullable=True)
    trace_log = Column(Text, nullable=True)

class ResearchStepDB(Base):
    __tablename__ = "research_steps"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    research_id = Column(String, nullable=False)
    step_id = Column(String, nullable=False)
    step_type = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    duration_seconds = Column(Float, nullable=True)

class DatabaseManager:
    def __init__(self):
        # Choose database URL based on configuration
        if settings.use_postgres and settings.postgres_url:
            database_url = settings.postgres_url
        else:
            database_url = settings.database_url
        
        self.engine = create_engine(database_url)
        Base.metadata.create_all(bind=self.engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.SessionLocal = SessionLocal
    
    def get_session(self):
        return self.SessionLocal()
    
    def save_research_request(self, request: ResearchRequest) -> None:
        with self.get_session() as session:
            # Save or update research request
            db_request = session.query(ResearchRequestDB).filter(
                ResearchRequestDB.research_id == request.research_id
            ).first()
            
            if db_request:
                db_request.status = request.status
                db_request.completed_at = request.completed_at
                db_request.final_result = request.final_result
                db_request.trace_log = "\n".join(request.trace_log)
            else:
                db_request = ResearchRequestDB(
                    research_id=request.research_id,
                    topic=request.topic,
                    status=request.status,
                    created_at=request.created_at,
                    completed_at=request.completed_at,
                    final_result=request.final_result,
                    trace_log="\n".join(request.trace_log)
                )
                session.add(db_request)
            
            session.commit()
    
    def save_research_step(self, step: ResearchStep, research_id: str) -> None:
        with self.get_session() as session:
            db_step = ResearchStepDB(
                research_id=research_id,
                step_id=step.step_id,
                step_type=step.step_type,
                description=step.description,
                status=step.status,
                input_data=step.input_data,
                output_data=step.output_data,
                error_message=step.error_message,
                timestamp=step.timestamp,
                duration_seconds=step.duration_seconds
            )
            session.add(db_step)
            session.commit()
    
    def get_research_request(self, research_id: str) -> Optional[ResearchRequest]:
        with self.get_session() as session:
            db_request = session.query(ResearchRequestDB).filter(
                ResearchRequestDB.research_id == research_id
            ).first()
            
            if not db_request:
                return None
            
            # Get all steps for this research
            db_steps = session.query(ResearchStepDB).filter(
                ResearchStepDB.research_id == research_id
            ).all()
            
            steps = []
            for db_step in db_steps:
                step = ResearchStep(
                    step_id=db_step.step_id,
                    step_type=db_step.step_type,
                    description=db_step.description,
                    status=db_step.status,
                    input_data=db_step.input_data,
                    output_data=db_step.output_data,
                    error_message=db_step.error_message,
                    timestamp=db_step.timestamp,
                    duration_seconds=db_step.duration_seconds
                )
                steps.append(step)
            
            return ResearchRequest(
                topic=db_request.topic,
                research_id=db_request.research_id,
                status=db_request.status,
                created_at=db_request.created_at,
                completed_at=db_request.completed_at,
                steps=steps,
                final_result=db_request.final_result,
                trace_log=db_request.trace_log.split("\n") if db_request.trace_log else []
            )
    
    def get_all_research_requests(self) -> List[ResearchRequest]:
        with self.get_session() as session:
            db_requests = session.query(ResearchRequestDB).all()
            requests = []
            
            for db_request in db_requests:
                # Get steps for each request
                db_steps = session.query(ResearchStepDB).filter(
                    ResearchStepDB.research_id == db_request.research_id
                ).all()
                
                steps = []
                for db_step in db_steps:
                    step = ResearchStep(
                        step_id=db_step.step_id,
                        step_type=db_step.step_type,
                        description=db_step.description,
                        status=db_step.status,
                        input_data=db_step.input_data,
                        output_data=db_step.output_data,
                        error_message=db_step.error_message,
                        timestamp=db_step.timestamp,
                        duration_seconds=db_step.duration_seconds
                    )
                    steps.append(step)
                
                request = ResearchRequest(
                    topic=db_request.topic,
                    research_id=db_request.research_id,
                    status=db_request.status,
                    created_at=db_request.created_at,
                    completed_at=db_request.completed_at,
                    steps=steps,
                    final_result=db_request.final_result,
                    trace_log=db_request.trace_log.split("\n") if db_request.trace_log else []
                )
                requests.append(request)
            
            return requests

    def delete_research_request(self, research_id: str) -> bool:
        with self.get_session() as session:
            # Delete steps first due to FK-like relationship (manual)
            session.query(ResearchStepDB).filter(ResearchStepDB.research_id == research_id).delete()
            # Delete request
            deleted = session.query(ResearchRequestDB).filter(ResearchRequestDB.research_id == research_id).delete()
            session.commit()
            return deleted > 0

    def delete_all_research_requests(self) -> int:
        with self.get_session() as session:
            steps_deleted = session.query(ResearchStepDB).delete()
            requests_deleted = session.query(ResearchRequestDB).delete()
            session.commit()
            return requests_deleted

# Global database manager instance
db_manager = DatabaseManager()
