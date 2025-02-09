from flask import Flask, request, jsonify
from dotenv import load_dotenv
from pathlib import Path
from os import getenv
from app.routes.customers import clients_blueprint, packages_blueprint
from app.routes.management import parcel_lockers_blueprint
import logging

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)


def create_app() -> Flask:
    with app.app_context():
        ENV_FILENAME = '.env'
        ENV_PATH = Path.cwd().absolute().joinpath(f'{ENV_FILENAME}')
        load_dotenv(ENV_PATH)

        @app.errorhandler(Exception)
        def handle_error(error: Exception):
            error_message = error.args[0]
            return jsonify({'error': error_message}), 500

        app.register_blueprint(clients_blueprint)
        app.register_blueprint(packages_blueprint)
        app.register_blueprint(parcel_lockers_blueprint)

        return app
