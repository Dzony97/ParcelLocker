import pytest
from main import create_app
import os
from dotenv import load_dotenv


@pytest.fixture
def app():
    """
    Fixture to create and return a Flask application instance for testing.

    This fixture uses the `create_app` function to initialize the Flask application,
    allowing for testing of the application's behavior.

    :return: A Flask app instance.
    """
    app = create_app()
    return app


def test_create_app(app):
    """
    Test case to ensure the app is created properly and configuration values are set.

    This test checks if the Flask app is not `None` and verifies that required
    configuration values like `JWT_SECRET` and `JWT_PREFIX` are set correctly.

    :param app: The Flask application instance.
    :return: None
    """
    assert app is not None
    assert app.config['JWT_SECRET'] is not None
    assert app.config['JWT_PREFIX'] == 'Bearer'


def test_dotenv_loading():
    """
    Test case to ensure that environment variables are loaded correctly from the `.env` file.

    This test checks if the `JWT_SECRET` and `JWT_PREFIX` environment variables
    are correctly loaded from the `.env` file using `load_dotenv`.

    :return: None
    """
    load_dotenv()
    assert os.getenv('JWT_SECRET') is not None
    assert os.getenv('JWT_PREFIX') == 'Bearer'
