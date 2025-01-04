import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue(), vueDevTools()],
  build: {
    sourcemap: true,
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)), // Указывает, что "@" это "src"
    },
  },
  server: {
    host: '0.0.0.0', // Для доступа к серверу внутри Docker
    port: 3000, // Оставьте порт, который используется в Docker (опционально)
    watch: {
      usePolling: true, // Полезно для окружений внутри Docker
    },
  },
  define: {
    'process.env': {},
  },
})
