"use client";

const events = [
  {
    time: "10:30 AM",
    title: "Repository Uploaded",
    description: "GitHub repository cloned and metadata extracted.",
    icon: "📦",
    color: "#2563eb",
  },
  {
    time: "10:31 AM",
    title: "Cognee Memory Created",
    description: "Repository indexed into persistent semantic memory.",
    icon: "🧠",
    color: "#22c55e",
  },
  {
    time: "10:32 AM",
    title: "Knowledge Graph Generated",
    description: "Relationships between files and code entities discovered.",
    icon: "🕸",
    color: "#a855f7",
  },
  {
    time: "10:33 AM",
    title: "Timeline Built",
    description: "Repository events organized chronologically.",
    icon: "📜",
    color: "#f59e0b",
  },
  {
    time: "10:34 AM",
    title: "AI Assistant Ready",
    description: "Repository is ready for semantic search and Q&A.",
    icon: "🤖",
    color: "#ec4899",
  },
];

export default function TimelineView() {
  return (
    <div className="glass-card">

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 35,
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
            🕒 Repository Timeline
          </h2>

          <p
            style={{
              color: "#94a3b8",
            }}
          >
            Complete lifecycle of your repository inside DevBrain AI.
          </p>
        </div>

        <div
          style={{
            background: "#052e16",
            color: "#4ade80",
            border: "1px solid #166534",
            padding: "8px 16px",
            borderRadius: 999,
            fontWeight: 600,
            fontSize: 14,
          }}
        >
          Live Events
        </div>
      </div>

      <div
        style={{
          position: "relative",
          marginLeft: 20,
        }}
      >
        {/* Vertical Line */}

        <div
          style={{
            position: "absolute",
            left: 24,
            top: 0,
            bottom: 0,
            width: 3,
            background: "#1e293b",
          }}
        />

        {events.map((event, index) => (
          <div
            key={index}
            style={{
              display: "flex",
              gap: 24,
              marginBottom: 35,
              position: "relative",
            }}
          >
            {/* Timeline Dot */}

            <div
              style={{
                width: 50,
                height: 50,
                borderRadius: "50%",
                background: event.color,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "#fff",
                fontSize: 22,
                zIndex: 2,
                boxShadow: `0 0 20px ${event.color}`,
                flexShrink: 0,
              }}
            >
              {event.icon}
            </div>

            {/* Content */}

            <div
              style={{
                flex: 1,
                background: "#111827",
                border: "1px solid #1f2937",
                borderRadius: 18,
                padding: 22,
                boxShadow: "0 10px 25px rgba(0,0,0,.25)",
              }}
            >
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  flexWrap: "wrap",
                  gap: 10,
                }}
              >
                <h3
                  style={{
                    color: "#fff",
                    fontSize: 20,
                    fontWeight: 700,
                  }}
                >
                  {event.title}
                </h3>

                <span
                  style={{
                    background: "#0f172a",
                    padding: "6px 12px",
                    borderRadius: 999,
                    color: "#94a3b8",
                    fontSize: 13,
                  }}
                >
                  {event.time}
                </span>
              </div>

              <p
                style={{
                  marginTop: 14,
                  color: "#cbd5e1",
                  lineHeight: 1.7,
                }}
              >
                {event.description}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}