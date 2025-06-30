from flask import Flask, request, render_template
from config import Config
import os

def create_server():
    app = Flask(__name__, template_folder="templates")
    config = Config()

    @app.route("/")
    def index():
        import time
        import requests

        time.sleep(config.RESPONSE_TIME / 1000)

        content = "Default Content"
        if config.EXTERNAL_CALL_URL:
            try:
                if config.EXTERNAL_CALL_METHOD.upper() == "GET":
                    response = requests.get(config.EXTERNAL_CALL_URL)
                elif config.EXTERNAL_CALL_METHOD.upper() == "POST":
                    response = requests.post(config.EXTERNAL_CALL_URL)
                else:
                    return "Invalid ExternalCallMethod", 500
                response.raise_for_status()
                content = response.text
            except requests.RequestException as e:
                return f"Error calling external service: {e}", 500

        pod_name = os.getenv("HOSTNAME", "unknown-pod")

        return render_template(
            "index.html",
            title=config.TITLE,
            content=content,
            pod_name=pod_name
        )

    return app