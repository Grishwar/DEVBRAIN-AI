"use client";

import DiffViewer from "../../components/DiffViewer";

export default function DiffPage() {
  return (
    <div>

      <div
        className="glass-card"
        style={{
          marginBottom: 30,
        }}
      >
        <h1
          style={{
            fontSize: "40px",
            fontWeight: 700,
            marginBottom: 15,
          }}
        >
          🔄 Semantic Diff
        </h1>

        <p
          style={{
            color: "#94a3b8",
          }}
        >
          Compare commits and understand what changed using AI-generated summaries.
        </p>
      </div>

      <DiffViewer />

    </div>
  );
}