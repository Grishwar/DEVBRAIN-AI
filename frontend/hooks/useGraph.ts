import { useEffect, useState } from "react";
import { getGraph } from "../lib/api";

export interface GraphNode {
  id: string;
  label: string;
}

export interface GraphEdge {
  source: string;
  target: string;
}

export default function useGraph(datasetId: string) {
  const [nodes, setNodes] = useState<GraphNode[]>([]);
  const [edges, setEdges] = useState<GraphEdge[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function refreshGraph() {
    if (!datasetId) return;

    setLoading(true);
    setError("");

    try {
      const data = await getGraph(datasetId);

      setNodes(data.nodes || []);
      setEdges(data.edges || []);
    } catch (err: any) {
      setError(err.message || "Unable to load knowledge graph.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refreshGraph();
  }, [datasetId]);

  return {
    nodes,
    edges,
    loading,
    error,
    refreshGraph,
  };
}