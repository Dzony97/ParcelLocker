from flask import Flask, jsonify
from routes.parcel_locker import clients_blueprint, packages_blueprint, parcel_lockers_blueprint
from routes.users import users_blueprint
from dotenv import load_dotenv
import os

app = Flask(__name__)


def create_app():
    load_dotenv()

    app.config['JWT_ISSUER'] = os.getenv('JWT_ISSUER')
    app.config['JWT_AUTHTYPE'] = os.getenv('JWT_AUTHTYPE')
    app.config['JWT_SECRET'] = os.getenv('JWT_SECRET')
    app.config['JWT_ACCESS_MAX_AGE'] = int(os.getenv('JWT_ACCESS_MAX_AGE'))
    app.config['JWT_REFRESH_MAX_AGE'] = int(os.getenv('JWT_REFRESH_MAX_AGE'))
    app.config['JWT_PREFIX'] = os.getenv('JWT_PREFIX')

    with app.app_context():
        @app.errorhandler(Exception)
        def handle_error(error: Exception):
            error_message = error.args[0]
            return jsonify({'error': error_message}), 500

        # --- USERS mikroserwis ---
        app.register_blueprint(users_blueprint)

        # --- PARCEL_LOCKERS mikroserwis ---
        app.register_blueprint(clients_blueprint)
        app.register_blueprint(packages_blueprint)
        app.register_blueprint(parcel_lockers_blueprint)

        return app

