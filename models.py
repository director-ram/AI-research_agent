"""
Data models for the AI Research Agent
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from enum import Enum

class ResearchStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class StepType(str, Enum):
    PLANNING = "planning"
    WEB_SEARCH = "web_search"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    VALIDATION = "validation"

class ResearchStep(BaseModel):
    step_id: str
    step_type: StepType
    description: str
    status: ResearchStatus
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    timestamp: datetime
    duration_seconds: Optional[float] = None

class ResearchRequest(BaseModel):
    topic: str
    research_id: str
    status: ResearchStatus
    created_at: datetime
    completed_at: Optional[datetime] = None
    steps: List[ResearchStep] = []
    final_result: Optional[Dict[str, Any]] = None
    trace_log: List[str] = []

class WebSearchResult(BaseModel):
    title: str
    url: str
    snippet: str
    relevance_score: float
    source: str

class ResearchResult(BaseModel):
    topic: str
    summary: str
    key_findings: List[str]
    sources: List[WebSearchResult]
    confidence_score: float
    research_metadata: Dict[str, Any]
    generated_at: datetime
