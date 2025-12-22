"""
Views for Braille Display Website
Restructured workflow with Helper and Visually Impaired paths
"""

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

# Import services
from .firebase_service import send_text_to_braille_device
from .gemini_service import get_gemini_service
from .news_service import get_news_service
from .books_service import get_books_service


# ============================================
# LANDING PAGE - Choose Helper or Visually Impaired
# ============================================

def landing(request):
    """
    Landing page with 2 options: Helper or Visually Impaired
    """
    context = {
        'page_title': 'Braille Display - Welcome',
        'instruction': 'Welcome to Braille Display System. Choose your option.',
    }
    return render(request, 'landing.html', context)


# ============================================
# VISUALLY IMPAIRED PATH
# ============================================

def visually_impaired_menu(request):
    """
    Menu for visually impaired users: Books, News, AI Helper
    """
    context = {
        'page_title': 'Visually Impaired Menu',
        'instruction': 'Choose an option: Books, News, or AI Helper',
    }
    return render(request, 'visually_impaired_menu.html', context)


def vi_books(request):
    """
    Popular books selection for visually impaired users.
    Shows 3-4 popular books (Atomic Habits, etc.)
    """
    # Popular books collection
    books = [
        {
            'id': 'atomic_habits',
            'title': 'Atomic Habits',
            'author': 'James Clear',
            'content': 'Atomic Habits by James Clear. Chapter 1: The Surprising Power of Atomic Habits. Habits are the compound interest of self-improvement. The same way that money multiplies through compound interest, the effects of your habits multiply as you repeat them.'
        },
        {
            'id': 'think_and_grow_rich',
            'title': 'Think and Grow Rich',
            'author': 'Napoleon Hill',
            'content': 'Think and Grow Rich by Napoleon Hill. Introduction: The Man Who Thought His Way into Partnership with Thomas Edison. This book teaches you the thirteen steps to riches. Success comes to those who become success conscious.'
        },
        {
            'id': 'power_of_now',
            'title': 'The Power of Now',
            'author': 'Eckhart Tolle',
            'content': 'The Power of Now by Eckhart Tolle. Chapter 1: You Are Not Your Mind. The greatest obstacle to enlightenment is identification with your mind, which causes thought to become compulsive.'
        },
        {
            'id': 'rich_dad_poor_dad',
            'title': 'Rich Dad Poor Dad',
            'author': 'Robert Kiyosaki',
            'content': "Rich Dad Poor Dad by Robert Kiyosaki. Introduction: The rich don't work for money. The poor and middle class work for money. The rich have money work for them. Learn the difference between assets and liabilities."
        }
    ]
    
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        selected_book = next((b for b in books if b['id'] == book_id), None)
        
        if selected_book:
            result = send_text_to_braille_device(selected_book['content'])
            return JsonResponse(result)
    
    context = {
        'page_title': 'Popular Books',
        'instruction': 'Select a book to read',
        'books': books
    }
    return render(request, 'vi_books.html', context)


def vi_news(request):
    """
    News category selection for visually impaired users
    """
    context = {
        'page_title': 'News Categories',
        'instruction': 'Choose a news category',
    }
    return render(request, 'vi_news.html', context)


def vi_news_category(request, category):
    """
    Fetch and send real-time news to Firebase/hardware
    """
    news_service = get_news_service()
    
    # Map URL categories to NewsAPI categories
    category_map = {
        'headlines': 'general',
        'technology': 'technology',
        'sports': 'sports',
        'business': 'business'
    }
    
    api_category = category_map.get(category, 'general')
    articles = news_service.get_top_headlines(category=api_category)
    
    if not articles:
        return redirect('/visually-impaired/news/')
    
    # Format news for sending to device
    news_text = f"{category.upper()} NEWS:\n\n"
    for i, article in enumerate(articles[:5], 1):
        news_text += f"{i}. {article['title']}\n{article.get('description', '')}\n\n"
    
    # Auto-send to Firebase
    result = send_text_to_braille_device(news_text)
    
    context = {
        'page_title': f'{category.title()} News',
        'category': category.title(),
        'articles': articles[:5],
        'send_result': result,
        'instruction': f'Sending {category} news to your device'
    }
    return render(request, 'vi_news_result.html', context)


def vi_ai_helper(request):
    """
    AI chat helper using Gemini API for visually impaired users.
    Voice input/output with braille display.
    """
    gemini_service = get_gemini_service()
    
    if request.method == 'POST':
        user_message = request.POST.get('message', '').strip()
        
        if user_message:
            # Get AI response
            ai_response = gemini_service.chat(user_message)
            
            # Send response to braille device
            firebase_result = send_text_to_braille_device(ai_response['response'])
            
            return JsonResponse({
                'status': 'success',
                'user_message': user_message,
                'ai_response': ai_response['response'],
                'firebase_sent': firebase_result['status'] == 'success'
            })
    
    context = {
        'page_title': 'AI Helper',
        'instruction': 'Ask me anything using voice or text'
    }
    return render(request, 'vi_ai_helper.html', context)


# ============================================
# HELPER PATH
# ============================================

def helper_menu(request):
    """
    Menu for helpers: Send Custom Text, PDF to Braille, Image Transcription
    """
    context = {
        'page_title': 'Helper Menu',
        'instruction': 'Choose an option: Custom Text, PDF, or Image'
    }
    return render(request, 'helper_menu.html', context)


def helper_custom_text(request):
    """
    Send custom text to braille device (voice or typing)
    """
    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        
        if text:
            result = send_text_to_braille_device(text)
            return JsonResponse(result)
    
    context = {
        'page_title': 'Send Custom Text',
        'instruction': 'Type or speak text to send to braille device'
    }
    return render(request, 'helper_custom_text.html', context)


def helper_pdf_to_braille(request):
    """
    Upload PDF and extract text to send to braille device
    """
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        
        # Save file
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        file_path = fs.path(filename)
        
        try:
            # Extract text from PDF
            import PyPDF2
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
            
            # Send to Firebase
            result = send_text_to_braille_device(text)
            
            # Clean up file
            fs.delete(filename)
            
            return JsonResponse({
                'status': 'success',
                'message': f'Extracted {len(text)} characters from PDF',
                'firebase_result': result
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error processing PDF: {str(e)}'
            })
    
    context = {
        'page_title': 'PDF to Braille',
        'instruction': 'Upload a PDF file to convert to braille'
    }
    return render(request, 'helper_pdf_to_braille.html', context)


def helper_image_transcription(request):
    """
    Upload image and get description using Gemini Vision API
    """
    gemini_service = get_gemini_service()
    
    if request.method == 'POST' and request.FILES.get('image_file'):
        image_file = request.FILES['image_file']
        
        # Validate file type
        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
        valid_content_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/bmp']
        
        file_ext = os.path.splitext(image_file.name)[1].lower()
        
        if file_ext not in valid_extensions:
            return JsonResponse({
                'status': 'error',
                'message': f'Invalid file format. Only image files are supported (JPEG, PNG, GIF, WebP, BMP). Your file: {image_file.name}'
            })
        
        if image_file.content_type not in valid_content_types:
            return JsonResponse({
                'status': 'error',
                'message': f'Invalid file type. Only image files are supported. Detected type: {image_file.content_type}'
            })
        
        # Validate file size (10MB max)
        max_size = 10 * 1024 * 1024  # 10MB
        if image_file.size > max_size:
            size_mb = image_file.size / (1024 * 1024)
            return JsonResponse({
                'status': 'error',
                'message': f'File too large. Maximum size is 10MB. Your file: {size_mb:.2f}MB'
            })
        
        # Save file
        fs = FileSystemStorage()
        try:
            filename = fs.save(image_file.name, image_file)
            file_path = fs.path(filename)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error saving file: {str(e)}'
            })
        
        try:
            # Get image description from Gemini
            result = gemini_service.describe_image(
                file_path,
                prompt="Describe this image in detail for a visually impaired person. Include colors, objects, people, actions, text, and spatial relationships."
            )
            
            if result['status'] == 'success':
                # Send description to Firebase
                firebase_result = send_text_to_braille_device(result['description'])
                
                # Clean up file - use try/except for Windows file locks
                try:
                    import time
                    time.sleep(0.5)  # Brief delay for file handle release
                    fs.delete(filename)
                except:
                    pass  # Ignore deletion errors
                
                return JsonResponse({
                    'status': 'success',
                    'description': result['description'],
                    'firebase_result': firebase_result
                })
            else:
                try:
                    fs.delete(filename)
                except:
                    pass
                return JsonResponse(result)
        except Exception as e:
            try:
                fs.delete(filename)
            except:
                pass
            return JsonResponse({
                'status': 'error',
                'message': f'Error processing image: {str(e)}'
            })
    
    context = {
        'page_title': 'Image Transcription',
        'instruction': 'Upload an image to get a detailed description'
    }
    return render(request, 'helper_image_transcription.html', context)


# ============================================
# API ENDPOINTS for Voice Commands
# ============================================

@csrf_exempt
def voice_command(request):
    """
    Handle voice commands from JavaScript
    """
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            command = data.get('command', '').lower()
            
            response = {'status': 'success'}
            
            # Navigation commands
            if 'helper' in command:
                response['action'] = 'navigate'
                response['url'] = '/helper/'
            elif 'visually impaired' in command or 'blind' in command:
                response['action'] = 'navigate'
                response['url'] = '/visually-impaired/'
            elif 'book' in command:
                if '/visually-impaired/' in request.META.get('HTTP_REFERER', ''):
                    response['url'] = '/visually-impaired/books/'
                else:
                    response['url'] = '/helper/'
                response['action'] = 'navigate'
            elif 'news' in command:
                response['action'] = 'navigate'
                response['url'] = '/visually-impaired/news/'
            elif 'ai' in command or 'assistant' in command:
                response['action'] = 'navigate'
                response['url'] = '/visually-impaired/ai-helper/'
            elif 'custom text' in command or 'type' in command:
                response['action'] = 'navigate'
                response['url'] = '/helper/custom-text/'
            elif 'pdf' in command:
                response['action'] = 'navigate'
                response['url'] = '/helper/pdf-to-braille/'
            elif 'image' in command or 'picture' in command:
                response['action'] = 'navigate'
                response['url'] = '/helper/image-transcription/'
            elif 'back' in command or 'go back' in command:
                response['action'] = 'back'
            else:
                response['status'] = 'unknown'
                response['message'] = f'Command not recognized: {command}'
            
            return JsonResponse(response)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
