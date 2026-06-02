import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  root: resolve(__dirname),
  base: './',
  server: {
    host: true,
    port: 5173
  },
  build: {
    outDir: resolve(__dirname, 'dist'),
    assetsDir: 'assets',
    emptyOutDir: true,
    sourcemap: true
  }
})