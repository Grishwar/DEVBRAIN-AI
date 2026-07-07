"use client";

import TimelineView from "../../components/TimelineView";

export default function TimelinePage() {
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
          🕒 Repository Timeline
        </h1>

        <p
          style={{
            color: "#94a3b8",
          }}
        >
          Replay how DevBrain AI built memory from your repository.
        </p>
      </div>

      <TimelineView />

    </div>
  );
}