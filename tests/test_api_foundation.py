from fastapi.testclient import TestClient

from src.api.app import app


client = TestClient(app)


def test_health_and_version_contracts():
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    version = client.get("/version")
    assert version.status_code == 200
    assert "version" in version.json()


def test_metrics_endpoint_exposes_prometheus_text():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "openalex_http_requests_total" in response.text


def test_validation_errors_use_normalized_shape():
    response = client.get("/works?limit=0")
    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "validation_error"
    assert body["error"]["request_id"] is not None
