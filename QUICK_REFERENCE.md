# 🚀 QUICK REFERENCE CARD

## ⚡ Start the Server (1 Command)

```cmd
start_server.bat
```

**Or manually:**
```cmd
C:\Users\swast\anaconda3\Scripts\activate.bat
conda activate drf
python manage.py runserver
```

**Then open:** http://localhost:8000

---

## 🎤 Voice Commands

| Command | Action |
|---------|--------|
| "Visually Impaired" | Select user type |
| "Helper" | Go to main menu |
| "Main Menu" | Return to main menu |
| "Custom Text" | Open text input |
| "Voice Assistant" | Open Q&A |
| "News" | Browse news |
| "Books" | Open library |
| "Back" | Previous page |
| "Help" | Hear help |
| "Repeat" | Repeat content |
| "One" / "Two" / etc. | Select option by number |
| "Next" | Next chapter (books) |
| "Previous" | Previous chapter |

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **Ctrl + Space** | Toggle voice input |
| **H** | Help message |
| **R** | Repeat page |
| **Esc** | Stop speaking |
| **Tab** | Next button |
| **Shift + Tab** | Previous button |
| **Enter** / **Space** | Activate button |

---

## 📁 Important Files

| File | What It Does |
|------|--------------|
| `manage.py` | Run Django commands |
| `braille_project/settings.py` | Configuration & Firebase |
| `braille_app/views.py` | All page logic |
| `braille_app/firebase_service.py` | Firebase & chunking |
| `braille_app/templates/` | HTML pages |
| `braille_app/static/js/voice.js` | Voice system |
| `braille_app/static/css/style.css` | Styling |

---

## 🔥 Firebase Setup

1. Get credentials from [Firebase Console](https://console.firebase.google.com/)
2. Save as `firebase-credentials.json` in project root
3. Update `braille_project/settings.py`:
   ```python
   FIREBASE_CONFIG = {
       'apiKey': "YOUR_KEY",
       'databaseURL': "https://YOUR_PROJECT.firebaseio.com",
       'projectId': "YOUR_PROJECT_ID",
   }
   ```

---

## 🛠️ Common Commands

```cmd
# Start server
python manage.py runserver

# Run migrations
python manage.py migrate

# Run tests
python manage.py test braille_app

# Check for issues
python manage.py check

# Create superuser (admin)
python manage.py createsuperuser

# Collect static files (production)
python manage.py collectstatic
```

---

## 🎯 Features Map

| URL | Feature |
|-----|---------|
| `/` | Landing page |
| `/user-type/` | User selection |
| `/main-menu/` | Main navigation |
| `/custom-text/` | Text input |
| `/voice-assistant/` | Q&A |
| `/news/` | News categories |
| `/news/<category>/` | Articles |
| `/books/` | Book library |
| `/books/<book_id>/` | Chapter reader |

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Server won't start | Check Django installed: `python -c "import django"` |
| Voice not working | Use Chrome/Edge, allow mic permissions |
| Port 8000 in use | Use: `python manage.py runserver 8080` |
| Firebase errors | Check console, runs in mock mode by default |
| Static files missing | Run: `python manage.py collectstatic` |

---

## 📝 Customization Points

### Change device settings:
**File:** `braille_project/settings.py`
```python
DEVICE_CHAR_LIMIT = 80    # Characters per chunk
CHUNK_SEND_DELAY = 2      # Delay between chunks
```

### Add news articles:
**File:** `braille_app/views.py`  
**Function:** `news_category()`  
**Variable:** `news_articles` dict

### Add books:
**File:** `braille_app/views.py`  
**Function:** `book_reader()`  
**Variable:** `books_content` dict

### Change colors:
**File:** `braille_app/static/css/style.css`  
**Section:** `:root` variables

### Add voice commands:
**File:** `braille_app/static/js/voice.js`  
**Method:** `processVoiceCommand()`

---

## 📚 Documentation Files

| File | Content |
|------|---------|
| `README.md` | Full documentation |
| `SETUP_GUIDE.md` | Quick setup steps |
| `PROJECT_SUMMARY.md` | Completion report |
| `ARCHITECTURE.md` | System design |
| `CHECKLIST.md` | Feature checklist |
| `QUICK_REFERENCE.md` | This file |

---

## 🔒 Security Checklist

- [ ] Change `SECRET_KEY` in `settings.py`
- [ ] Set `DEBUG = False` for production
- [ ] Update `ALLOWED_HOSTS`
- [ ] Add `firebase-credentials.json` to `.gitignore`
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS in production

---

## 🎨 Accessibility Features

✅ WCAG AAA compliant  
✅ High contrast (black/gold)  
✅ Large fonts (1.25rem+)  
✅ ARIA labels everywhere  
✅ Screen reader optimized  
✅ Keyboard navigation  
✅ Voice input/output  
✅ Braille output via Firebase  

---

## 📞 Support Resources

| Resource | Location |
|----------|----------|
| Django Docs | https://docs.djangoproject.com/ |
| Web Speech API | https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API |
| Firebase Docs | https://firebase.google.com/docs |
| WCAG Guidelines | https://www.w3.org/WAI/WCAG21/quickref/ |

---

## 🎯 Quick Test

1. ✅ Run `start_server.bat`
2. ✅ Open http://localhost:8000
3. ✅ Click 🎤 button (allow mic)
4. ✅ Say "Visually Impaired"
5. ✅ Say "Main Menu"
6. ✅ Say "Custom Text"
7. ✅ Type something and submit
8. ✅ Check console for "[MOCK]" logs

**If all works: You're ready! 🎉**

---

## 💡 Pro Tips

1. **Voice works best in Chrome/Edge**
2. **Check browser console (F12) for logs**
3. **Terminal shows Firebase chunk logs**
4. **Use keyboard shortcuts for speed**
5. **Test with eyes closed to verify accessibility**
6. **Mock mode lets you test without Firebase**
7. **All features work offline**

---

## 🚀 Deploy to Production

1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables (SECRET_KEY, DEBUG, etc.)
3. Add Firebase credentials
4. Run migrations: `python manage.py migrate`
5. Collect static: `python manage.py collectstatic`
6. Use gunicorn: `gunicorn braille_project.wsgi`
7. Set up Nginx as reverse proxy
8. Enable HTTPS

---

**📌 Bookmark this page for quick reference!**

**Need more details? Check README.md or SETUP_GUIDE.md**

---

**🎤♿🔥 Voice-Enabled | Accessible | Firebase-Ready**
