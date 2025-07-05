from flask import Flask, request, render_template, Response
from config import Config
import os
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

REQUEST_COUNT = Counter('app_requests_total', 'Total req', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Req latency', ['endpoint'])

def create_server():
    app = Flask(__name__, template_folder="templates")
    config = Config()

    @app.route("/healthz")
    def healthz():
        return "OK", 200

    @app.route("/ready")
    def ready():
        if config.EXTERNAL_CALL_URL:
            import requests
            try:
                if config.EXTERNAL_CALL_METHOD.upper() == "GET":
                    r = requests.get(config.EXTERNAL_CALL_URL, timeout=2)
                elif config.EXTERNAL_CALL_METHOD.upper() == "POST":
                    r = requests.post(config.EXTERNAL_CALL_URL, timeout=2)
                else:
                    return "Invalid ExternalCallMethod", 500
                if r.status_code != 200:
                    return "Dependency not ready", 503
            except Exception:
                return "Dependency not ready", 503
        return "READY", 200

    @app.route("/")
    def index():
        import time
        import requests

        start_time = time.time()
        REQUEST_COUNT.labels(method=request.method, endpoint='/').inc()

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

        REQUEST_LATENCY.labels(endpoint='/').observe(time.time() - start_time)

        return render_template(
            "index.html",
            title=config.TITLE,
            content=content,
            pod_name=pod_name
        )

    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

    return app