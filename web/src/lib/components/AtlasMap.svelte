<script lang="ts" module>
  /** A place on the atlas. Places not [visited] yet are faint dots without a name. */
  export interface AtlasPoint { id: string; name: string; lat: number; lon: number; visited: boolean; weight: number }
</script>

<script lang="ts">
  import Canvas from './Canvas.svelte'
  import Icon from './Icon.svelte'
  import { mapData, type MapData } from '../data/content.ts'
  import { theme, alpha } from '../ui/theme.svelte.ts'

  /** Zoomable map of all [points]; pinch or scroll to zoom, drag to pan, double tap to zoom in, tap a dot to select it. */
  let { points, selected, onselect, style = '' }: { points: AtlasPoint[]; selected: string | null; onselect: (id: string) => void; style?: string } = $props()

  const MAX_ZOOM = 150
  /** Minimum distance between two shown dots. */
  const MIN_DIST = 16

  let data = $state<MapData | null>(null)
  $effect(() => { mapData().then((d) => (data = d)) })
  let scale = $state(1)
  let ox = $state(0)
  let oy = $state(0)
  let size = { w: 1, h: 1 }

  /** Viewport that fits all points (equirectangular, longitude shrunk by cos(lat)), then zoom and pan. */
  function projection(w: number, h: number, bbox: number[]) {
    const minLon = Math.min(...points.map((p) => p.lon)), maxLon = Math.max(...points.map((p) => p.lon))
    const minLat = Math.min(...points.map((p) => p.lat)), maxLat = Math.max(...points.map((p) => p.lat))
    const k = Math.cos((((minLat + maxLat) / 2) * Math.PI) / 180)
    let sx = Math.max((maxLon - minLon) * k * 1.15, 4)
    let sy = Math.max((maxLat - minLat) * 1.15, (4 * h) / w)
    const aspect = w / h
    if (sx / sy > aspect) sy = sx / aspect
    else sx = sy * aspect
    const keep = (c: number, half: number, lo: number, hi: number) => (hi - lo >= 2 * half ? Math.min(Math.max(c, lo + half), hi - half) : (lo + hi) / 2)
    const cx = keep(((minLon + maxLon) / 2) * k, sx / 2, bbox[0] * k, bbox[2] * k)
    const cy = keep((minLat + maxLat) / 2, sy / 2, bbox[1], bbox[3])
    return (lon: number, lat: number): [number, number] => [
      ((lon * k - (cx - sx / 2)) / sx) * w * scale + ox,
      ((cy + sy / 2 - lat) / sy) * h * scale + oy,
    ]
  }

  /** A point is hidden while closer than MIN_DIST to a more important one (selected > visited > weight). */
  function declutter(pr: (lon: number, lat: number) => [number, number]) {
    const ordered = [...points].sort((a, b) =>
      Number(a.id !== selected) - Number(b.id !== selected) || Number(!a.visited) - Number(!b.visited) || b.weight - a.weight || (a.id < b.id ? -1 : 1))
    const shown: [AtlasPoint, number, number][] = []
    for (const pt of ordered) {
      const [x, y] = pr(pt.lon, pt.lat)
      if (shown.every(([, sx, sy]) => Math.hypot(sx - x, sy - y) >= MIN_DIST)) shown.push([pt, x, y])
    }
    return shown
  }

  function clamp(nx: number, ny: number, s: number) {
    ox = Math.min(0, Math.max(size.w * (1 - s), nx))
    oy = Math.min(0, Math.max(size.h * (1 - s), ny))
    scale = s
  }

  function zoomAt(px: number, py: number, factor: number) {
    const ns = Math.min(MAX_ZOOM, Math.max(1, scale * factor))
    clamp((ox - px) * (ns / scale) + px, (oy - py) * (ns / scale) + py, ns)
  }

  function draw(ctx: CanvasRenderingContext2D, w: number, h: number) {
    size = { w, h }
    const c = theme.extra
    ctx.fillStyle = c.sea
    ctx.fillRect(0, 0, w, h)
    const map = data
    if (!map || !points.length) return
    const pr = projection(w, h, map.bbox)
    const path = (poly: number[][], close: boolean) => {
      ctx.beginPath()
      poly.forEach((q, i) => { const [x, y] = pr(q[0], q[1]); if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y) })
      if (close) ctx.closePath()
    }
    ctx.fillStyle = c.land
    for (const poly of map.land) { path(poly, true); ctx.fill() }
    ctx.strokeStyle = c.river; ctx.lineWidth = 2; ctx.lineCap = 'round'; ctx.lineJoin = 'round'
    for (const r of map.rivers) { path(r.line, false); ctx.stroke() }
    ctx.fillStyle = c.river
    for (const poly of map.lakes) { path(poly, true); ctx.fill() }

    const inside = (x: number, y: number) => x > -24 && y > -24 && x < w + 24 && y < h + 24
    const dot = (x: number, y: number, r: number, color: string) => { ctx.fillStyle = color; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill() }
    const shown = declutter(pr)
    for (const [pt, x, y] of shown) if (!pt.visited && inside(x, y)) dot(x, y, 3.5, alpha(c.marker, 0.3))
    const visited = shown.filter(([pt]) => pt.visited)
    for (const [pt, x, y] of [...visited].reverse()) {
      if (!inside(x, y)) continue
      if (pt.id === selected) dot(x, y, 15, alpha(c.marker, 0.22))
      dot(x, y, 5.5, c.marker)
      dot(x, y, 2.2, c.land)
    }
    // labels: right of the dot, else left; skipped if they would cover another label or dot
    ctx.font = '600 12px ' + getComputedStyle(document.body).fontFamily
    ctx.textBaseline = 'middle'
    ctx.fillStyle = c.marker
    const taken: [number, number, number, number][] = []
    const overlaps = (a: number[], b: number[]) => a[0] < b[2] && b[0] < a[2] && a[1] < b[3] && b[1] < a[3]
    visited.forEach(([pt, x, y], i) => {
      if (!inside(x, y)) return
      const tw = ctx.measureText(pt.name).width, th = 16, gap = 9
      const cands: [number, number, number, number][] = [[x + gap, y - th / 2, x + gap + tw, y + th / 2], [x - gap - tw, y - th / 2, x - gap, y + th / 2]]
      const r = cands.find((cand) => cand[0] >= 0 && cand[2] <= w && !taken.some((t) => overlaps(t, cand)) &&
        !visited.some(([, dx, dy], j) => j !== i && dx > cand[0] - 4 && dx < cand[2] + 4 && dy > cand[1] - 4 && dy < cand[3] + 4))
      if (!r) return
      taken.push(r)
      ctx.fillText(pt.name, r[0], y)
    })
  }

  // ── gestures ──
  const pointers = new Map<number, { x: number; y: number }>()
  let moved = false
  let lastTap = 0
  let pinch: { d: number; cx: number; cy: number } | null = null
  let canvasEl = $state<HTMLCanvasElement>()

  function local(e: PointerEvent) {
    const r = canvasEl!.getBoundingClientRect()
    return { x: e.clientX - r.left, y: e.clientY - r.top }
  }

  function down(e: PointerEvent) {
    canvasEl!.setPointerCapture(e.pointerId)
    pointers.set(e.pointerId, local(e))
    moved = false
    if (pointers.size === 2) {
      const [a, b] = [...pointers.values()]
      pinch = { d: Math.hypot(a.x - b.x, a.y - b.y), cx: (a.x + b.x) / 2, cy: (a.y + b.y) / 2 }
    }
  }

  function move(e: PointerEvent) {
    const prev = pointers.get(e.pointerId)
    if (!prev) return
    const p = local(e)
    pointers.set(e.pointerId, p)
    if (pointers.size === 2 && pinch) {
      const [a, b] = [...pointers.values()]
      const d = Math.hypot(a.x - b.x, a.y - b.y)
      const cx = (a.x + b.x) / 2, cy = (a.y + b.y) / 2
      const ns = Math.min(MAX_ZOOM, Math.max(1, scale * (d / pinch.d)))
      clamp((ox - pinch.cx) * (ns / scale) + cx, (oy - pinch.cy) * (ns / scale) + cy, ns)
      pinch = { d, cx, cy }
      moved = true
    } else if (pointers.size === 1) {
      const dx = p.x - prev.x, dy = p.y - prev.y
      if (Math.abs(dx) + Math.abs(dy) > 0.5) moved = moved || Math.hypot(dx, dy) > 3
      clamp(ox + dx, oy + dy, scale)
    }
  }

  function up(e: PointerEvent) {
    const p = pointers.get(e.pointerId)
    pointers.delete(e.pointerId)
    if (pointers.size < 2) pinch = null
    if (!p || moved || pointers.size > 0) return
    const now = Date.now()
    if (now - lastTap < 300) { zoomAt(p.x, p.y, 2.5); lastTap = 0; return }
    lastTap = now
    // tap: select the nearest shown dot
    const map = data
    if (!map || !points.length) return
    const pr = projection(size.w, size.h, map.bbox)
    let best: AtlasPoint | null = null, bd = 28
    for (const [pt, x, y] of declutter(pr)) { const d = Math.hypot(x - p.x, y - p.y); if (d < bd) { bd = d; best = pt } }
    if (best) onselect(best.id)
  }

  function wheel(e: WheelEvent) {
    e.preventDefault()
    const r = canvasEl!.getBoundingClientRect()
    zoomAt(e.clientX - r.left, e.clientY - r.top, Math.exp(-e.deltaY * 0.002))
  }

  $effect(() => {
    const el = canvasEl
    if (!el) return
    el.addEventListener('pointermove', move)
    el.addEventListener('pointerup', up)
    el.addEventListener('pointercancel', up)
    el.addEventListener('wheel', wheel, { passive: false })
    return () => {
      el.removeEventListener('pointermove', move)
      el.removeEventListener('pointerup', up)
      el.removeEventListener('pointercancel', up)
      el.removeEventListener('wheel', wheel)
    }
  })
</script>

<div class="atlas" {style}>
  <Canvas bind:el={canvasEl} label="Karte aller Orte" style="touch-action:none" {draw} onpointerdown={down} />
  {#if scale > 1.01}
    <button class="reset" onclick={() => { scale = 1; ox = 0; oy = 0 }} aria-label="Ganze Karte zeigen">
      <Icon name="zoomOut" color="var(--primary)" />
    </button>
  {/if}
</div>

<style>
  .atlas { position: relative; overflow: hidden; }
  .reset {
    position: absolute; top: 10px; right: 10px; border: 0; border-radius: 50%; padding: 8px; cursor: pointer; display: flex;
    background: color-mix(in srgb, var(--surface) 90%, transparent);
  }
</style>
