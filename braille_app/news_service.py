"""
News API Service Module for Braille Display Website

This module integrates with NewsAPI to fetch real-time news articles.
"""

from django.conf import settings
import requests
from datetime import datetime

# Check if newsapi-python is available
try:
    from newsapi import NewsApiClient
    NEWSAPI_AVAILABLE = True
except ImportError:
    NEWSAPI_AVAILABLE = False
    print("Warning: newsapi-python not installed. Install with: pip install newsapi-python")


class NewsService:
    """
    Service class for fetching news from NewsAPI.
    Falls back to placeholder content if API is not configured.
    """
    
    def __init__(self):
        self.api_key = settings.NEWS_API_KEY
        self.articles_per_category = settings.NEWS_API_ARTICLES_PER_CATEGORY
        self.newsapi = None
        
        # Initialize API client if available
        if NEWSAPI_AVAILABLE and self.api_key and self.api_key != 'YOUR_NEWS_API_KEY_HERE':
            try:
                self.newsapi = NewsApiClient(api_key=self.api_key)
                print("NewsAPI initialized successfully")
            except Exception as e:
                print(f"NewsAPI initialization failed: {e}")
    
    def get_top_headlines(self, category='general', country='us'):
        """
        Fetch top headlines for a specific category.
        
        Args:
            category: news category (general, technology, sports, etc.)
            country: country code (us, uk, etc.)
        
        Returns:
            list: List of article dictionaries
        """
        if self.newsapi:
            try:
                response = self.newsapi.get_top_headlines(
                    category=category,
                    country=country,
                    page_size=self.articles_per_category
                )
                
                if response['status'] == 'ok':
                    articles = []
                    for article in response['articles']:
                        articles.append({
                            'title': article['title'],
                            'content': article['description'] or article['content'] or 'No content available.',
                            'source': article['source']['name'],
                            'url': article['url'],
                            'published_at': article['publishedAt']
                        })
                    return articles
            except Exception as e:
                print(f"Error fetching news: {e}")
        
        # Fallback to placeholder content
        return self._get_placeholder_news(category)
    
    def search_news(self, query, sort_by='relevancy'):
        """
        Search for news articles by keyword.
        
        Args:
            query: search query
            sort_by: sorting method (relevancy, popularity, publishedAt)
        
        Returns:
            list: List of article dictionaries
        """
        if self.newsapi:
            try:
                response = self.newsapi.get_everything(
                    q=query,
                    sort_by=sort_by,
                    page_size=self.articles_per_category,
                    language='en'
                )
                
                if response['status'] == 'ok':
                    articles = []
                    for article in response['articles']:
                        articles.append({
                            'title': article['title'],
                            'content': article['description'] or article['content'] or 'No content available.',
                            'source': article['source']['name'],
                            'url': article['url'],
                            'published_at': article['publishedAt']
                        })
                    return articles
            except Exception as e:
                print(f"Error searching news: {e}")
        
        return self._get_placeholder_news('search')
    
    def _get_placeholder_news(self, category):
        """
        Fallback placeholder news when API is not available.
        """
        placeholder_articles = {
            'general': [
                {
                    'title': 'Latest Global News Headlines',
                    'content': 'World leaders meet to discuss important international matters. The summit aims to address pressing global challenges and foster cooperation among nations.',
                    'source': 'Placeholder News',
                    'url': '#',
                    'published_at': datetime.now().isoformat()
                },
                {
                    'title': 'Economic Updates and Market Trends',
                    'content': 'Markets show steady growth as investors respond positively to recent policy announcements. Analysts predict continued momentum in the coming months.',
                    'source': 'Placeholder News',
                    'url': '#',
                    'published_at': datetime.now().isoformat()
                }
            ],
            'technology': [
                {
                    'title': 'New Accessibility Features Launched',
                    'content': 'Major tech companies announce groundbreaking accessibility features designed to help visually impaired users. The updates include improved screen reader support and enhanced voice navigation.',
                    'source': 'Placeholder News',
                    'url': '#',
                    'published_at': datetime.now().isoformat()
                },
                {
                    'title': 'Advances in Braille Display Technology',
                    'content': 'Researchers develop innovative refreshable braille displays that are more affordable and portable. The new technology uses advanced actuators for clearer tactile feedback.',
                    'source': 'Placeholder News',
                    'url': '#',
                    'published_at': datetime.now().isoformat()
                }
            ],
            'sports': [
                {
                    'title': 'Paralympic Athletes Break Records',
                    'content': 'Inspiring performances at international sports events showcase the incredible achievements of athletes with disabilities. New world records are set in multiple categories.',
                    'source': 'Placeholder News',
                    'url': '#',
                    'published_at': datetime.now().isoformat()
                }
            ]
        }
        
        return placeholder_articles.get(category, placeholder_articles['general'])


# Singleton instance
_news_service = None

def get_news_service():
    """Get or create NewsService instance."""
    global _news_service
    if _news_service is None:
        _news_service = NewsService()
    return _news_service
