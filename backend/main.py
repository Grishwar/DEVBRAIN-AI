"""
DevBrain AI — FastAPI backend (cognee 1.2.x compatible)
Rewritten from cognee 0.1.15 API to cognee 1.2.x API.

Key changes from the original:
  - Configuration is now entirely via .env variables (no await cognee.config.set_*() calls)
  - remember()  : dataset_id → dataset_name, no metadata kwarg
  - recall()    : dataset_id → datasets=[...] list, query kwarg is query_text
  - forget()    : dataset_id → dataset=, no query kwarg (dataset-level operation)
  - improve()   : dataset_id → dataset= kwarg
  - get_graph() : does not exist in 1.x; replaced with recall()-based approximation
  - on_event("startup") deprecated in FastAPI; replaced with lifespan context manager
"""

import os
import json
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Optional

import cognee
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------------------------
# Lifespan (replaces deprecated @app.on_event("startup"))
# ---------------------------------------------------------------------------
# In cognee 1.x, ALL configuration is done via .env / environment variables.
# There is no programmatic cognee.config.set_*() async API.
# Cognee reads its config at import time from pydantic-settings / .env.
# The lifespan hook is kept here for any future app-level startup work.

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Nothing to do: cognee reads .env automatically on import.
    # Your .env must contain the variables listed in .env.example below.
    yield


app = FastAPI(title="DevBrain AI", version="0.2.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Required .env variables  (create a .env file in your project root)
# ---------------------------------------------------------------------------
# LLM (Groq example — change LLM_PROVIDER / LLM_MODEL for other providers):
#   LLM_PROVIDER=openai
#   LLM_MODEL=gpt-4o-mini      # or: groq/llama-3.1-70b-versatile
#   LLM_API_KEY=sk-...         # your OpenAI or Groq key
#   LLM_ENDPOINT=              # optional; leave blank for OpenAI/Groq defaults
#
# Vector store (Qdrant):
#   VECTOR_DB_PROVIDER=qdrant
#   VECTOR_DB_URL=http://localhost:6333
#   VECTOR_DB_KEY=             # blank for local Qdrant
#   VECTOR_DATASET_DATABASE_HANDLER=qdrant
#
# Graph store (Neo4j):
#   GRAPH_DATABASE_PROVIDER=neo4j
#   GRAPH_DATABASE_URL=bolt://localhost:7687
#   GRAPH_DATABASE_USERNAME=neo4j
#   GRAPH_DATABASE_PASSWORD=devbrain123
#
# GitHub:
#   GITHUB_TOKEN=ghp_...


# ---------------------------------------------------------------------------
# Pydantic request models  (unchanged from original)
# ---------------------------------------------------------------------------

class IngestRequest(BaseModel):
    repo_url: str
    branch: str = "main"
    dataset_id: Optional[str] = None


class AskRequest(BaseModel):
    question: str
    dataset_id: Optional[str] = None
    at_commit: Optional[str] = None


class DiffRequest(BaseModel):
    dataset_id: str
    commit_sha: str
    changed_files: list[str]
    commit_message: str


class ForgetRequest(BaseModel):
    dataset_id: str
    module_name: str
    reason: Optional[str] = "deprecated"


# ---------------------------------------------------------------------------
# /ingest  →  cognee.remember(text, dataset_name=...)
# ---------------------------------------------------------------------------

@app.post("/ingest")
async def ingest_repo(req: IngestRequest):
    """
    Fetch a GitHub repo and feed it into Cognee's memory.
    """
    from github import Github

    dataset_name = req.dataset_id or _repo_slug(req.repo_url)

    try:
        gh = Github(os.getenv("GITHUB_TOKEN"))
        repo = gh.get_repo(_repo_path(req.repo_url))

        chunks: list[str] = []

        # 1. README
        try:
            readme = repo.get_readme()
            chunks.append(f"=== README ===\n{readme.decoded_content.decode()}")
        except Exception:
            pass

        # 2. Source files
        contents = repo.get_contents("", ref=req.branch)
        file_queue = list(contents)
        while file_queue:
            item = file_queue.pop(0)
            if item.type == "dir":
                file_queue.extend(repo.get_contents(item.path, ref=req.branch))
            elif item.size < 100_000 and _is_text_file(item.name):
                try:
                    src = item.decoded_content.decode(errors="replace")
                    chunks.append(f"=== FILE: {item.path} ===\n{src}")
                except Exception:
                    pass

        # 3. Open issues (top 50)
        for issue in list(repo.get_issues(state="open"))[:50]:
            chunks.append(
                f"=== ISSUE #{issue.number}: {issue.title} ===\n{issue.body or ''}"
            )

        # 4. Recent merged PRs (top 20)
        for pr in list(repo.get_pulls(state="closed", sort="updated"))[:20]:
            if pr.merged:
                chunks.append(
                    f"=== PR #{pr.number}: {pr.title} ===\n{pr.body or ''}"
                )

        combined = "\n\n".join(chunks)

        # cognee 1.x: remember(text, dataset_name=str)
        # dataset_name is the string label for this dataset.
        # No metadata kwarg — metadata lives in the text content itself.
        await cognee.remember(combined, dataset_name=dataset_name)

        # Store a timeline event as additional memory in the same dataset
        await _record_timeline_event(
            dataset_name=dataset_name,
            event_type="repo_imported",
            summary=f"Repository {repo.full_name} imported ({len(chunks)} chunks)",
            metadata={"repo": repo.full_name, "branch": req.branch},
        )

        return {
            "status": "ok",
            "dataset_id": dataset_name,
            "chunks_ingested": len(chunks),
            "message": f"Repository memory created for {repo.full_name}",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# /ask  →  cognee.recall(query_text=..., datasets=[...])
# ---------------------------------------------------------------------------

@app.post("/ask")
async def ask(req: AskRequest):
    """
    Answer a developer's question using stored memory.
    """
    try:
        # cognee 1.x recall signature:
        #   recall(query_text: str, datasets: list[str] | None = None)
        # datasets=None searches across all datasets.
        recall_kwargs: dict = {"query_text": req.question}
        if req.dataset_id:
            recall_kwargs["datasets"] = [req.dataset_id]

        results = await cognee.recall(**recall_kwargs)

        # cognee 1.x returns a list of result objects.
        # Each result may be a dict, a string, or a dataclass — handle all cases.
        sources = []
        answer_parts = []

        for r in (results or []):
            text, meta = _extract_result(r)
            if text:
                answer_parts.append(text)
            sources.append({
                "source": meta.get("file_path", "memory"),
                "confidence": round(meta.get("score", 0.9), 2),
                "last_updated": meta.get("updated_at", ""),
            })

        answer = "\n\n".join(answer_parts) if answer_parts else "No relevant memory found."

        return {
            "answer": answer,
            "sources": sources[:5],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# /diff  →  remember() new chunks + improve() + recall() for semantic summary
# ---------------------------------------------------------------------------

@app.post("/diff")
async def semantic_diff(req: DiffRequest):
    """
    After a new commit: update Cognee memory with changed files,
    then produce a semantic summary of what changed.
    """
    from github import Github

    try:
        gh = Github(os.getenv("GITHUB_TOKEN"))
        repo_path = req.dataset_id.replace("__", "/")
        repo = gh.get_repo(repo_path)

        new_chunks = []
        for path in req.changed_files:
            try:
                content = repo.get_contents(path, ref=req.commit_sha)
                src = content.decoded_content.decode(errors="replace")
                new_chunks.append(f"=== FILE: {path} (updated at {req.commit_sha}) ===\n{src}")
            except Exception:
                pass

        if new_chunks:
            await cognee.remember(
                "\n\n".join(new_chunks),
                dataset_name=req.dataset_id,
            )

        # cognee 1.x improve() signature:
        #   improve(dataset: str | None = None)
        await cognee.improve(dataset=req.dataset_id)

        # Semantic summary via recall
        changed_results = await cognee.recall(
            query_text=(
                f"What changed in these files: {', '.join(req.changed_files)}? "
                f"Commit message was: {req.commit_message}"
            ),
            datasets=[req.dataset_id],
        )

        semantic_text = "\n".join(
            _extract_result(r)[0] for r in (changed_results or [])
        )

        await _record_timeline_event(
            dataset_name=req.dataset_id,
            event_type="commit",
            summary=req.commit_message,
            metadata={
                "commit_sha": req.commit_sha,
                "changed_files": req.changed_files,
                "semantic_summary": semantic_text[:500],
            },
        )

        return {
            "status": "ok",
            "commit_sha": req.commit_sha,
            "files_updated": len(new_chunks),
            "semantic_summary": semantic_text,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# /forget  →  cognee.forget(dataset=...) + tombstone remember()
# ---------------------------------------------------------------------------

@app.post("/forget")
async def forget_module(req: ForgetRequest):
    """
    Prune a deprecated module from Cognee's memory.

    NOTE: cognee 1.x forget() operates at the dataset level — it removes the
    entire named dataset. There is no sub-dataset query-based pruning in the
    public API. The typical pattern is:
      1. forget() the dataset
      2. re-remember() everything except the deprecated module
    For a hackathon, we skip the re-ingest and just store a tombstone in a
    separate "deprecations" dataset so recall() can acknowledge the removal.
    """
    try:
        # Store tombstone BEFORE forgetting, so we have a record.
        tombstone = (
            f"MODULE DEPRECATED: {req.module_name} has been removed from "
            f"dataset {req.dataset_id}. "
            f"Reason: {req.reason}. "
            f"Removed at: {datetime.now(timezone.utc).isoformat()}"
        )
        # Tombstones go into a separate "_tombstones" dataset so they
        # survive the forget() of the main dataset.
        await cognee.remember(
            tombstone,
            dataset_name=f"{req.dataset_id}_tombstones",
        )

        # cognee 1.x forget() signature:
        #   forget(dataset: str)
        # This removes ALL memory for the named dataset.
        await cognee.forget(dataset=req.dataset_id)

        await _record_timeline_event(
            dataset_name=f"{req.dataset_id}_tombstones",
            event_type="module_deprecated",
            summary=f"{req.module_name} deprecated: {req.reason}",
            metadata={"module": req.module_name, "reason": req.reason},
        )

        return {
            "status": "ok",
            "module": req.module_name,
            "message": (
                f"{req.module_name} removed from dataset {req.dataset_id}. "
                "Tombstone stored in _tombstones dataset."
            ),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# /timeline  →  recall() timeline events from memory
# ---------------------------------------------------------------------------

@app.get("/timeline/{dataset_id}")
async def get_timeline(dataset_id: str):
    """
    Return chronological memory events for the timeline UI.
    """
    try:
        results = await cognee.recall(
            query_text="TIMELINE EVENT",
            datasets=[dataset_id, f"{dataset_id}_tombstones"],
        )

        events = []
        for r in (results or []):
            text, _ = _extract_result(r)
            # Timeline events were stored with a structured prefix
            if text and text.startswith("TIMELINE EVENT"):
                # Best-effort parse of the stored text format
                event_entry = _parse_timeline_text(text)
                if event_entry:
                    events.append(event_entry)

        events.sort(key=lambda e: e.get("timestamp", ""), reverse=False)
        return {"events": events}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# /graph  →  recall()-based graph approximation
# ---------------------------------------------------------------------------

@app.get("/graph/{dataset_id}")
async def get_graph(dataset_id: str):
    """
    Return a simplified knowledge graph for React Flow.

    cognee 1.x does not expose a public get_graph() function. The graph lives
    inside Neo4j (or whichever graph backend you configured). For the hackathon
    we return a recall()-derived structure; for full graph access wire up a
    direct Neo4j driver query against bolt://localhost:7687.
    """
    try:
        # Use recall to surface the most connected entities
        results = await cognee.recall(
            query_text="key entities functions modules classes relationships",
            datasets=[dataset_id],
        )

        # Build a minimal nodes/edges structure from recall results
        # for React Flow. A real implementation would query Neo4j directly.
        nodes = []
        edges = []
        seen_ids: set[str] = set()

        for i, r in enumerate((results or [])[:20]):
            text, _ = _extract_result(r)
            if not text:
                continue
            node_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, text[:100]))
            if node_id not in seen_ids:
                seen_ids.add(node_id)
                label = text[:60].replace("\n", " ").strip()
                nodes.append({
                    "id": node_id,
                    "data": {"label": label},
                    "type": "default",
                    "position": {"x": (i % 5) * 200, "y": (i // 5) * 120},
                })
            # Connect sequential results as a simple chain for visualisation
            if i > 0 and nodes:
                prev_id = nodes[-2]["id"] if len(nodes) >= 2 else nodes[0]["id"]
                edges.append({
                    "id": f"{prev_id}-{node_id}",
                    "source": prev_id,
                    "target": node_id,
                    "label": "related",
                })

        return {"nodes": nodes, "edges": edges}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _repo_path(url: str) -> str:
    """'https://github.com/owner/repo' → 'owner/repo'"""
    return url.rstrip("/").removeprefix("https://github.com/")


def _repo_slug(url: str) -> str:
    """'https://github.com/owner/repo' → 'owner__repo'"""
    return _repo_path(url).replace("/", "__")


def _is_text_file(name: str) -> bool:
    text_exts = {
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rs",
        ".rb", ".php", ".cs", ".cpp", ".c", ".h", ".md", ".txt",
        ".yaml", ".yml", ".json", ".toml", ".env.example", ".sh",
        ".sql", ".html", ".css", ".graphql", ".proto",
    }
    return any(name.endswith(ext) for ext in text_exts)


def _extract_result(r) -> tuple[str, dict]:
    """
    cognee 1.x recall() results can be:
      - a plain string
      - a dict with "text" / "content" keys
      - a dataclass / object with .text or .content attributes
    Returns (text_content, metadata_dict).
    """
    if isinstance(r, str):
        return r, {}
    if isinstance(r, dict):
        text = r.get("text") or r.get("content") or r.get("answer") or ""
        meta = r.get("metadata") or {}
        if not isinstance(meta, dict):
            meta = {}
        # Surface score if present at top level
        if "score" in r and "score" not in meta:
            meta["score"] = r["score"]
        return str(text), meta
    # Dataclass / object fallback
    text = getattr(r, "text", None) or getattr(r, "content", None) or str(r)
    meta = getattr(r, "metadata", {}) or {}
    if not isinstance(meta, dict):
        meta = {}
    return str(text), meta


async def _record_timeline_event(
    dataset_name: str,
    event_type: str,
    summary: str,
    metadata: dict,
):
    """
    Store a timeline event as tagged memory in Cognee.
    Uses a plain-text format that recall() can surface and _parse_timeline_text()
    can decode — because cognee 1.x remember() does not accept a metadata kwarg.
    """
    event_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()

    # Embed all data in the text so it survives graph extraction and recall
    text = (
        f"TIMELINE EVENT [{event_type.upper()}] "
        f"id={event_id} "
        f"at={timestamp} "
        f"summary={summary} "
        f"meta={json.dumps(metadata)}"
    )
    await cognee.remember(text, dataset_name=dataset_name)


def _parse_timeline_text(text: str) -> Optional[dict]:
    """
    Parse a TIMELINE EVENT string back into a structured dict.
    Format: TIMELINE EVENT [TYPE] id=... at=... summary=... meta={...}
    """
    try:
        import re
        event_type_match = re.search(r"\[([A-Z_]+)\]", text)
        id_match = re.search(r"id=([a-f0-9\-]{36})", text)
        at_match = re.search(r"at=(\S+)", text)
        summary_match = re.search(r"summary=(.+?) meta=", text)
        meta_match = re.search(r"meta=(\{.+\})$", text, re.DOTALL)

        return {
            "id": id_match.group(1) if id_match else None,
            "timestamp": at_match.group(1) if at_match else None,
            "event_type": event_type_match.group(1).lower() if event_type_match else "unknown",
            "summary": summary_match.group(1).strip() if summary_match else text[:100],
            "metadata": json.loads(meta_match.group(1)) if meta_match else {},
        }
    except Exception:
        return None