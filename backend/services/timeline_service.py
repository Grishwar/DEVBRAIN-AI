"""
Timeline Service

Responsible for:
- Retrieving timeline events from Cognee
- Formatting them for the frontend
"""

from memory.cognee_service import CogneeService
from models.schemas import (
    TimelineEvent,
    TimelineResponse,
)


class TimelineService:

    def __init__(self):

        self.memory = CogneeService()

    async def get_timeline(
        self,
        dataset_id: str,
    ) -> TimelineResponse:

        # Search both the main dataset and tombstones
        datasets = [
            dataset_id,
            f"{dataset_id}_tombstones",
        ]

        events = await self.memory.get_timeline_events(
            datasets=datasets,
        )

        timeline = []

        for event in events:

            timeline.append(

                TimelineEvent(

                    id=event.get("id"),

                    timestamp=event.get("timestamp"),

                    event_type=event.get("event_type"),

                    summary=event.get("summary"),

                    metadata=event.get("metadata", {}),

                )

            )

        return TimelineResponse(
            events=timeline
        )