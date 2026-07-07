"use client";

import { useState, useRef } from "react";
import { ingestRepository } from "../lib/api";

export default function RepoUploader() {
  const [repoUrl, setRepoUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("");
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  const inputRef = useRef<HTMLInputElement>(null);

  function validateGithub(url: string) {
    return /^https:\/\/github\.com\/[^/]+\/[^/]+\/?$/.test(url);
  }

  async function uploadRepository() {
    if (!repoUrl.trim()) {
      setError("Please enter a GitHub repository URL.");
      return;
    }

    if (!validateGithub(repoUrl)) {
      setError("Enter a valid GitHub repository URL.");
      return;
    }

    setLoading(true);
    setProgress(5);
    setStatus("Connecting to backend...");
    setError("");
    setResult(null);

    const timer = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) return prev;
        return prev + 5;
      });
    }, 250);

    try {
      setStatus("Downloading repository...");

      const data = await ingestRepository(repoUrl);

      clearInterval(timer);

      setProgress(100);
      setStatus("Repository indexed successfully.");

      if (data.detail) throw new Error(data.detail);

      setResult(data);
    } catch (err: any) {
      clearInterval(timer);

      setError(err.message || "Repository upload failed.");
    } finally {
      setLoading(false);
    }
  }

  function clearAll() {
    setRepoUrl("");
    setResult(null);
    setError("");
    setProgress(0);
    setStatus("");

    inputRef.current?.focus();
  }

  async function copyDataset() {
    if (!result?.dataset_id) return;

    await navigator.clipboard.writeText(result.dataset_id);

    alert("Dataset ID copied.");
  }

  return (
    <div className="glass-card">

      <h2 style={{ fontSize: 30, marginBottom: 10 }}>
        🚀 Upload GitHub Repository
      </h2>

      <p
        style={{
          color: "#94a3b8",
          marginBottom: 25,
          lineHeight: 1.7,
        }}
      >
        Upload a public GitHub repository to build a persistent AI memory using
        Cognee.
      </p>

      <input
        ref={inputRef}
        className="upload-input"
        placeholder="https://github.com/username/repository"
        value={repoUrl}
        onChange={(e) => setRepoUrl(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") uploadRepository();
        }}
      />

      <div
        style={{
          display: "flex",
          gap: 15,
          marginTop: 20,
          flexWrap: "wrap",
        }}
      >
        <button
          className="upload-button"
          onClick={uploadRepository}
          disabled={loading}
        >
          {loading ? "⏳ Building Memory..." : "🚀 Upload Repository"}
        </button>

        <button
          className="upload-button"
          style={{
            background: "#334155",
          }}
          onClick={clearAll}
        >
          Clear
        </button>
      </div>

      {loading && (
        <div style={{ marginTop: 25 }}>

          <div
            style={{
              width: "100%",
              height: 12,
              background: "#1e293b",
              borderRadius: 999,
              overflow: "hidden",
            }}
          >
            <div
              style={{
                width: `${progress}%`,
                height: "100%",
                background: "#2563eb",
                transition: ".25s",
              }}
            />
          </div>

          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              marginTop: 10,
              color: "#94a3b8",
              fontSize: 14,
            }}
          >
            <span>{status}</span>
            <span>{progress}%</span>
          </div>
        </div>
      )}

      {error && (
        <div
          style={{
            marginTop: 25,
            padding: 18,
            borderRadius: 14,
            background: "#3b1111",
            border: "1px solid #dc2626",
            color: "#fecaca",
            lineHeight: 1.6,
          }}
        >
          ❌ {error}
        </div>
      )}

      {result && (
        <div
          style={{
            marginTop: 25,
            padding: 22,
            borderRadius: 16,
            background: "#052e16",
            border: "1px solid #16a34a",
          }}
        >
          <h3
            style={{
              color: "#4ade80",
              marginBottom: 15,
            }}
          >
            ✅ Repository Imported Successfully
          </h3>

          <p>
            <strong>Dataset ID:</strong> {result.dataset_id}
          </p>

          <p>
            <strong>Chunks Indexed:</strong> {result.chunks_ingested}
          </p>

          <p style={{ marginTop: 10 }}>
            {result.message}
          </p>

          <div
            style={{
              display: "flex",
              gap: 15,
              marginTop: 20,
              flexWrap: "wrap",
            }}
          >
            <button
              className="upload-button"
              onClick={copyDataset}
            >
              📋 Copy Dataset ID
            </button>

            <a
              href={repoUrl}
              target="_blank"
              rel="noreferrer"
            >
              <button className="upload-button">
                🌐 Open Repository
              </button>
            </a>
          </div>
        </div>
      )}
    </div>
  );
}