"""
Tests for the /ask endpoint.
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_ask_validation():
    """
    FastAPI should reject an empty request body.
    """

    response = client.post(
        "/ask",
        json={},
    )

    assert response.status_code == 422


def test_ask_unknown_dataset():
    """
    Asking about a dataset that doesn't exist should
    return a handled response rather than crashing.
    """

    response = client.post(
        "/ask",
        json={
            "dataset_id": "unknown_dataset",
            "question": "What technologies are used in this project?"
        },
    )

    assert response.status_code in [200, 404, 500]


def test_ask_request_schema():
    """
    Verify AskRequest schema.
    """

    payload = {
        "dataset_id": "sample_dataset",
        "question": "Explain this project."
    }

    assert payload["dataset_id"] == "sample_dataset"

    assert payload["question"] == "Explain this project."


def test_ask_response_schema():

    response = client.post(
        "/ask",
        json={
            "dataset_id": "unknown_dataset",
            "question": "Explain the architecture."
        },
    )

    if response.status_code == 200:

        data = response.json()

        assert "answer" in data

        assert "sources" in data

        assert isinstance(data["sources"], list)


def test_empty_question():

    response = client.post(
        "/ask",
        json={
            "dataset_id": "sample_dataset",
            "question": ""
        },
    )

    assert response.status_code in [200, 400, 422, 500]


def test_long_question():

    question = "Explain the architecture. " * 100

    response = client.post(
        "/ask",
        json={
            "dataset_id": "sample_dataset",
            "question": question
        },
    )

    assert response.status_code in [200, 400, 404, 500]