import unittest
import json
from app import create_app, db

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        
        db.create_all()
        self.create_test_user()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def create_test_user(self):
        self.client.post('/register', data=json.dumps({
            'name': 'John Doe',
            'email': 'john@example.com',
            'password': 'password123'
        }), content_type='application/json')

    def get_access_token(self):
        response = self.client.post('/login', data=json.dumps({
            'email': 'john@example.com',
            'password': 'password123'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
        return data['access_token']

    def test_delete_user(self):
        response = self.client.delete('/users/1', headers={
            'Authorization': f'Bearer {self.get_access_token()}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('User deleted successfully', str(response.data))

    def test_get_user(self):
        response = self.client.get('/users/1', headers={
            'Authorization': f'Bearer {self.get_access_token()}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('John Doe', str(response.data))

    def test_update_user(self):
        response = self.client.put('/users/1', headers={
            'Authorization': f'Bearer {self.get_access_token()}'
        }, data=json.dumps({
            'name': 'John Updated',
            'email': 'john_updated@example.com'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('John Updated', str(response.data))
