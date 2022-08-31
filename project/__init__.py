from flask import Flask,jsonify
import os 
from project.auth import auth
from project.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from project.numbers import numbers
from project.database import db
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from project.config.swagger import template,swagger_config

def create_app(test_configuration=None):

    app = Flask(__name__,
    instance_relative_config=True)

    if test_configuration is None:

        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY"),

            SWAGGER={
                'title': "Bookmarks API",
                'uiversion': 3
            }
        )
    else:
        app.config.from_mapping(test_configuration)
    
    @app.route('/')
    def index():
        return jsonify({"message":"Hello world"})

    #Handle errors
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'error':'Not found'}),HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'error':'Something went wrong, we are working on it'}),HTTP_500_INTERNAL_SERVER_ERROR

    db.app=app
    db.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(numbers)

    Swagger(app, config=swagger_config, template=template)

    return app
        