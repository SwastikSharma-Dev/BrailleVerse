# Braille Display - Voice-Enabled Accessibility Website

## 🎯 Project Overview

This is a **fully voice-enabled, accessibility-first Django website** designed for a Refreshable Braille Display hardware project. The website allows visually impaired users to interact with content entirely through voice commands and sends text to a braille device via Firebase.

### Key Features

✅ **100% Voice Navigable** - Every page can be controlled via voice commands  
✅ **WCAG AAA Compliant** - High contrast, large fonts, screen reader optimized  
✅ **Firebase Integration** - Sends text to ESP32 braille device in chunks  
✅ **Simple & Minimal UI** - No visual clutter, designed for accessibility  
✅ **Web Speech API** - SpeechRecognition for input, SpeechSynthesis for output  
✅ **Multiple Features** - Custom text, voice assistant, news, books  

---

## 🚀 Quick Start

### Prerequisites

- Anaconda or Python 3.8+
- Django 5.0+
- Modern browser (Chrome, Edge, or Safari for voice features)

### Installation

1. **Activate your conda environment:**
   ```cmd
   C:\Users\swast\anaconda3\Scripts\activate.bat
   conda activate drf
   ```

2. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

3. **Run database migrations:**
   ```cmd
   python manage.py migrate
   ```

4. **Start the development server:**
   ```cmd
   python manage.py runserver
   ```

5. **Open in browser:**
   ```
   http://localhost:8000
   ```

---

## 📁 Project Structure

```
Website/
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
├── braille_project/                   # Django project settings
│   ├── settings.py                    # Configuration (Firebase, device settings)
│   ├── urls.py                        # Main URL routing
│   ├── wsgi.py & asgi.py             # WSGI/ASGI configuration
│   └── __init__.py
├── braille_app/                       # Main Django app
│   ├── views.py                       # All view logic
│   ├── urls.py                        # App URL routing
│   ├── firebase_service.py            # Firebase integration & text chunking
│   ├── apps.py                        # App configuration
│   ├── templates/                     # HTML templates
│   │   ├── base.html                  # Base template with voice controls
│   │   ├── landing.html               # Welcome page
│   │   ├── user_type.html             # User type selection
│   │   ├── main_menu.html             # Main navigation menu
│   │   ├── custom_text.html           # Custom text input
│   │   ├── custom_text_result.html    # Text sent confirmation
│   │   ├── voice_assistant.html       # Q&A interface
│   │   ├── voice_assistant_result.html
│   │   ├── news.html                  # News categories
│   │   ├── news_category.html         # News articles
│   │   ├── books.html                 # Book library
│   │   └── book_reader.html           # Chapter-by-chapter reading
│   └── static/                        # Static assets
│       ├── css/
│       │   └── style.css              # Accessibility-first CSS
│       └── js/
│           └── voice.js               # Voice navigation system
├── firebase.json                      # Existing Firebase config
└── esp32_code/                        # ESP32 hardware code (separate)
```

---

## 🔧 Configuration

### Firebase Setup

1. **Get your Firebase credentials:**
   - Go to [Firebase Console](https://console.firebase.google.com/)
   - Create or select your project
   - Go to Project Settings → Service Accounts
   - Generate a new private key (JSON file)

2. **Update `braille_project/settings.py`:**
   ```python
   FIREBASE_CONFIG = {
       'apiKey': "YOUR_API_KEY",
       'authDomain': "YOUR_PROJECT_ID.firebaseapp.com",
       'databaseURL': "https://YOUR_PROJECT_ID-default-rtdb.firebaseio.com",
       'projectId': "YOUR_PROJECT_ID",
       'storageBucket': "YOUR_PROJECT_ID.appspot.com",
       'messagingSenderId': "YOUR_SENDER_ID",
       'appId': "YOUR_APP_ID",
   }
   ```

3. **Place your service account JSON:**
   - Save the downloaded JSON as `firebase-credentials.json` in the project root
   - Or update `FIREBASE_CREDENTIALS_PATH` in settings.py

### Device Configuration

Adjust these settings in `braille_project/settings.py`:

```python
DEVICE_CHAR_LIMIT = 80           # Max characters per chunk
CHUNK_SEND_DELAY = 2             # Delay between chunks (seconds)
FIREBASE_TEXT_PATH = '/braille_display/text'  # Firebase path
```

---

## 🎙️ Voice Navigation Guide

### Global Commands

- **"Main Menu"** - Go to main menu
- **"Back"** - Go to previous page
- **"Help"** - Hear help message
- **"Repeat"** - Repeat page content

### Page-Specific Commands

On any page with options, you can:
- Say the **option name** (e.g., "Custom Text", "News")
- Say the **option number** (e.g., "One", "Two", "Three")

### Keyboard Shortcuts

- **Ctrl/Cmd + Space** - Toggle voice input
- **H** - Help
- **R** - Repeat page content
- **Escape** - Stop speaking
- **Tab** - Navigate between buttons

---

## 📱 Features

### 1. Custom Text
- Type or speak text
- Automatically chunked based on device capacity
- Sent sequentially to Firebase → ESP32

### 2. Voice Assistant
- Ask questions via voice or text
- Receives spoken answers
- Answers sent to braille device

### 3. News
- Browse by category (Headlines, Technology, Sports)
- Read full articles
- Send articles to braille device

### 4. Books
- Library of accessible books
- Chapter-by-chapter navigation
- Voice commands: "Next", "Previous", "Repeat"

---

## 🔥 Firebase Integration

### How It Works

1. **Text Chunking:**
   - Text is split into chunks (default: 80 characters)
   - Word boundaries are respected
   
2. **Sequential Sending:**
   - Chunks sent one at a time
   - Configurable delay between chunks
   
3. **Firebase Structure:**
   ```json
   {
     "braille_display": {
       "text": {
         "text": "Chunk content here",
         "chunk_number": 1,
         "total_chunks": 5,
         "timestamp": 1703174400
       }
     }
   }
   ```

4. **ESP32 Listens:**
   - ESP32 code (in `esp32_code/`) listens to Firebase
   - Converts text to braille based on hardware logic
   - Displays on refreshable braille pins

### Mock Mode

If Firebase credentials are not configured:
- Website runs in **mock mode**
- Text chunks are logged to console
- All features work normally (except actual Firebase sending)

---

## ♿ Accessibility Features

### WCAG AAA Compliance

✅ High contrast colors (black/gold theme)  
✅ Large, readable fonts (minimum 1.25rem)  
✅ Clear focus indicators (4px green outline)  
✅ ARIA labels on all interactive elements  
✅ Screen reader optimized HTML  
✅ Keyboard navigation support  
✅ Touch-friendly button sizes (80px minimum)  

### Screen Reader Support

- Semantic HTML structure
- Live regions for dynamic content
- Skip-to-content link
- Descriptive button labels
- Status announcements

### Browser Compatibility

- **Voice Input:** Chrome, Edge, Safari
- **Voice Output:** All modern browsers
- **Fallback:** Keyboard navigation always works

---

## 🧪 Testing

### Run the server:
```cmd
python manage.py runserver
```

### Test voice features:
1. Allow microphone permissions
2. Click the 🎤 button or press Ctrl+Space
3. Speak commands

### Test Firebase (mock mode):
- Check terminal/console for chunk logs
- Verify text splitting works correctly

---

## 🛠️ Development

### Add new features:

1. **Create view** in `braille_app/views.py`
2. **Add URL** in `braille_app/urls.py`
3. **Create template** in `braille_app/templates/`
4. **Add voice commands** in `static/js/voice.js`

### Customize appearance:

Edit `braille_app/static/css/style.css`:
- Change colors in `:root` variables
- Adjust font sizes
- Modify button styles

---

## 📦 Production Deployment

### Collect static files:
```cmd
python manage.py collectstatic
```

### Set DEBUG = False:
In `braille_project/settings.py`:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
```

### Use production server:
```cmd
gunicorn braille_project.wsgi:application
```

---

## 🔒 Security Notes

⚠️ **Never commit Firebase credentials to version control**

- Add `firebase-credentials.json` to `.gitignore`
- Use environment variables for production
- Rotate keys regularly

---

## 📝 License

This project is part of a Capstone project for a Refreshable Braille Display hardware system.

---

## 🤝 Support

For issues or questions:
1. Check console logs for errors
2. Verify Firebase configuration
3. Test with mock mode first
4. Ensure browser supports Web Speech API

---

## 🎨 Credits

**Design Philosophy:**
- Accessibility-first approach
- Minimal visual complexity
- Voice-enabled everything
- Screen reader optimized

**Technologies:**
- Django 5.0
- Web Speech API
- Firebase Realtime Database
- Vanilla JavaScript (no frameworks)
- Semantic HTML5
- WCAG AAA Guidelines

---

**Built with ❤️ for accessibility**
