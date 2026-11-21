import { CITY_STEPS, LIFE, TREES, progress } from '../data/garden.ts'
import { Rng } from '../util/random.ts'
import { circle, drawTree, line, type SceneColors } from './treeDraw.ts'
import { ALL, LIFE_FRUITS, LIFE_TREE, treeById } from './trees.ts'

type Ctx = CanvasRenderingContext2D

/*
 * The garden as seen on the home screen (port of ui/garden/GardenScene.kt). All positions are
 * fractions of the scene's width/height (the scene is 1 : 1.02).
 */

/** Height : width of the garden scene. */
export const SCENE_ASPECT = 1.02
const HORIZON = 0.24

/** [x, y, size] per garden place, in the order in which they are filled. */
const SLOTS: [number, number, number][] = [
  [0.16, 0.961, 0.69], [0.7, 0.579, 0.46], [0.32, 0.645, 0.57], [0.882, 0.798, 0.68],
  [0.091, 0.628, 0.48], [0.922, 0.495, 0.46], [0.383, 0.459, 0.39], [0.608, 0.409, 0.36],
  [0.177, 0.396, 0.44], [0.803, 0.362, 0.38], [0.296, 0.286, 0.43], [0.676, 0.275, 0.46],
]
/** The growing tree in front … */
const FRONT: [number, number, number] = [0.516, 0.98, 0.55]
/** … and the tree of life, which grows at the water and stays there. */
const LIFE_PLACE: [number, number, number] = [0.513, 0.979, 0.9]

/** Center line of the river: from the source at the horizon to the front right. */
const RIVER: [number, number][] = [[0.5, 0.262], [0.505, 0.34], [0.49, 0.44], [0.5, 0.55], [0.575, 0.66], [0.68, 0.78], [0.75, 0.9], [0.79, 1.03]]

function riverPt(u: number): [number, number] {
  const n = RIVER.length - 1
  const x = Math.min(1, Math.max(0, u)) * n
  const i = Math.min(n - 1, Math.floor(x))
  const f = x - i
  const p0 = RIVER[Math.max(0, i - 1)], p1 = RIVER[i], p2 = RIVER[i + 1], p3 = RIVER[Math.min(n, i + 2)]
  const cr = (a: number, b: number, c: number, d: number) => 0.5 * (2 * b + (-a + c) * f + (2 * a - 5 * b + 4 * c - d) * f * f + (-a + 3 * b - 3 * c + d) * f * f * f)
  return [cr(p0[0], p1[0], p2[0], p3[0]), cr(p0[1], p1[1], p2[1], p3[1])]
}

/** Hes 47,3–5: the water gets deeper with every grown tree. */
function riverStage(done: number): { reach: number; w: number } | null {
  const k = Math.min(done, TREES)
  if (k <= 0) return null
  const f = (k - 1) / 11
  return { reach: Math.min(1, 0.16 + 0.84 * Math.pow(f, 0.7)), w: 0.007 + 0.078 * Math.pow(f, 1.2) }
}

/** After 36 fruits every fruit changes in turn to the fruit of the next „month“. */
export function lifeFruitColor(n: number): (k: number) => string {
  return (k) => {
    const extra = n - CITY_STEPS
    const g = extra > k ? Math.floor((extra - 1 - k) / CITY_STEPS) + 1 : 0
    return LIFE_FRUITS[(k + g * 5) % 12]
  }
}

// ── the golden city (Offb 21): comes down from heaven with every fruit ──

const STONES = [0x7fb89a, 0x3e64b5, 0x8fa9b8, 0x2e9e6a, 0xc8644a, 0xb0303a, 0xc9c04a, 0x5fb5b0, 0xe0a030, 0x8ccb6a, 0x5a6fd0, 0x8e5bb5].map((v) => '#' + v.toString(16).padStart(6, '0'))

const BUILDINGS = (() => {
  const r = new Rng(42)
  return Array.from({ length: 12 }, (_, i) => {
    const side = i % 2 === 1 ? 1 : -1
    const rank = Math.ceil(i / 2)
    const x = side * rank * 0.07 + (i === 0 ? 0 : (r.next() - 0.5) * 0.02)
    const wd = 0.075 + r.next() * 0.03
    const ht = 1 - rank * 0.13 - r.next() * 0.08
    return { x, wd, ht, dome: r.next() < 0.4 }
  })
})()

const GOLD_LIGHT = '#F7DA7C'
const GOLD_DARK = '#D9A520'

function drawCity(ctx: Ctx, w: number, h: number, fruits: number, sc: SceneColors) {
  if (fruits <= 0) return
  const p = Math.min(1, Math.max(0, fruits / CITY_STEPS))
  const cx = 0.5 * w, cw = 0.42 * w, base = 0.264 * h, fh = 0.014 * h, wallH = 0.05 * h, cityH = 0.2 * h
  const al = 0.1 + 0.9 * p
  ctx.save()
  ctx.translate(0, -(1 - p) * 0.045 * h)
  // its radiance (21,11.23)
  const glow = ctx.createRadialGradient(cx, base - cityH * 0.5, 0, cx, base - cityH * 0.5, cw * 0.95)
  glow.addColorStop(0, `rgba(247,218,124,${0.6 * p * al})`)
  glow.addColorStop(1, 'rgba(247,218,124,0)')
  ctx.fillStyle = glow
  ctx.fillRect(cx - cw, base - cityH * 2.2, 2 * cw, cityH * 2.6)
  ctx.globalAlpha = al
  // golden buildings (21,18)
  for (let i = BUILDINGS.length - 1; i >= 0; i--) {
    const b = BUILDINGS[i]
    const bw = b.wd * cw, bh = b.ht * cityH
    const bx = cx + b.x * cw - bw / 2, by = base - fh - bh
    const g = ctx.createLinearGradient(bx, 0, bx + bw, 0)
    g.addColorStop(0, GOLD_LIGHT)
    g.addColorStop(1, GOLD_DARK)
    ctx.fillStyle = g
    ctx.fillRect(bx, by, bw, bh)
    if (b.dome) {
      ctx.beginPath()
      ctx.moveTo(bx + bw / 2, by)
      ctx.arc(bx + bw / 2, by, bw / 2, Math.PI, 2 * Math.PI)
      ctx.closePath()
      ctx.fill()
    }
    ctx.fillStyle = 'rgba(255,250,230,0.7)'
    for (let k = 0; k < 3; k++) ctx.fillRect(bx + bw * (0.2 + k * 0.25), by + bh * 0.25, bw * 0.1, bh * 0.25)
  }
  // jasper wall with twelve pearl gates (21,12.18.21)
  ctx.fillStyle = '#A9D9C4'
  ctx.fillRect(cx - cw / 2, base - fh - wallH, cw, wallH)
  ctx.fillStyle = '#CDEBDD'
  ctx.fillRect(cx - cw / 2, base - fh - wallH, cw, Math.max(1, wallH * 0.12))
  for (let i = 0; i < 12; i++) {
    const gx = cx - cw / 2 + ((i + 0.5) * cw) / 12, gw = (cw / 12) * 0.46, gh = wallH * 0.72
    ctx.beginPath()
    ctx.moveTo(gx - gw / 2, base - fh)
    ctx.lineTo(gx - gw / 2, base - fh - gh + gw / 2)
    ctx.ellipse(gx, base - fh - gh + gw / 2, gw / 2, gw / 2, 0, Math.PI, 2 * Math.PI)
    ctx.lineTo(gx + gw / 2, base - fh)
    ctx.closePath()
    ctx.fillStyle = '#F6F1E7'
    ctx.fill()
    ctx.fillStyle = 'rgba(200,190,170,0.55)'
    ctx.fillRect(gx - gw * 0.08, base - fh - gh * 0.75, gw * 0.16, gh * 0.75)
  }
  // twelve foundation stones (21,19–20)
  for (let i = 0; i < 12; i++) {
    const x = cx - cw / 2 + (i * cw) / 12 + 0.5
    ctx.fillStyle = STONES[i]
    ctx.fillRect(x, base - fh, cw / 12 - 1, fh)
    ctx.fillStyle = 'rgba(255,255,255,0.35)'
    ctx.fillRect(x, base - fh, cw / 12 - 1, fh * 0.3)
  }
  ctx.globalAlpha = 1
  // clouds while it comes down (21,2)
  if (p < 1) for (let k = -3; k <= 3; k++) {
    const rx = cw * 0.13, ry = 0.02 * h, ox = cx + k * cw * 0.15, oy = base + 0.004 * h
    ctx.globalAlpha = (1 - p) * 0.9
    ctx.fillStyle = sc.white
    ctx.beginPath()
    ctx.ellipse(ox, oy, rx, ry, 0, 0, 2 * Math.PI)
    ctx.fill()
  }
  ctx.restore()
  ctx.globalAlpha = 1
}

function drawRiver(ctx: Ctx, w: number, h: number, done: number, sc: SceneColors) {
  const st = riverStage(done)
  if (!st) return
  const n = 90
  const mid = Array.from({ length: n + 1 }, (_, i) => {
    const u = (st.reach * i) / n
    const [x, y] = riverPt(u)
    const [x2, y2] = riverPt(Math.min(1, u + 0.004))
    let nx = -(y2 - y) * h, ny = (x2 - x) * w
    const ln = Math.hypot(nx, ny) || 1
    nx /= ln; ny /= ln
    const tip = Math.min(1, (st.reach - u) / 0.04 + 0.1)
    const hw = w * st.w * (0.12 + (y - HORIZON) / 0.6) * Math.sqrt(Math.max(0, tip))
    return { x: x * w, y: y * h, hw, nx, ny }
  })
  const band = (grow: number, color: string) => {
    ctx.beginPath()
    mid.forEach((m, i) => {
      const k = m.hw + grow * (0.5 + m.y / h)
      if (i === 0) ctx.moveTo(m.x + m.nx * k, m.y + m.ny * k)
      else ctx.lineTo(m.x + m.nx * k, m.y + m.ny * k)
    })
    for (let i = mid.length - 1; i >= 0; i--) {
      const m = mid[i], k = m.hw + grow * (0.5 + m.y / h)
      ctx.lineTo(m.x - m.nx * k, m.y - m.ny * k)
    }
    ctx.closePath()
    ctx.fillStyle = color
    ctx.fill()
  }
  band(w * Math.min(0.012, 0.004 + st.w * 0.15), sc.bank)
  band(0, sc.water)
  // light current lines – more of them the wider it gets
  const lanes = done <= 2 ? 1 : done <= 6 ? 2 : 3
  for (let j = 0; j < lanes; j++) {
    const off = lanes === 1 ? 0 : (j / (lanes - 1) - 0.5) * 0.9
    for (let i = 3 + j * 4; i < n - 3; i += 11) {
      const a = mid[i], b = mid[i + 4]
      line(ctx, sc.water2, a.x + a.nx * a.hw * off, a.y + a.ny * a.hw * off, b.x + b.nx * b.hw * off, b.y + b.ny * b.hw * off, Math.max(0.8, w * 0.005 * (a.y / h)))
    }
  }
  // reeds from the brook on
  if (done >= 3) {
    const r = new Rng(5)
    const tall = 0.6 + Math.min(done, TREES) / 12
    for (let i = 10; i < n; i += 6) {
      const m = mid[i]
      if (r.next() >= 0.5) {
        const sd = r.next() < 0.5 ? 1 : -1
        const k = m.hw + w * 0.012
        const bx = m.x + sd * m.nx * k, by = m.y + sd * m.ny * k, s = m.y / h
        for (let q = -1; q <= 1; q++) {
          line(ctx, sc.reed, bx + q * w * 0.006 * s, by, bx + q * w * 0.011 * s, by - h * (0.03 + 0.008 * (q & 1)) * s * tall, Math.max(0.7, w * 0.003 * s))
        }
      }
    }
  }
  // the source
  const [sx, sy] = RIVER[0]
  const rx = w * (0.012 + st.w * 0.5), ry = h * (0.004 + st.w * 0.06)
  ctx.fillStyle = sc.water
  ctx.beginPath()
  ctx.ellipse(sx * w, sy * h, rx, ry, 0, 0, 2 * Math.PI)
  ctx.fill()
}

/**
 * Paints the whole garden into a w × h area at the origin.
 * [total] may be fractional while the front tree grows. [planted] = species by position.
 */
export function drawGarden(ctx: Ctx, w: number, h: number, total: number, planted: string[], sc: SceneColors) {
  const g = progress(total)
  const done = g.done
  // sky, far hills, meadow
  ctx.fillStyle = sc.sky
  ctx.fillRect(0, 0, w, h)
  ctx.beginPath()
  ctx.moveTo(0, h * HORIZON)
  for (let x = 0; x <= w; x += 4) {
    const f = x / w
    ctx.lineTo(x, h * HORIZON - (Math.sin(f * Math.PI * 2.1 + 0.7) * 0.012 + Math.sin(f * Math.PI) * 0.025 + 0.01) * h)
  }
  ctx.lineTo(w, h)
  ctx.lineTo(0, h)
  ctx.closePath()
  ctx.fillStyle = sc.hill2
  ctx.fill()
  ctx.fillStyle = sc.hill
  ctx.fillRect(0, h * (HORIZON + 0.012), w, h * (1 - HORIZON))
  drawCity(ctx, w, h, g.fruits, sc)
  drawRiver(ctx, w, h, done, sc)

  // garden trees, back to front
  const items = Array.from({ length: Math.min(done, TREES) }, (_, i) => i)
    .filter((i) => planted[i] !== undefined)
    .sort((a, b) => SLOTS[a][1] - SLOTS[b][1])
  for (const i of items) {
    const [x, y, s] = SLOTS[i]
    drawTree(ctx, treeById(planted[i]), 1, x * w, y * h, h * 0.5 * s, sc, { fin: 1, groundColor: sc.hill2, groundR: 0.2 })
  }
  // the growing tree in front; a seed while the next tree is not chosen yet
  const t = g.t
  if (done < TREES) {
    const [x, y, s] = FRONT
    const sp = planted[done] !== undefined ? treeById(planted[done]) : null
    const tt = sp ? Math.max(t, 0.0001) : 0
    drawTree(ctx, sp ?? ALL[0], tt, w * x, h * y, h * s * (1.3 - 0.3 * tt), sc, { groundColor: sc.ground, groundR: 0.17 })
  } else {
    const [x, y, s] = LIFE_PLACE
    const chosen = planted.includes(LIFE)
    const tt = done > TREES ? 1 : !chosen ? 0 : Math.max(t, 0.0001)
    drawTree(ctx, LIFE_TREE, tt, w * x, h * y, h * 0.5 * s * (1.3 - 0.3 * tt), sc, {
      groundColor: sc.ground, groundR: 0.17, fruitN: done > TREES ? g.fruits : 0, fruitColor: lifeFruitColor(g.fruits),
    })
  }
}

/** Name of the river stage for texts. */
export function riverName(done: number): string | null {
  const k = Math.min(done, TREES)
  if (k === 0) return null
  if (k <= 2) return 'eine Quelle, knöcheltief'
  if (k <= 5) return 'ein Bach, knietief'
  if (k <= 8) return 'ein Fluss, hüfttief'
  if (k <= 11) return 'ein Fluss, tief'
  return 'ein Strom'
}

export { circle }
