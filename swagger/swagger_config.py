swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Music Streaming API",
        "description": "API for a music streaming service",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer {token}'"
        }
    },
    "security": [
        {
            "Bearer": []
        }
    ],
    "definitions": {
        "User": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string"}
            }
        },
        "Auth": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "email": {"type": "string"},
                "password": {"type": "string"},
                "user_id": {"type": "integer"}
            }
        },
        "Song": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "title": {"type": "string"},
                "artist": {"type": "string"},
                "album": {"type": "string"},
                "duration": {"type": "integer"}
            }
        },
        "Playlist": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "user_id": {"type": "integer"},
                "songs": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/Song"}
                }
            }
        },
        "PlaylistSong": {
            "type": "object",
            "properties": {
                "playlist_id": {"type": "integer"},
                "song_id": {"type": "integer"}
            }
        }
    }
}
