"""
URL configuration for braille_app
"""
from django.urls import path
from . import views

urlpatterns = [
    # Landing and user type selection
    path('', views.landing, name='landing'),
    path('user-type/', views.user_type, name='user_type'),
    
    # Main menu
    path('main-menu/', views.main_menu, name='main_menu'),
    
    # Custom text
    path('custom-text/', views.custom_text, name='custom_text'),
    
    # Voice assistant
    path('voice-assistant/', views.voice_assistant, name='voice_assistant'),
    
    # News
    path('news/', views.news, name='news'),
    path('news/<str:category>/', views.news_category, name='news_category'),
    path('news/<str:category>/<int:article_index>/', views.news_article, name='news_article'),
    
    # Books
    path('books/', views.books, name='books'),
    path('books/<str:book_id>/', views.book_reader, name='book_reader'),
    
    # API endpoints
    path('api/voice-command/', views.voice_command, name='voice_command'),
]
