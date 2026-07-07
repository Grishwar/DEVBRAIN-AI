"use client";

import Link from "next/link";

export default function HomePage() {
  return (
    <div>
      <div className="hero-card">

        <h1
          style={{
            fontSize: "42px",
            fontWeight: 700,
            marginBottom: 12,
          }}
        >
          DevBrain AI
        </h1>

        <p
          style={{
            fontSize: 18,
            color: "#94a3b8",
            maxWidth: 800,
          }}
        >
          AI-powered Codebase Memory Assistant built with Cognee.
          Upload any GitHub repository and explore it using semantic search,
          interactive knowledge graphs, persistent memory, timeline replay,
          and intelligent code understanding.
        </p>

        <div
          style={{
            display: "flex",
            gap: 16,
            marginTop: 30,
            flexWrap: "wrap",
          }}
        >
          <Link href="/dashboard" className="primary-btn">
            🚀 Open Dashboard
          </Link>

          <Link href="/graph" className="secondary-btn">
            🧠 View Knowledge Graph
          </Link>

          <Link href="/ask" className="secondary-btn">
            💬 Ask AI
          </Link>
        </div>
      </div>

      <div className="stats-grid">

        <div className="glass-card">
          <h2>🧠 Persistent Memory</h2>
          <p>
            Powered by Cognee remember(), recall(), improve() and forget().
          </p>
        </div>

        <div className="glass-card">
          <h2>📈 Semantic Graph</h2>
          <p>
            Interactive knowledge graph built from your GitHub repository.
          </p>
        </div>

        <div className="glass-card">
          <h2>⚡ AI Chat</h2>
          <p>
            Ask natural language questions about any codebase.
          </p>
        </div>

        <div className="glass-card">
          <h2>🕒 Timeline</h2>
          <p>
            Track repository evolution and semantic changes over time.
          </p>
        </div>

      </div>
    </div>
  );
}