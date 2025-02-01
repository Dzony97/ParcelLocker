import httpx
from flask import Flask, request, Response


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "Hello from HTTPX-based API Gateway!"

    @app.route("/users/<path:subpath>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    def proxy_users(subpath):
        target_url = f"http://users-webapp:8200/users/{subpath}"

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
