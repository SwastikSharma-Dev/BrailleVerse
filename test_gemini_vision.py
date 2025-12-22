"""
Test Gemini Vision API connection
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'braille_project.settings')
django.setup()

from django.conf import settings
import google.generativeai as genai

def test_gemini_vision():
    """Test if Gemini Vision API works"""
    print("=" * 60)
    print("Testing Gemini Vision API")
    print("=" * 60)
    
    api_key = settings.GEMINI_API_KEY
    print(f"API Key configured: {'Yes' if api_key and api_key != 'YOUR_GEMINI_API_KEY_HERE' else 'No'}")
    
    if not api_key or api_key == 'YOUR_GEMINI_API_KEY_HERE':
        print("❌ ERROR: No valid API key configured")
        return
    
    try:
        # Configure API
        genai.configure(api_key=api_key)
        print("✓ API configured")
        
        # Test listing models
        print("\nAvailable models:")
        for model in genai.list_models():
            if 'vision' in model.name.lower() or 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name}")
        
        # Try gemini-1.5-flash
        print("\n" + "=" * 60)
        print("Testing gemini-1.5-flash model...")
        print("=" * 60)
        
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content("Say 'hello' if you can hear me")
            print(f"✓ Text generation works: {response.text}")
        except Exception as e:
            print(f"❌ gemini-1.5-flash error: {e}")
            
        # Try gemini-pro
        print("\n" + "=" * 60)
        print("Testing gemini-pro model...")
        print("=" * 60)
        
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content("Say 'hello' if you can hear me")
            print(f"✓ gemini-pro works: {response.text}")
        except Exception as e:
            print(f"❌ gemini-pro error: {e}")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gemini_vision()
