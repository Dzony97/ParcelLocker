import httpx
from flask import Flask, request, Response, jsonify

app = Flask(__name__)


def create_app():

    with app.app_context():
        @app.errorhandler(Exception)
        def handle_error(error: Exception):
            error_message = error.args[0]
            return jsonify({'error': error_message}), 500

        #
        # --- USERS mikroserwis ---
        #
        @app.route("/users/<path:subpath>", methods=["GET", "POST"])
        def proxy_users(subpath):
            target_url = f"http://users-nginx:82/users/{subpath}"
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

        #
        # --- PARCEL_LOCKERS mikroserwis ---
        #
        @app.route("/clients/<int:client_id>", methods=["GET"])
        def proxy_clients_get(client_id):
            target_url = "http://parcel_lockers-nginx:81/packages"
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

        @app.route("/packages", methods=["POST"])
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

        @app.route("/packages/<int:package_id>", methods=["PUT"])
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

        return app

