from flask import Flask, jsonify
from routes.parcel_locker import clients_blueprint, packages_blueprint, parcel_lockers_blueprint
from routes.users import users_blueprint

app = Flask(__name__)


def create_app():

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

