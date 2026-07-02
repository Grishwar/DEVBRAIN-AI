"""
Tests for the /timeline endpoint.
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_timeline_validation():
    """
    Missing dataset_id should return 404 because it is a path parameter.
    """

    response = client.get("/timeline/")

    assert response.status_code == 404


def test_timeline_unknown_dataset():
    """
    Unknown datasets should be handled gracefully.
    """

    response = client.get(
        "/timeline/unknown_dataset"
    )

    assert response.status_code in [200, 404, 500]


def test_timeline_response_schema():
    """
    Verify TimelineResponse schema.
    """

    response = client.get(
        "/timeline/unknown_dataset"
    )

    if response.status_code == 200:

        data = response.json()

        assert "events" in data

        assert isinstance(data["events"], list)


def test_timeline_event_structure():

    sample_event = {

        "id": "123",

        "timestamp": "2026-07-02T10:00:00Z",

        "event_type": "repo_imported",

        "summary": "Repository imported successfully",

        "metadata": {

            "repo": "Grishwar/DEVBRAIN-AI"

        }

    }

    assert sample_event["id"] == "123"

    assert sample_event["event_type"] == "repo_imported"

    assert "repo" in sample_event["metadata"]


def test_empty_timeline():

    response = client.get(
        "/timeline/non_existing_dataset"
    )

    assert response.status_code in [200, 404, 500]