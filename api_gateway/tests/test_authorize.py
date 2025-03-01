import pytest
import jwt
from flask import Flask, jsonify
from security.authorize import authorize


@pytest.fixture
def app():
    """
    Fixture to create a Flask app for testing.

    This fixture sets up a basic Flask app with the necessary configuration for testing JWT authentication.
    A protected route `/protected` is defined, which requires the 'admin' role to access.

    :return: A Flask application instance configured for testing.
    """
    app = Flask(__name__)
    app.config.update({
        "TESTING": True,
        "JWT_SECRET": "test_secret",
        "JWT_ISSUER": "test_issuer",
        "JWT_AUTHTYPE": "HS256",
        "JWT_ACCESS_MAX_AGE": 5,
        "JWT_PREFIX": "Bearer"
    })

    @app.route('/protected', methods=['GET'])
    @authorize(['admin'])
    def protected_route():
        """
        Protected route that requires the 'admin' role to access.

        :return: A JSON response with a message indicating access was granted.
        """
        return jsonify({"message": "Access granted"})

    return app


@pytest.fixture
def client(app):
    """
    Fixture to create a test client for the Flask app.

    :param app: The Flask app instance.
    :return: A test client instance that can be used to simulate requests to the Flask app.
    """
    return app.test_client()


def test_no_auth_header(client):
    """
    Test case for when no Authorization header is provided in the request.

    :param client: The test client instance.
    :return: None
    """
    response = client.get("/protected")
    assert response.status_code == 401
    assert response.json == {"message": "Authorization failed - no header"}


def test_invalid_token_format(client):
    """
    Test case for when the Authorization header is malformed or missing the 'Bearer' prefix.

    :param client: The test client instance.
    :return: None
    """
    headers = {"Authorization": "InvalidTokenWithoutBearer"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401
    assert response.json == {"message": "Authorization failed - access token without prefix"}


def test_invalid_token_signature(client):
    """
    Test case for when the token has an invalid signature.

    :param client: The test client instance.
    :return: None
    """
    bad_token = jwt.encode({"role": "admin"}, "wrong_secret", algorithm="HS256")
    headers = {"Authorization": f"Bearer {bad_token}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401
    assert response.json == {"message": "Authorization failed"}


def test_invalid_role(client):
    """
    Test case for when the token has an invalid role that does not match the required roles.

    :param client: The test client instance.
    :return: None
    """
    token = jwt.encode({"role": "user"}, "test_secret", algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 403
    assert response.json == {"message": "Access denied!"}


def test_valid_token(client):
    """
    Test case for when the token is valid and the role matches the required role.

    :param client: The test client instance.
    :return: None
    """
    token = jwt.encode({"role": "admin"}, "test_secret", algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
    assert response.json == {"message": "Access granted"}
