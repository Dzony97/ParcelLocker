from flask import Flask, request, jsonify, Response
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import getenv
from dotenv import load_dotenv
from pathlib import Path
from app.db.configuration import sa
from app.mail.configuration import MailSender
from app.db.entity import UserEntity, ClientEntity
from app.routes.resource import RegisterUserResource, ActivationUserResource
from app.config import MAIL_SETTINGS, DB_URL, JWT_CONFIG
from app.security.configuration import configure_security
import logging

logging.basicConfig(level=logging.INFO)


def create_app() -> Flask:
    app = Flask(__name__)

    with app.app_context():

        @app.errorhandler(Exception)
        def handle_error(error: Exception):
            return {'message': str(error)}, 500

        app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
        app.config['SQLALCHEMY_ECHO'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        sa.init_app(app)
        migrate = Migrate(app, sa)

        app.config.update(MAIL_SETTINGS)
        MailSender(app, MAIL_SETTINGS['MAIL_USERNAME'])

        app.config.update(JWT_CONFIG)
        configure_security(app)

        api = Api(app)
        api.add_resource(RegisterUserResource, '/users/register')
        api.add_resource(ActivationUserResource, '/users/activate')

        return app
