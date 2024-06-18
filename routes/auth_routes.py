from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from models.auth import Auth
from models.user import User
from extensions.extensions import db
from schemas.user_schema import user_schema
from logs.logging_config import logger
from marshmallow import ValidationError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        description: The user's login credentials
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              example: "user@example.com"
            password:
              type: string
              example: "password123"
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            access_token:
              type: string
      400:
        description: Missing or invalid request body
      401:
        description: Invalid credentials
    """
    data = request.get_json()
    if not data:
        return jsonify({"msg": "Missing JSON in request"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    auth = Auth.query.filter_by(email=email).first()

    if auth and auth.check_password(password):
        access_token = create_access_token(identity=auth.user_id)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Invalid credentials"}), 401

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    User registration endpoint
    ---
    tags:
      - Authentication
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        description: The user's registration details
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
        description: User registered successfully
        schema:
          $ref: '#/definitions/User'
      400:
        description: Missing or invalid request body
    """
    try:
        data = request.get_json()
        user_data = user_schema.load(data)
    except ValidationError as err:
        logger.error(f"Validation error: {err.messages}")
        return jsonify(err.messages), 400

    if Auth.query.filter_by(email=user_data['email']).first():
        logger.error(f"Email {user_data['email']} already registered")
        return jsonify({"msg": "Email already registered"}), 400

    new_user = User(name=user_data['name'], email=user_data['email'])
    db.session.add(new_user)
    db.session.commit()

    new_auth = Auth(email=user_data['email'], password=user_data['password'], user_id=new_user.id)
    db.session.add(new_auth)
    db.session.commit()
    logger.info(f"User {new_user.name} registered successfully")
    return jsonify(user_schema.dump(new_user)), 201
