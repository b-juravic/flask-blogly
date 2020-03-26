from unittest import TestCase
from app import app

class BloglyTests(TestCase):
    "Tests for our Blogly user management app."

    def test_home_page(self):
        """Test to check the home page route and ensure
        it redirects to users list."""
        with app.test_client() as client:
            resp = client.get('/')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/users")
    
    def test_users_list(self):
        """Test to check the users list route and ensure
        it redirects to users list."""
        with app.test_client() as client:
            resp = client.get('/')

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "http://localhost/users")
    
