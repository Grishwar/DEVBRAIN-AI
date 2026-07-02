"""
Graph Layout

Responsible for positioning graph nodes.

Currently uses a simple grid layout that works well with React Flow.

Future improvements:
- Dagre Layout
- ELK Layout
- Force-directed Layout
"""

from models.schemas import GraphNode


class GraphLayout:
    """
    Applies layout positions to graph nodes.
    """

    def apply_grid_layout(
        self,
        nodes: list[GraphNode],
        columns: int = 5,
        x_spacing: int = 220,
        y_spacing: int = 140,
    ) -> list[GraphNode]:
        """
        Arrange nodes in a simple grid.
        """

        for index, node in enumerate(nodes):

            row = index // columns
            col = index % columns

            node.position = {
                "x": col * x_spacing,
                "y": row * y_spacing,
            }

        return nodes

    def apply_vertical_layout(
        self,
        nodes: list[GraphNode],
        spacing: int = 120,
    ) -> list[GraphNode]:
        """
        Arrange nodes vertically.
        """

        for index, node in enumerate(nodes):

            node.position = {
                "x": 0,
                "y": index * spacing,
            }

        return nodes

    def apply_horizontal_layout(
        self,
        nodes: list[GraphNode],
        spacing: int = 220,
    ) -> list[GraphNode]:
        """
        Arrange nodes horizontally.
        """

        for index, node in enumerate(nodes):

            node.position = {
                "x": index * spacing,
                "y": 0,
            }

        return nodes

    def layout(
        self,
        nodes: list[GraphNode],
        mode: str = "grid",
    ) -> list[GraphNode]:
        """
        Main layout selector.
        """

        if mode == "vertical":
            return self.apply_vertical_layout(nodes)

        if mode == "horizontal":
            return self.apply_horizontal_layout(nodes)

        return self.apply_grid_layout(nodes)