from types import SimpleNamespace

from fastapi.testclient import TestClient

from src.api.app import app
from src.api import routes


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


def test_post_works_delegates_to_ingestion_service(monkeypatch):
    def fake_ingest(self, openalex_id: str):
        assert openalex_id == "W2741809807"
        return SimpleNamespace(
            ingestion_run_id=7,
            work_id=11,
            work_openalex_id="https://openalex.org/W2741809807",
            created=True,
            authors_synced=2,
            topics_synced=1,
            source_synced=True,
        )

    monkeypatch.setattr(routes.OpenAlexIngestionService, "ingest_work_by_openalex_id", fake_ingest)

    response = client.post("/works", json={"openalex_id": "W2741809807"})

    assert response.status_code == 200
    assert response.json() == {
        "ingestion_run_id": 7,
        "work_id": 11,
        "work_openalex_id": "https://openalex.org/W2741809807",
        "created": True,
        "authors_synced": 2,
        "topics_synced": 1,
        "source_synced": True,
    }
