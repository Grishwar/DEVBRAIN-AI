"""
Health Service

Provides health information about the backend and its
dependencies.

This endpoint can later be extended to verify:
- Cognee
- Neo4j
- Qdrant
- GitHub API
"""

from datetime import datetime, timezone

from memory.cognee_service import CogneeService
from models.schemas import HealthResponse


class HealthService:

    def __init__(self):

        self.memory = CogneeService()

    async def check(self) -> HealthResponse:

        status = "ok"

        # Check Cognee connectivity
        try:

            await self.memory.health()

        except Exception:

            status = "degraded"

        return HealthResponse(

            status=status,

            timestamp=datetime.now(
                timezone.utc
            ).isoformat(),

        )