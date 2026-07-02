"""
Graph Mapper

Maps Cognee recall results into normalized graph entities.

This keeps graph transformation logic separate from graph building.
"""

from typing import List, Tuple


class GraphMapper:
    """
    Converts Cognee recall output into normalized graph data.
    """

    def map_results(
        self,
        recall_results: List[Tuple[str, dict]],
    ) -> List[dict]:
        """
        Convert recall results into dictionaries.

        Example output:

        [
            {
                "label": "...",
                "metadata": {...}
            }
        ]
        """

        mapped = []

        for text, metadata in recall_results:

            if not text:
                continue

            mapped.append(
                {
                    "label": text.strip(),
                    "metadata": metadata or {},
                }
            )

        return mapped

    def filter_duplicates(
        self,
        mapped_results: List[dict],
    ) -> List[dict]:
        """
        Remove duplicate graph nodes.
        """

        unique = []
        seen = set()

        for item in mapped_results:

            label = item["label"]

            if label in seen:
                continue

            seen.add(label)

            unique.append(item)

        return unique

    def map(
        self,
        recall_results: List[Tuple[str, dict]],
    ) -> List[dict]:
        """
        Complete mapping pipeline.
        """

        mapped = self.map_results(recall_results)

        return self.filter_duplicates(mapped)