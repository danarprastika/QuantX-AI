"""Unit tests for health check endpoints."""

import pytest
from fastapi.testclient import TestClient

from quantx.main import create_app


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


def test_liveness(client: TestClient) -> None:
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json()["status"] == "alive"


def test_health(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_root(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "quantx-api"
