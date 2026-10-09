// Único punto de salida hacia el backend. Todas las llamadas pasan por aquí.
const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function apiGet(path) {
  const res = await fetch(`${API_URL}${path}`);
  if (!res.ok) {
    // FastAPI manda el motivo en { detail: "..." }; lo mostramos si viene.
    let detail = "";
    try {
      detail = (await res.json()).detail ?? "";
    } catch {
      /* la respuesta no era JSON */
    }
    throw new Error(detail || `El backend respondió ${res.status}`);
  }
  return res.json();
}
