"""
Graph Builder

Converts Cognee recall results into a graph structure that
can be rendered by React Flow.

This module contains no FastAPI code.
"""

from models.schemas import GraphNode, GraphEdge, GraphResponse
from utils.helpers import make_node_id


class GraphBuilder:
    """
    Builds a lightweight knowledge graph from Cognee recall results.
    """

    def build(self, recall_results) -> GraphResponse:
        """
        Parameters
        ----------
        recall_results:
            List of tuples returned by Cognee.
            Example:
                [
                    ("FastAPI handles routing", {}),
                    ("Cognee stores semantic memory", {}),
                ]

        Returns
        -------
        GraphResponse
        """

        nodes = []
        edges = []
        seen = set()

        for index, (text, _) in enumerate(recall_results):

            if not text:
                continue

            node_id = make_node_id(text)

            if node_id not in seen:
                seen.add(node_id)

                nodes.append(
                    GraphNode(
                        id=node_id,
                        type="default",
                        data={
                            "label": text[:60].replace("\n", " ")
                        },
                        position={
                            "x": (index % 5) * 220,
                            "y": (index // 5) * 140,
                        },
                    )
                )

            if len(nodes) >= 2:
                previous = nodes[-2]

                edges.append(
                    GraphEdge(
                        id=f"{previous.id}-{node_id}",
                        source=previous.id,
                        target=node_id,
                        label="related",
                    )
                )

        return GraphResponse(
            nodes=nodes,
            edges=edges,
        )