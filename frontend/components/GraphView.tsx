"use client";

import {
  Background,
  Controls,
  MiniMap,
  ReactFlow,
  MarkerType,
  type Node,
  type Edge,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";

const nodes: Node[] = [
  {
    id: "1",
    type: "default",
    position: { x: 300, y: 20 },
    data: { label: "📦 GitHub Repository" },
    style: {
      background: "#2563eb",
      color: "#fff",
      border: "2px solid #60a5fa",
      borderRadius: 14,
      padding: 12,
      fontWeight: 700,
      fontSize: 15,
      minWidth: 180,
      textAlign: "center" as const,
    },
  },

  {
    id: "2",
    type: "default",
    position: { x: 300, y: 180 },
    data: { label: "🧠 Cognee Memory" },
    style: {
      background: "#16a34a",
      color: "#fff",
      border: "2px solid #4ade80",
      borderRadius: 14,
      padding: 12,
      fontWeight: 700,
      fontSize: 15,
      minWidth: 180,
      textAlign: "center" as const,
    },
  },

  {
    id: "3",
    type: "default",
    position: { x: 30, y: 380 },
    data: { label: "💬 Ask AI" },
    style: {
      background: "#7c3aed",
      color: "#fff",
      border: "2px solid #a78bfa",
      borderRadius: 14,
      padding: 12,
      fontWeight: 700,
      minWidth: 160,
      textAlign: "center" as const,
    },
  },

  {
    id: "4",
    type: "default",
    position: { x: 300, y: 380 },
    data: { label: "📜 Timeline" },
    style: {
      background: "#ea580c",
      color: "#fff",
      border: "2px solid #fdba74",
      borderRadius: 14,
      padding: 12,
      fontWeight: 700,
      minWidth: 160,
      textAlign: "center" as const,
    },
  },

  {
    id: "5",
    type: "default",
    position: { x: 570, y: 380 },
    data: { label: "🕸 Knowledge Graph" },
    style: {
      background: "#0891b2",
      color: "#fff",
      border: "2px solid #67e8f9",
      borderRadius: 14,
      padding: 12,
      fontWeight: 700,
      minWidth: 180,
      textAlign: "center" as const,
    },
  },

  {
    id: "6",
    type: "default",
    position: { x: 300, y: 560 },
    data: { label: "🔄 Semantic Diff" },
    style: {
      background: "#db2777",
      color: "#fff",
      border: "2px solid #f9a8d4",
      borderRadius: 14,
      padding: 12,
      fontWeight: 700,
      minWidth: 180,
      textAlign: "center" as const,
    },
  },
];

const edges: Edge[] = [
  {
    id: "1-2",
    source: "1",
    target: "2",
    animated: true,
    markerEnd: {
      type: MarkerType.ArrowClosed,
    },
  },
  {
    id: "2-3",
    source: "2",
    target: "3",
    animated: true,
    markerEnd: {
      type: MarkerType.ArrowClosed,
    },
  },
  {
    id: "2-4",
    source: "2",
    target: "4",
    animated: true,
    markerEnd: {
      type: MarkerType.ArrowClosed,
    },
  },
  {
    id: "2-5",
    source: "2",
    target: "5",
    animated: true,
    markerEnd: {
      type: MarkerType.ArrowClosed,
    },
  },
  {
    id: "5-6",
    source: "5",
    target: "6",
    animated: true,
    markerEnd: {
      type: MarkerType.ArrowClosed,
    },
  },
];

export default function GraphView() {
  return (
    <div
      style={{
        width: "100%",
        height: 720,
        borderRadius: 22,
        overflow: "hidden",
        border: "1px solid #1f2937",
        background: "#020617",
        boxShadow: "0 15px 40px rgba(0,0,0,.35)",
      }}
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        fitViewOptions={{
          padding: 0.2,
        }}
      >
        <Background gap={20} size={1.2} />
        <MiniMap pannable zoomable />
        <Controls />
      </ReactFlow>
    </div>
  );
}