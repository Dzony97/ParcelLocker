import pytest
from dotenv import load_dotenv
from users.main import create_app

load_dotenv('.env.test')


@pytest.fixture
def app():
    """
    Creates a new instance of the Flask application for each test.

    The 'create_app()' function is defined in 'app.main', which sets up
    the Flask app, configures the database, mail, security, etc.
    This fixture yields the app inside its context.
    """
    test_app = create_app()
    test_app.config['TESTING'] = True

    with test_app.app_context():
        yield test_app


@pytest.fixture
def client(app):
    """
    Provides a Flask test client for sending HTTP requests to the app.
    The client is session-based, meaning that cookies persist during the test.
    """
    return app.test_client()
