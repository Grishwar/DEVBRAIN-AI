"""
Ingest Service

Responsible for:
- Fetching a GitHub repository
- Building repository memory
- Storing repository knowledge in Cognee
- Creating timeline events
"""

import time

from github_client.github_service import GitHubService
from memory.cognee_service import CogneeService

from models.schemas import (
    IngestRequest,
    IngestResponse,
)

from utils.helpers import dataset_name


class IngestService:

    def __init__(self):
        self.github = GitHubService()
        self.memory = CogneeService()

    async def ingest(
        self,
        request: IngestRequest,
    ) -> IngestResponse:

        total_start = time.time()

        print("\n" + "=" * 70)
        print("🚀 DEVBRAIN INGEST STARTED")
        print("=" * 70)

        # -------------------------------------------------
        # Dataset Name
        # -------------------------------------------------

        dataset = (
            request.dataset_id
            if request.dataset_id
            else dataset_name(request.repo_url)
        )

        print(f"📦 Dataset: {dataset}")

        # -------------------------------------------------
        # Repository Path
        # -------------------------------------------------

        repo_path = (
            request.repo_url
            .replace("https://github.com/", "")
            .replace("http://github.com/", "")
            .strip("/")
        )

        print(f"📂 Repository: {repo_path}")

        # -------------------------------------------------
        # Load GitHub Repository
        # -------------------------------------------------

        start = time.time()

        repo = self.github.get_repo(repo_path)

        print(
            f"✅ GitHub repository loaded in {time.time() - start:.2f} sec"
        )

        # -------------------------------------------------
        # Read Repository Files
        # -------------------------------------------------

        start = time.time()

        chunks = self.github.collect_chunks(
            repo=repo,
            branch=request.branch,
        )

        print(
            f"✅ Repository parsed in {time.time() - start:.2f} sec"
        )

        if not chunks:
            raise Exception(
                "Repository contains no readable files."
            )

        print(f"📄 Total Chunks: {len(chunks)}")

        # -------------------------------------------------
        # Store Repository in Cognee
        # -------------------------------------------------

        start = time.time()

        await self.memory.add_repository(
            dataset_name=dataset,
            chunks=chunks,
        )

        print(
            f"✅ Cognee indexing completed in {time.time() - start:.2f} sec"
        )

        # -------------------------------------------------
        # Verify Dataset Exists
        # -------------------------------------------------

        start = time.time()

        exists = await self.memory.dataset_exists(dataset)

        print(
            f"✅ Dataset verification completed in {time.time() - start:.2f} sec"
        )

        if not exists:
            raise Exception(
                f"Repository was ingested, but dataset '{dataset}' was not found in Cognee."
            )

        # -------------------------------------------------
        # Record Timeline Event
        # -------------------------------------------------

        start = time.time()

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

        print(
            f"✅ Timeline stored in {time.time() - start:.2f} sec"
        )

        print(
            f"\n🎉 TOTAL INGEST TIME: {time.time() - total_start:.2f} sec"
        )

        print("=" * 70 + "\n")

        # -------------------------------------------------
        # Success Response
        # -------------------------------------------------

        return IngestResponse(
            status="ok",
            dataset_id=dataset,
            chunks_ingested=len(chunks),
            message=f"Repository memory created for {repo.full_name}",
        )