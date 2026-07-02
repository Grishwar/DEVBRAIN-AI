"""
Pydantic schemas used across the DevBrain AI backend.

This file contains every request and response model used by
FastAPI endpoints.

Author: Grishwar
Project: DevBrain AI
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ============================================================
# INGEST
# ============================================================

class IngestRequest(BaseModel):
    repo_url: str = Field(..., description="GitHub repository URL")
    branch: str = Field(default="main")
    dataset_id: Optional[str] = None


class IngestResponse(BaseModel):
    status: str
    dataset_id: str
    chunks_ingested: int
    message: str


# ============================================================
# ASK
# ============================================================

class AskRequest(BaseModel):
    dataset_id: str
    question: str


class SourceReference(BaseModel):
    source: str
    confidence: float
    last_updated: str = ""


class AskResponse(BaseModel):
    answer: str
    sources: List[SourceReference]


# ============================================================
# DIFF
# ============================================================

class DiffRequest(BaseModel):
    dataset_id: str
    commit_sha: str
    changed_files: List[str]
    commit_message: str


class DiffResponse(BaseModel):
    status: str
    commit_sha: str
    files_updated: int
    semantic_summary: str


# ============================================================
# FORGET
# ============================================================

class ForgetRequest(BaseModel):
    dataset_id: str
    module_name: str
    reason: Optional[str] = "Deprecated"


class ForgetResponse(BaseModel):
    status: str
    module: str
    message: str


# ============================================================
# TIMELINE
# ============================================================

class TimelineEvent(BaseModel):
    id: Optional[str] = None
    timestamp: Optional[str] = None
    event_type: str
    summary: str
    metadata: Dict[str, Any] = {}


class TimelineResponse(BaseModel):
    events: List[TimelineEvent]


# ============================================================
# GRAPH
# ============================================================

class GraphNode(BaseModel):
    id: str
    data: Dict[str, Any]
    type: str = "default"
    position: Dict[str, float]


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: str = "related"


class GraphResponse(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]


# ============================================================
# HEALTH
# ============================================================

class HealthResponse(BaseModel):
    status: str
    timestamp: str


# ============================================================
# GENERIC
# ============================================================

class MessageResponse(BaseModel):
    status: str
    message: str