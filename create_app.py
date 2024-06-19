import os
from flask import Flask, redirect, jsonify
from config.config import config
from extensions.extensions import db, migrate
from flasgger import Swagger
from flask_jwt_extended import JWTManager
from logs.logging_config import logger
# REST
from routes.rest.users_routes import users_bp
from routes.rest.songs_routes import songs_bp
from routes.rest.playlists_routes import playlists_bp
from routes.rest.auth_routes import auth_bp
# GRAPHQL
from flask_graphql import GraphQLView
from routes.graphql.schema import schema

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
        # Importar rotas usando Blueprints REST
        app.register_blueprint(users_bp)
        app.register_blueprint(songs_bp)
        app.register_blueprint(playlists_bp)
        app.register_blueprint(auth_bp)

        db.create_all()

    # Importar manipuladores de erro
    register_error_handlers(app)

    # Adicionando o endpoint GraphQL
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=False  # desativa a interface do GraphiQL aqui
        )
    )

    # Adicionando um endpoint separado para a interface do GraphiQL
    app.add_url_rule(
        '/graphiql',
        view_func=GraphQLView.as_view(
            'graphiql',
            schema=schema,
            graphiql=True  # habilita a interface do GraphiQL aqui
        )
    )

    @app.route('/')
    def index():
        return redirect('/apidocs')

    return app
