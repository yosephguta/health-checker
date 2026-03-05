from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from datetime import datetime, timezone

from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_check_endpoint_success():
    fake_result = {
        "url": "https://google.com",
        "status": "up",
        "status_code": 200,
        "response_time_ms": 12.3,
        "checked_at": datetime.now(timezone.utc).isoformat()
    }

    with patch("app.main.check_url", new=AsyncMock(return_value=fake_result)):
        response = client.post("/check", json={"url": "https://google.com", "timeout": 5})

    assert response.status_code == 200
    data = response.json()

    # Required fields exist
    assert "status" in data
    assert "url" in data
    assert "checked_at" in data

    # Basic correctness
    assert data["url"] == "https://google.com"
    assert data["status"] == "up"


def test_check_endpoint_batch():
    fake_results = [
        {
            "url": "https://google.com",
            "status": "up",
            "status_code": 200,
            "response_time_ms": 10.0,
            "checked_at": datetime.now(timezone.utc).isoformat()
        },
        {
            "url": "https://example.com",
            "status": "up",
            "status_code": 200,
            "response_time_ms": 15.0,
            "checked_at": datetime.now(timezone.utc).isoformat()
        },
    ]

    # AsyncMock will be awaited twice by asyncio.gather in your batch endpoint
    with patch("app.main.check_url", new=AsyncMock(side_effect=fake_results)):
        response = client.post(
            "/check/batch",
            json=[
                {"url": "https://google.com", "timeout": 5},
                {"url": "https://example.com", "timeout": 5},
            ],
        )

    assert response.status_code == 200
    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["url"] == "https://google.com"
    assert data[1]["url"] == "https://example.com"
    assert "checked_at" in data[0]
    assert "checked_at" in data[1]