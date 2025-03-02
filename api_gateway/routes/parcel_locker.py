from flask import Flask, request, Blueprint, Response, make_response
from security.authorize import authorize
import httpx

clients_blueprint = Blueprint('clients', __name__, url_prefix='/clients')
packages_blueprint = Blueprint('packages', __name__, url_prefix='/packages')
parcel_lockers_blueprint = Blueprint('parcel_lockers', __name__, url_prefix='/parcel_lockers')


@clients_blueprint.route('/<int:client_id>')
@authorize(['admin', 'user'])
def proxy_clients_get(client_id: int) -> Response:
    """
    Proxies GET requests to the clients endpoint.

    :param client_id: The ID of the client to retrieve.
    :return: The response from the proxied request.
    """
    target_url = f"http://parcel_lockers-webapp:8100/clients/{client_id}"
    forwarded_headers = {
        k: v for k, v in request.headers if k.lower() != "host"
    }

    resp = httpx.request(
        method=request.method,
        url=target_url,
        headers=forwarded_headers,
        content=request.get_data(),
        follow_redirects=False
    )
    return make_response(resp.content, resp.status_code, dict(resp.headers))


@packages_blueprint.route('', methods=['POST'])
@authorize(['admin', 'user'])
def proxy_packages_post() -> Response:
    """
    Proxies POST requests to the packages endpoint.

    :return: The response from the proxied request.
    """
    target_url = "http://parcel_lockers-webapp:8100/packages"
    forwarded_headers = {
        k: v for k, v in request.headers if k.lower() != "host"
    }

    resp = httpx.request(
        method=request.method,
        url=target_url,
        headers=forwarded_headers,
        content=request.get_data(),
        follow_redirects=False
    )
    return make_response(resp.content, resp.status_code, dict(resp.headers))


@packages_blueprint.route('/<int:package_id>', methods=['PUT'])
@authorize(['admin', 'user'])
def proxy_packages_put(package_id: int) -> Response:
    """
    Proxies PUT requests to update a package.

    :param package_id: The ID of the package to update.
    :return: The response from the proxied request.
    """
    target_url = f"http://parcel_lockers-webapp:8100/packages/{package_id}"
    forwarded_headers = {
        k: v for k, v in request.headers if k.lower() != "host"
    }

    resp = httpx.request(
        method=request.method,
        url=target_url,
        headers=forwarded_headers,
        content=request.get_data(),
        follow_redirects=False
    )
    return make_response(resp.content, resp.status_code, dict(resp.headers))


@parcel_lockers_blueprint.route('/parcel_locker', methods=['POST'])
@authorize(['admin'])
def proxy_add_parcel_locker() -> Response:
    """
    Proxies POST requests to add a new parcel locker.

    :return: The response from the proxied request.
    """
    target_url = "http://parcel_lockers-webapp:8100/parcel_lockers/parcel_locker"
    forwarded_headers = {
        k: v for k, v in request.headers if k.lower() != "host"
    }

    resp = httpx.request(
        method=request.method,
        url=target_url,
        headers=forwarded_headers,
        content=request.get_data(),
        follow_redirects=False
    )
    return make_response(resp.content, resp.status_code, dict(resp.headers))


@parcel_lockers_blueprint.route('/locker', methods=['POST'])
@authorize(['admin'])
def proxy_add_locker() -> Response:
    """
    Proxies POST requests to add a new locker to a parcel locker.

    :return: The response from the proxied request.
    """
    target_url = "http://parcel_lockers-webapp:8100/parcel_lockers/locker"
    forwarded_headers = {
        k: v for k, v in request.headers if k.lower() != "host"
    }

    resp = httpx.request(
        method=request.method,
        url=target_url,
        headers=forwarded_headers,
        content=request.get_data(),
        follow_redirects=False
    )
    return make_response(resp.content, resp.status_code, dict(resp.headers))


