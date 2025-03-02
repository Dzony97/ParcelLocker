from flask import Flask, jsonify, request, Response, make_response, Blueprint
from app.src.configuration import create_parcel_locker_service
from flask_pydantic import validate
from pydantic import BaseModel, Field
import logging
from enum import Enum

logging.basicConfig(level=logging.INFO)


clients_blueprint = Blueprint('clients', __name__, url_prefix='/clients')
packages_blueprint = Blueprint('packages', __name__, url_prefix='/packages')


class PackageRequestModel(BaseModel):
    sender_id: int = Field(..., ge=0, description='Sender ID')
    receiver_id: int = Field(..., ge=0, description='Receiver ID')
    max_distance: float = Field(..., ge=0, description='Max distance parcel lockers from the user')
    size: str = Field(..., description='Size: S, M or L')


class PackageSize(Enum):
    S = "S"
    M = "M"
    L = "L"


@clients_blueprint.route('/<int:client_id>')
def get_clients_location_route(client_id: int) -> Response:
    """
    Route to get the location of a client by their ID.

    :param client_id: The ID of the client whose location is being requested.
    :return: A JSON response with the location of the client or an error message.
    """
    try:
        service = create_parcel_locker_service()
        client = service.client_repo.find_by_id(client_id)

        if not client:
            return make_response(jsonify({'message': f'Client {client_id} not found'}), 404)

        return make_response(jsonify({'location': service.find_client_location(client_id)}), 200)
    except Exception as e:
        return make_response(jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500)


# Route to send a package
@packages_blueprint.route('', methods=['POST'])
@validate()
def send_package_route(body: PackageRequestModel) -> Response:
    """
    Route to send a package from a sender to a receiver.

    :param body: The request body containing sender_id, receiver_id, max_distance, and size.
    :return: A JSON response with the package details or an error message.
    """
    try:
        sender_id = body.sender_id
        receiver_id = body.receiver_id
        max_distance = body.max_distance
        size = PackageSize(body.size)

        if size not in PackageSize:
            return make_response(jsonify({'message': f'The size must be S, M or L'}), 400)

        service = create_parcel_locker_service()
        package = service.send_package(sender_id, receiver_id, max_distance, size)

        return make_response(jsonify({'package': package}), 201)

    except Exception as e:
        return make_response(jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500)


@packages_blueprint.route('/<int:package_id>', methods=['PUT'])
def receive_package_route(package_id: int) -> Response:
    """
    Route to mark a package as received.

    :param package_id: The ID of the package to be received.
    :return: A JSON response with the package details or an error message.
    """
    try:
        service = create_parcel_locker_service()
        package = service.package_repo.find_by_id(package_id)

        if package is None:
            return make_response(jsonify({'message': 'The package is not found'}), 404)

        if package.status == 'Received':
            return make_response(jsonify({'message': 'The package was received'}), 409)

        service.receive_package(package_id)

        return make_response(jsonify({'package': package}), 200)
    except Exception as e:
        return make_response(jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500)
