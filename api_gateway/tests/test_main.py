import pytest
from main import create_app
import os
from dotenv import load_dotenv


@pytest.fixture
def app():
    app = create_app()
    return app


def test_create_app(app):
    assert app is not None
    assert app.config['JWT_SECRET'] is not None
    assert app.config['JWT_PREFIX'] == 'Bearer'


def test_dotenv_loading():
    load_dotenv()
    assert os.getenv('JWT_SECRET') is not None
    assert os.getenv('JWT_PREFIX') == 'Bearer'
