# Braille Display Website - Complete Setup Instructions

## Project Overview
This is a fully voice-enabled, accessibility-first Django website for a Refreshable Braille Display hardware project. The website communicates with ESP32 hardware via Firebase Realtime Database.

---

## 🔧 Hardware Setup

### ESP32 Configuration
The ESP32 code is located in `esp32_code/esp32_code.ino`

**Already Configured:**
- WiFi SSID: `iFiW`
- WiFi Password: `ABCD1234`
- Firebase Host: `braille-display-b87be-default-rtdb.asia-southeast1.firebasedatabase.app`
- Firebase Auth Token: `JmfhE3a7bXgX93GxdliKbI3uRbE5DpU2FGi45MZM`

**To Upload:**
1. Open `esp32_code/esp32_code.ino` in Arduino IDE
2. Install library: `Firebase ESP32 Client` by Mobizt (Tools → Manage Libraries)
3. Select your ESP32 board (Tools → Board)
4. Select COM port (Tools → Port)
5. Click Upload
6. Open Serial Monitor (115200 baud) to see connection status

---

## 💻 Django Website Setup

### 1. Python Environment Setup

**Activate your conda environment:**
```powershell
conda activate drf
```

### 2. Install Required Dependencies

```powershell
pip install django firebase-admin requests newsapi-python google-api-python-client
```

### 3. Configure API Keys (Optional but Recommended)

Edit `braille_project/settings.py`:

**For Real-time News (NewsAPI):**
- Get free API key from: https://newsapi.org/
- Replace: `NEWS_API_KEY = 'YOUR_NEWS_API_KEY_HERE'`

**For Book Search (Google Books):**
- Get API key from: https://console.cloud.google.com/
- Enable Google Books API
- Replace: `GOOGLE_BOOKS_API_KEY = 'YOUR_GOOGLE_BOOKS_API_KEY_HERE'`

> **Note:** The website works with placeholder content if you don't add API keys.

### 4. Firebase Configuration

✅ **Already Configured!** Firebase credentials are set in `settings.py`:
- Database URL: `https://braille-display-b87be-default-rtdb.asia-southeast1.firebasedatabase.app`
- Auth Token: `JmfhE3a7bXgX93GxdliKbI3uRbE5DpU2FGi45MZM`

The system automatically uses REST API mode for Firebase communication.

### 5. Run Database Migrations

```powershell
python manage.py migrate
```

### 6. Create Admin User (Optional)

```powershell
python manage.py createsuperuser
```

### 7. Start the Development Server

```powershell
python manage.py runserver
```

The website will be available at: **http://127.0.0.1:8000/**

---

## 🎯 Features

### 1. Voice Navigation (Always-On)
- **Automatic voice recognition** starts 2 seconds after page load
- Say commands like:
  - "option 1" or "first" or "one"
  - "custom text"
  - "voice assistant"
  - "news" → "headlines" or "technology" or "sports"
  - "books" → "search python programming"
  - "back" or "go back"

### 2. Custom Text to Braille
- Type or speak text
- Automatically sent to ESP32 device via Firebase
- Text is chunked (80 characters) for device capacity

### 3. Voice Assistant
- Ask questions about:
  - Braille
  - Technology
  - Accessibility
  - General topics

### 4. Real-time News
- Fetches latest news from NewsAPI
- Categories: Headlines, Technology, Sports
- Falls back to placeholder content if API unavailable

### 5. Online Book Search
- Search any book using Google Books API
- View book details and descriptions
- Falls back to curated collection if API unavailable

### 6. Firebase Integration
- Automatically sends text to ESP32 via Firebase Realtime Database
- Path: `/braille_display/text`
- Includes chunking and sequential sending

---

## 🧪 Testing the Complete System

### Test 1: Website Only
1. Start Django server: `python manage.py runserver`
2. Open browser: `http://127.0.0.1:8000/`
3. Test voice commands (allow microphone access)
4. Try custom text → Check browser console for Firebase sends

### Test 2: ESP32 Only
1. Upload code to ESP32
2. Open Serial Monitor (115200 baud)
3. Check WiFi connection
4. Check Firebase connection
5. Manually update Firebase database from Firebase Console

### Test 3: Full Integration
1. Start Django server
2. Ensure ESP32 is running (check Serial Monitor)
3. On website, go to "Custom Text"
4. Type: "Hello World"
5. Click "Send to Braille Device"
6. Check Serial Monitor → Should show braille pattern

### Test 4: Voice Commands
1. Open website landing page
2. Wait 2 seconds (voice recognition starts automatically)
3. Say: "custom text"
4. Should navigate to custom text page
5. Say: "back" → Returns to main menu

---

## 📁 Project Structure

```
Website/
├── braille_project/          # Django project settings
│   ├── settings.py          # ✅ Firebase + API keys configured
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI entry point
├── braille_app/             # Main Django app
│   ├── views.py             # ✅ All views updated with API services
│   ├── firebase_service.py  # ✅ Firebase REST API integration
│   ├── news_service.py      # ✅ NewsAPI integration
│   ├── books_service.py     # ✅ Google Books API integration
│   ├── templates/           # 12 HTML templates
│   └── static/
│       ├── css/style.css    # Accessible styles
│       └── js/voice.js      # ✅ Enhanced voice navigation
├── esp32_code/
│   └── esp32_code.ino       # ✅ ESP32 firmware (configured)
├── manage.py                # Django management
└── requirements.txt         # Python dependencies
```

---

## 🔍 Troubleshooting

### Issue: Voice not working
- **Solution:** Allow microphone access in browser
- Check browser console for errors
- Use Chrome/Edge (best Web Speech API support)

### Issue: Firebase not connecting from Django
- **Solution:** Check internet connection
- Verify Firebase URL in `settings.py`
- Check console logs for REST API calls
- Install requests: `pip install requests`

### Issue: ESP32 not receiving data
- **Solution:** Check Serial Monitor for connection status
- Verify WiFi credentials in `esp32_code.ino`
- Check Firebase Realtime Database rules (should allow read/write)
- Manually test Firebase from Firebase Console

### Issue: News/Books showing placeholder content
- **Solution:** Add API keys to `settings.py`
- Check API key validity
- Check internet connection
- Placeholder content is intentional fallback

### Issue: Django errors on startup
- **Solution:** Run migrations: `python manage.py migrate`
- Check conda environment: `conda activate drf`
- Install all dependencies from requirements.txt

---

## 🚀 Quick Start Commands

```powershell
# Activate environment
conda activate drf

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

Open: http://127.0.0.1:8000/

---

## 📝 API Keys Configuration

### NewsAPI (Free)
1. Go to: https://newsapi.org/
2. Sign up for free account
3. Copy API key
4. Add to `settings.py`: `NEWS_API_KEY = 'your_key_here'`

### Google Books API (Free)
1. Go to: https://console.cloud.google.com/
2. Create new project
3. Enable "Books API"
4. Create credentials → API Key
5. Add to `settings.py`: `GOOGLE_BOOKS_API_KEY = 'your_key_here'`

---

## ✅ Firebase Database Rules

Your Firebase Realtime Database should have these rules:

```json
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```

**Security Note:** For production, restrict these rules to authenticated users only.

---

## 🎓 Accessibility Features

- **WCAG AAA Compliance:** High contrast, large fonts
- **Screen Reader Support:** Full ARIA labels and landmarks
- **Keyboard Navigation:** All features accessible via keyboard
- **Voice Control:** Hands-free operation for visually impaired users
- **Skip Links:** Quick navigation to main content

---

## 📞 Support

For issues or questions:
1. Check Serial Monitor (ESP32 debugging)
2. Check browser console (JavaScript errors)
3. Check Django terminal (Python errors)
4. Verify all API keys are correct
5. Ensure Firebase rules allow read/write

---

## ✨ Project Complete!

All components are configured and ready:
- ✅ Django website with 7 major features
- ✅ Voice navigation (always-on mode)
- ✅ Firebase integration (REST API)
- ✅ ESP32 hardware code (configured)
- ✅ Real-time news API
- ✅ Online book search API
- ✅ Complete documentation

**Start the server and test your braille display!**
