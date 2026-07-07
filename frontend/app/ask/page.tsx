"use client";

import ChatBox from "../../components/ChatBox";

export default function AskPage() {
  return (
    <div
      style={{
        maxWidth: "1100px",
        margin: "0 auto",
      }}
    >
      <div
        className="glass-card"
        style={{
          marginBottom: 30,
          padding: "30px",
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
                fontSize: "38px",
                fontWeight: 700,
                marginBottom: 12,
              }}
            >
              💬 Ask DevBrain AI
            </h1>

            <p
              style={{
                color: "#94a3b8",
                fontSize: "17px",
                lineHeight: 1.7,
                maxWidth: 700,
              }}
            >
              Ask questions about your GitHub repository using Cognee's
              persistent memory, semantic search and knowledge graph.
            </p>
          </div>

          <div
            style={{
              padding: "10px 18px",
              borderRadius: 30,
              background: "#052e16",
              color: "#4ade80",
              fontWeight: 600,
              border: "1px solid #166534",
            }}
          >
            ● AI Ready
          </div>
        </div>
      </div>

      <ChatBox />
    </div>
  );
}