"""
FastAPI application for the AI Research Agent
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import List, Optional
import asyncio
from datetime import datetime
from starlette.requests import Request

from agent import AIResearchAgent
from models import ResearchRequest, ResearchStatus
from database import db_manager
# Celery imports removed - using synchronous processing for now

app = FastAPI(
    title="AI Research Agent",
    description="An AI-powered research agent that accepts topics and returns structured research results",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Initialize the agent
research_agent = AIResearchAgent()

# Job status tracking
job_status = {}

# Exception handlers for clearer 4xx responses
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Invalid request payload",
            "path": request.url.path,
            "details": exc.errors(),
        },
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP error",
            "path": request.url.path,
        },
    )

# Request/Response models
class ResearchTopicRequest(BaseModel):
    topic: str = Field(..., min_length=3, description="Research topic (min 3 chars)")

class ResearchResponse(BaseModel):
    research_id: str
    status: str
    message: str
    estimated_completion_time: Optional[str] = None

class ResearchResultResponse(BaseModel):
    research_id: str
    topic: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime]
    summary: Optional[str] = None
    key_findings: Optional[List[str]] = None
    sources: Optional[List[dict]] = None
    confidence_score: Optional[float] = None
    trace_log: List[str] = []
    steps: List[dict] = []

@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Serve the main web interface
    """
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Research Agent</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background: white;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #2c3e50;
                text-align: center;
                margin-bottom: 30px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #34495e;
            }
            input[type="text"] {
                width: 100%;
                padding: 12px;
                border: 2px solid #e1e8ed;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.3s;
            }
            input[type="text"]:focus {
                outline: none;
                border-color: #3498db;
            }
            button {
                background: #3498db;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            button:hover {
                background: #2980b9;
            }
            button:disabled {
                background: #bdc3c7;
                cursor: not-allowed;
            }
            .results {
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
                display: none;
            }
            .loading {
                text-align: center;
                color: #7f8c8d;
                font-style: italic;
            }
            .error {
                color: #e74c3c;
                background: #fdf2f2;
                padding: 10px;
                border-radius: 4px;
                margin: 10px 0;
            }
            .success {
                color: #27ae60;
                background: #f0f9f0;
                padding: 10px;
                border-radius: 4px;
                margin: 10px 0;
            }
            .research-item {
                background: white;
                border: 1px solid #e1e8ed;
                border-radius: 8px;
                padding: 15px;
                margin: 10px 0;
                cursor: pointer;
                transition: box-shadow 0.3s;
            }
            .research-item:hover {
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            .research-item h3 {
                margin: 0 0 10px 0;
                color: #2c3e50;
            }
            .research-item .status {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
            }
            .status.completed {
                background: #d4edda;
                color: #155724;
            }
            .status.in-progress {
                background: #fff3cd;
                color: #856404;
            }
            .status.failed {
                background: #f8d7da;
                color: #721c24;
            }
            .status.pending {
                background: #e2e3e5;
                color: #383d41;
            }
            .trace-log {
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 10px;
                margin: 10px 0;
                font-family: monospace;
                font-size: 12px;
                max-height: 200px;
                overflow-y: auto;
            }
            .key-findings {
                margin: 15px 0;
            }
            .key-findings ul {
                margin: 0;
                padding-left: 20px;
            }
            .key-findings li {
                margin: 5px 0;
            }
            .sources {
                margin: 15px 0;
            }
            .source-item {
                background: #f8f9fa;
                border-left: 3px solid #3498db;
                padding: 10px;
                margin: 5px 0;
            }
            .source-item a {
                color: #3498db;
                text-decoration: none;
            }
            .source-item a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 AI Research Agent</h1>
            <p style="text-align: center; color: #7f8c8d; margin-bottom: 30px;">
                Enter a topic and let our AI agent research it for you with explainable traces
            </p>
            
            <form id="researchForm">
                <div class="form-group">
                    <label for="topic">Research Topic:</label>
                    <input type="text" id="topic" name="topic" placeholder="e.g., Artificial Intelligence in Healthcare" required>
                </div>
                <button type="submit" id="submitBtn">Start Research</button>
            </form>
            
            <div id="results" class="results">
                <h2>Research Results</h2>
                <div id="researchList"></div>
            </div>
        </div>

        <script>
            const form = document.getElementById('researchForm');
            const results = document.getElementById('results');
            const researchList = document.getElementById('researchList');
            const submitBtn = document.getElementById('submitBtn');

            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                const topic = document.getElementById('topic').value;
                
                if (!topic.trim()) {
                    alert('Please enter a research topic');
                    return;
                }

                submitBtn.disabled = true;
                submitBtn.textContent = 'Researching...';
                results.style.display = 'block';
                researchList.innerHTML = '<div class="loading">Starting research...</div>';

                try {
                    const response = await fetch('/research', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ topic: topic })
                    });

                    const data = await response.json();
                    
                    if (response.ok) {
                        researchList.innerHTML = '<div class="success">Research started! Checking status...</div>';
                        pollResearchStatus(data.research_id);
                    } else {
                        researchList.innerHTML = `<div class="error">Error: ${data.detail}</div>`;
                    }
                } catch (error) {
                    researchList.innerHTML = `<div class="error">Error: ${error.message}</div>`;
                } finally {
                    submitBtn.disabled = false;
                    submitBtn.textContent = 'Start Research';
                }
            });

            async function pollResearchStatus(researchId) {
                const maxAttempts = 30; // 30 seconds max
                let attempts = 0;

                const poll = async () => {
                    try {
                        const response = await fetch(`/research/${researchId}`);
                        const data = await response.json();
                        
                        if (data.status === 'completed') {
                            displayResearchResult(data);
                        } else if (data.status === 'failed') {
                            researchList.innerHTML = `<div class="error">Research failed: ${data.trace_log[data.trace_log.length - 1] || 'Unknown error'}</div>`;
                        } else {
                            attempts++;
                            if (attempts < maxAttempts) {
                                researchList.innerHTML = `<div class="loading">Research in progress... (${attempts}/${maxAttempts})</div>`;
                                setTimeout(poll, 1000);
                            } else {
                                researchList.innerHTML = '<div class="error">Research timed out. Please try again.</div>';
                            }
                        }
                    } catch (error) {
                        researchList.innerHTML = `<div class="error">Error checking status: ${error.message}</div>`;
                    }
                };

                poll();
            }

            function displayResearchResult(data) {
                let html = `
                    <div class="research-item">
                        <h3>${data.topic}</h3>
                        <span class="status ${data.status}">${data.status}</span>
                        <p><strong>Completed:</strong> ${new Date(data.completed_at).toLocaleString()}</p>
                `;

                if (data.summary) {
                    html += `<div class="summary"><h4>Summary</h4><p>${data.summary.replace(/\\n/g, '<br>')}</p></div>`;
                }

                if (data.key_findings && data.key_findings.length > 0) {
                    html += `<div class="key-findings"><h4>Key Findings</h4><ul>`;
                    data.key_findings.forEach(finding => {
                        html += `<li>${finding}</li>`;
                    });
                    html += `</ul></div>`;
                }

                if (data.sources && data.sources.length > 0) {
                    html += `<div class="sources"><h4>Sources</h4>`;
                    data.sources.forEach(source => {
                        html += `
                            <div class="source-item">
                                <strong><a href="${source.url}" target="_blank">${source.title}</a></strong><br>
                                <small>${source.source} - ${source.snippet}</small>
                            </div>
                        `;
                    });
                    html += `</div>`;
                }

                if (data.confidence_score) {
                    html += `<p><strong>Confidence Score:</strong> ${(data.confidence_score * 100).toFixed(1)}%</p>`;
                }

                if (data.trace_log && data.trace_log.length > 0) {
                    html += `<div class="trace-log"><h4>Research Trace</h4><pre>${data.trace_log.join('\\n')}</pre></div>`;
                }

                html += `</div>`;
                researchList.innerHTML = html;
            }

            // Load existing research on page load
            window.addEventListener('load', async () => {
                try {
                    const response = await fetch('/research');
                    const data = await response.json();
                    
                    if (data.length > 0) {
                        results.style.display = 'block';
                        researchList.innerHTML = '<h3>Previous Research</h3>';
                        data.forEach(item => {
                            const itemDiv = document.createElement('div');
                            itemDiv.className = 'research-item';
                            itemDiv.innerHTML = `
                                <h3>${item.topic}</h3>
                                <span class="status ${item.status}">${item.status}</span>
                                <p><strong>Created:</strong> ${new Date(item.created_at).toLocaleString()}</p>
                                <button onclick="viewResearch('${item.research_id}')">View Details</button>
                            `;
                            researchList.appendChild(itemDiv);
                        });
                    }
                } catch (error) {
                    console.error('Error loading previous research:', error);
                }
            });

            async function viewResearch(researchId) {
                try {
                    const response = await fetch(`/research/${researchId}`);
                    const data = await response.json();
                    displayResearchResult(data);
                } catch (error) {
                    researchList.innerHTML = `<div class="error">Error loading research: ${error.message}</div>`;
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/research", response_model=ResearchResponse)
async def start_research(request: ResearchTopicRequest):
    """
    Start a new research session for the given topic
    """
    try:
        import uuid
        research_id = str(uuid.uuid4())
        
        # Store job status
        job_status[research_id] = {
            "task_id": research_id,
            "status": "IN_PROGRESS",
            "created_at": datetime.utcnow().isoformat(),
            "topic": request.topic
        }
        
        # Run research synchronously for now (without Celery)
        try:
            result = await research_agent.research_topic(request.topic)
            
            # Update job status
            job_status[research_id]["status"] = "COMPLETED"
            job_status[research_id]["completed_at"] = datetime.utcnow().isoformat()
            
            return ResearchResponse(
                research_id=research_id,
                status="COMPLETED",
                message="Research completed successfully",
                estimated_completion_time="0 minutes"
            )
        except Exception as e:
            # Update job status
            job_status[research_id]["status"] = "FAILED"
            job_status[research_id]["error"] = str(e)
            
            return ResearchResponse(
                research_id=research_id,
                status="FAILED",
                message=f"Research failed: {str(e)}",
                estimated_completion_time="0 minutes"
            )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start research: {str(e)}")

@app.get("/research/{research_id}/status")
async def get_research_status(research_id: str):
    """
    Get the status of a research job
    """
    if research_id not in job_status:
        raise HTTPException(status_code=404, detail="Research job not found")
    
    job_info = job_status[research_id]
    
    # Return the stored status (no Celery needed)
    return {
        "research_id": research_id,
        "status": job_info["status"],
        "message": job_info.get("message", "Processing..."),
        "progress": job_info.get("progress", {"current": 0, "total": 5})
    }

@app.get("/research/{research_id}", response_model=ResearchResultResponse)
async def get_research_result(research_id: str):
    """
    Get the result of a specific research session
    """
    research_request = research_agent.get_research_request(research_id)
    
    if not research_request:
        raise HTTPException(status_code=404, detail="Research not found")
    
    # Convert to response format
    response_data = {
        "research_id": research_request.research_id,
        "topic": research_request.topic,
        "status": research_request.status,
        "created_at": research_request.created_at,
        "completed_at": research_request.completed_at,
        "trace_log": research_request.trace_log,
        "steps": [step.dict() for step in research_request.steps]
    }
    
    # Add analysis data if available
    if research_request.final_result and "frontend_results" in research_request.final_result:
        frontend_results = research_request.final_result["frontend_results"]
        response_data.update({
            "workflow_steps": frontend_results.get("workflow_steps", []),
            "results": frontend_results.get("results", {})
        })
    elif research_request.final_result and "analysis" in research_request.final_result:
        analysis = research_request.final_result["analysis"]
        response_data.update({
            "summary": analysis.get("summary"),
            "key_findings": analysis.get("key_findings"),
            "sources": analysis.get("sources"),
            "confidence_score": analysis.get("confidence_score")
        })
    
    return ResearchResultResponse(**response_data)

@app.get("/research", response_model=List[ResearchResultResponse])
async def get_all_research():
    """
    Get all research sessions
    """
    research_requests = research_agent.get_all_research_requests()
    
    results = []
    for request in research_requests:
        response_data = {
            "research_id": request.research_id,
            "topic": request.topic,
            "status": request.status,
            "created_at": request.created_at,
            "completed_at": request.completed_at,
            "trace_log": request.trace_log,
            "steps": [step.dict() for step in request.steps]
        }
        
        # Add analysis data if available
        if request.final_result and "analysis" in request.final_result:
            analysis = request.final_result["analysis"]
            response_data.update({
                "summary": analysis.get("summary"),
                "key_findings": analysis.get("key_findings"),
                "sources": analysis.get("sources"),
                "confidence_score": analysis.get("confidence_score")
            })
        
        results.append(ResearchResultResponse(**response_data))
    
    return results

@app.delete("/research/{research_id}")
async def delete_research(research_id: str):
    """
    Delete a specific research session
    """
    from database import db_manager
    deleted = db_manager.delete_research_request(research_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Research not found")
    # Drop transient job status cache
    if research_id in job_status:
        del job_status[research_id]
    return {"deleted": True, "research_id": research_id}

@app.delete("/research")
async def delete_all_research():
    """
    Delete all research sessions
    """
    from database import db_manager
    count = db_manager.delete_all_research_requests()
    job_status.clear()
    return {"deleted": count}

@app.options("/{path:path}")
async def options_handler(path: str):
    """
    Handle OPTIONS requests for CORS
    """
    return {"message": "OK"}

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
