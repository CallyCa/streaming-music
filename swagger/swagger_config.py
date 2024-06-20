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
                "email": {"type": "string"},
                "nickname": {"type": "string"}
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
    },
    "paths": {
        "/users": {
            "get": {
                "tags": ["Users"],
                "summary": "Get a list of all users",
                "security": [{"Bearer": []}],
                "responses": {
                    "200": {
                        "description": "A list of users",
                        "schema": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/User"}
                        }
                    }
                }
            },
            "post": {
                "tags": ["Users"],
                "summary": "Create a new user",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "in": "body",
                        "name": "body",
                        "description": "The user to create",
                        "required": True,
                        "schema": {
                            "$ref": "#/definitions/User"
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "User created successfully",
                        "schema": {"$ref": "#/definitions/User"}
                    }
                }
            }
        },
        "/users/{id}": {
            "get": {
                "tags": ["Users"],
                "summary": "Get a specific user by ID",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "description": "The ID of the user to retrieve",
                        "required": True,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "User retrieved successfully",
                        "schema": {"$ref": "#/definitions/User"}
                    },
                    "404": {
                        "description": "User not found"
                    }
                }
            },
            "put": {
                "tags": ["Users"],
                "summary": "Update an existing user",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "description": "The ID of the user to update",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "in": "body",
                        "name": "body",
                        "description": "The updated user data",
                        "required": True,
                        "schema": {
                            "$ref": "#/definitions/User"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "User updated successfully",
                        "schema": {"$ref": "#/definitions/User"}
                    }
                }
            },
            "delete": {
                "tags": ["Users"],
                "summary": "Delete an existing user",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "description": "The ID of the user to delete",
                        "required": True,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "User deleted successfully"
                    }
                }
            }
        },
        "/playlists": {
            "get": {
                "tags": ["Playlists"],
                "summary": "Get a list of all playlists",
                "security": [{"Bearer": []}],
                "responses": {
                    "200": {
                        "description": "A list of playlists",
                        "schema": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/Playlist"}
                        }
                    }
                }
            },
            "post": {
                "tags": ["Playlists"],
                "summary": "Create a new playlist",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "in": "body",
                        "name": "body",
                        "description": "The playlist to create",
                        "required": True,
                        "schema": {
                            "$ref": "#/definitions/Playlist"
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Playlist created successfully",
                        "schema": {"$ref": "#/definitions/Playlist"}
                    }
                }
            }
        },
        "/playlists/{id}": {
            "get": {
                "tags": ["Playlists"],
                "summary": "Get a specific playlist by ID",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "description": "The ID of the playlist to retrieve",
                        "required": True,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Playlist retrieved successfully",
                        "schema": {"$ref": "#/definitions/Playlist"}
                    },
                    "404": {
                        "description": "Playlist not found"
                    }
                }
            },
            "put": {
                "tags": ["Playlists"],
                "summary": "Update an existing playlist",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "description": "The ID of the playlist to update",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "in": "body",
                        "name": "body",
                        "description": "The updated playlist data",
                        "required": True,
                        "schema": {
                            "$ref": "#/definitions/Playlist"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Playlist updated successfully",
                        "schema": {"$ref": "#/definitions/Playlist"}
                    }
                }
            },
            "delete": {
                "tags": ["Playlists"],
                "summary": "Delete an existing playlist",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "description": "The ID of the playlist to delete",
                        "required": True,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Playlist deleted successfully"
                    }
                }
            }
        },
        "/songs": {
            "get": {
                "tags": ["Songs"],
                "summary": "Get a list of all songs",
                "security": [{"Bearer": []}],
                "responses": {
                    "200": {
                        "description": "A list of songs",
                        "schema": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/Song"}
                        }
                    }
                }
            },
            "post": {
                "tags": ["Songs"],
                "summary": "Create a new song",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "in": "body",
                        "name": "body",
                        "description": "The song to create",
                        "required": True,
                        "schema": {
                            "$ref": "#/definitions/Song"
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Song created successfully",
                        "schema": {"$ref": "#/definitions/Song"}
                    }
                }
            }
        },
        "/songs/{id}": {
            "get": {
                "tags": ["Songs"],
                "summary": "Get a specific song by ID",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "description": "The ID of the song to retrieve",
                        "required": True,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Song retrieved successfully",
                        "schema": {"$ref": "#/definitions/Song"}
                    },
                    "404": {
                        "description": "Song not found"
                    }
                }
            },
            "put": {
                "tags": ["Songs"],
                "summary": "Update an existing song",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "description": "The ID of the song to update",
                        "required": True,
                        "type": "integer"
                    },
                    {
                        "in": "body",
                        "name": "body",
                        "description": "The updated song data",
                        "required": True,
                        "schema": {
                            "$ref": "#/definitions/Song"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Song updated successfully",
                        "schema": {"$ref": "#/definitions/Song"}
                    }
                }
            },
            "delete": {
                "tags": ["Songs"],
                "summary": "Delete an existing song",
                "security": [{"Bearer": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "description": "The ID of the song to delete",
                        "required": True,
                        "type": "integer"
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Song deleted successfully"
                    }
                }
            }
        }
    }
}
