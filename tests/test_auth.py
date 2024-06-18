import unittest
import json
from app import create_app
from extensions.extensions import db
from models.auth import Auth
from models.user import User

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Criar um usuário de teste
        user = User(name="Test User", email="test@example.com")
        db.session.add(user)
        db.session.commit()

        auth = Auth(email="test@example.com", password="testpassword", user_id=user.id)
        db.session.add(auth)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user(self):
        response = self.client.post('/register', data=json.dumps({
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123"
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        response = self.client.post('/login', data=json.dumps({
            "email": "test@example.com",
            "password": "testpassword"
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)

    def test_login_invalid_user(self):
        response = self.client.post('/login', data=json.dumps({
            "email": "wrong@example.com",
            "password": "wrongpassword"
        }), content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_register_existing_user(self):
        response = self.client.post('/register', data=json.dumps({
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
