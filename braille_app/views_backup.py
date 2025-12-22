"""
Django views for Braille Display Website

This module contains all views for the voice-enabled, accessibility-first website.
Each view is designed to be fully navigable via voice commands and screen readers.
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .firebase_service import send_text_to_braille_device
from .news_service import get_news_service
from .books_service import get_books_service


# ============================================
# LANDING PAGE - Initial user type selection
# ============================================

def landing(request):
    """
    Landing page that asks: "Are you visually impaired or a helper?"
    
    Features:
    - Automatically speaks welcome message
    - Two large buttons for selection
    - Voice command recognition
    """
    context = {
        'page_title': 'Welcome - Braille Display',
        'welcome_message': 'Welcome. Are you visually impaired or a helper?',
        'options': [
            {'id': 'visually_impaired', 'text': 'Visually Impaired', 'url': '/user-type/'},
            {'id': 'helper', 'text': 'Helper', 'url': '/main-menu/'}
        ]
    }
    return render(request, 'landing.html', context)


# ============================================
# USER TYPE SELECTION - For visually impaired users
# ============================================

def user_type(request):
    """
    Ask if user is fully or partially visually impaired.
    
    This helps customize the experience but both paths lead to main menu.
    """
    context = {
        'page_title': 'User Type - Braille Display',
        'question': 'Are you fully visually impaired or partially visually impaired?',
        'options': [
            {'id': 'fully', 'text': 'Fully Visually Impaired', 'url': '/main-menu/?type=fully'},
            {'id': 'partially', 'text': 'Partially Visually Impaired', 'url': '/main-menu/?type=partially'}
        ]
    }
    return render(request, 'user_type.html', context)


# ============================================
# MAIN MENU - Central navigation hub
# ============================================

def main_menu(request):
    """
    Main menu with all available features.
    
    Options:
    1. Send Custom Text
    2. Voice Assistant
    3. News
    4. Books
    5. Back (to landing)
    """
    user_type = request.GET.get('type', 'general')
    
    context = {
        'page_title': 'Main Menu - Braille Display',
        'greeting': 'Main Menu. Please select an option.',
        'user_type': user_type,
        'options': [
            {'id': 'custom_text', 'text': 'Send Custom Text', 'url': '/custom-text/'},
            {'id': 'voice_assistant', 'text': 'Voice Assistant', 'url': '/voice-assistant/'},
            {'id': 'news', 'text': 'News', 'url': '/news/'},
            {'id': 'books', 'text': 'Books', 'url': '/books/'},
            {'id': 'back', 'text': 'Back', 'url': '/'}
        ]
    }
    return render(request, 'main_menu.html', context)


# ============================================
# CUSTOM TEXT - Manual or voice text input
# ============================================

def custom_text(request):
    """
    Allow users to send custom text to braille device.
    
    Features:
    - Text input field
    - Voice-to-text button
    - Sends text to Firebase in chunks
    """
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        
        if text:
            # Send text to braille device
            result = send_text_to_braille_device(text)
            
            context = {
                'page_title': 'Custom Text - Braille Display',
                'success': result['status'] == 'success',
                'message': result.get('message', ''),
                'feedback': 'Text sent to braille device.' if result['status'] == 'success' else 'Error sending text.'
            }
            return render(request, 'custom_text_result.html', context)
    
    context = {
        'page_title': 'Send Custom Text - Braille Display',
        'instruction': 'Enter text to send to your braille device. You can type or use voice input.',
    }
    return render(request, 'custom_text.html', context)


# ============================================
# VOICE ASSISTANT - Q&A functionality
# ============================================

def voice_assistant(request):
    """
    Voice-activated assistant that answers questions.
    
    Flow:
    1. User speaks a question
    2. System processes it
    3. Responds via voice AND sends to braille device
    """
    if request.method == 'POST':
        question = request.POST.get('question', '').strip()
        
        if question:
            # Simple response logic (can be enhanced with AI later)
            answer = get_assistant_response(question)
            
            # Send answer to braille device
            result = send_text_to_braille_device(answer)
            
            context = {
                'page_title': 'Voice Assistant - Braille Display',
                'question': question,
                'answer': answer,
                'success': result['status'] == 'success'
            }
            return render(request, 'voice_assistant_result.html', context)
    
    context = {
        'page_title': 'Voice Assistant - Braille Display',
        'instruction': 'Ask me anything. Your answer will be spoken and sent to your braille device.',
    }
    return render(request, 'voice_assistant.html', context)


def get_assistant_response(question):
    """
    Generate response to user question.
    
    This is a simple implementation. Can be enhanced with:
    - OpenAI API
    - Local LLM
    - Wikipedia API
    - Custom knowledge base
    """
    question_lower = question.lower()
    
    # Simple keyword-based responses
    responses = {
        'artificial intelligence': 'Artificial Intelligence is the simulation of human intelligence processes by machines, especially computer systems. These processes include learning, reasoning, and self-correction.',
        'weather': 'I cannot access real-time weather data yet, but you can ask about weather conditions and I will provide information once connected to a weather API.',
        'time': 'I can help with time-related queries. Please specify what you would like to know about time.',
        'date': 'I can help with date-related queries. Please specify what you would like to know about dates.',
        'braille': 'Braille is a tactile writing system used by people who are visually impaired. It consists of patterns of raised dots arranged in cells of up to six dots.',
        'help': 'I am your voice assistant. You can ask me questions about various topics and I will provide answers both verbally and through your braille display.',
    }
    
    # Check for keyword matches
    for keyword, response in responses.items():
        if keyword in question_lower:
            return response
    
    # Default response
    return f"I received your question: '{question}'. This is a placeholder response. Enhanced AI responses will be available once connected to an AI service."


# ============================================
# NEWS MODULE - News articles
# ============================================

def news(request):
    """
    Display news categories for selection.
    """
    context = {
        'page_title': 'News - Braille Display',
        'instruction': 'Select a news category.',
        'categories': [
            {'id': 'headlines', 'text': 'Headlines', 'url': '/news/headlines/'},
            {'id': 'technology', 'text': 'Technology', 'url': '/news/technology/'},
            {'id': 'sports', 'text': 'Sports', 'url': '/news/sports/'},
            {'id': 'back', 'text': 'Back to Main Menu', 'url': '/main-menu/'}
        ]
    }
    return render(request, 'news.html', context)


def news_category(request, category):
    """
    Display news articles for selected category.
    
    Fetches real-time news from NewsAPI or falls back to placeholders.
    """
    # Map URL categories to NewsAPI categories
    category_map = {
        'headlines': 'general',
        'technology': 'technology',
        'sports': 'sports'
    }
    
    api_category = category_map.get(category, 'general')
    
    # Fetch news from API
    news_service = get_news_service()
    articles = news_service.get_top_headlines(category=api_category)
    
    if not articles:
        return redirect('/news/')
    
    context = {
        'page_title': f'{category.title()} News - Braille Display',
        'category': category.title(),
        'articles': articles,
        'instruction': f'{category.title()} news. Select an article to read.'
    }
    return render(request, 'news_category.html', context)


def news_article(request, category, article_index):
    """
    Display full news article and send to braille device.
    """
    # This would fetch the specific article
    # For now, redirecting to category view
    # In production, send article content to braille device
    
    if request.method == 'POST':
        article_text = request.POST.get('article_text', '')
        if article_text:
            result = send_text_to_braille_device(article_text)
            return JsonResponse(result)
    
    return redirect(f'/news/{category}/')


# ============================================
# BOOKS MODULE - Book reading
# ============================================

def books(request):
    """
    Display available books for reading.
    """
    books_service = get_books_service()
    search_query = request.GET.get('search', '')
    
    if search_query:
        # Search for books based on query
        books_list = books_service.search_books(search_query)
        search_performed = True
    else:
        # Show popular/placeholder books
        books_list = books_service.get_popular_books()
        search_performed = False
    
    # Add back button
    back_option = {'id': 'back', 'title': 'Back to Main Menu', 'url': '/main-menu/'}
    
    context = {
        'page_title': 'Books - Braille Display',
        'instruction': 'Search for books or select from popular titles.',
        'books': books_list,
        'back_option': back_option,
        'search_query': search_query,
        'search_performed': search_performed,
    }
    return render(request, 'books.html', context)


def book_reader(request, book_id):
    """
    Book reading interface with chapter navigation.
    
    Features:
    - Chapter-by-chapter navigation
    - Voice commands: "Next", "Repeat", "Back"
    - Sends text to braille device in chunks
    - Supports both local and Google Books API content
    """
    books_service = get_books_service()
    
    # Try to fetch book details from API
    book_data = books_service.get_book_details(book_id)
    
    if not book_data:
        return redirect('/books/')
    
    # Get current chapter/page
    chapter_num = int(request.GET.get('chapter', 1))
    chapter_index = chapter_num - 1
    
    if chapter_index < 0 or chapter_index >= len(book_data.get('chapters', [])):
        chapter_index = 0
    
    current_chapter = book_data['chapters'][chapter_index] if book_data.get('chapters') else None
    
    if not current_chapter:
        return redirect('/books/')
    
    # Handle POST requests (send to braille, navigate)
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'send_to_braille':
            result = send_text_to_braille_device(current_chapter['content'])
            return JsonResponse(result)
        elif action == 'next':
            if chapter_index < len(book_data['chapters']) - 1:
                return redirect(f'/books/{book_id}/?chapter={chapter_num + 1}')
        elif action == 'previous':
            if chapter_index > 0:
                return redirect(f'/books/{book_id}/?chapter={chapter_num - 1}')
    
    context = {
        'page_title': f'{book_data["title"]} - Braille Display',
        'book_title': book_data['title'],
        'chapter': current_chapter,
        'has_next': chapter_index < len(book_data['chapters']) - 1,
        'has_previous': chapter_index > 0,
        'book_id': book_id,
        'total_chapters': len(book_data['chapters'])
    }
    return render(request, 'book_reader.html', context)


# ============================================
# API ENDPOINTS - For voice command processing
# ============================================

@csrf_exempt
def voice_command(request):
    """
    API endpoint to process voice commands.
    
    Accepts JSON with voice command and returns appropriate action.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            command = data.get('command', '').lower()
            
            # Command routing
            response = {
                'status': 'success',
                'action': None,
                'url': None,
                'message': ''
            }
            
            # Navigation commands
            if 'main menu' in command or 'home' in command:
                response['action'] = 'navigate'
                response['url'] = '/main-menu/'
                response['message'] = 'Going to main menu'
            elif 'custom text' in command or 'send text' in command:
                response['action'] = 'navigate'
                response['url'] = '/custom-text/'
                response['message'] = 'Opening custom text'
            elif 'voice assistant' in command or 'assistant' in command:
                response['action'] = 'navigate'
                response['url'] = '/voice-assistant/'
                response['message'] = 'Opening voice assistant'
            elif 'news' in command:
                response['action'] = 'navigate'
                response['url'] = '/news/'
                response['message'] = 'Opening news'
            elif 'books' in command or 'read book' in command:
                response['action'] = 'navigate'
                response['url'] = '/books/'
                response['message'] = 'Opening books'
            elif 'back' in command or 'go back' in command:
                response['action'] = 'back'
                response['message'] = 'Going back'
            else:
                response['status'] = 'unknown'
                response['message'] = f'Command not recognized: {command}'
            
            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
