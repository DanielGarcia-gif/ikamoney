// Único punto de salida hacia el backend. Todas las llamadas pasan por aquí.
const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function apiGet(path) {
  const res = await fetch(`${API_URL}${path}`);
  if (!res.ok) {
    throw new Error(`El backend respondió ${res.status}`);
  }
  return res.json();
}
