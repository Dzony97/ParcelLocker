from flask import Flask, jsonify, request, Response, make_response, Blueprint
from app.src.configuration import parcel_locker_service
from app.src.entity import Size

import logging

logging.basicConfig(level=logging.INFO)

clients_blueprint = Blueprint('clients', __name__, url_prefix='/clients')
packages_blueprint = Blueprint('packages', __name__, url_prefix='/packages')


@clients_blueprint.route('/<int:client_id>')
def get_clients_location_route(client_id: int) -> Response:
    try:
        client = parcel_locker_service.client_repo.find_by_id(client_id)
        if not client:
            return jsonify({'message': f'Client {client_id} not found'}), 404
        return jsonify({'location': parcel_locker_service.find_client_location(client_id)}), 200
    except Exception as e:
        return jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500


@packages_blueprint.route('', methods=['POST'])
def send_package_route() -> Response:
    try:
        data = request.get_json()

        if not data:
            return jsonify({'message': 'No JSON payload provided'}), 400

        client_id = data.get('client_id')
        receiver_id = data.get('receiver_id')
        max_distance = data.get('max_distance')
        size = data.get('size')

        if not all([client_id, receiver_id, max_distance, size]):
            return jsonify({'message': 'Missing required fields'}), 400

        try:
            size_enum = Size[size].value
        except KeyError:
            return jsonify({'message': 'Invalid size value. Must be one of S, M, L.'}), 422

        package = parcel_locker_service.send_package(client_id, receiver_id, max_distance, size_enum)
        return jsonify({'package': package}), 201

    except Exception as e:
        return jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500


@packages_blueprint.route('/<int:package_id>', methods=['PUT'])
def receive_package_route(package_id: int) -> Response:
    try:
        package = parcel_locker_service.package_repo.find_by_id(package_id)
        if package is None:
            return jsonify({'message': 'The package is not found'}), 404
        if package.status == 'Received':
            return jsonify({'message': 'The package was received'}), 409
        parcel_locker_service.receive_package(package_id)
        return jsonify({'package': package}), 200
    except Exception as e:
        return jsonify({'message': f'An unexpected error occurred: {str(e)}'}), 500


