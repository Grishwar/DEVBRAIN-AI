export function cn(...classes: (string | undefined | false | null)[]) {
  return classes.filter(Boolean).join(" ");
}

export function formatDate(date: string | Date) {
  return new Date(date).toLocaleString("en-IN", {
    dateStyle: "medium",
    timeStyle: "short",
  });
}

export function truncate(text: string, length = 80) {
  if (!text) return "";

  return text.length > length
    ? text.substring(0, length) + "..."
    : text;
}

export function getStatusColor(status: string) {
  switch (status.toLowerCase()) {
    case "online":
    case "connected":
    case "ready":
    case "running":
      return "#22c55e";

    case "processing":
    case "building":
      return "#f59e0b";

    case "error":
    case "offline":
    case "failed":
      return "#ef4444";

    default:
      return "#94a3b8";
  }
}

export function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function capitalize(text: string) {
  if (!text) return "";

  return text.charAt(0).toUpperCase() + text.slice(1);
}