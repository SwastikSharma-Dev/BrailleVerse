# 🚀 QUICK SETUP GUIDE - Braille Display Website

## Step-by-Step Setup (5 minutes)

### ✅ Step 1: Open CMD Terminal

1. Press `Win + R`
2. Type `cmd` and press Enter
3. Navigate to project folder:
   ```cmd
   cd C:\Users\swast\Desktop\CapstoneWebsite\Website
   ```

---

### ✅ Step 2: Activate Conda Environment

```cmd
C:\Users\swast\anaconda3\Scripts\activate.bat
conda activate drf
```

---

### ✅ Step 3: Install Dependencies (First Time Only)

```cmd
pip install -r requirements.txt
```

**Expected packages:**
- Django 5.0+
- firebase-admin 6.4+

---

### ✅ Step 4: Run Migrations (First Time Only)

```cmd
python manage.py migrate
```

This creates the SQLite database file.

---

### ✅ Step 5: Start the Server

**Option A - Manual:**
```cmd
python manage.py runserver
```

**Option B - Using the batch file:**
```cmd
start_server.bat
```

---

### ✅ Step 6: Open in Browser

Navigate to: **http://localhost:8000**

**Recommended browsers for voice features:**
- Google Chrome
- Microsoft Edge
- Safari

---

## 🎤 Testing Voice Features

1. **Allow microphone permissions** when prompted
2. Click the **🎤 button** (bottom right corner)
3. Or press **Ctrl + Space**
4. Speak commands like:
   - "Visually Impaired"
   - "Main Menu"
   - "Custom Text"
   - "Help"

---

## 🔥 Firebase Configuration (Optional)

The website works in **mock mode** without Firebase credentials.

### To enable real Firebase:

1. Get your Firebase credentials from [Firebase Console](https://console.firebase.google.com/)
2. Download the service account JSON file
3. Save it as `firebase-credentials.json` in the project root
4. Update `braille_project/settings.py` with your Firebase config:

```python
FIREBASE_CONFIG = {
    'apiKey': "YOUR_API_KEY",
    'databaseURL': "https://YOUR_PROJECT_ID-default-rtdb.firebaseio.com",
    'projectId': "YOUR_PROJECT_ID",
    # ... other fields
}
```

---

## 🧪 Verify Installation

Run the test script:
```cmd
test_installation.bat
```

Or manually:
```cmd
python manage.py check
python manage.py test braille_app
```

---

## 📱 Features to Test

### 1. Landing Page
- Welcome message speaks automatically
- Two large buttons (Visually Impaired / Helper)
- Voice command: "Visually Impaired"

### 2. Main Menu
- 5 options displayed
- Voice commands for each option
- Say "Custom Text" or "One"

### 3. Custom Text
- Type or use voice input
- Sends to Firebase (or logs in mock mode)
- Check console for chunk logs

### 4. Voice Assistant
- Ask questions
- Get spoken responses
- Answers sent to braille device

### 5. News
- Browse categories
- Read articles
- Send to braille device

### 6. Books
- Browse book library
- Read chapter by chapter
- Navigate with voice: "Next", "Previous"

---

## ⌨️ Keyboard Shortcuts

- **Ctrl + Space** - Toggle voice input
- **H** - Help message
- **R** - Repeat page content
- **Esc** - Stop speaking
- **Tab** - Navigate between buttons
- **Enter** - Activate button

---

## 🐛 Troubleshooting

### Server won't start?
```cmd
# Check if Django is installed
python -c "import django; print(django.get_version())"

# If not, install it
pip install Django
```

### Voice not working?
- Use Chrome, Edge, or Safari
- Allow microphone permissions
- Check browser console for errors
- Try keyboard navigation instead

### Firebase errors?
- Website works without Firebase (mock mode)
- Check console for "[MOCK]" messages
- Add credentials only when ready

### Port 8000 already in use?
```cmd
python manage.py runserver 8080
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `manage.py` | Django management script |
| `braille_project/settings.py` | Configuration (Firebase, device settings) |
| `braille_app/views.py` | All page logic |
| `braille_app/firebase_service.py` | Firebase integration |
| `braille_app/templates/` | HTML pages |
| `braille_app/static/js/voice.js` | Voice navigation |
| `braille_app/static/css/style.css` | Accessibility styling |

---

## 🎯 Next Steps

1. ✅ **Test all pages** - Navigate through each feature
2. ✅ **Test voice commands** - Try different voice inputs
3. ✅ **Check console logs** - See how text chunking works
4. ✅ **Configure Firebase** - When ready to connect to hardware
5. ✅ **Customize content** - Update news articles, books in `views.py`
6. ✅ **Add AI assistant** - Integrate OpenAI API in `get_assistant_response()`

---

## 💡 Tips

- **Mock mode is fine for development** - You don't need Firebase initially
- **Check terminal output** - See chunk logs when sending text
- **Browser console (F12)** - See JavaScript logs and errors
- **Test accessibility** - Try navigating with eyes closed
- **Use keyboard only** - Verify Tab navigation works

---

## 🆘 Need Help?

1. Check `README.md` for detailed documentation
2. Review Django errors in terminal
3. Check browser console (F12) for JavaScript errors
4. Verify conda environment is activated
5. Make sure you're in the correct directory

---

## 🎉 You're All Set!

**Start the server and visit http://localhost:8000**

The website will automatically:
- Speak the welcome message
- Accept voice commands
- Navigate hands-free
- Work without Firebase (mock mode)

**Enjoy building an accessible future! ♿🎤🔥**
