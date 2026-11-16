import { fileURLToPath, URL } from "url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  build: {
    manifest: false,
    rollupOptions: {
      input: ["./supporttools_vue/main.js"],
      output: {
        // Fixed filenames so assets can be shipped with the package
        // and served via Django's collectstatic without a manifest lookup.
        entryFileNames: "supporttools/js/[name].js",
        chunkFileNames: "supporttools/js/[name].js",
        assetFileNames: "supporttools/css/[name][extname]",
      },
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