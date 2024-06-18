from models.user import User
from models.auth import Auth
from extensions.extensions import db
from models.song import Song
from models.playlist import Playlist

class ModelFactory:
    """
    Factory class to create instances of models.
    """

    @staticmethod
    def create_user(name, email, password):
        """
        Create a User instance.

        :param name: User's name
        :param email: User's email
        :param password: User's password
        :return: User instance
        """
        new_user = User(name=name, email=email)
        db.session.add(new_user)
        db.session.commit()

        new_auth = Auth(email=email, password=password, user_id=new_user.id)
        db.session.add(new_auth)
        db.session.commit()

        return new_user

    @staticmethod
    def create_song(title, artist, album, duration):
        """
        Create a Song instance.

        :param title: Song title
        :param artist: Song artist
        :param album: Song album
        :param duration: Song duration
        :return: Song instance
        """
        return Song(title=title, artist=artist, album=album, duration=duration)

    @staticmethod
    def create_playlist(name, user_id):
        """
        Create a Playlist instance.

        :param name: Playlist name
        :param user_id: User ID associated with the playlist
        :return: Playlist instance
        """
        return Playlist(name=name, user_id=user_id)
