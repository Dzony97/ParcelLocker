from flask import Flask, request, Blueprint
import httpx

clients_blueprint = Blueprint('clients', __name__, url_prefix='/clients')
packages_blueprint = Blueprint('packages', __name__, url_prefix='/packages')


@clients_blueprint.route('/<int:client_id>')
def proxy_clients_get(client_id):
    target_url = f"http://parcel_lockers-webapp:8100/clients/{client_id}"
    forwarded_headers = {
        k: v for k, v in request.headers if k.lower() != "host"
    }

    resp = httpx.request(
        method=request.method,
        url=target_url,
        headers=forwarded_headers,
        content=request.get_data(),
        cookies=request.cookies,
        follow_redirects=False
    )
    return (resp.content, resp.status_code, resp.headers.items())


@packages_blueprint.route('', methods=['POST'])
def proxy_packages_post():
    target_url = "http://parcel_lockers-webapp:8100/packages"
    forwarded_headers = {
        k: v for k, v in request.headers if k.lower() != "host"
    }

    resp = httpx.request(
        method=request.method,
        url=target_url,
        headers=forwarded_headers,
        content=request.get_data(),
        cookies=request.cookies,
        follow_redirects=False
    )
    return (resp.content, resp.status_code, resp.headers.items())


@packages_blueprint.route('/<int:package_id>', methods=['PUT'])
def proxy_packages_put(package_id):
    target_url = f"http://parcel_lockers-webapp:8100/packages/{package_id}"
    forwarded_headers = {
        k: v for k, v in request.headers if k.lower() != "host"
    }

    resp = httpx.request(
        method=request.method,
        url=target_url,
        headers=forwarded_headers,
        content=request.get_data(),
        cookies=request.cookies,
        follow_redirects=False
    )
    return (resp.content, resp.status_code, resp.headers.items())