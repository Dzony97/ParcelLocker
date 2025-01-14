from flask import Flask, request, jsonify, Response
from flask_restful import Api
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

        return app
