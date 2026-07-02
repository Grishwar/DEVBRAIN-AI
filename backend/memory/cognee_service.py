"""
Cognee Service

Central wrapper around Cognee 1.2.2.

This class is responsible for:
- remember()
- recall()
- improve()
- forget()
- timeline events

Every other service communicates with Cognee ONLY through this file.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Tuple

import cognee

from utils.helpers import (
    build_timeline_text,
    extract_result,
    parse_timeline_text,
)


class CogneeService:

    """
    Wrapper around Cognee APIs.
    """

    # --------------------------------------------------------
    # Remember
    # --------------------------------------------------------

    async def remember(
        self,
        text: str,
        dataset_name: str,
    ):

        """
        Store information inside Cognee memory.
        """

        await cognee.remember(
            text,
            dataset_name=dataset_name,
        )

    # --------------------------------------------------------
    # Recall
    # --------------------------------------------------------

    async def recall(
        self,
        query: str,
        datasets: List[str] | None = None,
    ) -> List[Tuple[str, Dict]]:

        kwargs = {
            "query_text": query,
        }

        if datasets:
            kwargs["datasets"] = datasets

        results = await cognee.recall(**kwargs)

        normalized = []

        for item in results or []:
            normalized.append(extract_result(item))

        return normalized

    # --------------------------------------------------------
    # Improve
    # --------------------------------------------------------

    async def improve(
        self,
        dataset_name: str,
    ):

        """
        Improve semantic relationships.
        """

        await cognee.improve(
            dataset=dataset_name,
        )

    # --------------------------------------------------------
    # Forget
    # --------------------------------------------------------

    async def forget(
        self,
        dataset_name: str,
    ):

        """
        Remove an entire dataset.
        """

        await cognee.forget(
            dataset=dataset_name,
        )

    # ========================================================
    # Timeline
    # ========================================================

    async def record_timeline_event(

        self,

        dataset_name: str,

        event_type: str,

        summary: str,

        metadata: Dict,

    ):

        event_id = str(uuid.uuid4())

        timestamp = datetime.now(
            timezone.utc,
        ).isoformat()

        text = build_timeline_text(

            event_type=event_type,

            event_id=event_id,

            timestamp=timestamp,

            summary=summary,

            metadata=metadata,

        )

        await self.remember(

            text=text,

            dataset_name=dataset_name,

        )

    # ========================================================
    # Timeline Reader
    # ========================================================

    async def get_timeline_events(

        self,

        datasets: List[str],

    ):

        results = await self.recall(

            query="TIMELINE_EVENT",

            datasets=datasets,

        )

        events = []

        for text, metadata in results:

            if not text:

                continue

            parsed = parse_timeline_text(text)

            if parsed:

                events.append(parsed)

        events.sort(

            key=lambda e: e.get("timestamp", "")

        )

        return events

    # ========================================================
    # Search Wrapper
    # ========================================================

    async def search(

        self,

        dataset_name: str,

        question: str,

    ):

        return await self.recall(

            question,

            datasets=[dataset_name],

        )

    # ========================================================
    # Add Repository
    # ========================================================

    async def add_repository(

        self,

        dataset_name: str,

        chunks: List[str],

    ):

        if not chunks:

            return

        combined = "\n\n".join(chunks)

        await self.remember(

            text=combined,

            dataset_name=dataset_name,

        )

        await self.improve(

            dataset_name,

        )

    # ========================================================
    # Update Repository
    # ========================================================

    async def update_repository(

        self,

        dataset_name: str,

        chunks: List[str],

    ):

        if not chunks:

            return

        combined = "\n\n".join(chunks)

        await self.remember(

            combined,

            dataset_name=dataset_name,

        )

        await self.improve(

            dataset_name,

        )

    # ========================================================
    # Delete Repository
    # ========================================================

    async def delete_repository(

        self,

        dataset_name: str,

    ):

        await self.forget(

            dataset_name,

        )

    # ========================================================
    # Dataset Exists
    # ========================================================

    async def dataset_exists(

        self,

        dataset_name: str,

    ) -> bool:

        try:

            results = await self.recall(

                "repository",

                datasets=[dataset_name],

            )

            return len(results) > 0

        except Exception:

            return False

    # ========================================================
    # Health Check
    # ========================================================

    async def health(self):

        try:

            await self.recall("health")

            return True

        except Exception:

            return False