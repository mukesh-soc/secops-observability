import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
os.environ["DEMO_PASSWORD"] = "test-pass"
from app import app  # noqa: E402

c = app.test_client()


def test_health():
    assert c.get("/health").status_code == 200


def test_login_success_and_failure():
    ok = c.post("/login", json={"username": "admin", "password": "test-pass"})
    assert ok.status_code == 200
    bad = c.post("/login", json={"username": "admin", "password": "nope"})
    assert bad.status_code == 401
    assert c.post("/login", json={}).status_code == 400


def test_tasks():
    assert c.post("/api/tasks", json={"title": "x"}).status_code == 201
    assert c.post("/api/tasks", json={"title": ""}).status_code == 400
    assert len(c.get("/api/tasks").get_json()) >= 1


def test_metrics_exposed():
    c.get("/health")
    body = c.get("/metrics").get_data(as_text=True)
    assert "http_requests_total" in body
    assert "auth_failures_total" in body
