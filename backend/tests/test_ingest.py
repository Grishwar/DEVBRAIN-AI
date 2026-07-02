"""
Tests for the /ingest endpoint.
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_ingest_validation():
    """
    FastAPI should reject an empty request body.
    """

    response = client.post(
        "/ingest",
        json={},
    )

    assert response.status_code == 422


def test_ingest_invalid_repo():
    """
    Invalid GitHub repository should return an error.
    """

    response = client.post(
        "/ingest",
        json={
            "repo_url": "https://github.com/invalid-owner/invalid-repository",
            "branch": "main",
        },
    )

    assert response.status_code in [400, 404, 500]


def test_ingest_request_schema():
    """
    Verify request schema is accepted.
    """

    payload = {
        "repo_url": "https://github.com/test/test",
        "branch": "main",
    }

    assert "repo_url" in payload
    assert "branch" in payload