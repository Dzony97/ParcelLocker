import pytest
from dotenv import load_dotenv

load_dotenv('.env.test')
import jwt
import datetime
from unittest.mock import patch, MagicMock
from flask import Flask
from app.security.configuration import configure_security, users_blueprint
from app.db.entity import UserEntity


@pytest.fixture
def mock_user(app):
    """
    Fixture that creates a mock user entity for testing.

    This mock user simulates a user from the database with attributes
    like ID, username, password, role, and account status.

    Args:
        app (Flask): The Flask application instance used for the app context.

    Returns:
        MagicMock: A mocked UserEntity object simulating a real user.
    """
    with app.app_context():
        user = MagicMock(spec=UserEntity)
        user.id_ = 1
        user.username = "testuser"
        user.password = "hashedpassword"
        user.role = "user"
        user.is_active = True
        user.check_password.return_value = True
    return user


def test_login_success(client, mocker, mock_user):
    """
    Test for successful login where correct credentials are provided.

    This test simulates a user logging in with correct username and password,
    and verifies that an access token and refresh token are returned.

    Args:
        client (FlaskClient): The Flask test client to simulate requests.
        mocker (MagicMock): The mocker used to patch the `find_by_username` method.
        mock_user (MagicMock): The mock user returned by `find_by_username`.
    """
    mocker.patch("app.db.repository.user_repository.find_by_username", return_value=mock_user)

    response = client.post("/users/login", json={"username": "testuser", "password": "correct_password"})

    assert response.status_code == 201
    assert "access_token" in response.json
    assert "refresh_token" in response.json
    assert response.headers["Access-Token"]
    assert response.headers["Refresh-Token"]


def test_login_user_not_found(client, mocker):
    """
    Test for the scenario where the user is not found during login.

    This test simulates an attempt to log in with a non-existent username,
    and expects an appropriate error message.

    Args:
        client (FlaskClient): The Flask test client to simulate requests.
        mocker (MagicMock): The mocker used to patch the `find_by_username` method.
    """
    mocker.patch("app.db.repository.user_repository.find_by_username", return_value=None)

    response = client.post("/users/login", json={"username": "unknown_user", "password": "some_password"})

    assert response.status_code == 400
    assert response.json["message"] == "Authentication - user not found"


def test_login_user_not_active(client, mocker, mock_user):
    """
    Test for the scenario where the user is not active during login.

    This test simulates an attempt to log in with a deactivated user and expects
    a response indicating that the user is inactive.

    Args:
        client (FlaskClient): The Flask test client to simulate requests.
        mocker (MagicMock): The mocker used to patch the `find_by_username` method.
        mock_user (MagicMock): The mock user returned by `find_by_username`.
    """
    mock_user.is_active = False
    mocker.patch("app.db.repository.user_repository.find_by_username", return_value=mock_user)

    response = client.post("/users/login", json={"username": "testuser", "password": "correct_password"})

    assert response.status_code == 500
    assert response.json["message"] == "Authentication - user is not active"


def test_login_wrong_password(client, mocker, mock_user):
    """
    Test for the scenario where an incorrect password is provided during login.

    This test simulates an attempt to log in with the correct username but
    incorrect password, and expects an error indicating the password is wrong.

    Args:
        client (FlaskClient): The Flask test client to simulate requests.
        mocker (MagicMock): The mocker used to patch the `find_by_username` method.
        mock_user (MagicMock): The mock user returned by `find_by_username`.
    """
    mock_user.check_password.return_value = False
    mocker.patch("app.db.repository.user_repository.find_by_username", return_value=mock_user)

    response = client.post("/users/login", json={"username": "testuser", "password": "wrong_password"})

    assert response.status_code == 400
    assert response.json["message"] == "Authentication - password is not correct"


def test_refresh_token_success(client, mocker, app):
    """
    Test for successful refresh token operation.

    This test simulates a user refreshing their token with a valid refresh token,
    and verifies that new access and refresh tokens are returned.

    Args:
        client (FlaskClient): The Flask test client to simulate requests.
        mocker (MagicMock): The mocker used to patch methods or add behavior during testing.
        app (Flask): The Flask application instance used for the app context.
    """
    with app.app_context():
        secret = app.config['JWT_SECRET']
        algorithm = app.config['JWT_AUTHTYPE']
        refresh_token_exp = int((datetime.datetime.now(datetime.UTC) + datetime.timedelta(
            minutes=app.config['JWT_REFRESH_MAX_AGE'])).timestamp())
        access_token_exp = int((datetime.datetime.now(datetime.UTC) + datetime.timedelta(
            minutes=app.config['JWT_ACCESS_MAX_AGE'])).timestamp())

        refresh_token_payload = {
            'iat': datetime.datetime.now(datetime.UTC),
            'exp': refresh_token_exp,
            'sub': "1",
            'role': "user",
            'access_token_exp': access_token_exp
        }

        refresh_token = jwt.encode(refresh_token_payload, secret, algorithm=algorithm)
        response = client.post("/users/refresh", json={"token": refresh_token})

    assert response.status_code == 201
    assert "access_token" in response.json
    assert "refresh_token" in response.json
    assert response.headers["Access-Token"]
    assert response.headers["Refresh-Token"]


def test_refresh_token_expired(client, mocker, app):
    """
    Test for the scenario where the refresh token has expired.

    This test simulates a user attempting to refresh their token using an expired refresh token,
    and expects an error message indicating the token has expired.

    Args:
        client (FlaskClient): The Flask test client to simulate requests.
        mocker (MagicMock): The mocker used to patch methods or add behavior during testing.
        app (Flask): The Flask application instance used for the app context.
    """
    with app.app_context():
        secret = app.config['JWT_SECRET']
        algorithm = app.config['JWT_AUTHTYPE']
        refresh_token_exp = int((datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=1)).timestamp())
        access_token_exp = int((datetime.datetime.now(datetime.UTC) - datetime.timedelta(minutes=10)).timestamp())

        refresh_token_payload = {
            'iat': datetime.datetime.now(datetime.UTC),
            'exp': refresh_token_exp,
            'sub': "1",
            'role': "user",
            'access_token_exp': access_token_exp
        }

        expired_refresh_token = jwt.encode(refresh_token_payload, secret, algorithm=algorithm)
        response = client.post("/users/refresh", json={"token": expired_refresh_token})

    assert response.status_code == 401
    assert response.json["message"] == "Cannot refresh token - refresh token has expired"


def test_refresh_token_invalid(client):
    """
    Test for the scenario where an invalid refresh token is provided.

    This test simulates a user attempting to refresh their token with an invalid refresh token,
    and expects an error message indicating the token is invalid.

    Args:
        client (FlaskClient): The Flask test client to simulate requests.
    """
    response = client.post("/users/refresh", json={"token": "invalid_token"})

    assert response.status_code == 401
