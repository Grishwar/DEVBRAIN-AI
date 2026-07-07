"use client";

import { useEffect, useRef, useState } from "react";

const API = "http://127.0.0.1:8000";

type Message = {
  role: "user" | "assistant";
  content: string;
};

export default function ChatBox() {
  const [dataset, setDataset] = useState("");
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "👋 Hi! I'm DevBrain AI.\n\nAsk me anything about your GitHub repository.",
    },
  ]);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  async function askQuestion() {
    if (!dataset.trim() || !question.trim()) return;

    const userMessage = question;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(`${API}/ask`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          dataset_id: dataset,
          question: userMessage,
        }),
      });

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            data.answer ||
            data.response ||
            JSON.stringify(data, null, 2),
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "❌ Unable to contact backend.",
        },
      ]);
    }

    setLoading(false);
  }

  return (
    <div className="glass-card">

      <h2
        style={{
          marginBottom: 20,
          fontSize: 30,
          fontWeight: 700,
        }}
      >
        💬 Repository Chat
      </h2>

      <input
        className="upload-input"
        placeholder="Dataset ID (Grishwar__DEVBRAIN-AI)"
        value={dataset}
        onChange={(e) => setDataset(e.target.value)}
      />

      <div
        style={{
          marginTop: 25,
          background: "#0f172a",
          borderRadius: 18,
          padding: 22,
          height: 430,
          overflowY: "auto",
          border: "1px solid #334155",
        }}
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            style={{
              display: "flex",
              justifyContent:
                msg.role === "user"
                  ? "flex-end"
                  : "flex-start",
              marginBottom: 20,
            }}
          >
            <div
              style={{
                maxWidth: "78%",
                padding: "16px 20px",
                borderRadius: 18,
                background:
                  msg.role === "user"
                    ? "linear-gradient(135deg,#2563eb,#1d4ed8)"
                    : "#1e293b",
                color: "white",
                whiteSpace: "pre-wrap",
                lineHeight: 1.7,
                boxShadow: "0 6px 18px rgba(0,0,0,.25)",
              }}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {loading && (
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 10,
              color: "#94a3b8",
              marginTop: 10,
            }}
          >
            <span
              style={{
                width: 10,
                height: 10,
                borderRadius: "50%",
                background: "#22c55e",
                display: "inline-block",
              }}
            />
            🤖 DevBrain AI is thinking...
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <textarea
        className="upload-input"
        rows={4}
        placeholder="Ask anything about this repository..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            askQuestion();
          }
        }}
        style={{
          marginTop: 20,
          resize: "none",
        }}
      />

      <button
        className="upload-button"
        disabled={loading}
        style={{
          marginTop: 20,
          opacity: loading ? 0.7 : 1,
          cursor: loading ? "not-allowed" : "pointer",
        }}
        onClick={askQuestion}
      >
        {loading ? "Thinking..." : "🚀 Send"}
      </button>

    </div>
  );
}