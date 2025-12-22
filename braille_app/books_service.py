"""
Books API Service Module for Braille Display Website

This module integrates with Google Books API to search and fetch book content.
"""

from django.conf import settings
import requests
from urllib.parse import quote


class BooksService:
    """
    Service class for searching and fetching books from Google Books API.
    """
    
    def __init__(self):
        self.api_key = settings.GOOGLE_BOOKS_API_KEY
        self.max_results = settings.BOOKS_SEARCH_MAX_RESULTS
        self.base_url = 'https://www.googleapis.com/books/v1/volumes'
        self.api_available = self.api_key and self.api_key != 'YOUR_GOOGLE_BOOKS_API_KEY_HERE'
        
        if self.api_available:
            print("Google Books API configured")
        else:
            print("Google Books API not configured - using placeholder content")
    
    def search_books(self, query, max_results=None):
        """
        Search for books by title, author, or keyword.
        
        Args:
            query: search query
            max_results: maximum number of results to return
        
        Returns:
            list: List of book dictionaries
        """
        if not max_results:
            max_results = self.max_results
        
        if self.api_available:
            try:
                params = {
                    'q': query,
                    'maxResults': max_results,
                    'orderBy': 'relevance',
                    'printType': 'books',
                    'langRestrict': 'en'
                }
                
                if self.api_key:
                    params['key'] = self.api_key
                
                response = requests.get(self.base_url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                books = []
                if 'items' in data:
                    for item in data['items']:
                        volume_info = item.get('volumeInfo', {})
                        books.append({
                            'id': item.get('id'),
                            'title': volume_info.get('title', 'Unknown Title'),
                            'authors': volume_info.get('authors', ['Unknown Author']),
                            'description': volume_info.get('description', 'No description available.'),
                            'publisher': volume_info.get('publisher', 'Unknown'),
                            'published_date': volume_info.get('publishedDate', 'Unknown'),
                            'page_count': volume_info.get('pageCount', 0),
                            'preview_link': volume_info.get('previewLink', ''),
                            'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', '')
                        })
                
                return books
            except Exception as e:
                print(f"Error searching books: {e}")
        
        # Fallback to placeholder
        return self._get_placeholder_books(query)
    
    def get_book_details(self, book_id):
        """
        Get detailed information about a specific book.
        
        Args:
            book_id: Google Books volume ID
        
        Returns:
            dict: Book details
        """
        if self.api_available:
            try:
                url = f"{self.base_url}/{book_id}"
                params = {}
                if self.api_key:
                    params['key'] = self.api_key
                
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                volume_info = data.get('volumeInfo', {})
                return {
                    'id': data.get('id'),
                    'title': volume_info.get('title', 'Unknown Title'),
                    'authors': volume_info.get('authors', ['Unknown Author']),
                    'description': volume_info.get('description', 'No description available.'),
                    'publisher': volume_info.get('publisher', 'Unknown'),
                    'published_date': volume_info.get('publishedDate', 'Unknown'),
                    'page_count': volume_info.get('pageCount', 0),
                    'content': self._extract_content(data),
                    'preview_link': volume_info.get('previewLink', ''),
                }
            except Exception as e:
                print(f"Error getting book details: {e}")
        
        return None
    
    def _extract_content(self, book_data):
        """
        Extract readable content from book data.
        """
        # Google Books API has limited access to full text
        # We'll use description and available preview text
        volume_info = book_data.get('volumeInfo', {})
        access_info = book_data.get('accessInfo', {})
        
        content = {
            'description': volume_info.get('description', ''),
            'has_preview': access_info.get('viewability') in ['PARTIAL', 'ALL_PAGES'],
            'preview_link': volume_info.get('previewLink', ''),
            'info_link': volume_info.get('infoLink', '')
        }
        
        return content
    
    def get_popular_books(self):
        """
        Get popular/recommended books for the landing page.
        
        Returns:
            list: List of popular books
        """
        # When API is available, could fetch bestsellers or featured books
        # For now, return curated placeholder collection
        return self._get_placeholder_books(query=None)
    
    def _get_placeholder_books(self, query):
        """
        Return placeholder books when API is not available.
        """
        # Return default book collection
        return [
            {
                'id': 'accessible_tech',
                'title': 'Accessible Technology: A Comprehensive Guide',
                'authors': ['Various Authors'],
                'description': 'A comprehensive guide to accessible technology covering screen readers, braille displays, and voice technology.',
                'publisher': 'Tech Accessibility Press',
                'published_date': '2024',
                'page_count': 350,
                'preview_link': '#',
                'thumbnail': ''
            },
            {
                'id': 'braille_history',
                'title': 'The History and Evolution of Braille',
                'authors': ['Louis Braille Foundation'],
                'description': 'Explore the fascinating history of the Braille system and its impact on accessibility.',
                'publisher': 'Braille Foundation',
                'published_date': '2023',
                'page_count': 200,
                'preview_link': '#',
                'thumbnail': ''
            },
            {
                'id': 'independence',
                'title': 'Living Independently with Visual Impairment',
                'authors': ['Dr. Sarah Johnson'],
                'description': 'Practical advice and strategies for independent living with visual impairments.',
                'publisher': 'Independence Press',
                'published_date': '2024',
                'page_count': 280,
                'preview_link': '#',
                'thumbnail': ''
            }
        ]
    
    def get_book_content_for_reading(self, book_id):
        """
        Get book content formatted for chapter-by-chapter reading.
        Note: Full text access is limited by Google Books API.
        """
        # For actual reading, we'll use our placeholder content
        # Real implementation would need full text access via publishers
        
        placeholder_books = {
            'accessible_tech': {
                'title': 'Accessible Technology: A Guide',
                'chapters': [
                    {
                        'number': 1,
                        'title': 'Introduction to Accessible Technology',
                        'content': 'Accessible technology refers to devices, software, and systems designed to be usable by people with disabilities. This chapter explores the fundamental principles of accessible design and why it matters in our increasingly digital world.'
                    },
                    {
                        'number': 2,
                        'title': 'Screen Readers and Voice Technology',
                        'content': 'Screen readers are essential tools for visually impaired users. They convert digital text into synthesized speech or refreshable braille. Modern screen readers can navigate complex web pages, documents, and applications.'
                    },
                    {
                        'number': 3,
                        'title': 'Braille Displays and Tactile Interfaces',
                        'content': 'Refreshable braille displays provide tactile feedback by raising and lowering pins to form braille characters. These devices connect to computers and smartphones, allowing users to read digital content in braille.'
                    }
                ]
            }
        }
        
        return placeholder_books.get(book_id)


# Singleton instance
_books_service = None

def get_books_service():
    """Get or create BooksService instance."""
    global _books_service
    if _books_service is None:
        _books_service = BooksService()
    return _books_service
