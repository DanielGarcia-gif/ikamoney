import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// envDir: "..": el .env único vive en la raíz del repo.
// Solo las variables que empiezan con VITE_ llegan al navegador.
export default defineConfig({
  plugins: [react()],
  envDir: "..",
  server: { port: 5173 },
});
