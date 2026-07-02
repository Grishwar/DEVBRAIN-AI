"""
GitHub Service

Responsible for:
- Connecting to GitHub
- Reading repositories
- Downloading source code
- Reading README
- Reading commits
- Reading pull requests
- Reading issues
"""

from __future__ import annotations

import os
from typing import List, Optional

from github import Github
from github.Repository import Repository

from utils.helpers import (
    is_text_file,
    repo_path,
)


class GitHubService:
    """
    Wrapper around the PyGithub library.
    """

    def __init__(self, token: Optional[str] = None):

        self.token = token or os.getenv("GITHUB_TOKEN")

        if not self.token:
            raise ValueError("GITHUB_TOKEN is missing from .env")

        self.client = Github(self.token)

    # ------------------------------------------------------------
    # Repository
    # ------------------------------------------------------------

    def get_repository(self, repository: str) -> Repository:
        """
        Returns a Repository object.

        Example:
            "Grishwar/DEVBRAIN-AI"
        """

        return self.client.get_repo(repository)

    def get_repository_from_url(self, url: str) -> Repository:
        """
        Returns repository from GitHub URL.
        """

        return self.get_repository(repo_path(url))

    # ------------------------------------------------------------
    # README
    # ------------------------------------------------------------

    def get_readme(self, repo: Repository) -> str:

        try:
            readme = repo.get_readme()

            return readme.decoded_content.decode(
                "utf-8",
                errors="ignore",
            )

        except Exception:

            return ""

    # ------------------------------------------------------------
    # Source Files
    # ------------------------------------------------------------

    def get_source_files(
        self,
        repo: Repository,
        branch: str = "main",
    ) -> List[str]:

        chunks = []

        try:

            queue = repo.get_contents("", ref=branch)

            while queue:

                item = queue.pop(0)

                if item.type == "dir":

                    queue.extend(
                        repo.get_contents(
                            item.path,
                            ref=branch,
                        )
                    )

                elif item.type == "file":

                    if not is_text_file(item.name):
                        continue

                    if item.size > 100000:
                        continue

                    try:

                        code = item.decoded_content.decode(
                            "utf-8",
                            errors="ignore",
                        )

                        chunks.append(
                            f"=== FILE: {item.path} ===\n{code}"
                        )

                    except Exception:
                        pass

        except Exception:
            pass

        return chunks

    # ------------------------------------------------------------
    # Issues
    # ------------------------------------------------------------

    def get_open_issues(
        self,
        repo: Repository,
        limit: int = 50,
    ) -> List[str]:

        chunks = []

        try:

            for issue in repo.get_issues(state="open")[:limit]:

                chunks.append(
                    f"""
ISSUE #{issue.number}

Title:
{issue.title}

Body:
{issue.body or ""}
"""
                )

        except Exception:
            pass

        return chunks

    # ------------------------------------------------------------
    # Pull Requests
    # ------------------------------------------------------------

    def get_pull_requests(
        self,
        repo: Repository,
        limit: int = 20,
    ) -> List[str]:

        chunks = []

        try:

            pulls = repo.get_pulls(
                state="closed",
                sort="updated",
            )

            count = 0

            for pr in pulls:

                if not pr.merged:
                    continue

                chunks.append(
                    f"""
PULL REQUEST #{pr.number}

Title:
{pr.title}

Body:
{pr.body or ""}
"""
                )

                count += 1

                if count >= limit:
                    break

        except Exception:
            pass

        return chunks

    # ------------------------------------------------------------
    # Collect Repository Memory
    # ------------------------------------------------------------

    def collect_chunks(
        self,
        repo: Repository,
        branch: str = "main",
    ) -> List[str]:

        chunks = []

        readme = self.get_readme(repo)

        if readme:

            chunks.append(
                f"=== README ===\n{readme}"
            )

        chunks.extend(
            self.get_source_files(
                repo,
                branch,
            )
        )

        chunks.extend(
            self.get_open_issues(repo)
        )

        chunks.extend(
            self.get_pull_requests(repo)
        )

        return chunks

    # ------------------------------------------------------------
    # Fetch Single File
    # ------------------------------------------------------------

    def fetch_file(
        self,
        repo: Repository,
        path: str,
        ref: str,
    ) -> Optional[str]:

        try:

            content = repo.get_contents(
                path,
                ref=ref,
            )

            return content.decoded_content.decode(
                "utf-8",
                errors="ignore",
            )

        except Exception:

            return None