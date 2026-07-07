# Claude Development Guide

## Project

DevBrain AI

AI-powered Codebase Memory Assistant

---

## Goal

DevBrain AI allows developers to upload a GitHub repository once and build persistent semantic memory using Cognee.

Users can:

- Upload repositories
- Build AI memory
- Query repositories using natural language
- Visualize repository knowledge
- Track repository timeline
- Compare semantic code changes

---

## Tech Stack

### Frontend

- Next.js 15
- React
- TypeScript
- React Flow
- Tailwind CSS

### Backend

- FastAPI
- Python 3.13

### AI

- Cognee
- LiteLLM
- Gemini / Groq

### Databases

- Neo4j
- Qdrant

### External APIs

- GitHub REST API

---

## Folder Structure

frontend/
├── app/
├── components/
├── hooks/
├── lib/

backend/
├── app/
├── github_client/
├── memory/
├── models/
├── services/
├── utils/

---

## Main Features

### Repository Upload

Uploads a GitHub repository and converts it into semantic memory.

---

### AI Chat

Allows users to ask repository questions using Cognee Recall.

---

### Knowledge Graph

Visualizes repository entities and relationships.

---

### Timeline

Displays repository memory lifecycle events.

---

### Semantic Diff

Explains code changes using AI-generated summaries.

---

## Backend Flow

GitHub Repository

↓

GitHub Service

↓

Chunk Extraction

↓

Cognee Remember()

↓

Neo4j

+

Qdrant

↓

Recall()

↓

FastAPI Response

↓

Next.js UI

---

## Coding Standards

- TypeScript on frontend
- Python type hints on backend
- Async FastAPI endpoints
- Reusable React components
- Custom React hooks for API communication
- Consistent error handling
- Clean folder structure

---

## Future Roadmap

- GitHub OAuth
- Multi-user workspaces
- Live repository synchronization
- AI pull request reviews
- Automatic documentation generation
- Repository health scoring
- Code quality analytics
- Deployment monitoring

---

## Deployment

Frontend:
- Vercel

Backend:
- Render / Railway

Databases:
- Neo4j
- Qdrant

---

## Project Vision

DevBrain AI transforms traditional code repositories into persistent AI memory, enabling developers to understand, search, and evolve complex codebases through natural language interactions.

---

Built with ❤️ for the Cognee Hackathon.