import pytest
from unittest.mock import patch
from main import create_app
from app.db.configuration import sa


@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def client(app):
    return app.test_client()


@pytest.fixture(scope='module')
def db_session(app):
    with app.app_context():
        yield sa.session
        sa.session.rollback()
