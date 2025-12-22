"""
Quick Firebase REST API Test
Run this to verify Firebase connection works
"""

import requests
import time
import json

# Firebase configuration
FIREBASE_URL = "https://braille-display-b87be-default-rtdb.asia-southeast1.firebasedatabase.app"
AUTH_TOKEN = "JmfhE3a7bXgX93GxdliKbI3uRbE5DpU2FGi45MZM"
PATH = "/braille_display/text"

def test_firebase_connection():
    """Test Firebase REST API connection"""
    print("\n" + "="*60)
    print("🔥 FIREBASE REST API TEST")
    print("="*60)
    
    print(f"\nFirebase URL: {FIREBASE_URL}")
    print(f"Path: {PATH}")
    print(f"Auth Token: {AUTH_TOKEN[:20]}...")
    
    # Prepare test data
    url = f"{FIREBASE_URL}{PATH}.json?auth={AUTH_TOKEN}"
    data = {
        'text': 'Hello from test script!',
        'chunk_number': 1,
        'total_chunks': 1,
        'timestamp': time.time()
    }
    
    print(f"\n📤 Sending test data to Firebase...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.put(url, json=data, timeout=10)
        print(f"\n✅ Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            print("\n🎉 SUCCESS! Firebase connection is working!")
            print("Your ESP32 should now receive the data.")
            return True
        else:
            print(f"\n❌ FAILED with status {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("\n❌ ERROR: Request timed out (10 seconds)")
        print("Check your internet connection")
        return False
    except requests.exceptions.RequestException as e:
        print(f"\n❌ ERROR: {e}")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        return False

def test_firebase_read():
    """Test reading data from Firebase"""
    print("\n" + "="*60)
    print("📖 READING FROM FIREBASE")
    print("="*60)
    
    url = f"{FIREBASE_URL}{PATH}.json?auth={AUTH_TOKEN}"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"\n✅ Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Current data in Firebase:")
            print(json.dumps(data, indent=2))
            return True
        else:
            print(f"❌ Failed to read: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error reading: {e}")
        return False

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🧪 FIREBASE CONNECTIVITY TEST")
    print("="*60)
    
    # Test write
    write_success = test_firebase_connection()
    
    # Test read
    if write_success:
        print("\n⏳ Waiting 2 seconds...")
        time.sleep(2)
        test_firebase_read()
    
    print("\n" + "="*60)
    print("✨ Test Complete!")
    print("="*60)
    
    if write_success:
        print("\n✅ Your Firebase connection is WORKING!")
        print("The Django website should now be able to send data.")
        print("\nNext steps:")
        print("1. Restart Django server if still showing errors")
        print("2. Try sending text from the website")
        print("3. Check ESP32 Serial Monitor to see if it receives data")
    else:
        print("\n❌ Firebase connection FAILED!")
        print("\nPossible issues:")
        print("1. Check internet connection")
        print("2. Verify Firebase URL and auth token")
        print("3. Check Firebase Database Rules (should allow read/write)")
        print("4. Ensure 'requests' library is installed: pip install requests")
