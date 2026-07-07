import { useEffect, useState } from "react";
import { getTimeline } from "../lib/api";

export interface TimelineEvent {
  id?: string;
  event_type?: string;
  title?: string;
  summary?: string;
  created_at?: string;
  timestamp?: string;
}

export default function useTimeline(datasetId: string) {
  const [events, setEvents] = useState<TimelineEvent[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function refreshTimeline() {
    if (!datasetId) return;

    setLoading(true);
    setError("");

    try {
      const data = await getTimeline(datasetId);

      if (Array.isArray(data)) {
        setEvents(data);
      } else if (Array.isArray(data.events)) {
        setEvents(data.events);
      } else {
        setEvents([]);
      }
    } catch (err: any) {
      setError(err.message || "Unable to load timeline.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refreshTimeline();
  }, [datasetId]);

  return {
    events,
    loading,
    error,
    refreshTimeline,
  };
}