"use client";

import Link from "next/link";

import RepoUploader from "@/components/RepoUploader";
import StatsCard from "@/components/StatsCard";
import QuickActionCard from "@/components/QuickActionCard";

export default function DashboardPage() {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 30,
      }}
    >
      {/* Hero */}

      <div
        className="glass-card"
        style={{
          padding: 35,
        }}
      >
        <h1
          style={{
            fontSize: 42,
            fontWeight: 800,
            marginBottom: 10,
          }}
        >
          🚀 DevBrain Dashboard
        </h1>

        <p
          style={{
            color: "#94a3b8",
            fontSize: 18,
            lineHeight: 1.8,
            maxWidth: 900,
          }}
        >
          Upload a GitHub repository, build a persistent AI memory with
          Cognee, explore your knowledge graph, ask semantic questions,
          visualize commit history and understand your codebase instantly.
        </p>
      </div>

      {/* Stats */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(230px,1fr))",
          gap: 20,
        }}
      >
        <StatsCard
          icon="📦"
          title="Repositories"
          value="1"
          color="#60a5fa"
        />

        <StatsCard
          icon="🧠"
          title="Knowledge Graph"
          value="Ready"
          color="#22c55e"
        />

        <StatsCard
          icon="⚡"
          title="Backend"
          value="Online"
          color="#22c55e"
        />

        <StatsCard
          icon="🕒"
          title="Timeline"
          value="0"
          color="#f59e0b"
        />
      </div>

      {/* Upload Repository */}

      <RepoUploader />

      {/* Quick Actions */}

      <h2
        style={{
          marginTop: 10,
          marginBottom: -10,
          fontSize: 30,
          fontWeight: 700,
        }}
      >
        Quick Actions
      </h2>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(260px,1fr))",
          gap: 20,
        }}
      >
        <Link href="/ask" style={{ textDecoration: "none" }}>
          <QuickActionCard
            icon="🧠"
            title="Ask AI"
            description="Ask natural language questions about any repository."
            color="#3b82f6"
          />
        </Link>

        <Link href="/graph" style={{ textDecoration: "none" }}>
          <QuickActionCard
            icon="🕸"
            title="Knowledge Graph"
            description="Visualize repository memory using an interactive graph."
            color="#10b981"
          />
        </Link>

        <Link href="/timeline" style={{ textDecoration: "none" }}>
          <QuickActionCard
            icon="📜"
            title="Timeline"
            description="Track repository events and memory evolution."
            color="#f59e0b"
          />
        </Link>

        <Link href="/diff" style={{ textDecoration: "none" }}>
          <QuickActionCard
            icon="🔄"
            title="Semantic Diff"
            description="Understand commit changes with AI-generated summaries."
            color="#8b5cf6"
          />
        </Link>
      </div>
    </div>
  );
}