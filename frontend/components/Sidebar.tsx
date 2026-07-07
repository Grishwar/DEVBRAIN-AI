"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const menuItems = [
  {
    name: "Dashboard",
    href: "/",
    icon: "🏠",
  },
  {
    name: "Knowledge Graph",
    href: "/graph",
    icon: "🧠",
  },
  {
    name: "Ask AI",
    href: "/ask",
    icon: "💬",
  },
  {
    name: "Timeline",
    href: "/timeline",
    icon: "📜",
  },
  {
    name: "Semantic Diff",
    href: "/diff",
    icon: "🔄",
  },
  {
    name: "Settings",
    href: "/settings",
    icon: "⚙️",
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside
      style={{
        width: "260px",
        height: "100vh",
        background: "#0f172a",
        borderRight: "1px solid #1e293b",
        position: "fixed",
        left: 0,
        top: 0,
        display: "flex",
        flexDirection: "column",
        padding: "28px 20px",
        overflowY: "auto",
      }}
    >
      {/* Logo */}

      <div
        style={{
          marginBottom: 40,
        }}
      >
        <h1
          className="gradient-text"
          style={{
            fontSize: 34,
            fontWeight: 800,
            marginBottom: 8,
            letterSpacing: "-1px",
          }}
        >
          DevBrain AI
        </h1>

        <p
          style={{
            color: "#94a3b8",
            fontSize: 14,
            lineHeight: 1.6,
          }}
        >
          AI Codebase Memory Assistant
        </p>

        <div
          style={{
            marginTop: 14,
            display: "inline-flex",
            alignItems: "center",
            gap: 8,
            background: "#0b1220",
            padding: "8px 12px",
            borderRadius: 999,
            border: "1px solid #1e293b",
            color: "#22c55e",
            fontSize: 13,
            fontWeight: 600,
          }}
        >
          <span
            style={{
              width: 8,
              height: 8,
              borderRadius: "50%",
              background: "#22c55e",
            }}
          />
          AI Ready
        </div>
      </div>

      {/* Navigation */}

      <nav
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 10,
        }}
      >
        {menuItems.map((item) => {
          const active = pathname === item.href;

          return (
            <Link
              key={item.name}
              href={item.href}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 14,
                padding: "15px 16px",
                borderRadius: 14,
                textDecoration: "none",
                transition: "all .25s ease",
                background: active
                  ? "linear-gradient(135deg,#2563eb,#1d4ed8)"
                  : "transparent",
                color: active ? "#fff" : "#cbd5e1",
                fontWeight: active ? 700 : 600,
                boxShadow: active
                  ? "0 10px 25px rgba(37,99,235,.35)"
                  : "none",
              }}
            >
              <span
                style={{
                  fontSize: 22,
                  width: 28,
                  textAlign: "center",
                }}
              >
                {item.icon}
              </span>

              <span
                style={{
                  flex: 1,
                }}
              >
                {item.name}
              </span>

              {active && (
                <div
                  style={{
                    width: 8,
                    height: 8,
                    borderRadius: "50%",
                    background: "#fff",
                  }}
                />
              )}
            </Link>
          );
        })}
      </nav>

      {/* Bottom Card */}

      <div
        style={{
          marginTop: "auto",
        }}
      >
        <div
          style={{
            background: "#111827",
            border: "1px solid #1f2937",
            borderRadius: 18,
            padding: 18,
            boxShadow: "0 8px 25px rgba(0,0,0,.25)",
          }}
        >
          <div
            style={{
              fontWeight: 700,
              fontSize: 17,
              marginBottom: 10,
            }}
          >
            🚀 Hackathon
          </div>

          <p
            style={{
              color: "#cbd5e1",
              fontSize: 13,
              lineHeight: 1.6,
              marginBottom: 14,
            }}
          >
            Powered by Cognee Memory Lifecycle with Neo4j, Qdrant and AI-powered semantic search.
          </p>

          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <span
              style={{
                fontSize: 12,
                color: "#94a3b8",
              }}
            >
              Version
            </span>

            <span
              style={{
                background: "#2563eb",
                color: "#fff",
                padding: "4px 10px",
                borderRadius: 999,
                fontSize: 12,
                fontWeight: 700,
              }}
            >
              v1.0
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
}