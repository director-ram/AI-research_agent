"""
Analysis and synthesis service for the AI Research Agent
"""
import asyncio
from typing import List, Dict, Any
from models import WebSearchResult, ResearchResult
from datetime import datetime
import json

class AnalysisService:
    """
    Service for analyzing and synthesizing research results
    """
    
    def __init__(self):
        pass
    
    async def summarize_article(self, article: WebSearchResult) -> str:
        """
        Summarize a single article
        """
        # Simulate AI-powered summarization
        await asyncio.sleep(0.2)  # Simulate processing time
        
        # Extract key points from the article
        content = f"{article.title} {article.snippet}"
        words = content.lower().split()
        
        # Simple extractive summarization
        summary_parts = [
            f"Title: {article.title}",
            f"Source: {article.source}",
            f"Key Points: {article.snippet[:150]}...",
            f"Relevance Score: {article.relevance_score:.2f}"
        ]
        
        return "\n".join(summary_parts)
    
    async def extract_keywords(self, article: WebSearchResult) -> List[str]:
        """
        Extract keywords from an article
        """
        # Simulate keyword extraction
        await asyncio.sleep(0.1)
        
        # Simple keyword extraction based on content
        content = f"{article.title} {article.snippet}".lower()
        
        # Common technical terms and important words
        keywords = []
        
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
