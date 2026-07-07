"use client";

const changes = [
  {
    file: "backend/services/ask_service.py",
    status: "Modified",
    color: "#2563eb",
    icon: "🧠",
    summary:
      "Improved semantic search by integrating Cognee memory retrieval before LLM generation.",
  },
  {
    file: "frontend/components/ChatBox.tsx",
    status: "Added",
    color: "#16a34a",
    icon: "💬",
    summary:
      "Implemented AI chat interface with streaming responses and repository context.",
  },
  {
    file: "backend/memory/cognee_service.py",
    status: "Modified",
    color: "#f59e0b",
    icon: "⚡",
    summary:
      "Added remember(), recall(), improve(), and forget() lifecycle support.",
  },
];

export default function DiffViewer() {
  return (
    <div className="glass-card">

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 35,
          flexWrap: "wrap",
          gap: 20,
        }}
      >
        <div>
          <h2
            style={{
              fontSize: 30,
              fontWeight: 700,
              marginBottom: 8,
            }}
          >
            🔄 AI Semantic Diff
          </h2>

          <p
            style={{
              color: "#94a3b8",
            }}
          >
            AI-generated explanations of repository changes.
          </p>
        </div>

        <div
          style={{
            background: "#052e16",
            border: "1px solid #166534",
            color: "#4ade80",
            padding: "8px 18px",
            borderRadius: 999,
            fontWeight: 600,
          }}
        >
          AI Analysis Complete
        </div>
      </div>

      {changes.map((change, index) => (
        <div
          key={index}
          style={{
            background: "#111827",
            border: `1px solid ${change.color}`,
            borderRadius: 18,
            padding: 24,
            marginBottom: 24,
            boxShadow: "0 12px 30px rgba(0,0,0,.25)",
            transition: ".25s",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              flexWrap: "wrap",
              gap: 15,
              marginBottom: 18,
            }}
          >
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 14,
              }}
            >
              <div
                style={{
                  width: 55,
                  height: 55,
                  borderRadius: "50%",
                  background: `${change.color}20`,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: 26,
                }}
              >
                {change.icon}
              </div>

              <div>
                <h3
                  style={{
                    color: "#fff",
                    fontSize: 20,
                    marginBottom: 6,
                  }}
                >
                  {change.file}
                </h3>

                <div
                  style={{
                    color: "#94a3b8",
                    fontSize: 13,
                  }}
                >
                  AI Repository Analysis
                </div>
              </div>
            </div>

            <span
              style={{
                background: change.color,
                color: "#fff",
                padding: "8px 16px",
                borderRadius: 999,
                fontSize: 13,
                fontWeight: 700,
              }}
            >
              {change.status}
            </span>
          </div>

          <div
            style={{
              background: "#0f172a",
              border: "1px solid #1e293b",
              borderRadius: 14,
              padding: 18,
            }}
          >
            <div
              style={{
                color: "#22c55e",
                fontWeight: 700,
                marginBottom: 12,
              }}
            >
              🤖 AI Summary
            </div>

            <p
              style={{
                color: "#cbd5e1",
                lineHeight: 1.8,
              }}
            >
              {change.summary}
            </p>
          </div>
        </div>
      ))}

      <div
        style={{
          marginTop: 35,
          background: "#0f172a",
          border: "1px solid #1f2937",
          borderRadius: 18,
          padding: 24,
        }}
      >
        <h3
          style={{
            color: "#fff",
            marginBottom: 12,
          }}
        >
          📊 Diff Overview
        </h3>

        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit,minmax(180px,1fr))",
            gap: 20,
          }}
        >
          <div>
            <div
              style={{
                color: "#94a3b8",
                fontSize: 13,
              }}
            >
              Files Analysed
            </div>

            <div
              style={{
                color: "#3b82f6",
                fontSize: 30,
                fontWeight: 700,
              }}
            >
              3
            </div>
          </div>

          <div>
            <div
              style={{
                color: "#94a3b8",
                fontSize: 13,
              }}
            >
              AI Summaries
            </div>

            <div
              style={{
                color: "#22c55e",
                fontSize: 30,
                fontWeight: 700,
              }}
            >
              3
            </div>
          </div>

          <div>
            <div
              style={{
                color: "#94a3b8",
                fontSize: 13,
              }}
            >
              Repository Status
            </div>

            <div
              style={{
                color: "#f59e0b",
                fontSize: 30,
                fontWeight: 700,
              }}
            >
              Healthy
            </div>
          </div>
        </div>
      </div>

    </div>
  );
}