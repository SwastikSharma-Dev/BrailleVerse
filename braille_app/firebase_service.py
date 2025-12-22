"""
Firebase Service Module for Braille Display Integration

This module handles all Firebase communication for sending text to the braille device.
It splits text into chunks based on device capacity and sends them sequentially.
"""

import time
import json
from django.conf import settings

# Import requests for REST API
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    print("Warning: requests not installed. Install with: pip install requests")

# Import Firebase Admin SDK
try:
    import firebase_admin
    from firebase_admin import credentials, db
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("Warning: firebase-admin not installed. Using REST API mode")


class FirebaseService:
    """
    Service class for Firebase Realtime Database operations.
    Handles initialization, text chunking, and sequential sending to braille device.
    """
    
    _initialized = False
    
    @classmethod
    def initialize(cls):
        """
        Initialize Firebase with REST API or Admin SDK.
        Uses REST API if Admin SDK not available or credentials missing.
        """
        if cls._initialized:
            return
        
        if not FIREBASE_AVAILABLE:
            print("Firebase Admin SDK not installed - using REST API mode")
            cls._initialized = True
            return
        
        try:
            # Try to initialize with Admin SDK if credentials exist
            cred_path = settings.FIREBASE_CREDENTIALS_PATH
            if cred_path and hasattr(credentials, 'Certificate'):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': settings.FIREBASE_CONFIG.get('databaseURL')
                })
                cls._initialized = True
                print("Firebase Admin SDK initialized successfully")
        except Exception as e:
            print(f"Firebase Admin SDK initialization skipped: {e}")
            print("Using REST API mode with auth token")
            cls._initialized = True
    
    @staticmethod
    def chunk_text(text, chunk_size=None):
        """
        Split text into chunks based on device character limit.
        
        Args:
            text (str): The text to split
            chunk_size (int): Maximum characters per chunk (defaults to settings.DEVICE_CHAR_LIMIT)
        
        Returns:
            list: List of text chunks
        """
        if chunk_size is None:
            chunk_size = settings.DEVICE_CHAR_LIMIT
        
        # Split text into chunks without breaking words
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 for space
            
            if current_length + word_length > chunk_size:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = [word]
                    current_length = word_length
                else:
                    # Single word is longer than chunk_size, split it
                    chunks.append(word[:chunk_size])
                    current_chunk = [word[chunk_size:]] if len(word) > chunk_size else []
                    current_length = len(current_chunk[0]) if current_chunk else 0
            else:
                current_chunk.append(word)
                current_length += word_length
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    @classmethod
    def send_text_to_device(cls, text, delay=None):
        """
        Main function to send text to the braille device.
        
        This function:
        1. Splits text into appropriate chunks
        2. Sends each chunk sequentially to Firebase
        3. Includes delays between chunks if specified
        
        Args:
            text (str): The text to send to the braille device
            delay (float): Delay between chunks in seconds (defaults to settings.CHUNK_SEND_DELAY)
        
        Returns:
            dict: Result with status and details
        """
        if not text:
            return {'status': 'error', 'message': 'No text provided'}
        
        if delay is None:
            delay = settings.CHUNK_SEND_DELAY
        
        # Chunk the text
        chunks = cls.chunk_text(text)
        
        result = {
            'status': 'success',
            'total_chunks': len(chunks),
            'chunks_sent': 0,
            'mode': 'firebase' if cls._initialized and FIREBASE_AVAILABLE else 'mock'
        }
        
        try:
            for i, chunk in enumerate(chunks):
                if cls._initialized and FIREBASE_AVAILABLE:
                    # Try Admin SDK first
                    try:
                        ref = db.reference(settings.FIREBASE_TEXT_PATH)
                        ref.set({
                            'text': chunk,
                            'chunk_number': i + 1,
                            'total_chunks': len(chunks),
                            'timestamp': time.time()
                        })
                    except:
                        # Fallback to REST API
                        cls._send_via_rest_api(chunk, i + 1, len(chunks))
                else:
                    # Use REST API directly
                    cls._send_via_rest_api(chunk, i + 1, len(chunks))
                
                result['chunks_sent'] += 1
                
                # Add delay between chunks (except after last chunk)
                if i < len(chunks) - 1 and delay > 0:
                    time.sleep(delay)
            
            result['message'] = f"Successfully sent {len(chunks)} chunk(s) to braille device"
            
        except Exception as e:
            result['status'] = 'error'
            result['message'] = f"Error sending text: {str(e)}"
        
        return result
    
    @classmethod
    def _send_via_rest_api(cls, text, chunk_num, total_chunks, retry_count=0):
        """
        Send data to Firebase using REST API with retry logic and SSL error handling.
        Used when Admin SDK is not available.
        """
        if not REQUESTS_AVAILABLE:
            print(f"[MOCK] Chunk {chunk_num}/{total_chunks}: {text[:50]}...")
            print("Install 'requests' library: pip install requests")
            return
        
        database_url = settings.FIREBASE_CONFIG.get('databaseURL')
        auth_token = settings.FIREBASE_CONFIG.get('authToken')
        
        if not database_url or not auth_token:
            print(f"[MOCK] Chunk {chunk_num}/{total_chunks}: {text[:50]}...")
            return
        
        max_retries = 3
        retry_delay = 1  # seconds
        
        for attempt in range(max_retries):
            try:
                # Firebase REST API endpoint
                path = settings.FIREBASE_TEXT_PATH.strip('/')
                url = f"{database_url}/{path}.json?auth={auth_token}"
                
                data = {
                    'text': text,
                    'chunk_number': chunk_num,
                    'total_chunks': total_chunks,
                    'timestamp': time.time()
                }
                
                # Create a session with retry adapter for better SSL handling
                session = requests.Session()
                adapter = requests.adapters.HTTPAdapter(
                    max_retries=requests.adapters.Retry(
                        total=3,
                        backoff_factor=0.5,
                        status_forcelist=[500, 502, 503, 504]
                    )
                )
                session.mount('https://', adapter)
                
                # Send request with extended timeout and keep-alive disabled
                response = session.put(
                    url, 
                    json=data, 
                    timeout=15,
                    headers={'Connection': 'close'}  # Disable keep-alive to avoid SSL EOF errors
                )
                response.raise_for_status()
                session.close()
                print(f"✓ Sent chunk {chunk_num}/{total_chunks} to Firebase via REST API")
                return
                
            except requests.exceptions.SSLError as ssl_err:
                print(f"⚠ SSL Error on attempt {attempt + 1}/{max_retries}: {ssl_err}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                    continue
                else:
                    print(f"✗ Failed after {max_retries} attempts due to SSL error")
                    raise
                    
            except requests.exceptions.ConnectionError as conn_err:
                print(f"⚠ Connection Error on attempt {attempt + 1}/{max_retries}: {conn_err}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                else:
                    raise
                    
            except Exception as e:
                print(f"✗ Error sending to Firebase: {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                else:
                    raise
    
    @classmethod
    def send_single_message(cls, message):
        """
        Send a single short message without chunking.
        Use for quick notifications or short responses.
        
        Args:
            message (str): Short message to send
        
        Returns:
            dict: Result with status
        """
        try:
            if cls._initialized and FIREBASE_AVAILABLE:
                try:
                    ref = db.reference(settings.FIREBASE_TEXT_PATH)
                    ref.set({
                        'text': message,
                        'timestamp': time.time(),
                        'type': 'notification'
                    })
                except:
                    cls._send_via_rest_api(message, 1, 1)
            else:
                cls._send_via_rest_api(message, 1, 1)
            
            return {'status': 'success', 'message': 'Message sent'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}


# Initialize Firebase when module is imported
FirebaseService.initialize()


# Convenience function for easy import
def send_text_to_braille_device(text, delay=None):
    """
    Convenience function to send text to braille device.
    
    Usage:
        from braille_app.firebase_service import send_text_to_braille_device
        result = send_text_to_braille_device("Hello, this is a test message")
    
    Args:
        text (str): Text to send
        delay (float): Optional delay between chunks
    
    Returns:
        dict: Result dictionary with status and details
    """
    return FirebaseService.send_text_to_device(text, delay)
