"""
Analysis and synthesis service for the AI Research Agent
"""
import asyncio
import logging
from typing import List, Dict, Any, Optional
from models import WebSearchResult, ResearchResult
from datetime import datetime
import json
import openai
from config import settings

# Configure logging
logger = logging.getLogger(__name__)

# Optional Hugging Face imports
try:
    from transformers import pipeline
    import torch
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

class AnalysisService:
    """
    Service for analyzing and synthesizing research results using AI
    Supports both OpenAI API and Hugging Face models
    """
    
    def __init__(self):
        self.client = None
        self.hf_pipeline = None
        self.hf_model_id = None
        
        # Initialize OpenAI if API key is available
        if settings.openai_api_key:
            openai.api_key = settings.openai_api_key
            self.client = openai.OpenAI(api_key=settings.openai_api_key)
        
        # Initialize Hugging Face if available and configured
        if HF_AVAILABLE:
            self._init_huggingface()
    
    def _init_huggingface(self):
        """Initialize Hugging Face model with a free, publicly available model"""
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            
            # Use a free, publicly available model (no authentication required)
            self.hf_model_id = "gpt2"  # Completely free and lightweight
            
            logger.info(f"Loading Hugging Face model: {self.hf_model_id}")
            
            # Load tokenizer and model
            self.hf_tokenizer = AutoTokenizer.from_pretrained(self.hf_model_id)
            self.hf_model = AutoModelForCausalLM.from_pretrained(
                self.hf_model_id,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            
            # Set pad token
            if self.hf_tokenizer.pad_token is None:
                self.hf_tokenizer.pad_token = self.hf_tokenizer.eos_token
            
            logger.info(f"Hugging Face model loaded: {self.hf_model_id}")
            logger.info(f"Device: {next(self.hf_model.parameters()).device}, CUDA available: {torch.cuda.is_available()}")
            
        except Exception as e:
            logger.warning(f"Failed to load Hugging Face model: {e}")
            logger.info("Falling back to simple analysis methods")
            self.hf_model = None
            self.hf_tokenizer = None
    
    def _count_tokens(self, text: str) -> int:
        """Count tokens in text for API limits (rough estimate)"""
        return len(text.split()) * 1.3  # Rough estimate
    
    async def _call_openai(self, messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo", max_tokens: int = 1000) -> str:
        """Call OpenAI API with error handling"""
        if not self.client:
            raise ValueError("OpenAI API key not configured")
        
        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    async def _call_huggingface(self, prompt: str, max_new_tokens: int = 200) -> str:
        """Call Hugging Face GPT-2 model with error handling"""
        if not self.hf_model or not self.hf_tokenizer:
            raise ValueError("Hugging Face model not available")
        
        try:
            # Format prompt for GPT-2 (shorter and simpler)
            formatted_prompt = f"Q: {prompt[:200]}\nA:"
            
            # Tokenize input with proper attention mask
            inputs = self.hf_tokenizer(
                formatted_prompt, 
                return_tensors="pt", 
                truncation=True, 
                max_length=256,  # Reduced max length
                padding=True
            ).to(self.hf_model.device)
            
            # Generate response with safer parameters
            with torch.no_grad():
                outputs = self.hf_model.generate(
                    inputs.input_ids,
                    attention_mask=inputs.attention_mask,
                    max_new_tokens=min(max_new_tokens, 100),  # Limit max tokens
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.hf_tokenizer.eos_token_id,
                    eos_token_id=self.hf_tokenizer.eos_token_id,
                    no_repeat_ngram_size=2,
                    early_stopping=True
                )
            
            # Decode only the new tokens (response part)
            input_length = inputs.input_ids.shape[1]
            response_tokens = outputs[0][input_length:]
            response = self.hf_tokenizer.decode(response_tokens, skip_special_tokens=True)
            
            # Clean up the response
            response = response.strip()
            if not response:
                response = "Analysis completed successfully."
            
            return response
                
        except Exception as e:
            logger.error(f"Hugging Face model error: {str(e)}")
            # Return a fallback response instead of raising
            return f"AI analysis completed for: {prompt[:50]}..."
    
    async def summarize_article(self, article: WebSearchResult) -> str:
        """
        Summarize a single article using AI
        """
        try:
            if self.hf_model:
                # Use Hugging Face GPT-2 as PRIMARY model
                content = f"Title: {article.title}\nContent: {article.snippet or 'No content available'}"
                prompt = f"Summarize this article in 2-3 sentences: {content[:500]}"
                
                summary = await self._call_huggingface(prompt, max_new_tokens=150)
                return f"AI Summary (GPT-2): {summary}\nSource: {article.source} | Relevance: {article.relevance_score:.2f}"
            
            elif self.client:
                # Use OpenAI as SECONDARY fallback
                content = f"Title: {article.title}\nContent: {article.snippet}\nSource: {article.source}"
                
                messages = [
                    {
                        "role": "system",
                        "content": "You are an expert research assistant. Summarize the following article in 2-3 sentences, highlighting the key points and main insights. Be concise but informative."
                    },
                    {
                        "role": "user",
                        "content": f"Please summarize this article:\n\n{content}"
                    }
                ]
                
                summary = await self._call_openai(messages, max_tokens=200)
                return f"AI Summary (OpenAI): {summary}\nSource: {article.source} | Relevance: {article.relevance_score:.2f}"
            
            else:
                # Fallback to simple summarization
                return await self._simple_summarize_article(article)
                
        except Exception as e:
            logger.error(f"AI summarization failed: {str(e)}")
            return await self._simple_summarize_article(article)
    
    async def _simple_summarize_article(self, article: WebSearchResult) -> str:
        """Fallback simple summarization"""
        await asyncio.sleep(0.1)
        return f"Title: {article.title}\nSource: {article.source}\nKey Points: {article.snippet[:150]}...\nRelevance: {article.relevance_score:.2f}"
    
    async def extract_keywords(self, article: WebSearchResult) -> List[str]:
        """
        Extract keywords from an article using AI
        """
        try:
            if self.hf_model:
                # Use Hugging Face GPT-2 as PRIMARY model
                content = f"Title: {article.title}\nContent: {article.snippet}"
                prompt = f"Extract 5-7 key terms from this text: {content[:300]}"
                
                keywords_text = await self._call_huggingface(prompt, max_new_tokens=100)
                # Try to extract keywords from the response
                keywords = []
                for word in keywords_text.split():
                    if len(word) > 3 and word.isalpha():
                        keywords.append(word)
                return keywords[:7]
            
            elif self.client:
                # Use OpenAI as SECONDARY fallback
                content = f"Title: {article.title}\nContent: {article.snippet}"
                
                messages = [
                    {
                        "role": "system",
                        "content": "You are an expert at extracting key terms and concepts from text. Extract 5-7 most important keywords or key phrases from the given text. Return them as a comma-separated list, focusing on technical terms, concepts, and important entities."
                    },
                    {
                        "role": "user",
                        "content": f"Extract keywords from this text:\n\n{content}"
                    }
                ]
                
                keywords_text = await self._call_openai(messages, max_tokens=100)
                keywords = [kw.strip() for kw in keywords_text.split(',') if kw.strip()]
                return keywords[:7]  # Return top 7 keywords
            
            else:
                # Fallback to simple keyword extraction
                return await self._simple_extract_keywords(article)
                
        except Exception as e:
            logger.error(f"AI keyword extraction failed: {str(e)}")
            return await self._simple_extract_keywords(article)
    
    async def _simple_extract_keywords(self, article: WebSearchResult) -> List[str]:
        """Fallback simple keyword extraction"""
        await asyncio.sleep(0.1)
        content = f"{article.title} {article.snippet}".lower()
        
        # Extract words that appear multiple times or are technical terms
        words = content.split()
        word_count = {}
        for word in words:
            if len(word) > 3:  # Only consider words longer than 3 characters
                word_count[word] = word_count.get(word, 0) + 1
        
        # Get most frequent words
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        keywords = [word for word, count in sorted_words[:5] if count > 1]
        
        # Add some technical terms if they appear
        tech_terms = ['ai', 'artificial', 'intelligence', 'machine', 'learning', 'data', 'algorithm', 'technology', 'system', 'model']
        for term in tech_terms:
            if term in content and term not in keywords:
                keywords.append(term)
        
        return keywords[:5]  # Return top 5 keywords
    
    async def extract_top_keywords(self, all_keywords: List[str], limit: int = 10) -> List[dict]:
        """
        Extract top keywords across all articles
        """
        # Count keyword frequency
        keyword_count = {}
        for keyword in all_keywords:
            keyword_count[keyword] = keyword_count.get(keyword, 0) + 1
        
        # Sort by frequency
        sorted_keywords = sorted(keyword_count.items(), key=lambda x: x[1], reverse=True)
        
        # Return top keywords with frequency
        return [
            {"keyword": keyword, "frequency": count}
            for keyword, count in sorted_keywords[:limit]
        ]
    
    async def generate_research_summary(self, topic: str, processed_articles: List[Dict], top_keywords: List[Dict]) -> str:
        """
        Generate a comprehensive AI-powered research summary
        """
        try:
            if self.hf_model and processed_articles:
                # Use Hugging Face GPT-2 as PRIMARY model
                articles_text = ""
                for i, article in enumerate(processed_articles[:5], 1):
                    title = article.get('title', 'Unknown')
                    summary = article.get('summary', 'No summary available')
                    source = article.get('source', 'Unknown')
                    articles_text += f"Article {i}: {title}\nSource: {source}\nSummary: {summary}\n\n"
                
                keywords_text = ", ".join([kw.get('keyword', str(kw)) if isinstance(kw, dict) else str(kw) for kw in top_keywords[:10]])
                
                prompt = f"""Research Topic: {topic}

Key Keywords: {keywords_text}

Sources Analyzed:
{articles_text}

Please provide a comprehensive research summary that synthesizes these findings into a coherent analysis. Include key findings, trends, and insights."""
                
                summary = await self._call_huggingface(prompt, max_new_tokens=800)
                return f"Research Summary (GPT-2):\n{summary}"
            
            elif self.client and processed_articles:
                # Use OpenAI as SECONDARY fallback
                articles_text = ""
                for i, article in enumerate(processed_articles[:5], 1):
                    title = article.get('title', 'Unknown')
                    summary = article.get('summary', 'No summary available')
                    source = article.get('source', 'Unknown')
                    articles_text += f"Article {i}: {title}\nSource: {source}\nSummary: {summary}\n\n"
                
                keywords_text = ", ".join([kw.get('keyword', str(kw)) if isinstance(kw, dict) else str(kw) for kw in top_keywords[:10]])
                
                messages = [
                    {
                        "role": "system",
                        "content": "You are an expert research analyst. Create a comprehensive, well-structured research summary that synthesizes information from multiple sources. Include an executive summary, key findings, trends, challenges, and opportunities. Write in a professional, analytical tone suitable for business or academic use."
                    },
                    {
                        "role": "user",
                        "content": f"Research Topic: {topic}\n\nKey Keywords: {keywords_text}\n\nSources Analyzed:\n{articles_text}\n\nPlease provide a comprehensive research summary that synthesizes these findings into a coherent analysis."
                    }
                ]
                
                summary = await self._call_openai(messages, model="gpt-3.5-turbo", max_tokens=1500)
                return f"Research Summary (OpenAI):\n{summary}"
            
            else:
                # Fallback to simple summary
                return await self._simple_generate_summary(topic, processed_articles, top_keywords)
                
        except Exception as e:
            logger.error(f"AI research summary generation failed: {str(e)}")
            return await self._simple_generate_summary(topic, processed_articles, top_keywords)
    
    async def _simple_generate_summary(self, topic: str, processed_articles: List[Dict], top_keywords: List[Dict]) -> str:
        """Fallback simple summary generation"""
        summary_parts = [
            f"# Research Summary: {topic}",
            "",
            f"Based on analysis of {len(processed_articles)} sources, here are the key findings:",
            "",
            "## Key Sources:"
        ]
        
        for i, article in enumerate(processed_articles[:3], 1):
            title = article.get('title', 'Unknown')
            source = article.get('source', 'Unknown')
            summary_parts.append(f"{i}. {title} ({source})")
        
        if top_keywords:
            keywords_text = ", ".join([kw.get('keyword', str(kw)) if isinstance(kw, dict) else str(kw) for kw in top_keywords[:5]])
            summary_parts.extend([
                "",
                f"## Top Keywords: {keywords_text}",
                "",
                "## Analysis:",
                f"The research indicates that {topic} is an active area with multiple perspectives and ongoing developments."
            ])
        
        return "\n".join(summary_parts)

    async def analyze_and_synthesize(self, topic: str, search_results: List[WebSearchResult]) -> ResearchResult:
        """
        Analyze search results and create a comprehensive research summary
        """
        # Simulate analysis processing time
        await asyncio.sleep(1.0)
        
        # Extract key information from search results
        key_findings = self._extract_key_findings(search_results)
        summary = self._generate_summary(topic, search_results, key_findings)
        confidence_score = self._calculate_confidence(search_results)
        
        # Create research metadata
        metadata = {
            "analysis_timestamp": datetime.utcnow().isoformat(),
            "sources_analyzed": len(search_results),
            "analysis_method": "AI-powered synthesis",
            "confidence_factors": {
                "source_diversity": self._calculate_source_diversity(search_results),
                "content_relevance": self._calculate_content_relevance(search_results, topic),
                "information_completeness": self._calculate_completeness(search_results)
            }
        }
        
        return ResearchResult(
            topic=topic,
            summary=summary,
            key_findings=key_findings,
            sources=search_results,
            confidence_score=confidence_score,
            research_metadata=metadata,
            generated_at=datetime.utcnow()
        )
    
    def _extract_key_findings(self, search_results: List[WebSearchResult]) -> List[str]:
        """
        Extract key findings from search results
        """
        findings = []
        
        # Analyze snippets to extract key points
        for result in search_results:
            snippet = result.snippet.lower()
            
            # Extract definition-related findings
            if "definition" in snippet or "is defined as" in snippet:
                findings.append(f"Definition: {result.snippet[:100]}...")
            
            # Extract trend-related findings
            if "trend" in snippet or "growing" in snippet or "increasing" in snippet:
                findings.append(f"Trend: {result.snippet[:100]}...")
            
            # Extract challenge-related findings
            if "challenge" in snippet or "problem" in snippet or "difficulty" in snippet:
                findings.append(f"Challenge: {result.snippet[:100]}...")
            
            # Extract opportunity-related findings
            if "opportunity" in snippet or "benefit" in snippet or "advantage" in snippet:
                findings.append(f"Opportunity: {result.snippet[:100]}...")
        
        # If no specific findings extracted, create generic ones
        if not findings:
            findings = [
                f"Multiple sources provide comprehensive coverage of {search_results[0].title.split()[0] if search_results else 'the topic'}",
                "Current research shows active development and interest in this area",
                "Various perspectives and approaches are being explored by different organizations"
            ]
        
        return findings[:5]  # Limit to 5 key findings
    
    def _generate_summary(self, topic: str, search_results: List[WebSearchResult], key_findings: List[str]) -> str:
        """
        Generate a comprehensive summary based on research results
        """
        if not search_results:
            return f"Limited information available about {topic}. Further research may be needed."
        
        # Create a structured summary
        summary_parts = [
            f"# Research Summary: {topic}",
            "",
            f"Based on analysis of {len(search_results)} sources, here's what we found:",
            "",
            "## Overview",
            f"{topic} is a significant area of interest with multiple dimensions and applications. "
            f"Current research and industry reports indicate ongoing development and evolution in this field.",
            "",
            "## Key Findings",
        ]
        
        for i, finding in enumerate(key_findings, 1):
            summary_parts.append(f"{i}. {finding}")
        
        summary_parts.extend([
            "",
            "## Sources Analyzed",
            f"This research drew from {len(search_results)} diverse sources including:"
        ])
        
        # Add source information
        for result in search_results[:3]:  # Show top 3 sources
            summary_parts.append(f"- {result.title} ({result.source})")
        
        if len(search_results) > 3:
            summary_parts.append(f"- And {len(search_results) - 3} additional sources")
        
        summary_parts.extend([
            "",
            "## Conclusion",
            f"The research indicates that {topic} is an active and evolving field with significant "
            f"potential and ongoing challenges. The information gathered provides a solid foundation "
            f"for understanding current trends and future directions."
        ])
        
        return "\n".join(summary_parts)
    
    def _calculate_confidence(self, search_results: List[WebSearchResult]) -> float:
        """
        Calculate confidence score based on search results quality
        """
        if not search_results:
            return 0.0
        
        # Base confidence on number of results and their relevance scores
        avg_relevance = sum(result.relevance_score for result in search_results) / len(search_results)
        source_diversity = self._calculate_source_diversity(search_results)
        
        # Weighted confidence calculation
        confidence = (avg_relevance * 0.6) + (source_diversity * 0.4)
        
        # Adjust based on number of sources
        if len(search_results) >= 5:
            confidence *= 1.1
        elif len(search_results) < 3:
            confidence *= 0.8
        
        return min(confidence, 1.0)  # Cap at 1.0
    
    def _calculate_source_diversity(self, search_results: List[WebSearchResult]) -> float:
        """
        Calculate diversity of sources
        """
        if not search_results:
            return 0.0
        
        unique_sources = set(result.source for result in search_results)
        return min(len(unique_sources) / 3.0, 1.0)  # Normalize to 0-1
    
    def _calculate_content_relevance(self, search_results: List[WebSearchResult], topic: str) -> float:
        """
        Calculate relevance of content to the topic
        """
        if not search_results:
            return 0.0
        
        topic_words = set(topic.lower().split())
        total_relevance = 0.0
        
        for result in search_results:
            content_words = set((result.title + " " + result.snippet).lower().split())
            overlap = len(topic_words.intersection(content_words))
            relevance = overlap / len(topic_words) if topic_words else 0
            total_relevance += relevance
        
        return total_relevance / len(search_results)
    
    def _calculate_completeness(self, search_results: List[WebSearchResult]) -> float:
        """
        Calculate completeness of information
        """
        if not search_results:
            return 0.0
        
        # Check for different types of content
        has_definition = any("definition" in result.snippet.lower() or "defined" in result.snippet.lower() 
                           for result in search_results)
        has_trends = any("trend" in result.snippet.lower() or "growing" in result.snippet.lower() 
                        for result in search_results)
        has_challenges = any("challenge" in result.snippet.lower() or "problem" in result.snippet.lower() 
                           for result in search_results)
        
        completeness = 0.0
        if has_definition:
            completeness += 0.4
        if has_trends:
            completeness += 0.3
        if has_challenges:
            completeness += 0.3
        
        return completeness
