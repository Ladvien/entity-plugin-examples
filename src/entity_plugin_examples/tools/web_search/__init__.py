"""Web search tool collection - Internet search and retrieval plugins."""

from .search_engine_plugin import SearchEnginePlugin
from .url_extractor import URLExtractorPlugin
from .web_scraper import WebScraperPlugin

__all__ = [
    "SearchEnginePlugin",
    "URLExtractorPlugin", 
    "WebScraperPlugin",
]