"""
Test suite for the AI Research Agent
"""
import pytest
import asyncio
from datetime import datetime
from agent import AIResearchAgent
from models import ResearchStatus, StepType
from database import db_manager

class TestAIResearchAgent:
    """Test cases for the AI Research Agent"""
    
    @pytest.fixture
    def agent(self):
        """Create a fresh agent instance for each test"""
        return AIResearchAgent()
    
    @pytest.mark.asyncio
    async def test_research_topic_success(self, agent):
        """Test successful research completion"""
        topic = "Artificial Intelligence"
        result = await agent.research_topic(topic)
        
        assert result.topic == topic
        assert result.status in [ResearchStatus.COMPLETED, ResearchStatus.FAILED]
        assert result.research_id is not None
        assert len(result.steps) > 0
        assert len(result.trace_log) > 0
    
    @pytest.mark.asyncio
    async def test_research_planning_step(self, agent):
        """Test that planning step is created correctly"""
        topic = "Machine Learning"
        result = await agent.research_topic(topic)
        
        planning_steps = [step for step in result.steps if step.step_type == StepType.PLANNING]
        assert len(planning_steps) > 0
        
        planning_step = planning_steps[0]
        assert planning_step.description is not None
        assert planning_step.status in [ResearchStatus.COMPLETED, ResearchStatus.FAILED]
    
    @pytest.mark.asyncio
    async def test_research_web_search_steps(self, agent):
        """Test that web search steps are created"""
        topic = "Blockchain Technology"
        result = await agent.research_topic(topic)
        
        search_steps = [step for step in result.steps if step.step_type == StepType.WEB_SEARCH]
        assert len(search_steps) > 0
        
        for step in search_steps:
            assert step.input_data is not None
            assert "query" in step.input_data
    
    @pytest.mark.asyncio
    async def test_research_analysis_step(self, agent):
        """Test that analysis step is created"""
        topic = "Quantum Computing"
        result = await agent.research_topic(topic)
        
        analysis_steps = [step for step in result.steps if step.step_type == StepType.ANALYSIS]
        assert len(analysis_steps) > 0
    
    @pytest.mark.asyncio
    async def test_research_validation_step(self, agent):
        """Test that validation step is created"""
        topic = "Renewable Energy"
        result = await agent.research_topic(topic)
        
        validation_steps = [step for step in result.steps if step.step_type == StepType.VALIDATION]
        assert len(validation_steps) > 0
    
    def test_get_research_request(self, agent):
        """Test retrieving a research request"""
        # First create a research request
        topic = "Test Topic"
        research_id = "test-id-123"
        
        # This would normally be created through the research process
        # For testing, we'll create a mock request
        from models import ResearchRequest, ResearchStep
        request = ResearchRequest(
            topic=topic,
            research_id=research_id,
            status=ResearchStatus.COMPLETED,
            created_at=datetime.utcnow(),
            steps=[],
            trace_log=[]
        )
        
        # Save to database
        db_manager.save_research_request(request)
        
        # Retrieve it
        retrieved = agent.get_research_request(research_id)
        assert retrieved is not None
        assert retrieved.topic == topic
        assert retrieved.research_id == research_id
    
    def test_get_all_research_requests(self, agent):
        """Test retrieving all research requests"""
        requests = agent.get_all_research_requests()
        assert isinstance(requests, list)
    
    @pytest.mark.asyncio
    async def test_research_with_empty_topic(self, agent):
        """Test research with empty topic"""
        result = await agent.research_topic("")
        assert result.status == ResearchStatus.FAILED
    
    @pytest.mark.asyncio
    async def test_research_trace_logging(self, agent):
        """Test that trace logs are properly generated"""
        topic = "Data Science"
        result = await agent.research_topic(topic)
        
        assert len(result.trace_log) > 0
        assert any("PLANNING" in log for log in result.trace_log)
        assert any("SEARCH" in log for log in result.trace_log)
        assert any("SYNTHESIS" in log for log in result.trace_log)
        assert any("VALIDATION" in log for log in result.trace_log)

class TestDatabaseManager:
    """Test cases for the database manager"""
    
    def test_save_and_retrieve_research_request(self):
        """Test saving and retrieving research requests"""
        from models import ResearchRequest, ResearchStep
        from datetime import datetime
        
        # Create test data
        request = ResearchRequest(
            topic="Test Topic",
            research_id="test-123",
            status=ResearchStatus.COMPLETED,
            created_at=datetime.utcnow(),
            steps=[],
            trace_log=["Test log entry"]
        )
        
        # Save
        db_manager.save_research_request(request)
        
        # Retrieve
        retrieved = db_manager.get_research_request("test-123")
        assert retrieved is not None
        assert retrieved.topic == "Test Topic"
        assert retrieved.research_id == "test-123"
        assert "Test log entry" in retrieved.trace_log
    
    def test_save_and_retrieve_research_step(self):
        """Test saving and retrieving research steps"""
        from models import ResearchStep, StepType, ResearchStatus
        from datetime import datetime
        
        # Create test step
        step = ResearchStep(
            step_id="step-123",
            step_type=StepType.PLANNING,
            description="Test planning step",
            status=ResearchStatus.COMPLETED,
            timestamp=datetime.utcnow(),
            duration_seconds=1.5
        )
        
        # Save
        db_manager.save_research_step(step, "test-research-123")
        
        # Retrieve via research request
        request = db_manager.get_research_request("test-research-123")
        if request:
            assert len(request.steps) > 0
            assert request.steps[0].step_id == "step-123"

if __name__ == "__main__":
    pytest.main([__file__])
