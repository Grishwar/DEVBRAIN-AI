import { useState } from "react";
import { askRepository } from "../lib/api";

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export default function useAsk() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content:
        "👋 Hi! I'm DevBrain AI.\n\nAsk me anything about your GitHub repository.",
    },
  ]);

  const [loading, setLoading] = useState(false);

  async function ask(dataset: string, question: string) {
    if (!dataset.trim() || !question.trim()) return;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: question,
      },
    ]);

    setLoading(true);

    try {
      const response = await askRepository(dataset, question);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            response.answer ??
            response.response ??
            "No response received.",
        },
      ]);
    } catch (error: any) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            error?.message ??
            "❌ Unable to communicate with the backend.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return {
    messages,
    loading,
    ask,
    setMessages,
  };
}