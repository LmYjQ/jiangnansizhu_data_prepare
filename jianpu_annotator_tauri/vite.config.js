import { defineConfig } from "vite";

export default defineConfig({
  clearScreen: false,
  server: {
    port: 5173,
    strictPort: false,
    watch: {
      ignored: ["**/src-tauri/**"],
    },
  },
});
