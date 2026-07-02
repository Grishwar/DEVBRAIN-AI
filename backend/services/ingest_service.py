"""
Ingest Service

Responsible for:
- Fetching a GitHub repository
- Building repository memory
- Storing repository knowledge in Cognee
- Creating timeline events
"""

from github_client.github_service import GitHubService
from memory.cognee_service import CogneeService

from models.schemas import (
    IngestRequest,
    IngestResponse,
)

from utils.helpers import (
    dataset_name,
)


class IngestService:

    def __init__(self):

        self.github = GitHubService()
        self.memory = CogneeService()

    async def ingest(
        self,
        request: IngestRequest,
    ) -> IngestResponse:

        # -------------------------------------
        # Dataset name
        # -------------------------------------

        dataset = (
            request.dataset_id
            if request.dataset_id
            else dataset_name(request.repo_url)
        )

        # -------------------------------------
        # Load repository
        # -------------------------------------

        repo = self.github.get_repository_from_url(
            request.repo_url
        )

        # -------------------------------------
        # Read repository
        # -------------------------------------

        chunks = self.github.collect_chunks(
            repo=repo,
            branch=request.branch,
        )

        if not chunks:
            raise Exception(
                "Repository contains no readable files."
            )

        # -------------------------------------
        # Store in Cognee
        # -------------------------------------

        await self.memory.remember(
            "\n\n".join(chunks),
            dataset_name=dataset,
        )

        # -------------------------------------
        # Timeline
        # -------------------------------------

        await self.memory.record_timeline_event(
            dataset_name=dataset,
            event_type="repository_imported",
            summary=f"Imported {repo.full_name}",
            metadata={
                "repository": repo.full_name,
                "branch": request.branch,
                "chunks": len(chunks),
            },
        )

        # -------------------------------------
        # Response
        # -------------------------------------

        return IngestResponse(
            status="ok",
            dataset_id=dataset,
            chunks_ingested=len(chunks),
            message=f"Repository memory created for {repo.full_name}",
        )