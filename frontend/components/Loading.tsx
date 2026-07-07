"use client";

export default function Loading() {
  return (
    <div
      style={{
        width: "100%",
        height: "80vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          textAlign: "center",
        }}
      >
        <div
          style={{
            width: 70,
            height: 70,
            border: "6px solid #1e293b",
            borderTop: "6px solid #3b82f6",
            borderRadius: "50%",
            animation: "spin 1s linear infinite",
            margin: "0 auto",
          }}
        />

        <h2
          style={{
            marginTop: 30,
            color: "white",
            fontSize: 28,
          }}
        >
          DevBrain AI
        </h2>

        <p
          style={{
            marginTop: 10,
            color: "#94a3b8",
            fontSize: 16,
          }}
        >
          Loading your AI workspace...
        </p>

        <p
          style={{
            marginTop: 8,
            color: "#64748b",
            fontSize: 14,
          }}
        >
          Connecting to Cognee • Neo4j • Qdrant
        </p>

        <style jsx>{`
          @keyframes spin {
            from {
              transform: rotate(0deg);
            }
            to {
              transform: rotate(360deg);
            }
          }
        `}</style>
      </div>
    </div>
  );
}