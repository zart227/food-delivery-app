import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)) // Указывает, что "@" это "src"
    }
  },
  server: {
    host: '127.0.0.1', // Укажите адрес (например, 'localhost' или '0.0.0.0' для доступа по сети)
    port: 3000,      // Укажите порт (например, 3000)
  },
})
