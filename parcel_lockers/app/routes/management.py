from pydantic import BaseModel, Field
from typing import Optional
from flask import Blueprint, jsonify, Response
from flask_pydantic import validate
from parcel_lockers.app.src.configuration import parcel_locker_service

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
    try:
        city = body.city
        postal_code = body.postal_code
        latitude = body.latitude
        longitude = body.longitude

        new_parcel_locker_id = parcel_locker_service.add_parcel_locker(
            city=city,
            postal_code=postal_code,
            latitude=latitude,
            longitude=longitude
        )

        return jsonify({'new_parcel_locker_id': new_parcel_locker_id}), 201

    except Exception as e:
        return jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500


@parcel_lockers_blueprint.route('/locker', methods=['POST'])
@validate()
def add_locker_route(body: AddLockerRequestModel) -> Response:
    try:
        parcel_locker_id = body.parcel_locker_id
        package_id = body.package_id
        client_id = body.client_id
        size = body.size
        status = body.status

        new_locker = parcel_locker_service.add_locker(
            parcel_locker_id=parcel_locker_id,
            package_id=package_id,
            client_id=client_id,
            size=size,
            status=status
        )

        return jsonify({'new_locker': new_locker}), 201

    except Exception as e:
        return jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500
