"""
Core AI Research Agent with planning, execution, and decision-making capabilities
"""
import asyncio
import uuid
import time
from datetime import datetime
from typing import List, Dict, Any, Optional
from models import ResearchRequest, ResearchStep, ResearchStatus, StepType, ResearchResult, WebSearchResult
from database import db_manager
from web_search import WebSearchService
from analysis import AnalysisService
from logger import AgentLogger

class AIResearchAgent:
    """
    Main AI Research Agent that orchestrates the research workflow
    """
    
    def __init__(self):
        self.web_search_service = WebSearchService()
        self.analysis_service = AnalysisService()
        self.logger = AgentLogger()
        
    async def research_topic(self, topic: str) -> ResearchRequest:
        """
        Main entry point for research following the 5-step workflow.
        """
        research_id = str(uuid.uuid4())
        start_time = datetime.utcnow()
        
        # Create initial research request
        request = ResearchRequest(
            topic=topic,
            research_id=research_id,
            status=ResearchStatus.PENDING,
            created_at=start_time,
            steps=[],
            trace_log=[]
        )
        
        self.logger.log(f"Starting 5-step research workflow for topic: {topic}", research_id)
        
        try:
            # Step 1: Input Parsing - Validate input and store request in DB
            request = await self._step1_input_parsing(request)
            
            # Step 2: Data Gathering - Fetch relevant articles from external APIs
            request = await self._step2_data_gathering(request)
            
            # Step 3: Processing - Extract top 5 articles, summarize each, extract keywords
            request = await self._step3_processing(request)
            
            # Step 4: Result Persistence - Save processed results and logs in DB
            request = await self._step4_result_persistence(request)
            
            # Step 5: Return to Frontend - Prepare structured results
            request = await self._step5_return_to_frontend(request)
            
            request.status = ResearchStatus.COMPLETED
            request.completed_at = datetime.utcnow()
            
            self.logger.log(f"5-step research workflow completed successfully for topic: {topic}", research_id)
            
        except Exception as e:
            request.status = ResearchStatus.FAILED
            request.completed_at = datetime.utcnow()
            self.logger.log(f"Research workflow failed for topic: {topic}. Error: {str(e)}", research_id)
            request.trace_log.append(f"ERROR: {str(e)}")
        
        # Save to database
        db_manager.save_research_request(request)
        
        return request
    
    async def _step1_input_parsing(self, request: ResearchRequest) -> ResearchRequest:
        """
        Step 1: Input Parsing - Validate the input and store the request in DB
        """
        step_id = f"step1_input_parsing_{uuid.uuid4().hex[:8]}"
        start_time = time.time()
        
        step = ResearchStep(
            step_id=step_id,
            step_type=StepType.PLANNING,
            description=f"Step 1: Input Parsing - Validating topic: {request.topic}",
            status=ResearchStatus.IN_PROGRESS,
            timestamp=datetime.utcnow()
        )
        
        request.steps.append(step)
        db_manager.save_research_step(step, request.research_id)
        
        self.logger.log(f"Step 1: Input Parsing for topic: {request.topic}", request.research_id)
        
        try:
            # Validate input
            if not request.topic or len(request.topic.strip()) < 3:
                raise ValueError("Topic must be at least 3 characters long")
            
            # Clean and normalize topic
            topic = request.topic.strip()
            request.topic = topic
            
            # Store initial request in DB
            db_manager.save_research_request(request)
            
            step.output_data = {
                "validated_topic": topic,
                "topic_length": len(topic),
                "validation_passed": True
            }
            step.status = ResearchStatus.COMPLETED
            step.duration_seconds = time.time() - start_time
            
            request.trace_log.append(f"STEP 1: Input validated and stored in DB - Topic: '{topic}'")
            
        except Exception as e:
            step.status = ResearchStatus.FAILED
            step.error_message = str(e)
            step.duration_seconds = time.time() - start_time
            request.trace_log.append(f"STEP 1 ERROR: {str(e)}")
        
        db_manager.save_research_step(step, request.research_id)
        return request
    
    async def _step2_data_gathering(self, request: ResearchRequest) -> ResearchRequest:
        """
        Step 2: Data Gathering - Fetch relevant articles from external APIs
        """
        step_id = f"step2_data_gathering_{uuid.uuid4().hex[:8]}"
        start_time = time.time()
        
        step = ResearchStep(
            step_id=step_id,
            step_type=StepType.WEB_SEARCH,
            description=f"Step 2: Data Gathering - Fetching articles for: {request.topic}",
            status=ResearchStatus.IN_PROGRESS,
            timestamp=datetime.utcnow()
        )
        
        request.steps.append(step)
        db_manager.save_research_step(step, request.research_id)
        
        self.logger.log(f"Step 2: Data Gathering for topic: {request.topic}", request.research_id)
        
        try:
            # Fetch articles from multiple sources
            all_articles = []
            
            # Wikipedia articles
            wiki_articles = await self.web_search_service.fetch_wikipedia_articles(request.topic)
            all_articles.extend(wiki_articles)
            
            # News articles (if NewsAPI key available)
            news_articles = await self.web_search_service.fetch_news_articles(request.topic)
            all_articles.extend(news_articles)
            
            # HackerNews articles
            hn_articles = await self.web_search_service.fetch_hackernews_articles(request.topic)
            all_articles.extend(hn_articles)
            
            # Fallback to general web search if no specific APIs available
            if not all_articles:
                general_articles = await self.web_search_service.search(request.topic, num_results=10)
                all_articles.extend(general_articles)
            
            step.output_data = {
                "total_articles_found": len(all_articles),
                "wikipedia_articles": len(wiki_articles),
                "news_articles": len(news_articles),
                "hackernews_articles": len(hn_articles),
                "articles": [article.dict() for article in all_articles]
            }
            step.status = ResearchStatus.COMPLETED
            step.duration_seconds = time.time() - start_time
            
            request.trace_log.append(f"STEP 2: Gathered {len(all_articles)} articles from multiple sources")
            
            # Store articles for next step
            request.final_result = {
                "raw_articles": [article.dict() for article in all_articles],
                "total_articles": len(all_articles)
            }
            
        except Exception as e:
            step.status = ResearchStatus.FAILED
            step.error_message = str(e)
            step.duration_seconds = time.time() - start_time
            request.trace_log.append(f"STEP 2 ERROR: {str(e)}")
        
        db_manager.save_research_step(step, request.research_id)
        return request
    
    async def _step3_processing(self, request: ResearchRequest) -> ResearchRequest:
        """
        Step 3: Processing - Extract top 5 articles, summarize each, and extract top keywords
        """
        step_id = f"step3_processing_{uuid.uuid4().hex[:8]}"
        start_time = time.time()
        
        step = ResearchStep(
            step_id=step_id,
            step_type=StepType.ANALYSIS,
            description=f"Step 3: Processing - Analyzing articles for: {request.topic}",
            status=ResearchStatus.IN_PROGRESS,
            timestamp=datetime.utcnow()
        )
        
        request.steps.append(step)
        db_manager.save_research_step(step, request.research_id)
        
        self.logger.log(f"Step 3: Processing articles for topic: {request.topic}", request.research_id)
        
        try:
            # Get raw articles from previous step
            raw_articles = []
            if request.final_result and "raw_articles" in request.final_result:
                raw_articles = [
                    WebSearchResult(**article) for article in request.final_result["raw_articles"]
                ]
            
            if not raw_articles:
                raise ValueError("No articles found to process")
            
            # Select top 5 articles based on relevance score
            top_articles = sorted(raw_articles, key=lambda x: x.relevance_score, reverse=True)[:5]
            
            # Process each article
            processed_articles = []
            all_keywords = []
            
            for i, article in enumerate(top_articles):
                # Summarize article
                summary = await self.analysis_service.summarize_article(article)
                
                # Extract keywords
                keywords = await self.analysis_service.extract_keywords(article)
                all_keywords.extend(keywords)
                
                processed_article = {
                    "rank": i + 1,
                    "title": article.title,
                    "url": article.url,
                    "source": article.source,
                    "relevance_score": article.relevance_score,
                    "snippet": article.snippet,
                    "summary": summary,
                    "keywords": keywords
                }
                processed_articles.append(processed_article)
            
            # Extract top keywords across all articles
            top_keywords = await self.analysis_service.extract_top_keywords(all_keywords, limit=10)
            
            step.output_data = {
                "processed_articles": processed_articles,
                "total_articles_processed": len(processed_articles),
                "top_keywords": top_keywords,
                "all_keywords_count": len(all_keywords)
            }
            step.status = ResearchStatus.COMPLETED
            step.duration_seconds = time.time() - start_time
            
            request.trace_log.append(f"STEP 3: Processed {len(processed_articles)} articles and extracted {len(top_keywords)} top keywords")
            
            # Update final result with processed data
            if not request.final_result:
                request.final_result = {}
            
            request.final_result.update({
                "processed_articles": processed_articles,
                "top_keywords": top_keywords,
                "processing_completed": True
            })
            
        except Exception as e:
            step.status = ResearchStatus.FAILED
            step.error_message = str(e)
            step.duration_seconds = time.time() - start_time
            request.trace_log.append(f"STEP 3 ERROR: {str(e)}")
        
        db_manager.save_research_step(step, request.research_id)
        return request
    
    async def _step4_result_persistence(self, request: ResearchRequest) -> ResearchRequest:
        """
        Step 4: Result Persistence - Save processed results and logs in DB
        """
        step_id = f"step4_result_persistence_{uuid.uuid4().hex[:8]}"
        start_time = time.time()
        
        step = ResearchStep(
            step_id=step_id,
            step_type=StepType.VALIDATION,
            description=f"Step 4: Result Persistence - Saving results for: {request.topic}",
            status=ResearchStatus.IN_PROGRESS,
            timestamp=datetime.utcnow()
        )
        
        request.steps.append(step)
        db_manager.save_research_step(step, request.research_id)
        
        self.logger.log(f"Step 4: Result Persistence for topic: {request.topic}", request.research_id)
        
        try:
            # Prepare structured results for persistence
            structured_results = {
                "topic": request.topic,
                "research_id": request.research_id,
                "status": request.status,
                "created_at": request.created_at.isoformat(),
                "completed_at": request.completed_at.isoformat() if request.completed_at else None,
                "steps_completed": len(request.steps),
                "trace_log": request.trace_log,
                "processed_articles": request.final_result.get("processed_articles", []),
                "top_keywords": request.final_result.get("top_keywords", []),
                "total_articles_processed": len(request.final_result.get("processed_articles", [])),
                "workflow_version": "5-step-v1.0"
            }
            
            # Save to database
            db_manager.save_research_request(request)
            
            step.output_data = {
                "results_saved": True,
                "structured_results": structured_results,
                "database_updated": True
            }
            step.status = ResearchStatus.COMPLETED
            step.duration_seconds = time.time() - start_time
            
            request.trace_log.append(f"STEP 4: Results and logs saved to database successfully")
            
        except Exception as e:
            step.status = ResearchStatus.FAILED
            step.error_message = str(e)
            step.duration_seconds = time.time() - start_time
            request.trace_log.append(f"STEP 4 ERROR: {str(e)}")
        
        db_manager.save_research_step(step, request.research_id)
        return request
    
    async def _step5_return_to_frontend(self, request: ResearchRequest) -> ResearchRequest:
        """
        Step 5: Return to Frontend - Prepare structured results for frontend consumption
        """
        step_id = f"step5_return_to_frontend_{uuid.uuid4().hex[:8]}"
        start_time = time.time()
        
        step = ResearchStep(
            step_id=step_id,
            step_type=StepType.SYNTHESIS,
            description=f"Step 5: Return to Frontend - Preparing results for: {request.topic}",
            status=ResearchStatus.IN_PROGRESS,
            timestamp=datetime.utcnow()
        )
        
        request.steps.append(step)
        db_manager.save_research_step(step, request.research_id)
        
        self.logger.log(f"Step 5: Return to Frontend for topic: {request.topic}", request.research_id)
        
        try:
            # Prepare frontend-ready structured results
            frontend_results = {
                "research_id": request.research_id,
                "topic": request.topic,
                "status": request.status,
                "created_at": request.created_at.isoformat(),
                "completed_at": request.completed_at.isoformat() if request.completed_at else None,
                "workflow_steps": [
                    {
                        "step_number": i + 1,
                        "step_id": step.step_id,
                        "step_type": step.step_type,
                        "description": step.description,
                        "status": step.status,
                        "duration_seconds": step.duration_seconds,
                        "timestamp": step.timestamp.isoformat(),
                        "output_data": step.output_data,
                        "error_message": step.error_message
                    }
                    for i, step in enumerate(request.steps)
                ],
                "trace_log": request.trace_log,
                "results": {
                    "processed_articles": request.final_result.get("processed_articles", []),
                    "top_keywords": request.final_result.get("top_keywords", []),
                    "total_articles_processed": len(request.final_result.get("processed_articles", [])),
                    "workflow_completed": True
                }
            }
            
            step.output_data = {
                "frontend_results": frontend_results,
                "results_prepared": True
            }
            step.status = ResearchStatus.COMPLETED
            step.duration_seconds = time.time() - start_time
            
            request.trace_log.append(f"STEP 5: Results prepared for frontend consumption")
            
            # Update final result with frontend-ready data
            if not request.final_result:
                request.final_result = {}
            
            request.final_result.update({
                "frontend_results": frontend_results,
                "frontend_ready": True
            })
            
        except Exception as e:
            step.status = ResearchStatus.FAILED
            step.error_message = str(e)
            step.duration_seconds = time.time() - start_time
            request.trace_log.append(f"STEP 5 ERROR: {str(e)}")
        
        db_manager.save_research_step(step, request.research_id)
        return request
    
    def get_research_request(self, research_id: str) -> Optional[ResearchRequest]:
        """
        Retrieve a research request by ID
        """
        return db_manager.get_research_request(research_id)
    
    def get_all_research_requests(self) -> List[ResearchRequest]:
        """
        Get all research requests
        """
        return db_manager.get_all_research_requests()
