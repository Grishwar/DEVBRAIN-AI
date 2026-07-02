"""
Ask Service

Responsible for:
- Querying Cognee memory
- Returning an AI answer
- Returning confidence scores
- Returning source references
"""

from memory.cognee_service import CogneeService
from models.schemas import (
    AskRequest,
    AskResponse,
    SourceReference,
)


class AskService:

    def __init__(self):

        self.memory = CogneeService()

    async def ask(
        self,
        request: AskRequest,
    ) -> AskResponse:

        # -----------------------------------------
        # Search Cognee Memory
        # -----------------------------------------

        results = await self.memory.search(

            dataset_name=request.dataset_id,

            question=request.question,

        )

        # -----------------------------------------
        # No Results
        # -----------------------------------------

        if not results:

            return AskResponse(

                answer="No relevant information was found in memory.",

                sources=[],

            )

        # -----------------------------------------
        # Build Answer
        # -----------------------------------------

        answer_parts = []

        sources = []

        for text, metadata in results:

            if text:

                answer_parts.append(text)

            sources.append(

                SourceReference(

                    source=metadata.get(

                        "source",

                        "Cognee Memory",

                    ),

                    confidence=float(

                        metadata.get(

                            "score",

                            0.90,

                        )

                    ),

                    last_updated=metadata.get(

                        "updated_at",

                        "",

                    ),

                )

            )

        # -----------------------------------------
        # Remove Duplicate Sources
        # -----------------------------------------

        unique = []

        seen = set()

        for source in sources:

            key = source.source

            if key not in seen:

                unique.append(source)

                seen.add(key)

        # -----------------------------------------
        # Final Answer
        # -----------------------------------------

        final_answer = "\n\n".join(answer_parts)

        if not final_answer.strip():

            final_answer = "Memory search completed, but no readable answer was produced."

        return AskResponse(

            answer=final_answer,

            sources=unique,

        )