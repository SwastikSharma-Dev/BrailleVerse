"""
Django settings for braille_project project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-replace-this-with-your-own-secret-key-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'braille_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'braille_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'braille_app' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'braille_project.wsgi.application'


# Database
# Using SQLite for simplicity (can be changed to PostgreSQL/MySQL if needed)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATIC_ROOT = str(BASE_DIR / 'staticfiles')
STATICFILES_DIRS = [
    str(BASE_DIR / 'braille_app' / 'static'),
]

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ========================================
# FIREBASE CONFIGURATION
# ========================================
# Firebase Realtime Database credentials
# Connected to ESP32 braille display hardware

FIREBASE_CONFIG = {
    'databaseURL': "https://braille-display-b87be-default-rtdb.asia-southeast1.firebasedatabase.app",
    'authToken': "JmfhE3a7bXgX93GxdliKbI3uRbE5DpU2FGi45MZM",
    'projectId': "braille-display-b87be",
}

# Path to Firebase service account JSON (optional, for admin SDK)
FIREBASE_CREDENTIALS_PATH = os.path.join(BASE_DIR, 'firebase-credentials.json')


# ========================================
# BRAILLE DEVICE CONFIGURATION
# ========================================
# Maximum characters the braille device can display at once
DEVICE_CHAR_LIMIT = 80

# Delay between sending chunks (in seconds) - adjust based on device needs
CHUNK_SEND_DELAY = 2

# Firebase Realtime Database path where text is sent
FIREBASE_TEXT_PATH = '/braille_display/text'


# ========================================
# EXTERNAL API CONFIGURATIONS
# ========================================

# NewsAPI Configuration
# Get your free API key from: https://newsapi.org/
NEWS_API_KEY = 'YOUR_NEWS_API_KEY_HERE'  # Replace with your actual key

# Google Books API Configuration  
# Get your API key from: https://console.cloud.google.com/
GOOGLE_BOOKS_API_KEY = 'YOUR_GOOGLE_BOOKS_API_KEY_HERE'  # Replace with your actual key

# Google Gemini API Configuration
# Get your API key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'AIzaSyBrEDIjj2Zen0-K1UseVMKUQrAPVOrpxg0')

# API Settings
NEWS_API_ARTICLES_PER_CATEGORY = 5
BOOKS_SEARCH_MAX_RESULTS = 10

# File Upload Settings
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
MAX_UPLOAD_SIZE = 10485760  # 10MB
