from marshmallow import Schema, fields, validate
from schemas.song_schema import SongSchema

class PlaylistSchema(Schema):
    """
    Schema for serializing and deserializing Playlist objects.
    
    Attributes:
        id (fields.Int): The playlist's ID.
        name (fields.Str): The name of the playlist.
        user_id (fields.Int): The ID of the user who owns the playlist.
        songs (fields.List): A list of songs in the playlist.
    """
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    user_id = fields.Int(required=True)
    songs = fields.List(fields.Nested(SongSchema))
    
playlist_schema = PlaylistSchema()
playlists_schema = PlaylistSchema(many=True)