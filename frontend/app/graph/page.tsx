"use client";

import GraphView from "../../components/GraphView";

export default function GraphPage() {
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
            fontSize: "38px",
            fontWeight: 700,
            marginBottom: 15,
          }}
        >
          🧠 Knowledge Graph
        </h1>

        <p
          style={{
            color: "#94a3b8",
            fontSize: "17px",
            lineHeight: 1.7,
          }}
        >
          Explore your repository as an interactive knowledge graph powered by
          Cognee's hybrid Graph + Vector Memory.
        </p>
      </div>

      <GraphView />

    </div>
  );
}