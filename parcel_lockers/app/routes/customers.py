from flask import Flask, jsonify, request, Response, make_response, Blueprint
from app.src.configuration import create_parcel_locker_service
from flask_pydantic import validate
from pydantic import BaseModel, Field


import logging

logging.basicConfig(level=logging.INFO)

clients_blueprint = Blueprint('clients', __name__, url_prefix='/clients')
packages_blueprint = Blueprint('packages', __name__, url_prefix='/packages')


class PackageRequestModel(BaseModel):
    sender_id: int = Field(..., ge=0, description='Sender ID')
    receiver_id: int = Field(..., ge=0, description='Receiver ID')
    max_distance: float = Field(..., ge=0, description='Max distance parcel lockers from the user')
    size: str = Field(..., description='Size: S, M or L')


@clients_blueprint.route('/<int:client_id>')
def get_clients_location_route(client_id: int) -> Response:
    try:
        service = create_parcel_locker_service()
        client = service.client_repo.find_by_id(client_id)
        if not client:
            return jsonify({'message': f'Client {client_id} not found'}), 404
        return jsonify({'location': service.find_client_location(client_id)}), 200
    except Exception as e:
        return jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500


@packages_blueprint.route('', methods=['POST'])
@validate()
def send_package_route(body: PackageRequestModel) -> Response:
    try:
        sender_id = body.sender_id
        receiver_id = body.receiver_id
        max_distance = body.max_distance
        size = body.size

        if size not in ['S', 'M', 'L']:
            return jsonify({'message': f'The size must be S, M or L'}), 400
        service = create_parcel_locker_service()
        package = service.send_package(sender_id, receiver_id, max_distance, size)
        return jsonify({'package': package}), 201

    except Exception as e:
        return jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500


@packages_blueprint.route('/<int:package_id>', methods=['PUT'])
def receive_package_route(package_id: int) -> Response:
    try:
        service = create_parcel_locker_service()
        package = service.package_repo.find_by_id(package_id)
        if package is None:
            return jsonify({'message': 'The package is not found'}), 404
        if package.status == 'Received':
            return jsonify({'message': 'The package was received'}), 409
        service.receive_package(package_id)
        return jsonify({'package': package}), 200
    except Exception as e:
        return jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500


