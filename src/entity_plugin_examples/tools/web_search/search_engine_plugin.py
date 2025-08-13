"""Search engine plugin for web searches (simulated)."""

from __future__ import annotations
import json
import re
from typing import Dict, Any, Optional, List
from urllib.parse import quote_plus

from entity.plugins.tool import ToolPlugin
from entity.workflow.stages import DO


class SearchEnginePlugin(ToolPlugin):
    """
    Search engine plugin for web searches.
    
    Simulates web search results for demonstration purposes.
    In production, would integrate with real search APIs like Google, Bing, DuckDuckGo.
    """
    
    supported_stages = [DO]
    
    def __init__(self, resources: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(resources, config)
        
        config = config or {}
        self.max_results = config.get("max_results", 10)
        self.search_engine = config.get("search_engine", "duckduckgo")  # duckduckgo, google, bing
        self.safe_search = config.get("safe_search", True)
        self.language = config.get("language", "en")
        
        # Simulated search database for demo
        self.demo_results = {
            "python": [
                {"title": "Python.org", "url": "https://www.python.org", "snippet": "Official Python programming language website"},
                {"title": "Python Tutorial", "url": "https://docs.python.org/tutorial/", "snippet": "Official Python tutorial"},
                {"title": "Real Python", "url": "https://realpython.com", "snippet": "Python tutorials and articles"}
            ],
            "entity framework": [
                {"title": "Entity Framework", "url": "https://github.com/ladvien/entity", "snippet": "AI agent framework for building intelligent applications"},
                {"title": "Entity Core Documentation", "url": "https://entity-core.readthedocs.io", "snippet": "Complete documentation for Entity Framework"}
            ],
            "machine learning": [
                {"title": "scikit-learn", "url": "https://scikit-learn.org", "snippet": "Machine learning library for Python"},
                {"title": "TensorFlow", "url": "https://tensorflow.org", "snippet": "Open source machine learning framework"},
                {"title": "PyTorch", "url": "https://pytorch.org", "snippet": "Deep learning framework"}
            ]
        }
    
    async def _execute_impl(self, context) -> str:
        """Execute web search."""
        query = (context.message or "").strip()
        
        if not query:
            return "Error: Empty search query"
        
        try:
            # Parse search parameters if provided
            search_params = self._parse_search_query(query)
            
            # Perform search (simulated)
            results = self._perform_search(search_params["query"])
            
            # Format results
            return self._format_search_results(search_params["query"], results)
            
        except Exception as e:
            return f"Search Error: {str(e)}"
    
    def _parse_search_query(self, query: str) -> Dict[str, Any]:
        """Parse search query and extract parameters."""
        params = {
            "query": query,
            "limit": self.max_results,
            "language": self.language
        }
        
        # Handle special search operators
        if " site:" in query:
            parts = query.split(" site:")
            params["query"] = parts[0].strip()
            params["site"] = parts[1].strip()
        
        if " filetype:" in query:
            parts = query.split(" filetype:")
            params["query"] = parts[0].strip()
            params["filetype"] = parts[1].strip()
        
        # Handle quoted phrases
        quoted_phrases = re.findall(r'"([^"]*)"', query)
        if quoted_phrases:
            params["exact_phrases"] = quoted_phrases
        
        return params
    
    def _perform_search(self, query: str) -> List[Dict[str, str]]:
        """Perform search and return results (simulated)."""
        query_lower = query.lower()
        
        # Find matching demo results
        results = []
        
        for demo_query, demo_results in self.demo_results.items():
            if demo_query in query_lower or any(word in query_lower for word in demo_query.split()):
                results.extend(demo_results)
        
        # If no demo results found, generate generic results
        if not results:
            results = self._generate_generic_results(query)
        
        # Limit results
        return results[:self.max_results]
    
    def _generate_generic_results(self, query: str) -> List[Dict[str, str]]:
        """Generate generic search results for unknown queries."""
        encoded_query = quote_plus(query)
        
        return [
            {
                "title": f"Search results for '{query}' - Wikipedia",
                "url": f"https://en.wikipedia.org/wiki/Special:Search?search={encoded_query}",
                "snippet": f"Wikipedia articles related to {query}"
            },
            {
                "title": f"{query} - Stack Overflow",
                "url": f"https://stackoverflow.com/search?q={encoded_query}",
                "snippet": f"Programming questions and answers about {query}"
            },
            {
                "title": f"{query} - GitHub",
                "url": f"https://github.com/search?q={encoded_query}",
                "snippet": f"Open source projects related to {query}"
            }
        ]
    
    def _format_search_results(self, query: str, results: List[Dict[str, str]]) -> str:
        """Format search results for display."""
        if not results:
            return f"No results found for '{query}'"
        
        output = [f"Search results for '{query}' ({len(results)} results):\n"]
        
        for i, result in enumerate(results, 1):
            output.append(f"{i}. **{result['title']}**")
            output.append(f"   {result['url']}")
            output.append(f"   {result['snippet']}\n")
        
        return "\n".join(output)
    
    def search_with_filters(self, query: str, **filters) -> str:
        """Search with additional filters."""
        # Apply filters like site:, filetype:, date range, etc.
        filtered_query = query
        
        if "site" in filters:
            filtered_query += f" site:{filters['site']}"
        
        if "filetype" in filters:
            filtered_query += f" filetype:{filters['filetype']}"
        
        if "exclude" in filters:
            for term in filters["exclude"]:
                filtered_query += f" -{term}"
        
        return filtered_query
    
    def get_search_suggestions(self, partial_query: str) -> List[str]:
        """Get search suggestions for partial query."""
        suggestions = []
        partial_lower = partial_query.lower()
        
        # Check demo queries for matches
        for demo_query in self.demo_results.keys():
            if demo_query.startswith(partial_lower):
                suggestions.append(demo_query)
        
        # Add common programming-related suggestions
        common_terms = [
            "python tutorial", "machine learning", "web development",
            "data science", "artificial intelligence", "software engineering",
            "javascript", "react", "node.js", "docker", "kubernetes"
        ]
        
        for term in common_terms:
            if term.startswith(partial_lower) and term not in suggestions:
                suggestions.append(term)
        
        return suggestions[:5]  # Limit to 5 suggestions


# Example usage:
"""
search = SearchEnginePlugin(resources={}, config={
    "max_results": 5,
    "search_engine": "duckduckgo",
    "safe_search": True
})

# Basic search
await search._execute_impl(Mock(message="python programming"))

# Search with site filter
await search._execute_impl(Mock(message="entity framework site:github.com"))

# Search with filetype filter
await search._execute_impl(Mock(message="machine learning filetype:pdf"))

# Get suggestions
suggestions = search.get_search_suggestions("python")
# Returns: ['python tutorial', 'python programming', ...]

# Advanced search with filters
filtered_query = search.search_with_filters(
    "machine learning",
    site="arxiv.org",
    filetype="pdf",
    exclude=["beginner", "introduction"]
)
"""