import pytest
from unittest.mock import patch
from main import create_app
from app.db.configuration import sa

@pytest.fixture(scope='module')
def app():
    """
    Fixture to create and configure a Flask app for testing. This fixture sets up
    the app with testing configurations such as in-memory SQLite database and
    disables modification tracking for SQLAlchemy.

    Yields:
        app (Flask): A Flask application instance configured for testing.
    """
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def client(app):
    """
    Fixture that provides a test client for making HTTP requests to the Flask app.

    Args:
        app (Flask): The Flask application instance created by the `app` fixture.

    Returns:
        FlaskClient: A test client for making requests to the Flask application.
    """
    return app.test_client()


@pytest.fixture(scope='module')
def db_session(app):
    """
    Fixture to provide a session for interacting with the database during tests.
    This session is rolled back after each test to ensure no persistent changes are made.

    Args:
        app (Flask): The Flask application instance created by the `app` fixture.

    Yields:
        session (SQLAlchemy Session): A database session for testing.
    """
    with app.app_context():
        yield sa.session
        sa.session.rollback()
