"""Task API instrumented for Prometheus, with security-focused metrics."""
import os
import time

from flask import Flask, g, jsonify, request
from prometheus_client import (CONTENT_TYPE_LATEST, Counter, Gauge, Histogram,
                               generate_latest)

app = Flask(__name__)

REQUESTS = Counter("http_requests_total", "HTTP requests",
                   ["method", "endpoint", "status"])
LATENCY = Histogram("http_request_duration_seconds", "Request latency",
                    ["endpoint"],
                    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5))
AUTH_FAILURES = Counter("auth_failures_total", "Failed login attempts", ["reason"])
AUTH_SUCCESS = Counter("auth_success_total", "Successful logins")
TASK_COUNT = Gauge("tasks_current", "Tasks currently stored")

# Demo credentials come from env, never hard-coded secrets in the image.
USERS = {os.getenv("DEMO_USER", "admin"): os.getenv("DEMO_PASSWORD", "change-me")}
TASKS = []


@app.before_request
def _start():
    g.start = time.perf_counter()


@app.after_request
def _record(resp):
    endpoint = request.url_rule.rule if request.url_rule else "unmatched"
    if endpoint != "/metrics":
        LATENCY.labels(endpoint).observe(time.perf_counter() - g.start)
        REQUESTS.labels(request.method, endpoint, resp.status_code).inc()
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Cache-Control"] = "no-store"
    return resp


@app.get("/")
def index():
    return jsonify(service="secops-task-api", status="ok")


@app.get("/health")
def health():
    return jsonify(status="healthy")


@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    user, pw = data.get("username"), data.get("password")
    if not user or not pw:
        AUTH_FAILURES.labels("missing_fields").inc()
        return jsonify(error="username and password required"), 400
    if USERS.get(user) != pw:
        AUTH_FAILURES.labels("bad_credentials").inc()
        return jsonify(error="invalid credentials"), 401
    AUTH_SUCCESS.inc()
    return jsonify(message="login ok")


@app.route("/api/tasks", methods=["GET", "POST"])
def tasks():
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        title = str(data.get("title", "")).strip()
        if not title or len(title) > 200:
            return jsonify(error="title required (max 200 chars)"), 400
        TASKS.append({"id": len(TASKS) + 1, "title": title})
        TASK_COUNT.set(len(TASKS))
        return jsonify(TASKS[-1]), 201
    return jsonify(TASKS)


@app.get("/slow")
def slow():
    time.sleep(0.4)
    return jsonify(status="slow ok")


@app.get("/error")
def error():
    return jsonify(error="simulated failure"), 500


@app.get("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
