# 🧠 DevBrain AI

## AI Codebase Memory Assistant

DevBrain AI is an intelligent codebase assistant built using Cognee Memory Lifecycle.

Instead of simply indexing source code, DevBrain AI creates persistent semantic memory that allows developers to:

- Upload GitHub repositories
- Build long-term repository memory
- Ask natural language questions
- View repository timelines
- Explore knowledge graphs
- Compare semantic code differences

---

# Architecture

Frontend

- Next.js 15
- React
- TypeScript

Backend

- FastAPI
- Python

AI

- Cognee
- LiteLLM
- Gemini / Groq

Databases

- Neo4j
- Qdrant

Repository Source

- GitHub API

---

# Memory Lifecycle

Repository

↓

GitHub Service

↓

Cognee Remember()

↓

Knowledge Graph

↓

Timeline

↓

Semantic Search

↓

AI Answer

---

# Features

✅ Repository Upload

✅ AI Chat

✅ Knowledge Graph

✅ Repository Timeline

✅ Semantic Diff

✅ Persistent Memory

---

# Folder Structure

frontend/
backend/

Frontend communicates with FastAPI.

FastAPI communicates with Cognee.

Cognee stores semantic memory inside Neo4j and Qdrant.

---

# Future Improvements

- Multi-user authentication
- GitHub OAuth
- Live repository synchronization
- PR review assistant
- AI code explanation
- Automatic documentation generation

---

Built for the Cognee Hackathon ❤️