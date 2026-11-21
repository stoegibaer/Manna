<script lang="ts">
  import { confetti } from '../ui/confetti.svelte.ts'
  import { store } from '../data/store.svelte.ts'
  import { showConfetti } from '../data/types.ts'
  import { theme } from '../ui/theme.svelte.ts'
  import { KotlinRandom } from '../util/random.ts'

  let canvas: HTMLCanvasElement
  let frame = 0

  interface P { angle: number; speed: number; spin: number; color: number; w: number; h: number }

  $effect(() => {
    const trigger = confetti.trigger
    const big = confetti.big
    if (trigger <= 0 || !showConfetti(store.settings)) return
    const pal = [theme.scheme.primary, theme.extra.blossom, theme.extra.leaf, theme.scheme.tertiary, theme.scheme.secondary]
    const rnd = new KotlinRandom(trigger * 31 + 7)
    const parts: P[] = Array.from({ length: big ? 90 : 36 }, () => ({
      angle: -90 + (rnd.nextFloat() - 0.5) * (big ? 150 : 110),
      speed: 0.55 + rnd.nextFloat() * 0.75,
      spin: (rnd.nextFloat() - 0.5) * 900,
      color: rnd.nextIntUntil(5),
      w: 6 + rnd.nextFloat() * 7,
      h: 4 + rnd.nextFloat() * 4,
    }))
    const dur = big ? 2200 : 1400
    const start = performance.now()
    cancelAnimationFrame(frame)
    const step = (now: number) => {
      const t = Math.min(1, (now - start) / dur)
      const dpr = Math.min(3, window.devicePixelRatio || 1)
      const W = window.innerWidth, H = window.innerHeight
      if (canvas.width !== Math.round(W * dpr)) canvas.width = Math.round(W * dpr)
      if (canvas.height !== Math.round(H * dpr)) canvas.height = Math.round(H * dpr)
      const ctx = canvas.getContext('2d')!
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
      ctx.clearRect(0, 0, W, H)
      if (t < 1) {
        const ox = W / 2, oy = H * (big ? 0.45 : 0.55), reach = H * 0.9
        for (const p of parts) {
          const r = (p.angle * Math.PI) / 180
          const x = ox + Math.cos(r) * p.speed * reach * t
          const y = oy + Math.sin(r) * p.speed * reach * t + 0.9 * reach * t * t
          ctx.globalAlpha = Math.min(1, Math.max(0, 1.6 - 1.6 * t))
          ctx.fillStyle = pal[p.color]
          ctx.save()
          ctx.translate(x, y)
          ctx.rotate((p.spin * t * Math.PI) / 180)
          ctx.fillRect(-p.w / 2, -p.h / 2, p.w, p.h)
          ctx.restore()
        }
        ctx.globalAlpha = 1
        frame = requestAnimationFrame(step)
      }
    }
    frame = requestAnimationFrame(step)
    return () => cancelAnimationFrame(frame)
  })
</script>

<canvas bind:this={canvas} aria-hidden="true"></canvas>

<style>
  canvas { position: fixed; inset: 0; width: 100vw; height: 100dvh; pointer-events: none; z-index: 60; }
</style>
