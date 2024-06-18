from marshmallow import Schema, fields, validate

class SongSchema(Schema):
    """
    Schema for serializing and deserializing Song objects.
    
    Attributes:
        id (fields.Int): The song's ID.
        title (fields.Str): The song's title.
        artist (fields.Str): The artist of the song.
        album (fields.Str): The album of the song.
        duration (fields.Int): The duration of the song in seconds.
    """
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1))
    artist = fields.Str(required=True, validate=validate.Length(min=1))
    album = fields.Str(required=True, validate=validate.Length(min=1))
    duration = fields.Int(required=True)

song_schema = SongSchema()
songs_schema = SongSchema(many=True)