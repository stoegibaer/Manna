import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import { VitePWA } from 'vite-plugin-pwa'

// BASE is set by the GitHub Pages workflow ("/Manna/"); locally the app runs at "/".
const base = process.env.BASE ?? '/'

export default defineConfig({
  base,
  plugins: [
    svelte(),
    VitePWA({
      registerType: 'prompt',
      injectRegister: false,
      includeAssets: ['icon.svg', 'apple-touch-icon.png', 'robots.txt'],
      manifest: {
        name: 'Manna – Bibel in Häppchen',
        short_name: 'Manna',
        description: 'Bibellesen in kleinen Abschnitten – ADHS-freundlich.',
        lang: 'de',
        start_url: base,
        scope: base,
        display: 'standalone',
        background_color: '#FAF7F0',
        theme_color: '#FAF7F0',
        icons: [
          { src: 'icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: 'icon-512.png', sizes: '512x512', type: 'image/png' },
          { src: 'icon-maskable-512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' },
        ],
      },
      workbox: {
        // everything (incl. the whole Bible) is precached, so Manna works offline right after the first visit
        globPatterns: ['**/*.{js,css,html,svg,png,json,wav}'],
        maximumFileSizeToCacheInBytes: 6 * 1024 * 1024,
        cleanupOutdatedCaches: true,
      },
    }),
  ],
})
