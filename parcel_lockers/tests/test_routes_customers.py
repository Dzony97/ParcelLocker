import pytest


def test_get_clients_location_success(client):
    response = client.get("/clients/1")
    assert response.status_code == 200
    assert b"location" in response.data


def test_get_clients_location_not_found(client):
    response = client.get("/clients/999")
    assert response.status_code == 404
    assert b"Client 999 not found" in response.data


def test_send_package_success(client):
    payload = {
        'sender_id': 1,
        'receiver_id': 2,
        'max_distance': 10000.0,
        'size': 'S'
    }
    response = client.post('/packages', json=payload)
    assert response.status_code == 201, response.data

    data = response.get_json()
    assert 'package' in data


def test_send_package_invalid_size(client):
    payload = {
        'sender_id': 1,
        'receiver_id': 2,
        'max_distance': 10.0,
        'size': 'XL'
    }
    response = client.post('/packages', json=payload)
    assert response.status_code == 400, response.data
    data = response.get_json()
    assert data['message'] == 'The size must be S, M or L'


def test_send_package_unexpected_error(client):
    payload = {
        'sender_id': 0,
        'receiver_id': 2,
        'max_distance': 10.0,
        'size': 'S'
    }
    response = client.post('/packages', json=payload)
    assert response.status_code == 500, response.data
    data = response.get_json()
    assert 'An unexpected error occurred:' in data['message']


def test_receive_package_not_found(client):
    response = client.put('/packages/99999')
    assert response.status_code == 404, response.data
    data = response.get_json()
    assert data['message'] == 'The package is not found'


def test_receive_package_success(client):
    response = client.put('/packages/2')
    assert response.status_code == 200, response.data
    data = response.get_json()
    assert 'package' in data


def test_receive_package_already_received(client):
    response = client.put('/packages/2')
    assert response.status_code == 409, response.data
    data = response.get_json()
    assert data['message'] == 'The package was received'


