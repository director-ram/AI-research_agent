"""
Logging system for the AI Research Agent
"""
import logging
import sys
from datetime import datetime
from typing import Optional
from config import settings

class AgentLogger:
    """
    Centralized logging system for the AI Research Agent
    """
    
    def __init__(self):
        self.logger = logging.getLogger("ai_research_agent")
        self.logger.setLevel(getattr(logging, settings.log_level.upper()))
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        
        # File handler
        file_handler = logging.FileHandler(settings.log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        # Add handlers if not already added
        if not self.logger.handlers:
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
    
    def log(self, message: str, research_id: Optional[str] = None, level: str = "INFO"):
        """
        Log a message with optional research ID
        """
        if research_id:
            message = f"[{research_id}] {message}"
        
        log_level = getattr(logging, level.upper())
        self.logger.log(log_level, message)
    
    def log_step_start(self, step_name: str, research_id: str, details: Optional[str] = None):
        """
        Log the start of a research step
        """
        message = f"Starting step: {step_name}"
        if details:
            message += f" - {details}"
        self.log(message, research_id, "INFO")
    
    def log_step_complete(self, step_name: str, research_id: str, duration: float, details: Optional[str] = None):
        """
        Log the completion of a research step
        """
        message = f"Completed step: {step_name} (took {duration:.2f}s)"
        if details:
            message += f" - {details}"
        self.log(message, research_id, "INFO")
    
    def log_step_error(self, step_name: str, research_id: str, error: str):
        """
        Log an error in a research step
        """
        message = f"Error in step: {step_name} - {error}"
        self.log(message, research_id, "ERROR")
    
    def log_research_start(self, topic: str, research_id: str):
        """
        Log the start of a research session
        """
        message = f"Starting research for topic: {topic}"
        self.log(message, research_id, "INFO")
    
    def log_research_complete(self, topic: str, research_id: str, duration: float, success: bool = True):
        """
        Log the completion of a research session
        """
        status = "completed successfully" if success else "failed"
        message = f"Research {status} for topic: {topic} (took {duration:.2f}s)"
        self.log(message, research_id, "INFO" if success else "ERROR")
    
    def log_decision(self, decision: str, reasoning: str, research_id: str):
        """
        Log a decision made by the agent
        """
        message = f"Decision: {decision} - Reasoning: {reasoning}"
        self.log(message, research_id, "DEBUG")
    
    def log_external_api_call(self, api_name: str, endpoint: str, research_id: str, success: bool = True):
        """
        Log external API calls
        """
        status = "successful" if success else "failed"
        message = f"API call to {api_name} ({endpoint}) {status}"
        self.log(message, research_id, "INFO" if success else "WARNING")
    
    def get_logs_for_research(self, research_id: str) -> list:
        """
        Get all logs for a specific research session
        """
        # This would typically read from the log file and filter by research_id
        # For simplicity, we'll return a placeholder
        return [f"Logs for research {research_id} would be retrieved here"]
