from unittest import TestCase
from app import app
from models import db, User, connect_db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyTests(TestCase):
    "Tests for our Blogly user management app."

    def setUp(self):
        "Add sample data for test db"

        User.query.delete()

        # Add user
        brit = User(first_name = "Brit", last_name="Juravic")

        # Add new object to session, so they'll persist
        db.session.add(brit)

        # Commit--otherwise, this never gets saved!
        db.session.commit()

        self.user_id = brit.id

    def tearDown(self):
        "Cleanup bad transactions"

        db.session.rollback()

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

    def test_user_detail(self):
        "Test route for viewing a specific user detail page"
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Brit Juravic</h1>', html)