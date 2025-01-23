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
import logging

logging.basicConfig(level=logging.INFO)


def create_app() -> Flask:
    app = Flask(__name__)

    with app.app_context():
        ENV_FILENAME = '.env'
        ENV_PATH = Path.cwd().absolute().joinpath(f'{ENV_FILENAME}')
        load_dotenv(ENV_PATH)

        @app.errorhandler(Exception)
        def handle_error(error: Exception):
            return {'message': str(error)}, 500

        db_username = getenv('DB_USERNAME', 'user')
        db_password = getenv('DB_PASSWORD', 'user1234')
        db_port = getenv('DB_PORT', 3307)
        db_name = getenv('DB_NAME', 'db_1')
        db_hostname = getenv('DB_HOSTNAME', 'mysql')

        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_name}'
        app.config['SQLALCHEMY_ECHO'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        sa.init_app(app)
        migrate = Migrate(app, sa)

        mail_settings = {
            'MAIL_SERVER': getenv('MAIL_SERVER', 'smtp.gmail.com'),
            'MAIL_PORT': int(getenv('MAIL_PORT', 465)),
            'MAIL_USE_SSL': bool(getenv('MAIL_USE_SSL', True)),
            'MAIL_USERNAME': getenv('MAIL_USERNAME', 'testowy2.kmprograms@gmail.com'),
            'MAIL_PASSWORD': getenv('MAIL_PASSWORD', 'jjtdkjurrfqdgqxu'),
        }
        logging.info(mail_settings)
        app.config.update(mail_settings)
        MailSender(app, getenv('MAIL_USERNAME', 'testowy2.kmprograms@gmail.com'))

        api = Api(app)
        api.add_resource(RegisterUserResource, '/users/register')
        api.add_resource(ActivationUserResource, '/users/activate')

        return app
