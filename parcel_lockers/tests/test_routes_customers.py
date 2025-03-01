def test_get_clients_location_success(client):
    """
    Test retrieving a client's location successfully.

    Sends a GET request to retrieve the location of client with ID 1.
    Expects a 200 OK response and presence of "location" in the response data.
    """
    response = client.get("/clients/1")
    assert response.status_code == 200
    assert b"location" in response.data


def test_get_clients_location_not_found(client):
    """
    Test retrieving a non-existent client's location.

    Sends a GET request for client ID 999, which does not exist.
    Expects a 404 Not Found response with an appropriate error message.
    """
    response = client.get("/clients/999")
    assert response.status_code == 404
    assert b"Client 999 not found" in response.data


def test_send_package_success(client):
    """
    Test sending a package successfully.

    Sends a POST request to create a package with valid data.
    Expects a 201 Created response and presence of "package" in response data.
    """
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
    """
    Test sending a package with an invalid size.

    Sends a POST request with an invalid size "XL".
    Expects a 400 Bad Request response and an appropriate error message.
    """
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
    """
    Test handling of an unexpected error when sending a package.

    Sends a POST request with an invalid sender ID (0) which triggers an error.
    Expects a 500 Internal Server Error response with an appropriate error message.
    """
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
    """
    Test attempting to receive a non-existent package.

    Sends a PUT request to update a package with an invalid ID (99999).
    Expects a 404 Not Found response with an appropriate error message.
    """
    response = client.put('/packages/99999')
    assert response.status_code == 404, response.data

    data = response.get_json()
    assert data['message'] == 'The package is not found'


def test_receive_package_success(client):
    """
    Test successfully receiving a package.

    Sends a PUT request to update a valid package (ID 2).
    Expects a 200 OK response and presence of "package" in response data.
    """
    response = client.put('/packages/2')
    assert response.status_code == 200, response.data

    data = response.get_json()
    assert 'package' in data


def test_receive_package_already_received(client):
    """
    Test attempting to receive a package that has already been received.

    Sends a PUT request to update a package that is already marked as received.
    Expects a 409 Conflict response with an appropriate error message.
    """
    response = client.put('/packages/2')
    assert response.status_code == 409, response.data

    data = response.get_json()
    assert data['message'] == 'The package was received'
