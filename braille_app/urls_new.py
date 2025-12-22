"""
URL Configuration for Braille Display Website
New workflow: Helper and Visually Impaired paths
"""

from django.urls import path
from . import views

urlpatterns = [
    # Landing page
    path('', views.landing, name='landing'),
    
    # Visually Impaired Path
    path('visually-impaired/', views.visually_impaired_menu, name='visually_impaired_menu'),
    path('visually-impaired/books/', views.vi_books, name='vi_books'),
    path('visually-impaired/news/', views.vi_news, name='vi_news'),
    path('visually-impaired/news/<str:category>/', views.vi_news_category, name='vi_news_category'),
    path('visually-impaired/ai-helper/', views.vi_ai_helper, name='vi_ai_helper'),
    
    # Helper Path
    path('helper/', views.helper_menu, name='helper_menu'),
    path('helper/custom-text/', views.helper_custom_text, name='helper_custom_text'),
    path('helper/pdf-to-braille/', views.helper_pdf_to_braille, name='helper_pdf_to_braille'),
    path('helper/image-transcription/', views.helper_image_transcription, name='helper_image_transcription'),
    
    # API Endpoints
    path('api/voice-command/', views.voice_command, name='voice_command'),
]
