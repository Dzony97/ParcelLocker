from flask import Flask, request, Blueprint
from security.authorize import authorize
import httpx

users_blueprint = Blueprint('users', __name__, url_prefix='/users')


@users_blueprint.route("/<path:subpath>", methods=["GET", "POST"])
def proxy_users(subpath):
    """
    Proxies GET and POST requests to the users service.

    :param subpath: The subpath of the request to be forwarded.
    :return: The response from the proxied request.
    """
    target_url = f"http://users-nginx:82/users/{subpath}"
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
    return resp.content, resp.status_code, resp.headers.items()
