import { useState } from "react";
import { ingestRepository } from "../lib/api";

export default function useIngest() {
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState("");
  const [result, setResult] = useState<any>(null);

  async function ingest(repoUrl: string) {
    if (!repoUrl.trim()) {
      setError("Please enter a GitHub repository URL.");
      return;
    }

    setLoading(true);
    setProgress(10);
    setError("");
    setResult(null);

    const timer = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 90) return prev;
        return prev + 10;
      });
    }, 300);

    try {
      const response = await ingestRepository(repoUrl);

      clearInterval(timer);
      setProgress(100);

      if (response.detail) {
        throw new Error(response.detail);
      }

      setResult(response);
      return response;
    } catch (err: any) {
      setError(err.message || "Repository ingestion failed.");
      throw err;
    } finally {
      clearInterval(timer);
      setLoading(false);
    }
  }

  function reset() {
    setLoading(false);
    setProgress(0);
    setError("");
    setResult(null);
  }

  return {
    loading,
    progress,
    error,
    result,
    ingest,
    reset,
  };
}