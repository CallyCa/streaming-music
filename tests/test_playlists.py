import unittest
import json
from app import create_app
from extensions.extensions import db
from models.auth import Auth
from models.user import User
from models.playlist import Playlist

class PlaylistTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Criar um usuário de teste e obter o token de acesso
        user = User(name="Test User", email="test@example.com")
        db.session.add(user)
        db.session.commit()

        auth = Auth(email="test@example.com", password="testpassword", user_id=user.id)
        db.session.add(auth)
        db.session.commit()

        self.token = self.get_access_token("test@example.com", "testpassword")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_access_token(self, email, password):
        response = self.client.post('/login', data=json.dumps({
            "email": email,
            "password": password
        }), content_type='application/json')
        data = json.loads(response.data)
        return data['access_token']

    def test_create_playlist(self):
        response = self.client.post('/playlists', data=json.dumps({
            "name": "My Playlist"
        }), headers={
            'Authorization': f'Bearer {self.token}'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_delete_playlist(self):
        playlist = Playlist(name="My Playlist", user_id=1)
        db.session.add(playlist)
        db.session.commit()
        response = self.client.delete(f'/playlists/{playlist.id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, 200)

    def test_update_playlist(self):
        playlist = Playlist(name="My Playlist", user_id=1)
        db.session.add(playlist)
        db.session.commit()
        response = self.client.put(f'/playlists/{playlist.id}', data=json.dumps({
            "name": "Updated Playlist"
        }), headers={
            'Authorization': f'Bearer {self.token}'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
