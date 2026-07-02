"""
DevBrain AI Helper Utilities

Shared utility functions used throughout the backend.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import uuid
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


# ==========================================================
# GitHub URL Helpers
# ==========================================================

def repo_path(repo_url: str) -> str:
    """
    https://github.com/user/repo
            ↓
    user/repo
    """
    return repo_url.rstrip("/").replace("https://github.com/", "")


def repo_slug(repo_url: str) -> str:
    """
    https://github.com/user/repo
            ↓
    user__repo
    """
    return repo_path(repo_url).replace("/", "__")


def repo_name(repo_url: str) -> str:
    """
    user/repo -> repo
    """
    return repo_path(repo_url).split("/")[-1]


def repo_owner(repo_url: str) -> str:
    """
    user/repo -> user
    """
    return repo_path(repo_url).split("/")[0]


# ==========================================================
# Dataset Helpers
# ==========================================================

def dataset_name(repo_url: str) -> str:
    return repo_slug(repo_url)


def make_node_id(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


# ==========================================================
# UUID Helpers
# ==========================================================

def new_uuid() -> str:
    return str(uuid.uuid4())


# ==========================================================
# File Helpers
# ==========================================================

TEXT_EXTENSIONS = {
    ".py",
    ".java",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".json",
    ".yaml",
    ".yml",
    ".md",
    ".txt",
    ".html",
    ".css",
    ".scss",
    ".xml",
    ".sql",
    ".env",
    ".toml",
    ".ini",
    ".dockerfile",
    ".sh",
    ".bat",
}


def is_text_file(filename: str) -> bool:
    suffix = Path(filename).suffix.lower()

    if suffix in TEXT_EXTENSIONS:
        return True

    if filename.lower() == "dockerfile":
        return True

    if filename.lower().endswith(".env.example"):
        return True

    return False


# ==========================================================
# Timeline Helpers
# ==========================================================

TIMELINE_PREFIX = "TIMELINE_EVENT"


def build_timeline_text(
    event_type: str,
    event_id: str,
    timestamp: str,
    summary: str,
    metadata: Dict[str, Any],
) -> str:
    """
    Store timeline events as plain text so Cognee can remember them.
    """

    return (
        f"{TIMELINE_PREFIX}|"
        f"{event_type}|"
        f"{event_id}|"
        f"{timestamp}|"
        f"{summary}|"
        f"{json.dumps(metadata)}"
    )


def parse_timeline_text(text: str):

    if not text.startswith(TIMELINE_PREFIX):
        return None

    try:

        _, event_type, event_id, timestamp, summary, metadata = text.split(
            "|",
            maxsplit=5,
        )

        return {
            "id": event_id,
            "timestamp": timestamp,
            "event_type": event_type,
            "summary": summary,
            "metadata": json.loads(metadata),
        }

    except Exception:
        return None


# ==========================================================
# Cognee Helpers
# ==========================================================

def extract_result(result) -> Tuple[str, Dict]:

    """
    Cognee may return

    str

    dict

    object

    Normalize everything.
    """

    if result is None:
        return "", {}

    if isinstance(result, str):
        return result, {}

    if isinstance(result, dict):

        text = (
            result.get("text")
            or result.get("content")
            or result.get("answer")
            or ""
        )

        metadata = result.get("metadata", {})

        return str(text), metadata

    text = getattr(result, "text", None)

    if text is None:
        text = getattr(result, "content", "")

    metadata = getattr(result, "metadata", {})

    return str(text), metadata


# ==========================================================
# Validation Helpers
# ==========================================================

GITHUB_PATTERN = r"^https://github\.com/[^/]+/[^/]+/?$"


def validate_repo_url(url: str) -> bool:
    return re.match(GITHUB_PATTERN, url) is not None


# ==========================================================
# Misc
# ==========================================================

def chunk_text(text: str, chunk_size: int = 2000):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start = end

    return chunks


def safe_read(path: str):

    try:

        with open(path, "r", encoding="utf-8") as f:

            return f.read()

    except Exception:

        return ""


def safe_write(path: str, content: str):

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:

        f.write(content)


def truncate(text: str, limit: int = 300):

    if len(text) <= limit:
        return text

    return text[:limit] + "..."


def current_timestamp():

    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()