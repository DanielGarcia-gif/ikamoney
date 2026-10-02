import { useEffect, useState } from "react";
import { apiGet } from "../api/client.js";

// Pantalla temporal: demuestra frontend -> backend -> base de datos.
export default function PipelineCheck() {
  const [state, setState] = useState({ status: "loading" });

  useEffect(() => {
    apiGet("/api/ping-db")
      .then((data) => setState({ status: "ok", message: data.message }))
      .catch((err) => setState({ status: "error", message: err.message }));
  }, []);

  return (
    <main style={{ fontFamily: "system-ui, sans-serif", maxWidth: 560, margin: "4rem auto", padding: "0 1rem" }}>
      <h1>IKAMONEY</h1>
      <p>Prueba de conexión entre frontend, backend y base de datos.</p>
      {state.status === "loading" && <p>Consultando al backend…</p>}
      {state.status === "ok" && <p>✅ {state.message}</p>}
      {state.status === "error" && (
        <p>
          ❌ No se pudo completar la conexión ({state.message}). Revisa que el backend y la
          base de datos estén corriendo; mira la sección “Si algo falla” del README.
        </p>
      )}
    </main>
  );
}
