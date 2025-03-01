import pytest
from unittest.mock import MagicMock
from flask import Flask, current_app
from flask.testing import FlaskClient
from routes.users import users_blueprint
from routes.parcel_locker import clients_blueprint, packages_blueprint, parcel_lockers_blueprint
from security.authorize import authorize
from main import create_app
import httpx
import jwt


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(clients_blueprint)
    app.register_blueprint(packages_blueprint)
    app.register_blueprint(parcel_lockers_blueprint)
    return app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture
def mock_jwt_token(mocker):
    jwt_secret = "test_secret"
    jwt_algorithm = "HS256"
    token_payload = {"role": "admin"}
    token = jwt.encode(token_payload, jwt_secret, algorithm=jwt_algorithm)

    mocker.patch.object(current_app, 'config', {
        "JWT_SECRET": jwt_secret,
        "JWT_AUTHTYPE": jwt_algorithm,
        "JWT_PREFIX": "Bearer",
        "APPLICATION_ROOT": "/",
        "PREFERRED_URL_SCHEME": "http",
        "TRUSTED_HOSTS": ["localhost", "127.0.0.1"],
        "SERVER_NAME": "localhost:5000",
        "PROPAGATE_EXCEPTIONS": True,
        "SECRET_KEY": "test_secret_key",
        "SECRET_KEY_FALLBACKS": ["test_fallback_secret_key1", "test_fallback_secret_key2"],
        "SESSION_COOKIE_NAME": "session_cookie_name",
        "MAX_CONTENT_LENGTH": 16 * 1024 * 1024,
        "SESSION_COOKIE_DOMAIN": "localhost",
        "SESSION_COOKIE_PATH": "/",
        "SESSION_COOKIE_SECURE": False,
        "SESSION_COOKIE_PARTITIONED": False,
        "SESSION_COOKIE_SAMESITE": "Lax",
        "SESSION_COOKIE_HTTPONLY": True,
        "TRAP_HTTP_EXCEPTIONS": True,
        "DEBUG": True
    })

    return token


def test_proxy_users(client, mocker):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"Mocked Response"
    mock_response.headers = {"Content-Type": "application/json"}

    mocker.patch.object(httpx, 'request', return_value=mock_response)

    response = client.get('/users/some-path')

    assert response.status_code == 200
    assert response.data == b"Mocked Response"
    assert response.headers["Content-Type"] == "application/json"


def test_proxy_clients_get(client, mocker, mock_jwt_token):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"client_id": 1, "name": "Test Client"}'
    mock_response.headers = {"Content-Type": "application/json"}

    mocker.patch.object(httpx, 'request', return_value=mock_response)

    response = client.get('/clients/1', headers={"Authorization": f"Bearer {mock_jwt_token}"})

    assert response.status_code == 200
    assert response.data == b'{"client_id": 1, "name": "Test Client"}'
    assert response.headers["Content-Type"] == "application/json"


def test_proxy_packages_post_success(client, mocker, mock_jwt_token):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"message": "success"}'
    mock_response.headers = {"Content-Type": "application/json"}

    mocker.patch.object(httpx, 'request', return_value=mock_response)

    response = client.post('/packages', data='{"key": "value"}', headers={"Authorization": f"Bearer {mock_jwt_token}"})

    assert response.status_code == 200
    assert response.data == b'{"message": "success"}'
    assert response.headers["Content-Type"] == "application/json"


def test_proxy_packages_put_success(client, mocker, mock_jwt_token):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"message": "success"}'
    mock_response.headers = {"Content-Type": "application/json"}

    mocker.patch.object(httpx, 'request', return_value=mock_response)

    package_id = 123
    data = '{"name": "Updated Package", "status": "Delivered"}'

    response = client.put(f'/packages/{package_id}', data=data, headers={"Authorization": f"Bearer {mock_jwt_token}"})

    assert response.status_code == 200
    assert response.data == b'{"message": "success"}'
    assert response.headers["Content-Type"] == "application/json"


def test_proxy_add_parcel_locker(client, mocker, mock_jwt_token):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"message": "Parcel locker added successfully"}'
    mock_response.headers = {"Content-Type": "application/json"}

    mocker.patch.object(httpx, 'request', return_value=mock_response)

    parcel_locker_data = '{"location": "Test Location", "name": "Parcel Locker 1"}'

    response = client.post('/parcel_lockers/parcel_locker', data=parcel_locker_data, headers={"Authorization": f"Bearer {mock_jwt_token}"})

    assert response.status_code == 200
    assert response.data == b'{"message": "Parcel locker added successfully"}'
    assert response.headers["Content-Type"] == "application/json"


def test_proxy_add_locker(client, mocker, mock_jwt_token):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"message": "Locker added successfully"}'
    mock_response.headers = {"Content-Type": "application/json"}

    mocker.patch.object(httpx, 'request', return_value=mock_response)

    locker_data = '{"location": "Test Location", "name": "Locker 1"}'

    response = client.post('/parcel_lockers/locker', data=locker_data, headers={"Authorization": f"Bearer {mock_jwt_token}"})

    assert response.status_code == 200
    assert response.data == b'{"message": "Locker added successfully"}'
    assert response.headers["Content-Type"] == "application/json"








