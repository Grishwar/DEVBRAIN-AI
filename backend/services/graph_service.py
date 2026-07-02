"""
Graph Service

Responsible for:
- Building a lightweight knowledge graph
- Converting Cognee recall results into React Flow nodes/edges

Future improvement:
Replace this with direct Neo4j queries for a true graph visualization.
"""

from memory.cognee_service import CogneeService
from models.schemas import (
    GraphNode,
    GraphEdge,
    GraphResponse,
)
from utils.helpers import make_node_id


class GraphService:

    def __init__(self):

        self.memory = CogneeService()

    async def get_graph(
        self,
        dataset_id: str,
    ) -> GraphResponse:

        # Retrieve the most important entities
        results = await self.memory.recall(

            query="functions classes modules api database services dependencies",

            datasets=[dataset_id],

        )

        nodes = []
        edges = []

        visited = set()

        previous = None

        for index, (text, metadata) in enumerate(results[:20]):

            if not text:
                continue

            node_id = make_node_id(text)

            if node_id in visited:
                continue

            visited.add(node_id)

            label = text.replace("\n", " ")

            if len(label) > 60:
                label = label[:60] + "..."

            node = GraphNode(

                id=node_id,

                data={

                    "label": label,

                },

                type="default",

                position={

                    "x": (index % 5) * 220,

                    "y": (index // 5) * 150,

                },

            )

            nodes.append(node)

            if previous:

                edges.append(

                    GraphEdge(

                        id=f"{previous.id}-{node.id}",

                        source=previous.id,

                        target=node.id,

                        label="related",

                    )

                )

            previous = node

        return GraphResponse(

            nodes=nodes,

            edges=edges,

        )