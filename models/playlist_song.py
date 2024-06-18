from extensions.extensions import db

class PlaylistSong(db.Model):
    """
    Association table for Playlist and Song.
    ---
    components:
      schemas:
        PlaylistSong:
          type: object
          properties:
            playlist_id:
              type: integer
            song_id:
              type: integer
    """
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), primary_key=True)
