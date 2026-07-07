"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

export default function Navbar() {
  const [time, setTime] = useState("");

  useEffect(() => {
    const updateClock = () => {
      setTime(
        new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
        })
      );
    };

    updateClock();

    const timer = setInterval(updateClock, 30000);

    return () => clearInterval(timer);
  }, []);

  return (
    <header
      style={{
        position: "sticky",
        top: 0,
        zIndex: 999,
        marginLeft: 260,
        height: 78,
        padding: "0 28px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        background: "rgba(15,23,42,.90)",
        backdropFilter: "blur(14px)",
        borderBottom: "1px solid #1e293b",
      }}
    >
      {/* Left */}

      <div>
        <h2
          style={{
            fontSize: 28,
            fontWeight: 800,
            marginBottom: 6,
            letterSpacing: "-0.5px",
          }}
        >
          Welcome to{" "}
          <span className="gradient-text">
            DevBrain AI
          </span>
        </h2>

        <p
          style={{
            color: "#94a3b8",
            fontSize: 14,
          }}
        >
          AI-powered Codebase Memory Assistant
        </p>
      </div>

      {/* Right */}

      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 16,
        }}
      >
        {/* Clock */}

        <div
          style={{
            background: "#111827",
            border: "1px solid #1f2937",
            padding: "10px 16px",
            borderRadius: 14,
            color: "#cbd5e1",
            fontWeight: 600,
            fontSize: 14,
          }}
        >
          🕒 {time}
        </div>

        {/* Backend Status */}

        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            background: "#052e16",
            border: "1px solid #166534",
            padding: "10px 16px",
            borderRadius: 999,
            color: "#4ade80",
            fontWeight: 600,
            fontSize: 14,
          }}
        >
          <span
            style={{
              width: 10,
              height: 10,
              borderRadius: "50%",
              background: "#22c55e",
            }}
          />

          Backend Online
        </div>

        {/* GitHub */}

        <button
          onClick={() =>
            window.open(
              "https://github.com/Grishwar/DEVBRAIN-AI",
              "_blank"
            )
          }
          className="secondary-btn"
          style={{
            padding: "11px 18px",
          }}
        >
          GitHub Repo
        </button>

        {/* Upload Repository */}

        <Link
          href="/dashboard"
          className="primary-btn"
          style={{
            padding: "11px 22px",
            textDecoration: "none",
            display: "inline-flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          Upload Repository
        </Link>

        {/* Avatar */}

        <div
          style={{
            width: 42,
            height: 42,
            borderRadius: "50%",
            background: "linear-gradient(135deg,#2563eb,#7c3aed)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "#fff",
            fontWeight: 700,
            fontSize: 18,
            boxShadow: "0 10px 25px rgba(37,99,235,.35)",
          }}
        >
          G
        </div>
      </div>
    </header>
  );
}