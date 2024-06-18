from extensions.extensions import db

class Song(db.Model):
    """
    Song model for storing song details.
    ---
    components:
      schemas:
        Song:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            artist:
              type: string
            album:
              type: string
            duration:
              type: integer
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    album = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        """
        Convert Song object to dictionary.

        :return: Dictionary representation of Song.
        """
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'album': self.album,
            'duration': self.duration
        }
