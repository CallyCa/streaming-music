import os
from flask import Flask, redirect, jsonify
from config.config import config
from extensions.extensions import db, migrate
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from logs.logging_config import logger

# Importar a configuração do Swagger e os manipuladores de erro
from swagger.swagger_config import swagger_config, swagger_template
from errors.error_handlers import register_error_handlers

def create_app(config_name=None):
    """
    Create and configure the Flask application.

    :return: Configured Flask application instance.
    """
    app = Flask(__name__)

    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')
    elif isinstance(config_name, object):  # Handle ScriptInfo object
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    # Configurar Swagger
    Swagger(app, config=swagger_config, template=swagger_template)

    jwt = JWTManager(app)

    with app.app_context():
        # Importar rotas usando Blueprints
        from routes.users_routes import users_bp
        from routes.songs_routes import songs_bp
        from routes.playlists_routes import playlists_bp
        from routes.auth_routes import auth_bp

        app.register_blueprint(users_bp)
        app.register_blueprint(songs_bp)
        app.register_blueprint(playlists_bp)
        app.register_blueprint(auth_bp)

        db.create_all()

    # Importar manipuladores de erro
    register_error_handlers(app)

    @app.route('/')
    def index():
        return redirect('/apidocs')

    return app
