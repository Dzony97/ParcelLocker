def test_add_parcel_locker_success(client):

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
    payload = {
        "postal_code": "12-345",
        "latitude": 50.1234,
        "longitude": 19.5678
    }
    response = client.post("/parcel_lockers/parcel_locker", json=payload)
    assert response.status_code in [400, 422], response.data


def test_add_locker_success(client):
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
    payload = {
        "parcel_locker_id": 1,
        "package_id": 10,
        "client_id": 99,
        "status": "Available"
    }
    response = client.post("/parcel_lockers/locker", json=payload)
    assert response.status_code in [400, 422], response.data
