import type { MannaColors } from '../ui/theme.svelte.ts'
import { frac, lerp, polyAt, rad, type Model } from './treeModel.ts'
import { Rng } from '../util/random.ts'
import { modelOf, type LeafShape, type TreeColors, type TreeSpecies } from './trees.ts'


type Ctx = CanvasRenderingContext2D

/** Colors of the surroundings (ground, sky, water, birds). Port of ui/garden/TreeDraw.kt. */
export interface SceneColors {
  dark: boolean; trunk: string; trunkDark: string; blossom: string; ground: string
  sky: string; hill: string; hill2: string; water: string; water2: string; bank: string; reed: string
  bird: string; birdWing: string; white: string
}

export function sceneColors(c: MannaColors): SceneColors {
  return c.dark
    ? { dark: true, trunk: c.trunk, trunkDark: '#8C6C4C', blossom: c.blossom, ground: c.ground, sky: '#1A1E22', hill: '#24272A', hill2: '#2C2E30', water: '#4F7F9C', water2: '#7FA9C2', bank: '#33383A', reed: '#7FA06A', bird: '#D9CFC2', birdWing: '#A89886', white: '#F3EEE6' }
    : { dark: false, trunk: c.trunk, trunkDark: '#5E4630', blossom: c.blossom, ground: c.ground, sky: '#F4EFE3', hill: '#E7DECB', hill2: '#DED3BD', water: '#8FB4CC', water2: '#C9DEEA', bank: '#D3CDB4', reed: '#7E9A5A', bird: '#5A4E44', birdWing: '#8C7B6B', white: '#FFFFFF' }
}

export interface TreeOpts {
  /** Progress of the finale moment 0..1, or null for none. */
  fin?: number | null
  ground?: boolean
  groundColor?: string
  groundR?: number
  /** Height of the ground shadow; default follows groundR. */
  groundRy?: number
  /** Brook at the foot (only when shown alone). */
  water?: boolean
  /** Only this many fruits, in ripening order, colored by fruitColor (tree of life). */
  fruitN?: number | null
  fruitColor?: (k: number) => string
}

// ── canvas helpers ──

export function oval(ctx: Ctx, color: string, cx: number, cy: number, rx: number, ry: number, rot = 0, a = 1) {
  if (rx <= 0 || ry <= 0 || a <= 0) return
  ctx.globalAlpha = a
  ctx.fillStyle = color
  ctx.beginPath()
  ctx.ellipse(cx, cy, rx, ry, rot, 0, Math.PI * 2)
  ctx.fill()
  ctx.globalAlpha = 1
}

export function circle(ctx: Ctx, color: string, x: number, y: number, r: number, a = 1) {
  oval(ctx, color, x, y, r, r, 0, a)
}

export function line(ctx: Ctx, color: string, ax: number, ay: number, bx: number, by: number, width: number, a = 1) {
  if (a <= 0) return
  ctx.globalAlpha = a
  ctx.strokeStyle = color
  ctx.lineWidth = width
  ctx.lineCap = 'round'
  ctx.beginPath()
  ctx.moveTo(ax, ay)
  ctx.lineTo(bx, by)
  ctx.stroke()
  ctx.globalAlpha = 1
}

function fill(ctx: Ctx, p: Path2D, color: string, a = 1) {
  ctx.globalAlpha = a
  ctx.fillStyle = color
  ctx.fill(p)
  ctx.globalAlpha = 1
}

function stroke(ctx: Ctx, p: Path2D, color: string, width: number, join: CanvasLineJoin = 'miter') {
  ctx.strokeStyle = color
  ctx.lineWidth = width
  ctx.lineCap = 'round'
  ctx.lineJoin = join
  ctx.stroke(p)
}

/** A leaf pointing in direction [angDeg] (math angle, y up) from (x, y). */
export function leaf(ctx: Ctx, x: number, y: number, angDeg: number, len: number, shape: LeafShape, wr: number, color: string) {
  if (len <= 0.3) return
  const path = new Path2D()
  const lobe = (rotDeg: number, l: number, w: number) => {
    const c = Math.cos(rad(rotDeg)), s = Math.sin(rad(rotDeg))
    const px = (x0: number, y0: number) => x0 * c - y0 * s
    const py = (x0: number, y0: number) => x0 * s + y0 * c
    const wl = l * w
    path.moveTo(0, 0)
    path.quadraticCurveTo(px(l * 0.5, -wl), py(l * 0.5, -wl), px(l, 0), py(l, 0))
    path.quadraticCurveTo(px(l * 0.5, wl), py(l * 0.5, wl), 0, 0)
  }
  if (shape === 'LOBED') { lobe(-38, len * 0.78, 0.34); lobe(0, len, 0.34); lobe(38, len * 0.78, 0.34) }
  else if (shape === 'ROUND') path.ellipse(len / 2, 0, len / 2, len * 0.36, 0, 0, Math.PI * 2)
  else lobe(0, len, wr)
  ctx.save()
  ctx.translate(x, y)
  ctx.rotate(rad(-angDeg))
  fill(ctx, path, color)
  ctx.restore()
}

function blossom(ctx: Ctx, x: number, y: number, r: number, color: string, center: string | undefined, petals: number) {
  for (let k = 0; k < petals; k++) {
    const a = (k * 2 * Math.PI) / petals + 0.4
    circle(ctx, color, x + Math.cos(a) * r * 0.55, y + Math.sin(a) * r * 0.55, r * 0.55)
  }
  if (center) circle(ctx, center, x, y, r * 0.3)
}

/** A small bird, sitting or (while [flying]) as a flapping silhouette. */
function bird(ctx: Ctx, x: number, y: number, s: number, flap: number, facing: number, body: string, wing: string, beak: string, flying: boolean) {
  ctx.save()
  ctx.translate(x, y)
  ctx.scale(facing, 1)
  if (flying) {
    const wy = Math.sin(flap) * s * 0.5
    const p = new Path2D()
    p.moveTo(-s, wy)
    p.quadraticCurveTo(-s * 0.4, -s * 0.2 + wy * 0.3, 0, 0)
    p.quadraticCurveTo(s * 0.4, -s * 0.2 + wy * 0.3, s, wy)
    stroke(ctx, p, body, Math.max(1, s * 0.18))
  } else {
    oval(ctx, body, 0, -s * 0.35, s * 0.55, s * 0.36, -0.25)
    circle(ctx, body, s * 0.45, -s * 0.72, s * 0.24)
    const tail = new Path2D()
    tail.moveTo(-s * 0.4, -s * 0.3); tail.lineTo(-s * 0.95, -s * 0.05); tail.lineTo(-s * 0.85, -s * 0.38); tail.closePath()
    fill(ctx, tail, body)
    const bk = new Path2D()
    bk.moveTo(s * 0.66, -s * 0.76); bk.lineTo(s * 0.88, -s * 0.7); bk.lineTo(s * 0.66, -s * 0.64); bk.closePath()
    fill(ctx, bk, beak)
    oval(ctx, wing, -s * 0.08, -s * 0.38, s * 0.32, s * 0.16, -0.35)
  }
  ctx.restore()
}

/** Draws one tree with its root at (rootX, rootY). [t] = growth 0..1, [scale] = pixels per tree unit. */
export function drawTree(ctx: Ctx, sp: TreeSpecies, t: number, rootX: number, rootY: number, scale: number, sc: SceneColors, o: TreeOpts = {}) {
  const m = modelOf(sp)
  const col = sc.dark ? sp.dark : sp.light
  const px = (x: number) => rootX + x * scale
  const py = (y: number) => rootY - y * scale
  const groundR = o.groundR ?? 0.3

  if (o.ground ?? true) oval(ctx, o.groundColor ?? sc.ground, rootX, rootY, scale * groundR, scale * (o.groundRy ?? 0.028 * (groundR / 0.3) * 1.3))
  if (o.water) {
    oval(ctx, sc.water, rootX + scale * 0.28, rootY + scale * 0.012, scale * 0.2, scale * 0.024)
    oval(ctx, sc.water2, rootX + scale * 0.3, rootY + scale * 0.008, scale * 0.08, scale * 0.007)
  }
  if (t < 0.012) { // the seed
    oval(ctx, sc.trunk, rootX, rootY - scale * 0.016, scale * 0.02, scale * 0.014)
    return
  }

  if (m.palmPts) drawPalm(ctx, m, t, px, py, scale, col)
  else {
    for (const s of m.segs) {
      const f = frac(t, s.birth, s.span)
      if (f <= 0) continue
      const pts = s.pts
      const upto = f * (pts.length - 1)
      const path = new Path2D()
      path.moveTo(px(pts[0].x), py(pts[0].y))
      for (let i = 1; i <= Math.ceil(upto); i++) {
        const u = Math.min(1, upto - (i - 1))
        const q = pts[i - 1], w = pts[i]
        path.lineTo(px(lerp(q.x, w.x, u)), py(lerp(q.y, w.y, u)))
      }
      const width = Math.max(0.6, s.w * scale * (0.6 + 0.4 * f) * (0.45 + 0.55 * t))
      stroke(ctx, path, col.trunk, width, 'round')
    }
    // seed leaves while it is a sprout
    const sprout = (1 - frac(t, 0.22, 0.2)) * frac(t, 0.012, 0.02)
    if (sprout > 0 && m.segs.length) {
      const s0 = m.segs[0]
      const [x, y] = polyAt(s0.pts, frac(t, s0.birth, s0.span))
      leaf(ctx, px(x), py(y), 55, 0.11 * scale * sprout, 'ELLIPSE', 0.38, col.leaf)
      leaf(ctx, px(x), py(y), 125, 0.11 * scale * sprout, 'ELLIPSE', 0.38, col.leafDark)
    }
    for (const st of m.strands) {
      const f = frac(t, st.birth, 0.1)
      if (f <= 0) continue
      const x = px(st.x), y = py(st.y), l = st.len * scale * f, sw = st.sway * scale
      const p = new Path2D()
      p.moveTo(x, y)
      p.quadraticCurveTo(x + sw, y + l * 0.5, x + sw * 1.6, y + l)
      stroke(ctx, p, st.dark ? col.leafDark : col.leaf, Math.max(0.8, scale * (sp.strandW ?? 0.006)))
    }
    for (const c of m.clumps) {
      const f = frac(t, c.birth, 0.08)
      if (f <= 0) continue
      const rr = c.r * scale * f
      const color = c.shade < 0.33 ? col.leafDark : c.shade < 0.8 ? col.leaf : col.leafLight ?? col.leaf
      oval(ctx, color, px(c.x), py(c.y), rr, rr * (c.flat ?? sp.flat ?? 0.85))
    }
    const shape = sp.leafShape ?? 'ELLIPSE'
    if (shape !== 'NONE') for (const l of m.leaves) {
      const f = frac(t, l.birth, 0.05)
      if (f <= 0) continue
      leaf(ctx, px(l.x), py(l.y), l.a, l.len * scale * 1.6 * f, shape, sp.leafW ?? 0.38, l.dark ? col.leafDark : col.leaf)
    }
    const fc = col.flower
    if (fc) for (const b of m.flowers) {
      const f = frac(t, b.birth, 0.06)
      if (f <= 0) continue
      const x = px(b.x), y = py(b.y), rr = b.r * scale * f
      switch (sp.flowerKind ?? 'BLOSSOM') {
        case 'BALL': circle(ctx, fc, x, y, rr * 0.7); break
        case 'PLUME': line(ctx, fc, x, y, x + rr * 0.3, y - rr * 1.6, Math.max(1, rr * 0.5)); break
        case 'BLOSSOM': blossom(ctx, x, y, rr, fc, col.flowerCenter, sp.petals ?? 4); break
        case 'CROSS':
          for (let k = 0; k < 4; k++) {
            const a = rad(k * 90 + 45)
            circle(ctx, fc, x + Math.cos(a) * rr * 0.55, y + Math.sin(a) * rr * 0.55, rr * 0.62)
          }
      }
    }
    const defaultFruit = col.fruit
    if (defaultFruit) {
      const list = o.fruitN != null ? m.fruitOrder.slice(0, Math.min(o.fruitN, m.fruits.length)).map((i) => m.fruits[i]) : m.fruits
      list.forEach((fr, k) => {
        const f = o.fruitN != null ? 1 : frac(t, fr.birth, 0.06)
        if (f <= 0) return
        const x = px(fr.x), y = py(fr.y), rr = fr.r * scale * f
        const c = o.fruitColor?.(k) ?? defaultFruit
        const kind = sp.fruitKind ?? 'ROUND'
        if (kind === 'OVAL') oval(ctx, c, x, y, rr * 0.7, rr, 0.3)
        else if (kind === 'PEAR') oval(ctx, c, x, y + rr * 0.2, rr, rr * 1.05)
        else circle(ctx, c, x, y, rr)
        if (kind === 'CROWN') {
          const p = new Path2D()
          p.moveTo(x - rr * 0.3, y - rr * 0.9); p.lineTo(x, y - rr * 1.35); p.lineTo(x + rr * 0.3, y - rr * 0.9); p.closePath()
          fill(ctx, p, col.fruitDark ?? c)
        }
        if (o.fruitN != null) circle(ctx, '#FFFFFF', x - rr * 0.3, y - rr * 0.3, rr * 0.3, 0.55)
      })
    }
  }
  const fin = o.fin
  if (fin != null && fin > 0 && sp.finale) drawFinale(ctx, sp, m, fin, px, py, scale, col, sc)
}

function drawPalm(ctx: Ctx, m: Model, t: number, px: (x: number) => number, py: (y: number) => number, scale: number, col: TreeColors) {
  const pts = m.palmPts!
  const trunkF = frac(t, 0, 0.8)
  const n = pts.length - 1
  const upto = Math.max(0.02, trunkF) * n
  let tip = pts[0]
  const path = new Path2D()
  path.moveTo(px(0), py(0))
  for (let i = 1; i <= Math.ceil(upto); i++) {
    const u = Math.min(1, upto - (i - 1))
    const q = pts[i - 1], w = pts[i]
    tip = { x: lerp(q.x, w.x, u), y: lerp(q.y, w.y, u) }
    path.lineTo(px(tip.x), py(tip.y))
  }
  const tw = m.palmW * scale * (0.5 + 0.5 * t)
  stroke(ctx, path, col.trunk, Math.max(1, tw), 'round')
  const ring = col.trunkDark ?? col.trunk
  for (let i = 2; i < Math.floor(upto); i++) {
    const q = pts[i], x = px(q.x), y = py(q.y), hw = tw * 0.5
    line(ctx, ring, x - hw, y + 1, x + hw, y - 1, Math.max(0.6, scale * 0.005))
  }
  const tx = px(tip.x), ty = py(tip.y)
  for (const fr of m.fronds) {
    const f = frac(t, fr.birth, 0.3)
    if (f <= 0) continue
    const l = fr.len * scale * f * (0.45 + 0.55 * t)
    const a = rad(fr.a)
    const ex = tx + Math.cos(a) * l, ey = ty - Math.sin(a) * l * 0.7 + fr.droop * l
    const cx = tx + Math.cos(a) * l * 0.5, cy = ty - Math.sin(a) * l * 0.7 - l * 0.12
    const c = fr.dark ? col.leafDark : col.leaf
    const p = new Path2D()
    p.moveTo(tx, ty)
    p.quadraticCurveTo(cx, cy, ex, ey)
    stroke(ctx, p, c, Math.max(1, scale * 0.006))
    const lw = Math.max(0.7, scale * 0.0045)
    const cs = Math.sign(Math.cos(a) === 0 ? 1 : Math.cos(a))
    for (let k = 2; k <= 12; k++) {
      const u = k / 13
      const bx = (1 - u) * (1 - u) * tx + 2 * (1 - u) * u * cx + u * u * ex
      const by = (1 - u) * (1 - u) * ty + 2 * (1 - u) * u * cy + u * u * ey
      const ll = l * 0.2 * Math.sin(u * Math.PI) + l * 0.03
      for (const sd of [-1, 1]) {
        const aa = a + sd * 1.1 - 0.3 * cs
        line(ctx, c, bx, by, bx + Math.cos(aa) * ll * 0.6, by + Math.abs(Math.sin(aa)) * ll * 0.9 + ll * 0.3, lw)
      }
    }
  }
  m.palmTip = tip
}

function perchPoint(m: Model, i: number): [number, number] {
  const p = m.perches[(i * 7) % m.perches.length]
  const [x, y] = polyAt(p.seg.pts, p.pos)
  return [x, y]
}

const ease = (lf: number) => 1 - Math.pow(1 - lf, 3)
const clamp01 = (x: number) => Math.min(1, Math.max(0, x))

function drawFinale(ctx: Ctx, sp: TreeSpecies, m: Model, fin: number, px: (x: number) => number, py: (y: number) => number, scale: number, col: TreeColors, sc: SceneColors) {
  switch (sp.finale) {
    case 'BIRDS_NEST': case 'CEDAR_BIRDS': birdsIn(ctx, m, fin, 3, true, px, py, scale, sc); break
    case 'PALM_BIRDS': birdsIn(ctx, m, fin, 2, false, px, py, scale, sc); sparkle(ctx, m, fin, '#E8B931', px, py, scale); break
    case 'DOVE': {
      if (!m.perches.length) return
      const lf = clamp01(fin * 1.3)
      const [qx, qy] = perchPoint(m, 1)
      const tx = px(qx), ty = py(qy)
      const e = ease(lf)
      const x = lerp(tx - scale * 0.9, tx, e)
      const y = lerp(ty - scale * 0.5, ty, e) - Math.sin(e * Math.PI) * scale * 0.06
      const s = scale * 0.065
      bird(ctx, x, y, s, fin * 30, 1, sc.white, '#C9D1D6', '#C98A2E', lf < 1)
      if (lf > 0.1) leaf(ctx, x + s * 0.8, y - s * 0.7, -20, s * 0.9, 'ELLIPSE', 0.25, col.leafDark)
      break
    }
    case 'FIGS': {
      const ripe = col.ripe
      if (!ripe) return
      const a = clamp01(fin * 1.5)
      for (const fr of m.fruits) oval(ctx, ripe, px(fr.x), py(fr.y) + fr.r * scale * 0.2, fr.r * scale, fr.r * scale * 1.05, 0, a)
      break
    }
    case 'PETALS': {
      const r = new Rng(3)
      const c = col.flower
      if (!c) return
      for (let i = 0; i < 14; i++) {
        const fx = (r.next() - 0.5) * 0.8, fy0 = 0.3 + r.next() * 0.5, fall = (fin * 0.6 + r.next()) % 1
        const a = clamp01(fin * 3) * (1 - fall * 0.6)
        oval(ctx, c, px(fx + Math.sin(fall * 6 + i) * 0.03), py(fy0 - fall * fy0), scale * 0.008, scale * 0.005, fall * 5, a)
      }
      break
    }
    case 'SPARKLE_WHITE': sparkle(ctx, m, fin, '#FFFFFF', px, py, scale); break
    case 'SPARKLE_GOLD': sparkle(ctx, m, fin, '#F2C94C', px, py, scale); break
    case 'SPARKLE_PINK': sparkle(ctx, m, fin, '#E7A6C0', px, py, scale); break
    case 'TENT': {
      const a = clamp01(fin * 1.5)
      const x = px(0.34), y = py(0), w = scale * 0.13 * a, h = scale * 0.1 * a
      const p1 = new Path2D(); p1.moveTo(x - w, y); p1.lineTo(x, y - h); p1.lineTo(x + w, y); p1.closePath()
      fill(ctx, p1, sc.dark ? '#8C7458' : '#B79A73')
      const p2 = new Path2D(); p2.moveTo(x - w * 0.25, y); p2.lineTo(x, y - h * 0.62); p2.lineTo(x + w * 0.25, y); p2.closePath()
      fill(ctx, p2, sc.dark ? '#3C3227' : '#6E5A41')
      break
    }
    case 'ZACCHAEUS': {
      const a = clamp01(fin * 1.4)
      if (a <= 0 || !m.perches.length) return
      const [qx, qy] = perchPoint(m, 0)
      const x = px(qx), y = py(qy), s = scale * 0.03
      const body = sc.dark ? '#D7B898' : '#8B5E3C'
      circle(ctx, body, x, y - s * 2.1, s * 0.55, a)
      const p = new Path2D(); p.moveTo(x - s * 0.7, y); p.quadraticCurveTo(x, y - s * 2.2, x + s * 0.7, y); p.closePath()
      fill(ctx, p, body, a)
      ctx.globalAlpha = a
      ctx.fillStyle = sc.dark ? '#C9A23A' : '#B8860B'
      ctx.fillRect(x - s * 0.75, y - s * 1.2, s * 1.5, s * 0.25)
      ctx.globalAlpha = 1
      break
    }
  }
}

function birdsIn(ctx: Ctx, m: Model, fin: number, count: number, nest: boolean, px: (x: number) => number, py: (y: number) => number, scale: number, sc: SceneColors) {
  const isPalm = m.palmPts !== null
  if (!m.perches.length && !isPalm) return
  for (let i = 0; i < count; i++) {
    const lf = clamp01(fin * 1.6 - i * 0.2)
    if (lf <= 0) continue
    const [tx, ty] = isPalm ? [px(m.palmTip.x + (i - 1) * 0.12), py(m.palmTip.y - 0.02)] : (([x, y]) => [px(x), py(y)])(perchPoint(m, i))
    const sx = tx + (i % 2 === 1 ? 1 : -1) * scale * 0.9
    const sy = ty - scale * 0.55
    const e = ease(lf)
    const x = lerp(sx, tx, e)
    const y = lerp(sy, ty, e) - Math.sin(e * Math.PI) * scale * 0.08
    const sz = scale * 0.055
    if (nest && i === 0 && lf >= 1) oval(ctx, sc.trunkDark, tx, ty + sz * 0.1, sz * 0.9, sz * 0.38)
    bird(ctx, x, y, sz, fin * 40 + i, i % 2 === 1 ? -1 : 1, sc.bird, sc.birdWing, sc.blossom, lf < 1)
  }
}

function sparkle(ctx: Ctx, m: Model, fin: number, color: string, px: (x: number) => number, py: (y: number) => number, scale: number) {
  const pts = [...m.flowers, ...m.fruits]
  if (!pts.length) return
  const k = Math.min(pts.length, 14)
  for (let i = 0; i < k; i++) {
    const q = pts[(i * 5) % pts.length]
    const x = px(q.x), y = py(q.y)
    const a = clamp01(fin * 2 - i / k) * (0.5 + 0.5 * Math.sin(fin * 12 + i)) * 0.8
    const r = scale * 0.022
    line(ctx, color, x - r, y, x + r, y, 1.2, a)
    line(ctx, color, x, y - r, x, y + r, 1.2, a)
  }
}
