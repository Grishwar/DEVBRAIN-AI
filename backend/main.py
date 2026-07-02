"""
DevBrain AI

Backend Entry Point

Responsibilities:
- Load environment variables
- Initialize FastAPI
- Configure CORS
- Register routes

All business logic lives in:

app/
services/
memory/
github/
models/
utils/
"""

from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ------------------------------------------------------------
# Load .env BEFORE importing Cognee
# ------------------------------------------------------------

load_dotenv(override=True)

# ------------------------------------------------------------
# Cognee
# ------------------------------------------------------------

import cognee  # noqa: F401

# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------

from app.routes import router


# ------------------------------------------------------------
# Lifespan
# ------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup / Shutdown Events
    """

    print("🚀 DevBrain AI Backend Started")

    yield

    print("🛑 DevBrain AI Backend Stopped")


# ------------------------------------------------------------
# FastAPI
# ------------------------------------------------------------

app = FastAPI(

    title="DevBrain AI",

    description="""
AI-powered Codebase Memory Assistant.

Upload a GitHub repository once.

Ask questions forever.
""",

    version="1.0.0",

    lifespan=lifespan,

)


# ------------------------------------------------------------
# CORS
# ------------------------------------------------------------

app.add_middleware(

    CORSMiddleware,

    allow_origins=[

        "http://localhost:3000",

        "http://127.0.0.1:3000",

        "*",

    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)


# ------------------------------------------------------------
# Register Routes
# ------------------------------------------------------------

app.include_router(router)


# ------------------------------------------------------------
# Root
# ------------------------------------------------------------

@app.get("/")

async def root():

    return {

        "application": "DevBrain AI",

        "version": "1.0.0",

        "status": "running",

        "framework": "FastAPI",

        "memory": "Cognee",

        "graph_database": "Neo4j",

        "vector_database": "Qdrant",

        "documentation": "/docs",

    }


# ------------------------------------------------------------
# Run
# ------------------------------------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "main:app",

        host="0.0.0.0",

        port=8000,

        reload=True,

    )