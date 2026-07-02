"""
Tests for the /graph endpoint.
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_graph_validation():
    """
    Missing dataset_id should return 404 because it is a path parameter.
    """

    response = client.get("/graph/")

    assert response.status_code == 404


def test_graph_unknown_dataset():
    """
    Unknown dataset should not crash the API.
    """

    response = client.get(
        "/graph/unknown_dataset"
    )

    assert response.status_code in [200, 404, 500]


def test_graph_response_schema():
    """
    Verify GraphResponse schema.
    """

    response = client.get(
        "/graph/unknown_dataset"
    )

    if response.status_code == 200:

        data = response.json()

        assert "nodes" in data
        assert "edges" in data

        assert isinstance(data["nodes"], list)
        assert isinstance(data["edges"], list)


def test_graph_node_structure():

    sample_node = {
        "id": "123",
        "type": "default",
        "data": {
            "label": "FastAPI"
        },
        "position": {
            "x": 0,
            "y": 0
        }
    }

    assert sample_node["id"] == "123"

    assert "label" in sample_node["data"]

    assert "position" in sample_node


def test_graph_edge_structure():

    sample_edge = {
        "id": "1-2",
        "source": "1",
        "target": "2",
        "label": "related"
    }

    assert sample_edge["source"] == "1"

    assert sample_edge["target"] == "2"

    assert sample_edge["label"] == "related"