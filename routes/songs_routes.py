from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models.song import Song
from extensions.extensions import db
from schemas.song_schema import song_schema, songs_schema
from logs.logging_config import logger
from marshmallow import ValidationError

songs_bp = Blueprint('songs', __name__)

@songs_bp.route('/songs', methods=['GET'])
@jwt_required()
def get_songs():
    """
    Get a list of all songs.
    ---
    tags:
      - Songs
    security:
      - Bearer: []
    responses:
      200:
        description: A list of songs
        schema:
          type: array
          items:
            $ref: '#/definitions/Song'
    """
    songs = Song.query.all()
    return jsonify(songs_schema.dump(songs)), 200

@songs_bp.route('/songs/<int:id>', methods=['GET'])
@jwt_required()
def get_song(id):
    """
    Get a specific song by ID.
    ---
    tags:
      - Songs
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        description: The ID of the song to retrieve
        required: true
        type: integer
    responses:
      200:
        description: Song retrieved successfully
        schema:
          $ref: '#/definitions/Song'
      404:
        description: Song not found
    """
    song = Song.query.get(id)
    if not song:
        logger.error(f"Song with id {id} not found")
        return jsonify({'error': 'Song not found'}), 404
    return jsonify(song_schema.dump(song)), 200

@songs_bp.route('/songs', methods=['POST'])
@jwt_required()
def create_song():
    """
    Create a new song.
    ---
    tags:
      - Songs
    security:
      - Bearer: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        description: The song to create
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Song Title"
            artist:
              type: string
              example: "Artist Name"
            album:
              type: string
              example: "Album Name"
            duration:
              type: integer
              example: 240
    responses:
      201:
        description: Song created successfully
        schema:
          $ref: '#/definitions/Song'
    """
    try:
        data = request.get_json()
        song_data = song_schema.load(data)
    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return jsonify(err.messages), 400

    new_song = Song(**song_data)
    db.session.add(new_song)
    db.session.commit()
    logger.info(f"Song {new_song.title} created successfully")
    return jsonify(song_schema.dump(new_song)), 201

@songs_bp.route('/songs/<int:id>', methods=['PUT'])
@jwt_required()
def update_song(id):
    """
    Update an existing song.
    ---
    tags:
      - Songs
    security:
      - Bearer: []
    consumes:
      - application/json
    parameters:
      - in: path
        name: id
        description: The ID of the song to update
        required: true
        type: integer
      - in: body
        name: body
        description: The updated song data
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: "Song Title"
            artist:
              type: string
              example: "Artist Name"
            album:
              type: string
              example: "Album Name"
            duration:
              type: integer
              example: 240
    responses:
      200:
        description: Song updated successfully
        schema:
          $ref: '#/definitions/Song'
    """
    song = Song.query.get(id)
    if not song:
        logger.error(f"Song with id {id} not found")
        return jsonify({"msg": "Song not found"}), 404

    try:
        data = request.get_json()
        song_data = song_schema.load(data, partial=True)
    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return jsonify(err.messages), 400

    for key, value in song_data.items():
        setattr(song, key, value)

    db.session.commit()
    logger.info(f"Song with id {id} updated successfully")
    return jsonify(song_schema.dump(song)), 200

@songs_bp.route('/songs/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_song(id):
    """
    Delete an existing song.
    ---
    tags:
      - Songs
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        description: The ID of the song to delete
        required: true
        type: integer
    responses:
      200:
        description: Song deleted successfully
    """
    song = Song.query.get(id)
    if not song:
        logger.error(f"Song with id {id} not found")
        return jsonify({'error': 'Song not found'}), 404

    db.session.delete(song)
    db.session.commit()
    logger.info(f"Song with id {id} deleted successfully")
    return jsonify({'message': 'Song deleted successfully'}), 200
