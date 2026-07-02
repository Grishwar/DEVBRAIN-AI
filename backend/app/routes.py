"""
FastAPI Routes

Thin HTTP layer.

Responsibilities:
- Validate requests
- Call the appropriate service
- Return responses

No business logic belongs here.
"""

from fastapi import APIRouter, HTTPException

from models.schemas import (
    AskRequest,
    AskResponse,
    DiffRequest,
    DiffResponse,
    ForgetRequest,
    ForgetResponse,
    GraphResponse,
    HealthResponse,
    IngestRequest,
    IngestResponse,
    TimelineResponse,
)

from services.ingest_service import IngestService
from services.ask_service import AskService
from services.diff_service import DiffService
from services.forget_service import ForgetService
from services.timeline_service import TimelineService
from services.graph_service import GraphService
from services.health_service import HealthService

router = APIRouter()

# ---------------------------------------------------------
# Service Singletons
# ---------------------------------------------------------

ingest_service = IngestService()
ask_service = AskService()
diff_service = DiffService()
forget_service = ForgetService()
timeline_service = TimelineService()
graph_service = GraphService()
health_service = HealthService()


# ---------------------------------------------------------
# POST /ingest
# ---------------------------------------------------------

@router.post(
    "/ingest",
    response_model=IngestResponse,
)
async def ingest(request: IngestRequest):

    try:

        return await ingest_service.ingest(request)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ---------------------------------------------------------
# POST /ask
# ---------------------------------------------------------

@router.post(
    "/ask",
    response_model=AskResponse,
)
async def ask(request: AskRequest):

    try:

        return await ask_service.ask(request)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ---------------------------------------------------------
# POST /diff
# ---------------------------------------------------------

@router.post(
    "/diff",
    response_model=DiffResponse,
)
async def diff(request: DiffRequest):

    try:

        return await diff_service.semantic_diff(request)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ---------------------------------------------------------
# POST /forget
# ---------------------------------------------------------

@router.post(
    "/forget",
    response_model=ForgetResponse,
)
async def forget(request: ForgetRequest):

    try:

        return await forget_service.forget_module(request)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ---------------------------------------------------------
# GET /timeline/{dataset_id}
# ---------------------------------------------------------

@router.get(
    "/timeline/{dataset_id}",
    response_model=TimelineResponse,
)
async def timeline(dataset_id: str):

    try:

        return await timeline_service.get_timeline(
            dataset_id,
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ---------------------------------------------------------
# GET /graph/{dataset_id}
# ---------------------------------------------------------

@router.get(
    "/graph/{dataset_id}",
    response_model=GraphResponse,
)
async def graph(dataset_id: str):

    try:

        return await graph_service.get_graph(
            dataset_id,
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# ---------------------------------------------------------
# GET /health
# ---------------------------------------------------------

@router.get(
    "/health",
    response_model=HealthResponse,
)
async def health():

    try:

        return await health_service.check()

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )