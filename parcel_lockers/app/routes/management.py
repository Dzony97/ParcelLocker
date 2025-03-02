from pydantic import BaseModel, Field
from typing import Optional
from flask import Blueprint, jsonify, Response, make_response
from flask_pydantic import validate
from app.src.configuration import create_parcel_locker_service

parcel_lockers_blueprint = Blueprint('parcel_lockers', __name__, url_prefix='/parcel_lockers')


class AddParcelLockerRequestModel(BaseModel):
    city: str = Field(..., description="City where the parcel locker is located.")
    postal_code: str = Field(..., description="Postal code of the parcel locker.")
    latitude: float = Field(..., description="Latitude coordinate.")
    longitude: float = Field(..., description="Longitude coordinate.")


class AddLockerRequestModel(BaseModel):
    parcel_locker_id: int = Field(..., ge=1, description="ID of the parcel locker.")
    package_id: Optional[int] = Field(None, ge=1, description="ID of the package in this locker (optional).")
    client_id: Optional[int] = Field(None, ge=1, description="ID of the client (optional).")
    size: str = Field(..., description="Size of the locker: S, M, or L.")
    status: str = Field(..., description="Status of the locker: e.g. 'EMPTY' or 'OCCUPIED'.")


@parcel_lockers_blueprint.route('/parcel_locker', methods=['POST'])
@validate()
def add_parcel_locker_route(body: AddParcelLockerRequestModel) -> Response:
    """
    Route to add a new parcel locker to the system.

    :param body: The request body containing city, postal_code, latitude, and longitude for the new parcel locker.
    :return: A JSON response with the new parcel locker ID or an error message.
    """
    try:
        city = body.city
        postal_code = body.postal_code
        latitude = body.latitude
        longitude = body.longitude
        service = create_parcel_locker_service()
        new_parcel_locker_id = service.add_parcel_locker(
            city=city,
            postal_code=postal_code,
            latitude=latitude,
            longitude=longitude
        )

        response = make_response(jsonify({'new_parcel_locker_id': new_parcel_locker_id}), 201)
        return response

    except Exception as e:
        response = make_response(jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500)
        return response


@parcel_lockers_blueprint.route('/locker', methods=['POST'])
@validate()
def add_locker_route(body: AddLockerRequestModel) -> Response:
    """
    Route to add a new locker to an existing parcel locker.

    :param body: The request body containing parcel_locker_id, package_id, client_id, size, and status.
    :return: A JSON response with the new locker details or an error message.
    """
    try:
        parcel_locker_id = body.parcel_locker_id
        package_id = body.package_id
        client_id = body.client_id
        size = body.size
        status = body.status

        service = create_parcel_locker_service()
        new_locker = service.add_locker(
            parcel_locker_id=parcel_locker_id,
            package_id=package_id,
            client_id=client_id,
            size=size,
            status=status
        )
        response = make_response(jsonify({'new_locker': new_locker}), 201)
        return response

    except Exception as e:
        response = make_response(jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500)
        return response
