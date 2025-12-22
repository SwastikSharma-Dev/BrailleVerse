"""
Quick Test Script for Braille Display Website
Tests Firebase connectivity and basic functionality
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'braille_project.settings')

# Setup Django
import django
django.setup()

from django.conf import settings
from braille_app.firebase_service import FirebaseService, send_text_to_braille_device
from braille_app.news_service import get_news_service
from braille_app.books_service import get_books_service

def test_firebase():
    """Test Firebase connection and text sending"""
    print("\n" + "="*60)
    print("🔥 TESTING FIREBASE CONNECTION")
    print("="*60)
    
    print(f"\nFirebase URL: {settings.FIREBASE_CONFIG.get('databaseURL')}")
    print(f"Firebase Path: {settings.FIREBASE_TEXT_PATH}")
    print(f"Auth Token: {'✓ Configured' if settings.FIREBASE_CONFIG.get('authToken') else '✗ Missing'}")
    
    # Test sending text
    test_text = "Hello from Django! This is a test message for the braille display."
    print(f"\n📤 Sending test message...")
    print(f"Text: {test_text}")
    
    result = send_text_to_braille_device(test_text)
    
    print(f"\n✅ Result: {result['status'].upper()}")
    print(f"Message: {result['message']}")
    print(f"Chunks sent: {result.get('chunks_sent', 0)}/{result.get('total_chunks', 0)}")
    print(f"Mode: {result.get('mode', 'unknown')}")
    
    return result['status'] == 'success'

def test_news_api():
    """Test NewsAPI integration"""
    print("\n" + "="*60)
    print("📰 TESTING NEWS API")
    print("="*60)
    
    news_service = get_news_service()
    print(f"\nNews API Key: {'✓ Configured' if settings.NEWS_API_KEY != 'YOUR_NEWS_API_KEY_HERE' else '✗ Using Placeholder'}")
    
    print("\n📡 Fetching technology news...")
    articles = news_service.get_top_headlines(category='technology')
    
    if articles:
        print(f"\n✅ Retrieved {len(articles)} articles:")
        for i, article in enumerate(articles[:3], 1):
            print(f"\n{i}. {article['title']}")
            print(f"   Source: {article.get('source', 'Unknown')}")
    else:
        print("\n⚠️  No articles retrieved (using placeholder content)")
    
    return bool(articles)

def test_books_api():
    """Test Google Books API integration"""
    print("\n" + "="*60)
    print("📚 TESTING GOOGLE BOOKS API")
    print("="*60)
    
    books_service = get_books_service()
    print(f"\nGoogle Books API Key: {'✓ Configured' if settings.GOOGLE_BOOKS_API_KEY != 'YOUR_GOOGLE_BOOKS_API_KEY_HERE' else '✗ Using Placeholder'}")
    
    print("\n🔍 Searching for 'Python programming'...")
    books = books_service.search_books('Python programming', max_results=3)
    
    if books:
        print(f"\n✅ Found {len(books)} books:")
        for i, book in enumerate(books, 1):
            authors = ', '.join(book.get('authors', ['Unknown']))
            print(f"\n{i}. {book['title']}")
            print(f"   By: {authors}")
    else:
        print("\n⚠️  No books found (using placeholder content)")
    
    return bool(books)

def test_voice_system():
    """Check voice system configuration"""
    print("\n" + "="*60)
    print("🎤 VOICE SYSTEM CONFIGURATION")
    print("="*60)
    
    voice_js_path = os.path.join(settings.BASE_DIR, 'braille_app', 'static', 'js', 'voice.js')
    
    if os.path.exists(voice_js_path):
        with open(voice_js_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        features = {
            'Always-on listening': 'this.autoRestart = true' in content,
            'Continuous recognition': 'continuous: true' in content,
            'Fuzzy matching': 'calculateSimilarity' in content,
            'Enhanced NLU': 'handleIntent' in content,
            'Number variants': 'option' in content.lower(),
        }
        
        print("\n✅ Voice.js Features:")
        for feature, enabled in features.items():
            status = "✓" if enabled else "✗"
            print(f"   {status} {feature}")
        
        return all(features.values())
    else:
        print("\n✗ voice.js not found!")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 BRAILLE DISPLAY WEBSITE - SYSTEM TEST")
    print("="*70)
    
    results = {
        'Firebase': test_firebase(),
        'News API': test_news_api(),
        'Books API': test_books_api(),
        'Voice System': test_voice_system()
    }
    
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "⚠️  NEEDS ATTENTION"
        print(f"\n{test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("🎉 ALL TESTS PASSED! System is ready.")
    else:
        print("⚠️  Some tests need attention. Check API keys if needed.")
    print("="*70)
    
    print("\n📝 Notes:")
    print("- Firebase uses REST API mode (firebase-admin not required)")
    print("- News/Books APIs use placeholder content without API keys")
    print("- Voice system works in Chrome/Edge browsers")
    print("- ESP32 should be connected and listening to Firebase")
    
    print("\n🚀 To start the server:")
    print("   python manage.py runserver")
    print("\n🌐 Open in browser:")
    print("   http://127.0.0.1:8000/")
    print("\n")

if __name__ == '__main__':
    main()
