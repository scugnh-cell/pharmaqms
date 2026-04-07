import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import AutoImport from "unplugin-auto-import/vite";
import Components from "unplugin-vue-components/vite";
import { ElementPlusResolver } from "unplugin-vue-components/resolvers";
import ElementPlus from "unplugin-element-plus/vite";
import viteCompression from "vite-plugin-compression";
import { resolve } from "path";

export default defineConfig({
  define: {
    "process.env": {
      NODE_ENV: "production",
      VUE_APP_BASE_API: "/api",
    },
  },
  resolve: {
    alias: {
      "@": resolve(__dirname, "./src"),
    },
    extensions: [".vue", ".js", ".json"],
  },
  server: {
    port: 8080,
    host: true,
    proxy: {
      "/api": {
        target: "http://localhost:8889",
        changeOrigin: true,
      },
    },
  },
  plugins: [
    vue(),
    viteCompression({ threshold: 4096 }),
    ElementPlus(),
    Components({
      dirs: ["src/components"],
      extensions: ["vue"],
      resolvers: [ElementPlusResolver()],
    }),
    AutoImport({
      imports: ["vue", "vue-router"],
    }),
    AutoImport({
      resolvers: [ElementPlusResolver()],
    }),
  ],
  build: {
    outDir: "dist",
    assetsDir: "static",
    minify: "esbuild",
    rollupOptions: {
      input: { index: resolve(__dirname, "index.html") },
      output: {
        chunkFileNames: "static/js/[name]-[hash].js",
        entryFileNames: "static/js/[name]-[hash].js",
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name.split(".");
          let extType = info[info.length - 1];
          if (/\.(png|jpe?g|gif|svg|ico)(\?.*)?$/.test(assetInfo.name)) extType = "img";
          else if (/\.(woff2?|eot|ttf|otf)(\?.*)?$/i.test(assetInfo.name)) extType = "fonts";
          return `static/${extType}/[name]-[hash][extname]`;
        },
      },
    },
  },
});
