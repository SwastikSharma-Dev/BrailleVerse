from django.test import TestCase, Client
from django.urls import reverse


class LandingPageTests(TestCase):
    """Tests for the landing page"""
    
    def setUp(self):
        self.client = Client()
    
    def test_landing_page_loads(self):
        """Test that landing page loads successfully"""
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome')
    
    def test_landing_page_has_options(self):
        """Test that landing page contains navigation options"""
        response = self.client.get(reverse('landing'))
        self.assertContains(response, 'Visually Impaired')
        self.assertContains(response, 'Helper')


class MainMenuTests(TestCase):
    """Tests for the main menu"""
    
    def setUp(self):
        self.client = Client()
    
    def test_main_menu_loads(self):
        """Test that main menu loads successfully"""
        response = self.client.get(reverse('main_menu'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Main Menu')
    
    def test_main_menu_has_all_options(self):
        """Test that main menu contains all expected options"""
        response = self.client.get(reverse('main_menu'))
        self.assertContains(response, 'Send Custom Text')
        self.assertContains(response, 'Voice Assistant')
        self.assertContains(response, 'News')
        self.assertContains(response, 'Books')


class CustomTextTests(TestCase):
    """Tests for custom text functionality"""
    
    def setUp(self):
        self.client = Client()
    
    def test_custom_text_page_loads(self):
        """Test that custom text page loads"""
        response = self.client.get(reverse('custom_text'))
        self.assertEqual(response.status_code, 200)
    
    def test_custom_text_submission(self):
        """Test submitting custom text"""
        response = self.client.post(reverse('custom_text'), {
            'text': 'This is a test message for the braille device.'
        })
        self.assertEqual(response.status_code, 200)
        # Should see success message
        self.assertContains(response, 'Text sent')


class FirebaseServiceTests(TestCase):
    """Tests for Firebase service module"""
    
    def test_text_chunking(self):
        """Test that text is properly chunked"""
        from braille_app.firebase_service import FirebaseService
        
        text = "This is a test message that should be split into multiple chunks based on the character limit."
        chunks = FirebaseService.chunk_text(text, chunk_size=20)
        
        # Should create multiple chunks
        self.assertGreater(len(chunks), 1)
        
        # Each chunk should be within limit
        for chunk in chunks:
            self.assertLessEqual(len(chunk), 20)
    
    def test_empty_text_handling(self):
        """Test handling of empty text"""
        from braille_app.firebase_service import send_text_to_braille_device
        
        result = send_text_to_braille_device('')
        self.assertEqual(result['status'], 'error')


# Add more tests as needed
