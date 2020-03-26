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
        it displays list of users."""
        with app.test_client() as client:
            resp = client.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<a href="/users/{self.user_id}">Brit Juravic</a>', html)

    def test_create_user(self):
        "Test to ensure new user form appears"
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<form action="/users/new" method="POST">', html)

    def test_create_user_submit(self):
        "Test to ensure new user form data is added to the database."
        with app.test_client() as client:
            d = {"first_name": "Graham", "last_name": "Trail"}
            resp = client.post('/users/new', data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'>Graham Trail</a>', html)

    def test_user_detail(self):
        "Test route for viewing a specific user detail page"
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Brit Juravic</h1>', html)
    
    def test_edit_user(self):
        "Test to ensure edit user form appears"
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user_id}/edit')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<form action="/users/{self.user_id}/edit" method="POST">', html)
    
    def test_edit_user_submit(self):
        "Test to ensure edit user form data is changed in the database."
        with app.test_client() as client:
            d = {"first_name": "Sunshine", "last_name": "Simba"}
            
            resp = client.post(f'/users/{self.user_id}/edit', data=d, follow_redirects=True)            
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(">Sunshine Simba</a>", html)