"""
GitHub service — fetches repository content using PyGithub.

Optimized for Groq Free Tier:
- Limits repository size
- Skips unnecessary folders
- Reduces token usage
"""

import os
from typing import Optional
from github import Github, Repository


# ---------------------------------------------------------
# Free Tier Limits
# ---------------------------------------------------------

MAX_FILES = 15
MAX_FILE_SIZE = 50_000

SKIP_FOLDERS = {
    ".git",
    ".github",
    ".next",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "__pycache__",
    ".venv",
    "venv",
    ".idea",
    ".vscode",
}

ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".json",
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".toml",
    ".css",
    ".html",
}


class GitHubService:
    """Wrapper around PyGithub."""

    def __init__(self, token: Optional[str] = None):
        self._token = token or os.getenv("GITHUB_TOKEN")
        self._client = Github(self._token)

    def get_repo(self, repo_path: str) -> Repository.Repository:
        return self._client.get_repo(repo_path)

    def collect_chunks(
        self,
        repo: Repository.Repository,
        branch: str = "main",
    ) -> list[str]:
        """
        Collect repository chunks.

        Order:
            README
            Source files
            Issues
            Pull Requests
        """

        chunks = []

        chunks.extend(self._readme_chunks(repo))
        chunks.extend(self._source_chunks(repo, branch))
        chunks.extend(self._issue_chunks(repo))
        chunks.extend(self._pr_chunks(repo))

        return chunks

    def fetch_file(
        self,
        repo: Repository.Repository,
        path: str,
        ref: str,
    ) -> Optional[str]:

        try:
            content = repo.get_contents(path, ref=ref)
            return content.decoded_content.decode(errors="replace")
        except Exception:
            return None

    # -----------------------------------------------------
    # README
    # -----------------------------------------------------

    def _readme_chunks(self, repo):

        try:

            readme = repo.get_readme()

            return [
                f"=== README ===\n"
                f"{readme.decoded_content.decode(errors='replace')[:3000]}"
            ]

        except Exception:
            return []

    # -----------------------------------------------------
    # Source Files
    # -----------------------------------------------------

    def _source_chunks(self, repo, branch):

        chunks = []

        try:

            queue = list(repo.get_contents("", ref=branch))

            count = 0

            while queue and count < MAX_FILES:

                item = queue.pop(0)

                # Skip unwanted folders

                if any(folder in item.path.split("/") for folder in SKIP_FOLDERS):
                    continue

                if item.type == "dir":

                    try:
                        queue.extend(
                            repo.get_contents(item.path, ref=branch)
                        )
                    except Exception:
                        pass

                    continue

                if item.size > MAX_FILE_SIZE:
                    continue

                _, ext = os.path.splitext(item.name)

                if ext.lower() not in ALLOWED_EXTENSIONS:
                    continue

                try:

                    source = item.decoded_content.decode(errors="replace")

                    chunks.append(
                        f"=== FILE: {item.path} ===\n{source}"
                    )

                    count += 1

                except Exception:
                    pass

        except Exception:
            pass

        return chunks

    # -----------------------------------------------------
    # Issues
    # -----------------------------------------------------

    def _issue_chunks(self, repo):

        chunks = []

        try:

            issues = list(repo.get_issues(state="open"))[:5]

            for issue in issues:

                chunks.append(
                    f"=== ISSUE #{issue.number}: {issue.title} ===\n"
                    f"{(issue.body or '')[:500]}"
                )

        except Exception:
            pass

        return chunks

    # -----------------------------------------------------
    # Pull Requests
    # -----------------------------------------------------

    def _pr_chunks(self, repo):

        chunks = []

        try:

            prs = list(
                repo.get_pulls(
                    state="closed",
                    sort="updated",
                )
            )[:5]

            for pr in prs:

                if pr.merged:

                    chunks.append(
                        f"=== PR #{pr.number}: {pr.title} ===\n"
                        f"{(pr.body or '')[:500]}"
                    )

        except Exception:
            pass

        return chunks