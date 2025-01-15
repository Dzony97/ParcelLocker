from flask import Flask, request, jsonify, Response
from flask_restful import Api
from os import getenv
from dotenv import load_dotenv
from pathlib import Path
from users.app.db.configuration import sa
from users.app.db.entity import UserEntity, ClientEntity
import logging

logging.basicConfig(level=logging.INFO)


def create_app() -> Flask:
    app = Flask(__name__)

    with app.app_context():
        @app.route('/', methods=['GET'])
        def index() -> Response:
            return {'api_gateway': 'application works'}

        @app.errorhandler(Exception)
        def handle_error(error: Exception):
            return {'message': str(error)}, 500

        db_username = getenv('DB_USERNAME', 'user')
        db_password = getenv('DB_PASSWORD', 'user1234')
        db_port = getenv('DB_PORT', 3307)
        db_name = getenv('DB_NAME', 'db_1')
        db_hostname = getenv('DB_HOST', 'mysql')

        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{db_username}:{db_password}@mysql:{db_port}/{db_name}'
        app.config['SQLALCHEMY_ECHO'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        sa.init_app(app)
        logging.info('----- [ BEFORE CREATE ALL ] -----')
        sa.drop_all()
        sa.create_all()
        logging.info('----- [ AFTER CREATE ALL ] ------')

        return app
