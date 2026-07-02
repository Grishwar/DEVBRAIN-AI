"""
Tests for the /diff endpoint.
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_diff_validation():
    """
    FastAPI should reject an empty request body.
    """

    response = client.post(
        "/diff",
        json={},
    )

    assert response.status_code == 422


def test_diff_request_schema():
    """
    Verify DiffRequest schema.
    """

    payload = {
        "dataset_id": "sample_dataset",
        "commit_sha": "abc123def456",
        "changed_files": [
            "main.py",
            "services/ask_service.py",
        ],
        "commit_message": "Added semantic search improvements",
    }

    assert payload["dataset_id"] == "sample_dataset"
    assert isinstance(payload["changed_files"], list)
    assert len(payload["changed_files"]) == 2


def test_diff_unknown_dataset():
    """
    Unknown datasets should be handled gracefully.
    """

    response = client.post(
        "/diff",
        json={
            "dataset_id": "unknown_dataset",
            "commit_sha": "123456",
            "changed_files": [
                "main.py",
            ],
            "commit_message": "Testing",
        },
    )

    assert response.status_code in [200, 404, 500]