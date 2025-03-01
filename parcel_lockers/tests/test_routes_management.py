def test_add_parcel_locker_success(client):
    """
    Test adding a new parcel locker successfully.

    This test sends a POST request to add a parcel locker with valid data
    and verifies that the response status code is 201 (Created). It also
    checks whether the response contains the new parcel locker ID.

    :param client: The test client for making HTTP requests.
    """
    payload = {
        "city": "Test City",
        "postal_code": "12345",
        "latitude": 50.1234,
        "longitude": 19.5678
    }
    response = client.post("/parcel_lockers/parcel_locker", json=payload)

    assert response.status_code == 201, response.data
    data = response.get_json()
    assert "new_parcel_locker_id" in data


def test_add_parcel_locker_missing_field(client):
    """
    Test adding a parcel locker with missing required fields.

    This test sends a POST request with missing 'city' field and expects a
    400 or 422 response indicating validation failure.

    :param client: The test client for making HTTP requests.
    """
    payload = {
        "postal_code": "12-345",
        "latitude": 50.1234,
        "longitude": 19.5678
    }
    response = client.post("/parcel_lockers/parcel_locker", json=payload)
    assert response.status_code in [400, 422], response.data


def test_add_locker_success(client):
    """
    Test adding a new locker successfully.

    This test sends a POST request with valid data for adding a locker
    and verifies that the response status code is 201 (Created). It also
    checks whether the response contains the new locker details.

    :param client: The test client for making HTTP requests.
    """
    payload = {
        "parcel_locker_id": 2,
        "package_id": None,
        "client_id": None,
        "size": "S",
        "status": "Occupied"
    }
    response = client.post("/parcel_lockers/locker", json=payload)
    assert response.status_code == 201, response.data

    data = response.get_json()
    assert "new_locker" in data


def test_add_locker_missing_size(client):
    """
    Test adding a locker with missing required field 'size'.

    This test sends a POST request without the 'size' field and expects a
    400 or 422 response indicating validation failure.

    :param client: The test client for making HTTP requests.
    """
    payload = {
        "parcel_locker_id": 1,
        "package_id": 10,
        "client_id": 99,
        "status": "Available"
    }
    response = client.post("/parcel_lockers/locker", json=payload)
    assert response.status_code in [400, 422], response.data
