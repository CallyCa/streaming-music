from extensions.extensions import db
from models.playlist_song import PlaylistSong

class Playlist(db.Model):
    """
    Playlist model for storing playlist details.

    :param id: Playlist ID
    :param name: Playlist name
    :param user_id: User ID associated with the playlist
    :param songs: List of songs in the playlist
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    songs = db.relationship('Song', secondary=PlaylistSong.__tablename__, lazy='subquery',
                            backref=db.backref('playlists', lazy=True))

    def to_dict(self):
        """
        Convert Playlist object to dictionary.

        :return: Dictionary representation of Playlist.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'songs': [song.to_dict() for song in self.songs]
        }
