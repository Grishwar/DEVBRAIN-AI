const API = "http://127.0.0.1:8000";

export async function ingestRepository(repoUrl: string) {
  const res = await fetch(`${API}/ingest`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      repo_url: repoUrl,
    }),
  });

  return await res.json();
}

export async function askRepository(dataset: string, question: string) {
  const res = await fetch(`${API}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      dataset_id: dataset,
      question,
    }),
  });

  return await res.json();
}

export async function getGraph(dataset: string) {
  const res = await fetch(`${API}/graph/${dataset}`);
  return await res.json();
}

export async function getTimeline(dataset: string) {
  const res = await fetch(`${API}/timeline/${dataset}`);
  return await res.json();
}

export async function getDiff(dataset: string) {
  const res = await fetch(`${API}/diff/${dataset}`);
  return await res.json();
}

export async function health() {
  const res = await fetch(`${API}/health`);
  return await res.json();
}