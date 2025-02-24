import pytest
import jwt
from flask import Flask, jsonify
from security.authorize import authorize


@pytest.fixture
def app():
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
        return jsonify({"message": "Access granted"})

    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_no_auth_header(client):
    response = client.get("/protected")
    assert response.status_code == 401
    assert response.json == {"message": "Authorization failed - no header"}


def test_invalid_token_format(client):
    headers = {"Authorization": "InvalidTokenWithoutBearer"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401
    assert response.json == {"message": "Authorization failed - access token without prefix"}


def test_invalid_token_signature(client):
    bad_token = jwt.encode({"role": "admin"}, "wrong_secret", algorithm="HS256")
    headers = {"Authorization": f"Bearer {bad_token}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 401
    assert response.json == {"message": "Authorization failed"}


def test_invalid_role(client):
    token = jwt.encode({"role": "user"}, "test_secret", algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 403
    assert response.json == {"message": "Access denied!"}


def test_valid_token(client):
    token = jwt.encode({"role": "admin"}, "test_secret", algorithm="HS256")
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
    assert response.json == {"message": "Access granted"}
