import pytest
from main import create_app
from app.db.configuration import sa
from flask import Flask


@pytest.fixture
def app() -> Flask:
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        sa.create_all()
        yield app
        sa.session.remove()
        sa.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_session(app):
    with app.app_context():
        yield sa.session
        sa.session.rollback()
