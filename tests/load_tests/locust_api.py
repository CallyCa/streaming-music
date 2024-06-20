import logging
from abc import ABC, abstractmethod

from locust.clients import HttpSession


class LocustAPI(ABC):
    def __init__(self, client: HttpSession):
        self.client = client
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def register(self, name, email, password):
        pass

    def login(self, email, password):
        pass

    def create_user(self, name, email, password):
        pass

    def update_user(self, user_id, name, email, password):
        pass

    def delete_user(self, user_id):
        pass

    def get_users(self):
        pass

    def create_song(self, title, artist, album, duration):
        pass

    def update_song(self, song_id, title, artist, album, duration):
        pass

    def delete_song(self, song_id):
        pass

    def get_songs(self):
        pass

    def create_playlist(self, name):
        pass

    def get_playlists(self):
        pass
