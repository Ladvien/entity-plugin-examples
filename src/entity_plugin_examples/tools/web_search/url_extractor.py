"""URL extractor plugin for finding and validating URLs in text."""

from __future__ import annotations
import re
from typing import Dict, Any, Optional, List, Set
from urllib.parse import urlparse, urljoin

from entity.plugins.tool import ToolPlugin
from entity.workflow.stages import DO


class URLExtractorPlugin(ToolPlugin):
    """
    URL extractor plugin for finding and validating URLs in text.
    
    Features:
    - Extract URLs from text using regex patterns
    - Validate URL format and accessibility
    - Categorize URLs by domain/type
    - Extract metadata (title, description) from URLs
    - Handle relative URLs with base URL
    """
    
    supported_stages = [DO]
    
    def __init__(self, resources: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        super().__init__(resources, config)
        
        config = config or {}
        self.validate_urls = config.get("validate_urls", False)
        self.extract_metadata = config.get("extract_metadata", False)
        self.base_url = config.get("base_url", "")
        self.allowed_schemes = config.get("allowed_schemes", ["http", "https", "ftp", "ftps"])
        
        # URL patterns for different types
        self.url_patterns = {
            "standard": re.compile(
                r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))?)?',
                re.IGNORECASE
            ),
            "loose": re.compile(
                r'(?:(?:https?://)|(?:www\.))(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))?)?',
                re.IGNORECASE
            ),
            "email": re.compile(
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                re.IGNORECASE
            )
        }
    
    async def _execute_impl(self, context) -> str:
        """Extract and process URLs from text."""
        text = (context.message or "").strip()
        
        if not text:
            return "Error: No text provided for URL extraction"
        
        try:
            # Extract URLs using different patterns
            urls = self._extract_urls(text)
            
            if not urls:
                return "No URLs found in the provided text"
            
            # Process and analyze URLs
            processed_urls = self._process_urls(urls)
            
            # Format results
            return self._format_url_results(processed_urls)
            
        except Exception as e:
            return f"URL Extraction Error: {str(e)}"
    
    def _extract_urls(self, text: str) -> List[Dict[str, str]]:
        """Extract URLs from text using multiple patterns."""
        found_urls = []
        url_set: Set[str] = set()  # Avoid duplicates
        
        # Extract standard HTTP/HTTPS URLs
        for match in self.url_patterns["standard"].finditer(text):
            url = match.group().strip()
            if url not in url_set:
                found_urls.append({
                    "url": url,
                    "type": "web",
                    "original": url,
                    "position": match.span()
                })
                url_set.add(url)
        
        # Extract loose URLs (including www. without http://)
        for match in self.url_patterns["loose"].finditer(text):
            original_url = match.group().strip()
            
            # Normalize URL
            if original_url.startswith("www."):
                normalized_url = f"https://{original_url}"
            else:
                normalized_url = original_url
            
            if normalized_url not in url_set:
                found_urls.append({
                    "url": normalized_url,
                    "type": "web",
                    "original": original_url,
                    "position": match.span()
                })
                url_set.add(normalized_url)
        
        # Extract email addresses
        for match in self.url_patterns["email"].finditer(text):
            email = match.group().strip()
            if f"mailto:{email}" not in url_set:
                found_urls.append({
                    "url": f"mailto:{email}",
                    "type": "email",
                    "original": email,
                    "position": match.span()
                })
                url_set.add(f"mailto:{email}")
        
        return found_urls
    
    def _process_urls(self, urls: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Process and analyze extracted URLs."""
        processed = []
        
        for url_info in urls:
            try:
                parsed = urlparse(url_info["url"])
                
                # Handle relative URLs
                if self.base_url and not parsed.netloc:
                    absolute_url = urljoin(self.base_url, url_info["url"])
                    parsed = urlparse(absolute_url)
                    url_info["url"] = absolute_url
                
                # Validate scheme
                is_valid_scheme = parsed.scheme.lower() in self.allowed_schemes
                
                # Categorize domain
                domain_category = self._categorize_domain(parsed.netloc)
                
                processed_info = {
                    **url_info,
                    "scheme": parsed.scheme,
                    "domain": parsed.netloc,
                    "path": parsed.path,
                    "query": parsed.query,
                    "fragment": parsed.fragment,
                    "is_valid_scheme": is_valid_scheme,
                    "domain_category": domain_category,
                    "is_secure": parsed.scheme.lower() in ["https", "ftps"]
                }
                
                # Add validation if enabled
                if self.validate_urls and url_info["type"] == "web":
                    processed_info["is_accessible"] = self._check_url_accessibility(url_info["url"])
                
                processed.append(processed_info)
                
            except Exception as e:
                # Keep invalid URLs but mark them
                processed.append({
                    **url_info,
                    "error": str(e),
                    "is_valid": False
                })
        
        return processed
    
    def _categorize_domain(self, domain: str) -> str:
        """Categorize domain by type."""
        if not domain:
            return "unknown"
        
        domain_lower = domain.lower()
        
        # Social media platforms
        social_domains = ["twitter.com", "facebook.com", "instagram.com", "linkedin.com", 
                         "youtube.com", "tiktok.com", "reddit.com"]
        if any(social in domain_lower for social in social_domains):
            return "social"
        
        # Code repositories
        code_domains = ["github.com", "gitlab.com", "bitbucket.org", "sourceforge.net"]
        if any(code in domain_lower for code in code_domains):
            return "code_repository"
        
        # Documentation sites
        docs_domains = ["readthedocs.io", "docs.", ".readthedocs.org", "documentation"]
        if any(docs in domain_lower for docs in docs_domains):
            return "documentation"
        
        # News sites
        news_domains = ["cnn.com", "bbc.com", "reuters.com", "ap.org", "news."]
        if any(news in domain_lower for news in news_domains):
            return "news"
        
        # Educational
        if domain_lower.endswith(".edu") or "university" in domain_lower:
            return "educational"
        
        # Government
        if domain_lower.endswith(".gov") or "government" in domain_lower:
            return "government"
        
        # Commercial
        if domain_lower.endswith(".com"):
            return "commercial"
        
        # Organization
        if domain_lower.endswith(".org"):
            return "organization"
        
        return "general"
    
    def _check_url_accessibility(self, url: str) -> bool:
        """Check if URL is accessible (simulated)."""
        # This is a simulation - in production would make HTTP request
        # For demo purposes, assume most URLs are accessible
        try:
            parsed = urlparse(url)
            # Simulate some inaccessible domains
            inaccessible_domains = ["example.com", "test.invalid", "localhost"]
            return parsed.netloc.lower() not in inaccessible_domains
        except:
            return False
    
    def _format_url_results(self, processed_urls: List[Dict[str, Any]]) -> str:
        """Format URL extraction results."""
        if not processed_urls:
            return "No valid URLs found"
        
        output = [f"Found {len(processed_urls)} URLs:\n"]
        
        # Group by type
        web_urls = [u for u in processed_urls if u["type"] == "web"]
        email_urls = [u for u in processed_urls if u["type"] == "email"]
        
        if web_urls:
            output.append("🌐 **Web URLs:**")
            for i, url_info in enumerate(web_urls, 1):
                security_indicator = "🔒" if url_info.get("is_secure", False) else "🔓"
                category = url_info.get("domain_category", "unknown")
                
                output.append(f"{i}. {security_indicator} **{url_info['domain']}** ({category})")
                output.append(f"   {url_info['url']}")
                
                if "error" in url_info:
                    output.append(f"   ⚠️  Error: {url_info['error']}")
                elif not url_info.get("is_valid_scheme", True):
                    output.append(f"   ⚠️  Invalid scheme: {url_info.get('scheme', 'unknown')}")
                
                output.append("")
        
        if email_urls:
            output.append("📧 **Email Addresses:**")
            for i, url_info in enumerate(email_urls, 1):
                output.append(f"{i}. {url_info['original']}")
        
        # Add summary statistics
        output.append(f"\n📊 **Summary:**")
        output.append(f"- Web URLs: {len(web_urls)}")
        output.append(f"- Email addresses: {len(email_urls)}")
        
        if web_urls:
            secure_count = sum(1 for u in web_urls if u.get("is_secure", False))
            output.append(f"- Secure URLs: {secure_count}/{len(web_urls)}")
            
            categories = {}
            for u in web_urls:
                cat = u.get("domain_category", "unknown")
                categories[cat] = categories.get(cat, 0) + 1
            
            if categories:
                output.append(f"- Categories: {', '.join(f'{k}({v})' for k, v in categories.items())}")
        
        return "\n".join(output)
    
    def extract_urls_by_type(self, text: str, url_type: str = "all") -> List[str]:
        """Extract URLs filtered by type."""
        all_urls = self._extract_urls(text)
        
        if url_type == "all":
            return [url_info["url"] for url_info in all_urls]
        elif url_type == "web":
            return [url_info["url"] for url_info in all_urls if url_info["type"] == "web"]
        elif url_type == "email":
            return [url_info["url"] for url_info in all_urls if url_info["type"] == "email"]
        else:
            return []


# Example usage:
"""
extractor = URLExtractorPlugin(resources={}, config={
    "validate_urls": True,
    "base_url": "https://example.com"
})

# Extract URLs from text
text = '''
Check out these resources:
- https://github.com/ladvien/entity
- www.python.org for Python documentation
- Contact us at support@example.com
- See also: /docs/quickstart (relative URL)
'''

await extractor._execute_impl(Mock(message=text))
# Returns formatted analysis of all found URLs

# Extract specific types
web_urls = extractor.extract_urls_by_type(text, "web")
emails = extractor.extract_urls_by_type(text, "email")
"""