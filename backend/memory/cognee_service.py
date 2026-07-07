"""
Cognee memory service — cognee 1.2.2 compatible.

Fix for DatasetNotFoundError:
- remember() uses cognee.add() + cognee.cognify() with fallback
- recall() falls back to global search if dataset lookup fails
- Debug prints kept to verify retrieval behaviour
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Tuple

import cognee

from utils.helpers import (
    extract_result,
    build_timeline_text,
    parse_timeline_text,
)


class CogneeService:

    # ============================================================
    # Remember
    # ============================================================

    async def remember(
        self,
        text: str,
        dataset_name: str,
    ) -> None:
        """
        Store text in Cognee memory.
        """
        try:
            await cognee.add(
                text,
                dataset_name=dataset_name,
            )
            await cognee.cognify(
                datasets=[dataset_name],
            )
            print(f"Dataset '{dataset_name}' indexed successfully.")

        except Exception as e:
            print("remember() failed:", e)
            try:
                await cognee.remember(
                    text,
                    dataset_name=dataset_name,
                )
                print("Fallback remember() succeeded.")
            except Exception as e2:
                print("remember() fallback also failed:", e2)
                raise

    # ============================================================
    # Recall
    # ============================================================

    async def recall(
        self,
        query: str,
        datasets: list[str] | None = None,
    ) -> list[tuple[str, dict]]:

        kwargs = {
            "query_text": query,
        }

        if datasets:
            kwargs["datasets"] = datasets

        try:
            raw_results = await cognee.recall(**kwargs)
            print("Dataset recall succeeded.")

        except Exception as e:
            print("Dataset lookup failed:", e)
            print("Trying global recall...")

            try:
                raw_results = await cognee.recall(
                    query_text=query,
                )
                print("Global recall succeeded.")

            except Exception as e2:
                print("Global recall also failed:", e2)
                raw_results = []

        print("Total Results:", len(raw_results or []))

        return [
            extract_result(r)
            for r in (raw_results or [])
        ]

    # ============================================================
    # Improve
    # ============================================================

    async def improve(self, dataset_name: str) -> None:
        try:
            await cognee.improve(dataset=dataset_name)
        except Exception:
            pass

    # ============================================================
    # Forget
    # ============================================================

    async def forget(self, dataset_name: str) -> None:
        try:
            await cognee.forget(dataset=dataset_name)
        except Exception:
            try:
                await cognee.prune(dataset=dataset_name)
            except Exception:
                pass

    # ============================================================
    # Timeline Event
    # ============================================================

    async def record_timeline_event(
        self,
        dataset_name: str,
        event_type: str,
        summary: str,
        metadata: Dict,
    ) -> None:
        event_id  = str(uuid.uuid4())
        timestamp = datetime.now(timezone.utc).isoformat()
        text = build_timeline_text(
            event_type=event_type,
            event_id=event_id,
            timestamp=timestamp,
            summary=summary,
            metadata=metadata,
        )
        try:
            await self.remember(text=text, dataset_name=dataset_name)
        except Exception:
            pass

    # ============================================================
    # Timeline Reader
    # ============================================================

    async def get_timeline_events(self, datasets: List[str]):
        results = await self.recall("TIMELINE EVENT", datasets=datasets)
        events = []
        for text, metadata in results:
            if not text:
                continue
            if "TIMELINE EVENT" not in text:
                continue
            parsed = parse_timeline_text(text)
            if parsed:
                events.append(parsed)
        events.sort(key=lambda e: e.get("timestamp", ""))
        return events

    # ============================================================
    # Search Wrapper
    # ============================================================

    async def search(self, dataset_name: str, question: str):
        return await self.recall(question, datasets=[dataset_name])

    # ============================================================
    # Repository Add
    # ============================================================

    async def add_repository(self, dataset_name: str, chunks: List[str]):
        if not chunks:
            return
        combined = "\n\n".join(chunks)
        await self.remember(combined, dataset_name)
        await self.improve(dataset_name)

    # ============================================================
    # Repository Update
    # ============================================================

    async def update_repository(self, dataset_name: str, chunks: List[str]):
        if not chunks:
            return
        combined = "\n\n".join(chunks)
        await self.remember(combined, dataset_name)
        await self.improve(dataset_name)

    # ============================================================
    # Repository Delete
    # ============================================================

    async def delete_repository(self, dataset_name: str):
        await self.forget(dataset_name)

    # ============================================================
    # Dataset Exists
    # ============================================================

    async def dataset_exists(self, dataset_name: str) -> bool:
        try:
            results = await self.recall("repository", datasets=[dataset_name])
            return len(results) > 0
        except Exception:
            return False

    # ============================================================
    # Health
    # ============================================================

    async def health(self) -> bool:
        try:
            await self.recall("health")
            return True
        except Exception:
            return False