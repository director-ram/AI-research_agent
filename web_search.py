"""
Web search service for the AI Research Agent
"""
import requests
import asyncio
from typing import List, Dict, Any
from models import WebSearchResult
from config import settings
import json

class WebSearchService:
    """
    Service for performing web searches and processing results
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AI Research Agent 1.0'
        })
    
    async def search(self, query: str, num_results: int = 5) -> List[WebSearchResult]:
        """
        Perform web search and return structured results
        """
        try:
            # In production, this would use a real search API like SerpAPI or Google Custom Search
            # For demo purposes, we'll simulate search results
            return await self._simulate_search(query, num_results)
            
        except Exception as e:
            print(f"Search error for query '{query}': {str(e)}")
            return []
    
    async def fetch_wikipedia_articles(self, topic: str) -> List[WebSearchResult]:
        """
        Fetch articles from Wikipedia API
        """
        try:
            # Wikipedia API implementation
            import requests
            import urllib.parse
            
            # Search Wikipedia for the topic
            search_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
            encoded_topic = urllib.parse.quote(topic)
            
            response = self.session.get(f"{search_url}{encoded_topic}")
            
            if response.status_code == 200:
                data = response.json()
                if 'title' in data and 'extract' in data:
                    return [WebSearchResult(
                        title=data['title'],
                        url=data['content_urls']['desktop']['page'],
                        snippet=data['extract'][:200] + "...",
                        relevance_score=0.9,
                        source="Wikipedia"
                    )]
            
            # Fallback to search API
            search_url = "https://en.wikipedia.org/w/api.php"
            params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': topic,
                'srlimit': 3
            }
            
            response = self.session.get(search_url, params=params)
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data.get('query', {}).get('search', [])[:3]:
                    results.append(WebSearchResult(
                        title=item['title'],
                        url=f"https://en.wikipedia.org/wiki/{urllib.parse.quote(item['title'])}",
                        snippet=item['snippet'],
                        relevance_score=0.8,
                        source="Wikipedia"
                    ))
                return results
            
            return []
            
        except Exception as e:
            print(f"Wikipedia API error for topic '{topic}': {str(e)}")
            return []
    
    async def fetch_news_articles(self, topic: str) -> List[WebSearchResult]:
        """
        Fetch articles from NewsAPI (requires API key)
        """
        try:
            from config import settings
            
            if not settings.newsapi_key:
                # Return mock data if no API key
                return await self._mock_news_articles(topic)
            
            # NewsAPI implementation
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': topic,
                'apiKey': settings.newsapi_key,
                'pageSize': 5,
                'sortBy': 'relevancy'
            }
            
            response = self.session.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                results = []
                for article in data.get('articles', [])[:5]:
                    results.append(WebSearchResult(
                        title=article['title'],
                        url=article['url'],
                        snippet=article['description'] or article['content'][:200] + "...",
                        relevance_score=0.85,
                        source=article['source']['name']
                    ))
                return results
            
            return []
            
        except Exception as e:
            print(f"NewsAPI error for topic '{topic}': {str(e)}")
            return await self._mock_news_articles(topic)
    
    async def fetch_hackernews_articles(self, topic: str) -> List[WebSearchResult]:
        """
        Fetch articles from HackerNews API
        """
        try:
            # HackerNews API implementation
            search_url = "https://hn.algolia.com/api/v1/search"
            params = {
                'query': topic,
                'tags': 'story',
                'hitsPerPage': 5
            }
            
            response = self.session.get(search_url, params=params)
            if response.status_code == 200:
                data = response.json()
                results = []
                for hit in data.get('hits', [])[:5]:
                    results.append(WebSearchResult(
                        title=hit['title'],
                        url=hit['url'] if hit['url'] else f"https://news.ycombinator.com/item?id={hit['objectID']}",
                        snippet=hit.get('story_text', hit.get('comment_text', ''))[:200] + "...",
                        relevance_score=0.7,
                        source="HackerNews"
                    ))
                return results
            
            return []
            
        except Exception as e:
            print(f"HackerNews API error for topic '{topic}': {str(e)}")
            return []
    
    async def _mock_news_articles(self, topic: str) -> List[WebSearchResult]:
        """
        Mock news articles for demo purposes
        """
        return [
            WebSearchResult(
                title=f"Latest News: {topic}",
                url=f"https://news.example.com/{topic.replace(' ', '-')}",
                snippet=f"Breaking news about {topic} and its impact on the industry.",
                relevance_score=0.8,
                source="Tech News"
            ),
            WebSearchResult(
                title=f"{topic} Trends in 2024",
                url=f"https://trends.example.com/{topic.replace(' ', '-')}",
                snippet=f"Analysis of current trends and developments in {topic}.",
                relevance_score=0.75,
                source="Industry Report"
            )
        ]
    
    async def _simulate_search(self, query: str, num_results: int) -> List[WebSearchResult]:
        """
        Simulate web search results for demo purposes
        """
        # Simulate API delay
        await asyncio.sleep(0.5)
        
        # Generate realistic mock results based on query
        mock_results = []
        
        # Different result templates based on query type
        if "definition" in query.lower():
            mock_results = [
                WebSearchResult(
                    title=f"Definition of {query.split()[0]} - Wikipedia",
                    url=f"https://en.wikipedia.org/wiki/{query.split()[0].replace(' ', '_')}",
                    snippet=f"A comprehensive definition of {query.split()[0]} including its origins, characteristics, and applications in various fields.",
                    relevance_score=0.95,
                    source="Wikipedia"
                ),
                WebSearchResult(
                    title=f"What is {query.split()[0]}? - Expert Guide",
                    url=f"https://example.com/guide/{query.split()[0].replace(' ', '-')}",
                    snippet=f"An expert guide explaining {query.split()[0]} with detailed examples and use cases.",
                    relevance_score=0.88,
                    source="Expert Guide"
                )
            ]
        elif "trends" in query.lower():
            mock_results = [
                WebSearchResult(
                    title=f"{query.split()[0]} Trends 2024 - Industry Report",
                    url=f"https://industry-report.com/{query.split()[0].replace(' ', '-')}-trends-2024",
                    snippet=f"Latest trends and developments in {query.split()[0]} for 2024, including market analysis and future predictions.",
                    relevance_score=0.92,
                    source="Industry Report"
                ),
                WebSearchResult(
                    title=f"Emerging Trends in {query.split()[0]} - Tech News",
                    url=f"https://technews.com/trends/{query.split()[0].replace(' ', '-')}",
                    snippet=f"Breaking news about emerging trends in {query.split()[0]} and their impact on the industry.",
                    relevance_score=0.85,
                    source="Tech News"
                )
            ]
        elif "challenges" in query.lower():
            mock_results = [
                WebSearchResult(
                    title=f"Challenges in {query.split()[0]} - Research Paper",
                    url=f"https://research.org/papers/{query.split()[0].replace(' ', '-')}-challenges",
                    snippet=f"Academic research on the main challenges facing {query.split()[0]} and potential solutions.",
                    relevance_score=0.90,
                    source="Academic Research"
                ),
                WebSearchResult(
                    title=f"Overcoming {query.split()[0]} Challenges - Best Practices",
                    url=f"https://bestpractices.com/{query.split()[0].replace(' ', '-')}-challenges",
                    snippet=f"Practical guide to overcoming common challenges in {query.split()[0]} implementation.",
                    relevance_score=0.82,
                    source="Best Practices Guide"
                )
            ]
        else:
            # Generic results
            mock_results = [
                WebSearchResult(
                    title=f"Complete Guide to {query}",
                    url=f"https://guide.com/{query.replace(' ', '-')}",
                    snippet=f"A comprehensive guide covering all aspects of {query} with practical examples and insights.",
                    relevance_score=0.87,
                    source="Guide Website"
                ),
                WebSearchResult(
                    title=f"{query} - Overview and Analysis",
                    url=f"https://analysis.com/{query.replace(' ', '-')}",
                    snippet=f"Detailed analysis of {query} including current state, trends, and future outlook.",
                    relevance_score=0.84,
                    source="Analysis Site"
                ),
                WebSearchResult(
                    title=f"Latest News on {query}",
                    url=f"https://news.com/{query.replace(' ', '-')}",
                    snippet=f"Recent news and updates about {query} from industry experts and thought leaders.",
                    relevance_score=0.79,
                    source="News Site"
                )
            ]
        
        # Return requested number of results
        return mock_results[:num_results]
    
    async def _real_search(self, query: str, num_results: int) -> List[WebSearchResult]:
        """
        Real web search implementation (requires API key)
        """
        if not settings.serpapi_key:
            raise ValueError("SerpAPI key not configured")
        
        # SerpAPI implementation
        params = {
            'q': query,
            'api_key': settings.serpapi_key,
            'num': num_results,
            'engine': 'google'
        }
        
        response = self.session.get('https://serpapi.com/search', params=params)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        for result in data.get('organic_results', []):
            web_result = WebSearchResult(
                title=result.get('title', ''),
                url=result.get('link', ''),
                snippet=result.get('snippet', ''),
                relevance_score=1.0,  # SerpAPI doesn't provide relevance scores
                source=self._extract_source(result.get('link', ''))
            )
            results.append(web_result)
        
        return results
    
    def _extract_source(self, url: str) -> str:
        """
        Extract source name from URL
        """
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            return domain.replace('www.', '').split('.')[0].title()
        except:
            return "Unknown"
