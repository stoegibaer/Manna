import { FIRST } from '../data/garden.ts'
import type { MannaColors } from '../ui/theme.svelte.ts'
import { mustard, rad, type Leaf, type Seg } from './treeModel.ts'

type Ctx = CanvasRenderingContext2D

/**
 * Growth 0..1 from the number of completed sections: fast at first, fully grown after
 * FIRST sections – then the view changes to the garden. Never shrinks.
 */
export function treeGrowth(sections: number): number {
  const x = Math.min(1, Math.max(0, sections / FIRST))
  return 1 - (1 - x) * (1 - x)
}

const model = mustard()
const f = (t: number, birth: number, span: number) => Math.min(1, Math.max(0, (t - birth) / span))

function leafAt(ctx: Ctx, x: number, y: number, angleDeg: number, length: number, color: string) {
  if (length <= 0.5) return
  ctx.save()
  ctx.translate(x, y)
  ctx.rotate(rad(-angleDeg))
  ctx.beginPath()
  ctx.moveTo(0, 0)
  ctx.quadraticCurveTo(length * 0.5, -length * 0.38, length, 0)
  ctx.quadraticCurveTo(length * 0.5, length * 0.38, 0, 0)
  ctx.closePath()
  ctx.fillStyle = color
  ctx.fill()
  ctx.restore()
}

/**
 * The mustard seed (Mk 4,30–32) that grows into a tree with every completed section
 * (port of ui/components/MustardTree.kt). Shown alone while the first tree grows.
 */
export function drawMustard(ctx: Ctx, w: number, h: number, sections: number, colors: MannaColors) {
  const t = treeGrowth(sections)
  const unit = Math.min(w * 1.05, h) * 0.95
  // zoom in while the plant is small so even a sprout fills the frame
  const scale = unit * (1.55 - 0.75 * t)
  const rx = w / 2, ry = h * 0.93
  const p = (x: number, y: number): [number, number] => [rx + x * scale, ry - y * scale]

  ctx.fillStyle = colors.ground
  ctx.beginPath()
  ctx.ellipse(rx, ry + unit * 0.005, unit * 0.32, unit * 0.03, 0, 0, Math.PI * 2)
  ctx.fill()

  if (t < 0.012) {
    ctx.fillStyle = colors.trunk
    ctx.beginPath()
    ctx.ellipse(rx, ry - scale * 0.018, scale * 0.02, scale * 0.014, 0, 0, Math.PI * 2)
    ctx.fill()
    return
  }

  const tip = (b: Seg): [number, number] => {
    const k = f(t, b.birth, b.span)
    const a = b.pts[0], e = b.pts[1]
    return p(a.x + (e.x - a.x) * k, a.y + (e.y - a.y) * k)
  }

  ctx.strokeStyle = colors.trunk
  ctx.lineCap = 'round'
  for (const b of model.segs) {
    const k = f(t, b.birth, b.span)
    if (k <= 0) continue
    ctx.lineWidth = b.w * scale * (0.6 + 0.4 * k) * (0.4 + 0.6 * t)
    const [x0, y0] = p(b.pts[0].x, b.pts[0].y)
    const [x1, y1] = tip(b)
    ctx.beginPath()
    ctx.moveTo(x0, y0)
    ctx.lineTo(x1, y1)
    ctx.stroke()
  }

  // first two seed leaves while the plant is a sprout
  const sprout = (1 - f(t, 0.22, 0.2)) * f(t, 0.012, 0.02)
  if (sprout > 0) {
    const [x, y] = tip(model.segs[0])
    leafAt(ctx, x, y, 55, 0.11 * scale * sprout, colors.leaf)
    leafAt(ctx, x, y, 125, 0.11 * scale * sprout, colors.leafDark)
  }

  for (const l of model.leaves as Required<Leaf>[]) {
    const k = f(t, l.birth, 0.05)
    if (k <= 0 || f(t, l.seg.birth, l.seg.span) < l.pos) continue
    const [x, y] = p(l.x, l.y)
    leafAt(ctx, x, y, l.a, l.len * scale * 1.6 * k, l.dark ? colors.leafDark : colors.leaf)
  }

  ctx.fillStyle = colors.blossom
  for (const bl of model.flowers) {
    const k = f(t, bl.birth, 0.06)
    if (k <= 0 || !bl.seg || f(t, bl.seg.birth, bl.seg.span) < 1) continue
    const [x, y] = p(bl.x, bl.y)
    const r = bl.r * scale * k
    for (let q = 0; q < 4; q++) {
      const a = rad(q * 90 + 45)
      ctx.beginPath()
      ctx.arc(x + Math.cos(a) * r * 0.55, y + Math.sin(a) * r * 0.55, r * 0.62, 0, Math.PI * 2)
      ctx.fill()
    }
  }
}
