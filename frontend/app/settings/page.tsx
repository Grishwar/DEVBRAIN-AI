"use client";

import { useState } from "react";

export default function SettingsPage() {
  const [backend, setBackend] = useState("http://127.0.0.1:8000");
  const [repo, setRepo] = useState("");

  function saveSettings() {
    alert("Settings saved successfully!");
  }

  return (
    <div
      style={{
        maxWidth: "1200px",
        margin: "0 auto",
      }}
    >
      {/* Header */}

      <div
        className="glass-card"
        style={{
          marginBottom: 30,
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            flexWrap: "wrap",
            gap: 20,
          }}
        >
          <div>
            <h1
              style={{
                fontSize: 40,
                fontWeight: 800,
                marginBottom: 12,
              }}
            >
              ⚙️ Settings
            </h1>

            <p
              style={{
                color: "#94a3b8",
                lineHeight: 1.7,
              }}
            >
              Configure DevBrain AI backend services and workspace.
            </p>
          </div>

          <div
            style={{
              background: "#052e16",
              color: "#4ade80",
              border: "1px solid #166534",
              padding: "10px 18px",
              borderRadius: 999,
              fontWeight: 700,
            }}
          >
            ● System Online
          </div>
        </div>
      </div>

      {/* Configuration */}

      <div className="glass-card">

        <h2
          style={{
            marginBottom: 30,
            fontSize: 28,
          }}
        >
          Backend Configuration
        </h2>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit,minmax(320px,1fr))",
            gap: 25,
          }}
        >
          {/* Backend */}

          <div>

            <label
              style={{
                display: "block",
                marginBottom: 10,
                fontWeight: 600,
              }}
            >
              FastAPI Endpoint
            </label>

            <input
              className="upload-input"
              value={backend}
              onChange={(e) => setBackend(e.target.value)}
            />

          </div>

          {/* Repo */}

          <div>

            <label
              style={{
                display: "block",
                marginBottom: 10,
                fontWeight: 600,
              }}
            >
              Default GitHub Repository
            </label>

            <input
              className="upload-input"
              value={repo}
              onChange={(e) => setRepo(e.target.value)}
              placeholder="https://github.com/user/repository"
            />

          </div>

        </div>

        {/* Status */}

        <div
          style={{
            marginTop: 40,
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit,minmax(230px,1fr))",
            gap: 20,
          }}
        >
          <StatusCard
            title="FastAPI"
            status="Online"
            color="#22c55e"
          />

          <StatusCard
            title="Cognee"
            status="Connected"
            color="#3b82f6"
          />

          <StatusCard
            title="Neo4j"
            status="Running"
            color="#f59e0b"
          />

          <StatusCard
            title="Qdrant"
            status="Running"
            color="#a855f7"
          />
        </div>

        {/* Model */}

        <div
          style={{
            marginTop: 40,
            background: "#111827",
            border: "1px solid #1f2937",
            borderRadius: 18,
            padding: 24,
          }}
        >
          <h3
            style={{
              marginBottom: 20,
            }}
          >
            🤖 AI Configuration
          </h3>

          <table
            style={{
              width: "100%",
            }}
          >
            <tbody>

              <Row
                name="LLM"
                value="Gemini 2.0 Flash"
              />

              <Row
                name="Embedding"
                value="all-MiniLM-L6-v2"
              />

              <Row
                name="Memory Engine"
                value="Cognee"
              />

              <Row
                name="Vector Database"
                value="Qdrant"
              />

              <Row
                name="Graph Database"
                value="Neo4j"
              />

            </tbody>
          </table>

        </div>

        {/* Save */}

        <button
          className="upload-button"
          style={{
            marginTop: 40,
          }}
          onClick={saveSettings}
        >
          💾 Save Settings
        </button>

      </div>
    </div>
  );
}

function StatusCard({
  title,
  status,
  color,
}: {
  title: string;
  status: string;
  color: string;
}) {
  return (
    <div
      style={{
        background: "#111827",
        border: `1px solid ${color}`,
        borderRadius: 18,
        padding: 20,
      }}
    >
      <div
        style={{
          color: "#94a3b8",
          marginBottom: 10,
        }}
      >
        {title}
      </div>

      <div
        style={{
          color,
          fontWeight: 700,
          fontSize: 20,
        }}
      >
        ● {status}
      </div>
    </div>
  );
}

function Row({
  name,
  value,
}: {
  name: string;
  value: string;
}) {
  return (
    <tr>
      <td
        style={{
          padding: "12px 0",
          color: "#94a3b8",
          fontWeight: 600,
        }}
      >
        {name}
      </td>

      <td
        style={{
          padding: "12px 0",
          textAlign: "right",
          color: "#fff",
        }}
      >
        {value}
      </td>
    </tr>
  );
}