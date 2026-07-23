import { fileURLToPath, URL } from "url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  build: {
    manifest: true,
    rollupOptions: {
      input: ["./supporttools_vue/main.js"],
    },
    outDir: "./supporttools/static/",
    assetsDir: "supporttools/assets",
    emptyOutDir: false,
  },
  base: "/static/",
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./supporttools_vue", import.meta.url)),
    },
  },
});