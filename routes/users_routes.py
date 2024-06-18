from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from models.auth import Auth
from models.user import User
from extensions.extensions import db
from factory.model_factory import ModelFactory
from schemas.user_schema import user_schema, users_schema
from marshmallow import ValidationError
from logs.logging_config import logger

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """
    Get a list of all users.
    ---
    tags:
      - Users
    security:
      - Bearer: []
    responses:
      200:
        description: A list of users
        schema:
          type: array
          items:
            $ref: '#/definitions/User'
    """
    users = User.query.all()
    return jsonify(users_schema.dump(users)), 200

@users_bp.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    """
    Get a specific user by ID.
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        description: The ID of the user to retrieve
        required: true
        type: integer
    responses:
      200:
        description: User retrieved successfully
        schema:
          $ref: '#/definitions/User'
      404:
        description: User not found
    """
    user = User.query.get(id)
    if not user:
        logger.error(f"User with id {id} not found")
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user_schema.dump(user)), 200

@users_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    """
    Create a new user.
    ---
    tags:
      - Users
    security:
      - Bearer: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        description: The user to create
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "John Doe"
            email:
              type: string
              example: "john@example.com"
            password:
              type: string
              example: "password123"
    responses:
      201:
        description: User created successfully
        schema:
          $ref: '#/definitions/User'
    """
    try:
        data = request.get_json()
        user_data = user_schema.load(data)
    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return jsonify(err.messages), 400

    if User.query.filter_by(email=user_data['email']).first() or Auth.query.filter_by(email=user_data['email']).first():
        logger.error(f"Email {user_data['email']} already registered")
        return jsonify({"msg": "Email already registered"}), 400

    new_user = ModelFactory.create_user(user_data['name'], user_data['email'], user_data['password'])
    return jsonify(user_schema.dump(new_user)), 201

@users_bp.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    """
    Update an existing user.
    ---
    tags:
      - Users
    security:
      - Bearer: []
    consumes:
      - application/json
    parameters:
      - in: path
        name: id
        description: The ID of the user to update
        required: true
        type: integer
      - in: body
        name: body
        description: The updated user data
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "John Doe"
            email:
              type: string
              example: "john@example.com"
            password:
              type: string
              example: "password123"
    responses:
      200:
        description: User updated successfully
        schema:
          $ref: '#/definitions/User'
    """
    user = User.query.get(id)
    if not user:
        logger.error(f"User with id {id} not found")
        return jsonify({"msg": "User not found"}), 404

    try:
        data = request.get_json()
        user_data = user_schema.load(data, partial=True)
    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return jsonify(err.messages), 400

    update_needed = False

    if 'name' in user_data and user_data['name'] != user.name:
        user.name = user_data['name']
        update_needed = True
    if 'email' in user_data and user_data['email'] != user.email:
        if User.query.filter_by(email=user_data['email']).first() or Auth.query.filter_by(email=user_data['email']).first():
            logger.error(f"Email {user_data['email']} already registered")
            return jsonify({"msg": "Email already registered"}), 400
        user.email = user_data['email']
        update_needed = True

    if 'password' in user_data:
        auth = Auth.query.filter_by(user_id=id).first()
        if auth and not auth.check_password(user_data['password']):
            auth.password = auth.set_password(user_data['password'])
            update_needed = True

    if update_needed:
        db.session.commit()
        logger.info(f"User with id {id} updated successfully")
        return jsonify(user_schema.dump(user)), 200
    else:
        logger.info(f"No changes detected for user with id {id}")
        return jsonify({"msg": "No changes detected"}), 200

@users_bp.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    """
    Delete an existing user.
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - in: path
        name: id
        description: The ID of the user to delete
        required: true
        type: integer
    responses:
      200:
        description: User deleted successfully
    """
    user = User.query.get(id)
    if not user:
        logger.error(f"User with id {id} not found")
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    logger.info(f"User with id {id} deleted successfully")
    return jsonify({'message': 'User deleted successfully'}), 200
