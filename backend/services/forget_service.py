"""
Forget Service

Responsible for:
- Removing obsolete knowledge
- Creating tombstone memories
- Recording timeline events
"""

from datetime import datetime, timezone

from memory.cognee_service import CogneeService
from models.schemas import (
    ForgetRequest,
    ForgetResponse,
)


class ForgetService:

    def __init__(self):

        self.memory = CogneeService()

    async def forget_module(
        self,
        request: ForgetRequest,
    ) -> ForgetResponse:

        # --------------------------------------------------
        # Tombstone Dataset
        # --------------------------------------------------

        tombstone_dataset = (
            f"{request.dataset_id}_tombstones"
        )

        # --------------------------------------------------
        # Create Tombstone
        # --------------------------------------------------

        tombstone = f"""
MODULE REMOVED

Module:
{request.module_name}

Reason:
{request.reason}

Timestamp:
{datetime.now(timezone.utc).isoformat()}
"""

        await self.memory.remember(

            text=tombstone,

            dataset_name=tombstone_dataset,

        )

        # --------------------------------------------------
        # Remove Dataset Memory
        # --------------------------------------------------

        await self.memory.forget(

            dataset_name=request.dataset_id,

        )

        # --------------------------------------------------
        # Timeline Event
        # --------------------------------------------------

        await self.memory.record_timeline_event(

            dataset_name=tombstone_dataset,

            event_type="module_removed",

            summary=f"{request.module_name} removed",

            metadata={

                "module": request.module_name,

                "reason": request.reason,

            },

        )

        # --------------------------------------------------
        # Response
        # --------------------------------------------------

        return ForgetResponse(

            status="ok",

            module=request.module_name,

            message=(
                f"{request.module_name} removed successfully. "
                "A tombstone record has been stored."
            ),

        )