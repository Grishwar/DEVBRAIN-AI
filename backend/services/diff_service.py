"""
Diff Service

Responsible for:
- Updating repository memory after new commits
- Performing semantic diff using Cognee
- Recording timeline events
"""

from github_client.github_service import GitHubService
from memory.cognee_service import CogneeService
from models.schemas import (
    DiffRequest,
    DiffResponse,
)


class DiffService:

    def __init__(self):
        self.github = GitHubService()
        self.memory = CogneeService()

    async def semantic_diff(
        self,
        request: DiffRequest,
    ) -> DiffResponse:

        # -----------------------------------------
        # Resolve repository
        # -----------------------------------------

        repository = request.dataset_id.replace("__", "/")

        repo = self.github.get_repository(repository)

        updated_chunks = []

        # -----------------------------------------
        # Download changed files
        # -----------------------------------------

        for file_path in request.changed_files:

            content = self.github.fetch_file(
                repo=repo,
                path=file_path,
                ref=request.commit_sha,
            )

            if content:

                updated_chunks.append(
                    f"""
=== UPDATED FILE ===

Path:
{file_path}

Commit:
{request.commit_sha}

Content:

{content}
"""
                )

        # -----------------------------------------
        # Update memory
        # -----------------------------------------

        if updated_chunks:

            await self.memory.update_repository(
                dataset_name=request.dataset_id,
                chunks=updated_chunks,
            )

        # -----------------------------------------
        # Improve semantic graph
        # -----------------------------------------

        try:
            await self.memory.improve(
                request.dataset_id,
            )
        except Exception:
            pass

        # -----------------------------------------
        # Semantic summary
        # -----------------------------------------

        prompt = f"""
Explain the semantic changes introduced by this commit.

Commit SHA:
{request.commit_sha}

Commit Message:
{request.commit_message}

Changed Files:
{", ".join(request.changed_files)}
"""

        summary = ""

        try:

            results = await self.memory.search(
                dataset_name=request.dataset_id,
                question=prompt,
            )

            for text, _ in results:

                if text:
                    summary += text + "\n\n"

        except Exception:

            summary = (
                "Repository updated successfully. "
                "Semantic summary is not available yet because "
                "Cognee is still indexing the updated dataset."
            )

        if not summary.strip():

            summary = (
                "Repository updated successfully. "
                "No semantic differences were detected."
            )

        # -----------------------------------------
        # Timeline
        # -----------------------------------------

        try:

            await self.memory.record_timeline_event(

                dataset_name=request.dataset_id,

                event_type="commit",

                summary=request.commit_message,

                metadata={
                    "commit": request.commit_sha,
                    "files": request.changed_files,
                },

            )

        except Exception:
            pass

        # -----------------------------------------
        # Response
        # -----------------------------------------

        return DiffResponse(

            status="ok",

            commit_sha=request.commit_sha,

            files_updated=len(updated_chunks),

            semantic_summary=summary.strip(),

        )