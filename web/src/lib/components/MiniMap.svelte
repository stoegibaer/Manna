<script lang="ts">
  import Canvas from './Canvas.svelte'
  import { mapData, type MapData } from '../data/content.ts'
  import type { Place } from '../data/plan.ts'
  import { theme, alpha } from '../ui/theme.svelte.ts'

  /**
   * Simple map centered on [place]. [reference] (usually Jerusalem) is shown as a small orientation dot
   * and included in the view, so one sees how far away the place is.
   */
  let { place, reference, style = '' }: { place: Place; reference?: Place | null; style?: string } = $props()
  let data = $state<MapData | null>(null)
  $effect(() => { mapData().then((d) => (data = d)) })

  function draw(ctx: CanvasRenderingContext2D, w: number, h: number) {
    const c = theme.extra
    ctx.fillStyle = c.sea
    ctx.fillRect(0, 0, w, h)
    const map = data
    if (!map) return
    const pts = [place, ...(reference && reference.id !== place.id ? [reference] : [])]
    const minLon = Math.min(...pts.map((p) => p.lon)), maxLon = Math.max(...pts.map((p) => p.lon))
    const minLat = Math.min(...pts.map((p) => p.lat)), maxLat = Math.max(...pts.map((p) => p.lat))
    const k = Math.cos((((minLat + maxLat) / 2) * Math.PI) / 180)
    let spanX = Math.max((maxLon - minLon) * k * 1.6, 3.2)
    let spanY = Math.max((maxLat - minLat) * 1.6, (3.2 * h) / w)
    const aspect = w / h
    if (spanX / spanY > aspect) spanY = spanX / aspect
    else spanX = spanY * aspect
    const cx = ((minLon + maxLon) / 2) * k, cy = (minLat + maxLat) / 2
    const p = (lon: number, lat: number): [number, number] => [((lon * k - (cx - spanX / 2)) / spanX) * w, ((cy + spanY / 2 - lat) / spanY) * h]
    const path = (poly: number[][], close: boolean) => {
      ctx.beginPath()
      poly.forEach((q, i) => { const [x, y] = p(q[0], q[1]); if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y) })
      if (close) ctx.closePath()
    }
    ctx.fillStyle = c.land
    for (const poly of map.land) { path(poly, true); ctx.fill() }
    ctx.strokeStyle = c.river; ctx.lineWidth = 2.2; ctx.lineCap = 'round'; ctx.lineJoin = 'round'
    for (const r of map.rivers) { path(r.line, false); ctx.stroke() }
    ctx.fillStyle = c.river
    for (const poly of map.lakes) { path(poly, true); ctx.fill() }

    const dot = (x: number, y: number, r: number, color: string) => { ctx.fillStyle = color; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill() }
    ctx.textBaseline = 'middle'
    if (reference && reference.id !== place.id) {
      const [rx, ry] = p(reference.lon, reference.lat)
      dot(rx, ry, 3.5, alpha(c.marker, 0.6))
      ctx.font = '400 13px ' + getComputedStyle(document.body).fontFamily
      ctx.fillStyle = alpha(c.marker, 0.8)
      ctx.fillText(reference.name, rx + 6, ry)
    }
    const [mx, my] = p(place.lon, place.lat)
    dot(mx, my, 16, alpha(c.marker, 0.22))
    dot(mx, my, 6, c.marker)
    dot(mx, my, 2.4, c.land)
    ctx.font = '600 13px ' + getComputedStyle(document.body).fontFamily
    const tw = ctx.measureText(place.name).width
    ctx.fillStyle = c.marker
    ctx.fillText(place.name, Math.min(mx + 12, w - tw - 4), my - 14)
  }
</script>

<div {style}><Canvas label={`Karte: ${place.name}`} {draw} /></div>
