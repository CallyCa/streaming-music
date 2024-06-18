import logging
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.playlist import Playlist
from extensions.extensions import db
from schemas.playlist_schema import playlist_schema, playlists_schema
from logs.logging_config import logger
from marshmallow import ValidationError

playlists_bp = Blueprint('playlists', __name__)

@playlists_bp.route('/playlists', methods=['GET'])
@jwt_required()
def get_playlists():
    """
    Get a list of all playlists.
    ---
    tags:
      - Playlists
    security:
      - Bearer: []
    responses:
      200:
        description: A list of playlists
        schema:
          type: array
          items:
            $ref: '#/definitions/Playlist'
    """
    playlists = Playlist.query.all()
    return jsonify(playlists_schema.dump(playlists)), 200

@playlists_bp.route('/playlists/<int:id>', methods=['GET'])
@jwt_required()
def get_playlist(id):
    """
    Get a specific playlist by ID.
    ---
    tags:
      - Playlists
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        description: The ID of the playlist to retrieve
        required: true
        type: integer
    responses:
      200:
        description: Playlist retrieved successfully
        schema:
          $ref: '#/definitions/Playlist'
      404:
        description: Playlist not found
    """
    playlist = Playlist.query.get(id)
    if not playlist:
        logger.error(f"Playlist with id {id} not found")
        return jsonify({'error': 'Playlist not found'}), 404
    return jsonify(playlist_schema.dump(playlist)), 200

@playlists_bp.route('/playlists', methods=['POST'])
@jwt_required()
def create_playlist():
    """
    Create a new playlist.
    ---
    tags:
      - Playlists
    security:
      - Bearer: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        description: The playlist to create
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "My Playlist"
            user_id:
              type: integer
              example: 1
            songs:
              type: array
              items:
                type: integer
                example: 1
    responses:
      201:
        description: Playlist created successfully
        schema:
          $ref: '#/definitions/Playlist'
    """
    data = request.get_json()
    logging.info(f"Request data: {data}")

    if not data:
        return jsonify({"msg": "Missing JSON in request"}), 400

    name = data.get('name')
    user_id = get_jwt_identity()

    if not name:
        return jsonify({"msg": "Missing playlist name"}), 400

    new_playlist = Playlist(name=name, user_id=user_id)
    db.session.add(new_playlist)
    db.session.commit()

    return jsonify(new_playlist.to_dict()), 201

@playlists_bp.route('/playlists/<int:id>', methods=['PUT'])
@jwt_required()
def update_playlist(id):
    """
    Update an existing playlist.
    ---
    tags:
      - Playlists
    security:
      - Bearer: []
    consumes:
      - application/json
    parameters:
      - in: path
        name: id
        description: The ID of the playlist to update
        required: true
        type: integer
      - in: body
        name: body
        description: The updated playlist data
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "My Playlist"
            songs:
              type: array
              items:
                type: integer
                example: 1
    responses:
      200:
        description: Playlist updated successfully
        schema:
          $ref: '#/definitions/Playlist'
    """
    playlist = Playlist.query.get(id)
    if not playlist:
        logger.error(f"Playlist with id {id} not found")
        return jsonify({"msg": "Playlist not found"}), 404

    try:
        data = request.get_json()
        playlist_data = playlist_schema.load(data, partial=True)
    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return jsonify(err.messages), 400

    for key, value in playlist_data.items():
        setattr(playlist, key, value)

    db.session.commit()
    logger.info(f"Playlist with id {id} updated successfully")
    return jsonify(playlist_schema.dump(playlist)), 200

@playlists_bp.route('/playlists/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_playlist(id):
    """
    Delete an existing playlist.
    ---
    tags:
      - Playlists
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        description: The ID of the playlist to delete
        required: true
        type: integer
    responses:
      200:
        description: Playlist deleted successfully
    """
    playlist = Playlist.query.get(id)
    if not playlist:
        logger.error(f"Playlist with id {id} not found")
        return jsonify({'error': 'Playlist not found'}), 404

    db.session.delete(playlist)
    db.session.commit()
    logger.info(f"Playlist with id {id} deleted successfully")
    return jsonify({'message': 'Playlist deleted successfully'}), 200
