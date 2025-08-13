"""Web scraper plugin for extracting content from web pages (simulated)."""

from __future__ import annotations
import re
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse, urljoin

from entity.plugins.tool import ToolPlugin
from entity.workflow.stages import DO


class WebScraperPlugin(ToolPlugin):
    """
    Web scraper plugin for extracting content from web pages.
    
    Features:
    - Extract text content from HTML (simulated)
    - Extract specific elements (titles, headers, links, images)
    - Handle different content types
    - Respect robots.txt (in production)
    - Rate limiting and polite scraping
    """
    
    supported_stages = [DO]
    
    def __init__(self, resources: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(resources, config)
        
        config = config or {}
        self.max_content_length = config.get("max_content_length", 10000)
        self.extract_links = config.get("extract_links", True)
        self.extract_images = config.get("extract_images", False)
        self.follow_redirects = config.get("follow_redirects", True)
        self.timeout = config.get("timeout", 30)
        self.user_agent = config.get("user_agent", "Entity Framework Web Scraper 1.0")
        
        # Simulated content database for demo
        self.demo_content = {
            "https://www.python.org": {
                "title": "Welcome to Python.org",
                "content": "Python is a programming language that lets you work quickly and integrate systems more effectively.",
                "headers": ["Welcome to Python.org", "Python Software Foundation", "Getting Started"],
                "links": ["https://docs.python.org", "https://pypi.org", "https://www.python.org/downloads"],
                "meta": {"description": "The official home of the Python Programming Language", "keywords": "python, programming, language"}
            },
            "https://github.com/ladvien/entity": {
                "title": "Entity Framework - GitHub",
                "content": "AI agent framework for building intelligent applications with a plugin-based architecture.",
                "headers": ["Entity Framework", "Features", "Installation", "Quick Start"],
                "links": ["https://entity-core.readthedocs.io", "https://github.com/ladvien/entity/issues"],
                "meta": {"description": "AI agent framework", "keywords": "ai, agents, framework, python"}
            },
            "https://docs.python.org": {
                "title": "Python Documentation",
                "content": "Python is an easy to learn, powerful programming language. It has efficient high-level data structures.",
                "headers": ["Python Documentation", "Tutorial", "Library Reference", "Language Reference"],
                "links": ["https://docs.python.org/tutorial/", "https://docs.python.org/library/"],
                "meta": {"description": "Python documentation", "keywords": "python, documentation, tutorial"}
            }
        }
    
    async def _execute_impl(self, context) -> str:
        """Scrape content from a web page."""
        url = (context.message or "").strip()
        
        if not url:
            return "Error: No URL provided for scraping"
        
        try:
            # Validate URL
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                return f"Error: Invalid URL format: {url}"
            
            # Scrape content (simulated)
            scraped_data = self._scrape_url(url)
            
            if not scraped_data:
                return f"Error: Could not scrape content from {url}"
            
            # Format results
            return self._format_scraped_content(url, scraped_data)
            
        except Exception as e:
            return f"Web Scraping Error: {str(e)}"
    
    def _scrape_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Scrape content from URL (simulated)."""
        # Check if we have demo content for this URL
        if url in self.demo_content:
            return self.demo_content[url]
        
        # Generate simulated content for unknown URLs
        return self._generate_simulated_content(url)
    
    def _generate_simulated_content(self, url: str) -> Dict[str, Any]:
        """Generate simulated content for demonstration."""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path
        
        # Generate content based on domain patterns
        if "github.com" in domain:
            title = f"GitHub Repository - {path.split('/')[-1] if path else 'Repository'}"
            content = "Open source repository with code, issues, documentation and collaboration features."
            headers = ["README", "Code", "Issues", "Pull Requests"]
            
        elif "stackoverflow.com" in domain:
            title = "Stack Overflow - Programming Q&A"
            content = "Programming questions and answers from the developer community."
            headers = ["Questions", "Answers", "Tags", "Users"]
            
        elif "wikipedia.org" in domain:
            title = f"Wikipedia Article - {path.split('/')[-1].replace('_', ' ') if path else 'Article'}"
            content = "Encyclopedia article with comprehensive information and references."
            headers = ["Contents", "References", "External Links"]
            
        elif "readthedocs.io" in domain or "docs." in domain:
            title = "Documentation"
            content = "Technical documentation with tutorials, guides, and API reference."
            headers = ["Getting Started", "Tutorials", "API Reference", "Examples"]
            
        else:
            # Generic content
            title = f"Web Page - {domain}"
            content = f"Content from {domain} website."
            headers = ["Home", "About", "Services", "Contact"]
        
        return {
            "title": title,
            "content": content,
            "headers": headers,
            "links": [url, f"{url}/about", f"{url}/contact"],
            "meta": {
                "description": f"Content from {domain}",
                "keywords": domain.replace(".", ", ")
            },
            "status": "simulated"
        }
    
    def _format_scraped_content(self, url: str, data: Dict[str, Any]) -> str:
        """Format scraped content for display."""
        output = [f"🌐 **Web Scraping Results for:** {url}\n"]
        
        # Title
        if "title" in data:
            output.append(f"📄 **Title:** {data['title']}")
        
        # Meta information
        if "meta" in data and data["meta"]:
            output.append(f"📝 **Description:** {data['meta'].get('description', 'N/A')}")
            if "keywords" in data["meta"]:
                output.append(f"🏷️  **Keywords:** {data['meta']['keywords']}")
        
        # Status indicator
        if data.get("status") == "simulated":
            output.append("⚠️  **Note:** This is simulated content for demonstration")
        
        output.append("")  # Empty line
        
        # Headers
        if "headers" in data and data["headers"]:
            output.append("📋 **Page Headers:**")
            for i, header in enumerate(data["headers"][:5], 1):  # Limit to 5 headers
                output.append(f"  {i}. {header}")
            output.append("")
        
        # Content preview
        if "content" in data:
            content = data["content"]
            if len(content) > self.max_content_length:
                content = content[:self.max_content_length] + "..."
            
            output.append("📖 **Content Preview:**")
            output.append(f"```\n{content}\n```")
            output.append("")
        
        # Links
        if self.extract_links and "links" in data and data["links"]:
            output.append("🔗 **Extracted Links:**")
            for i, link in enumerate(data["links"][:5], 1):  # Limit to 5 links
                output.append(f"  {i}. {link}")
            
            if len(data["links"]) > 5:
                output.append(f"  ... and {len(data['links']) - 5} more links")
            output.append("")
        
        # Statistics
        output.append("📊 **Scraping Statistics:**")
        output.append(f"- Content length: {len(data.get('content', ''))} characters")
        output.append(f"- Headers found: {len(data.get('headers', []))}")
        output.append(f"- Links found: {len(data.get('links', []))}")
        
        return "\n".join(output)
    
    def extract_specific_content(self, url: str, selector_type: str) -> List[str]:
        """Extract specific content type from URL."""
        scraped_data = self._scrape_url(url)
        
        if not scraped_data:
            return []
        
        if selector_type == "title":
            return [scraped_data.get("title", "")]
        elif selector_type == "headers":
            return scraped_data.get("headers", [])
        elif selector_type == "links":
            return scraped_data.get("links", [])
        elif selector_type == "content":
            return [scraped_data.get("content", "")]
        elif selector_type == "meta":
            meta = scraped_data.get("meta", {})
            return [f"{k}: {v}" for k, v in meta.items()]
        else:
            return []
    
    def batch_scrape(self, urls: List[str]) -> Dict[str, Dict[str, Any]]:
        """Scrape multiple URLs (simulated batch processing)."""
        results = {}
        
        for url in urls:
            try:
                scraped_data = self._scrape_url(url)
                if scraped_data:
                    results[url] = scraped_data
                else:
                    results[url] = {"error": "Could not scrape content"}
            except Exception as e:
                results[url] = {"error": str(e)}
        
        return results
    
    def get_scraping_stats(self) -> Dict[str, Any]:
        """Get scraping statistics."""
        return {
            "demo_urls_available": len(self.demo_content),
            "max_content_length": self.max_content_length,
            "extract_links": self.extract_links,
            "extract_images": self.extract_images,
            "timeout": self.timeout
        }


# Example usage:
"""
scraper = WebScraperPlugin(resources={}, config={
    "max_content_length": 5000,
    "extract_links": True,
    "timeout": 30
})

# Scrape a web page
await scraper._execute_impl(Mock(message="https://www.python.org"))

# Extract specific content
headers = scraper.extract_specific_content("https://www.python.org", "headers")
links = scraper.extract_specific_content("https://www.python.org", "links")

# Batch scraping
urls = ["https://www.python.org", "https://github.com/ladvien/entity"]
batch_results = scraper.batch_scrape(urls)

# Get scraping statistics
stats = scraper.get_scraping_stats()
"""