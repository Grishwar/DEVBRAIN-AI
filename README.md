# 🧠 DevBrain AI
### AI-Powered Codebase Memory Assistant using Cognee

DevBrain AI is an AI-powered code understanding platform that transforms any public GitHub repository into a searchable semantic memory. Built using Cognee, FastAPI, Neo4j, Qdrant, and Next.js, it enables developers to upload repositories, build persistent memory, perform semantic search, and explore repository information through an interactive web interface.

---

## 🚀 Features

### ✅ GitHub Repository Ingestion
- Import any public GitHub repository.
- Clone and process repositories automatically.
- Build persistent semantic memory using Cognee.
- Display indexing progress during ingestion.

### ✅ AI Codebase Assistant
- Ask natural language questions about the uploaded repository.
- Retrieve context using Cognee semantic memory.
- Generate repository-aware AI responses using Gemini.

### ✅ Persistent Memory
- Repository content indexed into Cognee.
- Semantic embeddings stored in Qdrant.
- Knowledge stored in Neo4j graph database.

### ✅ Interactive Dashboard
- Modern responsive UI built with Next.js.
- Backend health monitoring.
- Repository upload interface.
- Dataset management.

### ✅ Backend Status Monitoring
- FastAPI status
- Cognee connection
- Neo4j status
- Qdrant status
- AI model information

### 🚧 Work in Progress
The following modules are currently under development:

- Dynamic Knowledge Graph visualization
- Repository Timeline generation
- AI-powered Semantic Diff using Git commit history
- Automatic GitHub commit analysis

---

# 🏗️ Architecture

```
                 GitHub Repository
                         │
                         ▼
                Repository Ingestion
                         │
                         ▼
                     Cognee Memory
                  ┌────────┴────────┐
                  ▼                 ▼
             Neo4j Graph       Qdrant Vector DB
                  │                 │
                  └────────┬────────┘
                           ▼
                   Semantic Retrieval
                           │
                           ▼
                     Gemini AI Model
                           │
                           ▼
                 Next.js Web Dashboard
```

---

# 🛠 Tech Stack

## Frontend

- Next.js 15
- React
- TypeScript
- React Flow
- CSS
- Axios

## Backend

- FastAPI
- Python
- Cognee
- Neo4j
- Qdrant
- GitPython

## AI

- Google Gemini
- Cognee Semantic Memory
- Sentence Transformers
- Vector Search

---

# 📂 Project Structure

```
DEVBRAIN-AI
│
├── backend
│   ├── app
│   ├── github_client
│   ├── graph
│   ├── memory
│   ├── models
│   ├── services
│   ├── utils
│   ├── main.py
│   └── requirements.txt
│
├── frontend
│   ├── app
│   ├── components
│   ├── hooks
│   ├── lib
│   ├── public
│   └── types
│
├── docker-compose.yml
├── README.md
└── docs
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Grishwar/DEVBRAIN-AI.git

cd DEVBRAIN-AI
```

---

## Backend

```bash
cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

Run

```bash
uvicorn main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## Docker

```bash
docker compose up -d
```

Services

- Neo4j
- Qdrant

---

# 📌 Workflow

1. Upload a public GitHub repository.
2. Backend clones the repository.
3. Cognee indexes repository content.
4. Embeddings are stored in Qdrant.
5. Relationships are stored in Neo4j.
6. Users can query the repository using natural language.
7. AI generates context-aware responses.

---

# 📸 Current Screens

✅ Dashboard

✅ Repository Upload

✅ Ask AI

✅ Settings

🚧 Knowledge Graph (UI completed, dynamic graph in progress)

🚧 Timeline (dynamic events in progress)

🚧 Semantic Diff (Git commit integration in progress)

---

# 📊 Current Status

| Feature | Status |
|----------|--------|
| Repository Upload | ✅ Completed |
| Cognee Integration | ✅ Completed |
| Semantic Search | ✅ Completed |
| AI Chat | ✅ Completed |
| FastAPI Backend | ✅ Completed |
| Next.js Frontend | ✅ Completed |
| Neo4j Integration | ✅ Completed |
| Qdrant Integration | ✅ Completed |
| Knowledge Graph | 🚧 In Progress |
| Timeline | 🚧 In Progress |
| Semantic Diff | 🚧 In Progress |

---

# 🔮 Future Improvements

- Dynamic repository knowledge graph
- Automatic Git commit visualization
- Real semantic diff generation
- Multi-repository support
- Authentication
- Repository history replay
- Repository analytics dashboard
- Code dependency visualization
- Export reports
- Multi-user workspace

---

# 👨‍💻 Author

**Grishwar S V**

Computer Science & Engineering

Sri Ramakrishna Engineering College

GitHub:
https://github.com/Grishwar

LinkedIn:
https://www.linkedin.com/in/grishwar

---

# 📄 License

This project was developed as part of the Cognee Hackathon and is maintained as a personal AI portfolio project.
