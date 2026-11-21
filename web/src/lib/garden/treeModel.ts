import { KotlinRandom, Rng } from '../util/random.ts'

/*
 * Procedural tree shapes (port of ui/garden/TreeModel.kt). Units: the root is at (0, 0), y points up,
 * a grown tree is about 1 high. Every element has a birth time in growth t (0..1), so a tree grows a
 * little with every section. Same random sequences as on Android → the same trees.
 */

export const rad = (d: number) => (d * Math.PI) / 180
export const lerp = (a: number, b: number, f: number) => a + (b - a) * f
export const frac = (t: number, birth: number, span: number) => Math.min(1, Math.max(0, (t - birth) / span))

export interface Pt { x: number; y: number }
export interface Seg { pts: Pt[]; w: number; birth: number; span: number; depth: number }
export interface Leaf { x: number; y: number; a: number; len: number; dark: boolean; birth: number; seg?: Seg; pos?: number }
export interface Clump { x: number; y: number; r: number; shade: number; birth: number; flat?: number }
export interface Dot { x: number; y: number; r: number; birth: number; seg?: Seg }
export interface Strand { x: number; y: number; len: number; sway: number; birth: number; dark: boolean }
export interface Perch { seg: Seg; pos: number }
export interface Frond { a: number; len: number; droop: number; birth: number; dark: boolean }

export class Model {
  segs: Seg[] = []
  leaves: Leaf[] = []
  clumps: Clump[] = []
  flowers: Dot[] = []
  fruits: Dot[] = []
  strands: Strand[] = []
  perches: Perch[] = []
  palmPts: Pt[] | null = null
  fronds: Frond[] = []
  palmW = 0
  /** Visible top of the palm trunk from the last draw (for the finale). */
  palmTip: Pt = { x: 0, y: 0 }
  private order: number[] | null = null

  /** Fruits in a scattered order, for ripening one after the other. */
  get fruitOrder(): number[] {
    if (!this.order) {
      const r = new Rng(91)
      this.order = this.fruits.map((_, i) => [r.next(), i] as const).sort((a, b) => a[0] - b[0]).map((p) => p[1])
    }
    return this.order
  }
}

/** Point and direction (degrees) at fraction [f] along a polyline. */
export function polyAt(pts: Pt[], f: number): [number, number, number] {
  const n = pts.length - 1
  const x = f * n
  const i = Math.min(n - 1, Math.floor(x))
  const u = x - i
  const a = pts[i], b = pts[i + 1]
  return [lerp(a.x, b.x, u), lerp(a.y, b.y, u), (Math.atan2(b.y - a.y, b.x - a.x) * 180) / Math.PI]
}

export interface Flower { p: number; r: number; from: number; spread?: number; along?: number }
export interface Fruit { p: number; r: number; from: number; hang?: number }

/** Parameters of the branching generator. */
export interface Branchy {
  seed: number; depth: number
  trunkLen?: number; trunkW?: number; trunkSpan?: number; trunkCurve?: number; curve?: number
  up?: number; droop?: number; droopFrom?: number; gnarl?: number; squash?: number
  leaf?: boolean; leafFrom?: number; leafCount?: number; leafLen?: number
  clumpAlong?: number; clumpFrom?: number; clumpR?: number
  strands?: number; strandFrom?: number; strandLen?: number; tipClump?: number
  flower?: Flower; fruit?: Fruit
  trunkKids?: number; kids?: number; extraKid?: number; atMin?: number
  spread?: [number, number]; mainJit?: number; lenF?: [number, number]; sideBoost?: number; wF?: number
  trunks?: number; lean?: number; trunkFan?: number
}

export function branchy(q: Branchy): Model {
  const p = {
    trunkLen: 0.3, trunkW: 0.05, trunkSpan: 0.12, trunkCurve: 20, curve: 16, up: 0, droop: 0, droopFrom: 2, gnarl: 0, squash: 0,
    leaf: false, leafFrom: 1, leafCount: 3, leafLen: 0.05, clumpAlong: 0, clumpFrom: 2, clumpR: 0.06,
    strands: 0, strandFrom: 0, strandLen: 0, tipClump: 0, trunkKids: 3, kids: 2, extraKid: 0.35, atMin: 0.55,
    spread: [18, 40] as [number, number], mainJit: 16, lenF: [0.68, 0.8] as [number, number], sideBoost: 1, wF: 0.68,
    trunks: 1, lean: 0, trunkFan: 14, flower: undefined as Flower | undefined, fruit: undefined as Fruit | undefined,
    ...q,
  }
  const r = new Rng(p.seed)
  const m = new Model()
  const maxD = p.depth
  const spanD = (0.86 - p.trunkSpan) / maxD

  const grow = (x: number, y: number, ang: number, len: number, depth: number, birth: number, span: number, w: number) => {
    const n = 7
    const pts: Pt[] = [{ x, y }]
    let a = ang, cx = x, cy = y
    const bend = (r.next() - 0.5) * (depth === 0 ? p.trunkCurve : p.curve)
    for (let k = 0; k < n; k++) {
      a += bend / n
      a += ((90 - a) * p.up) / n
      if (p.droop !== 0 && depth >= p.droopFrom) {
        const tgt = Math.cos(rad(a)) >= 0 ? -90 : 270
        a += ((tgt - a) * p.droop * (depth / maxD)) / n
      }
      if (p.gnarl !== 0 && depth <= 1) a += (r.next() - 0.5) * p.gnarl
      cx += (Math.cos(rad(a)) * len) / n
      cy += ((Math.sin(rad(a)) * len) / n) * (p.squash !== 0 && depth > 0 ? p.squash : 1)
      pts.push({ x: cx, y: cy })
    }
    const seg: Seg = { pts, w, birth, span, depth }
    m.segs.push(seg)
    if (depth === 1 || depth === 2) m.perches.push({ seg, pos: 0.55 + r.next() * 0.35 })
    if (p.leaf && depth >= p.leafFrom) {
      const cnt = Math.round(p.leafCount * (0.7 + r.next() * 0.6))
      for (let k = 0; k < cnt; k++) {
        const pos = 0.3 + r.next() * 0.7
        const [lx, ly, la] = polyAt(pts, pos)
        const la2 = la + (r.next() < 0.5 ? 1 : -1) * (35 + r.next() * 40)
        const l = p.leafLen * (0.75 + r.next() * 0.5) * (1 - depth * 0.03)
        const dark = r.next() < 0.4
        m.leaves.push({ x: lx, y: ly, a: la2, len: l, dark, birth: birth + span * pos + 0.02 + r.next() * 0.04 })
      }
    }
    if (p.clumpAlong > 0 && depth >= p.clumpFrom) {
      for (let k = 0; k < p.clumpAlong; k++) {
        const pos = 0.4 + r.next() * 0.6
        const [lx, ly] = polyAt(pts, pos)
        const qx = lx + (r.next() - 0.5) * 0.03
        const qy = ly + (r.next() - 0.3) * 0.03
        const rr = p.clumpR * (0.6 + r.next() * 0.5) * (1.15 - depth * 0.06)
        m.clumps.push({ x: qx, y: qy, r: rr, shade: r.next(), birth: birth + span * pos + 0.02 })
      }
    }
    if (p.strands > 0 && depth >= p.strandFrom) {
      for (let k = 0; k < p.strands; k++) {
        const pos = 0.4 + r.next() * 0.6
        const [lx, ly] = polyAt(pts, pos)
        const l = p.strandLen * (0.6 + r.next() * 0.6)
        const sway = (r.next() - 0.5) * 0.04
        m.strands.push({ x: lx, y: ly, len: l, sway, birth: birth + span * pos + 0.03, dark: r.next() < 0.45 })
      }
    }
    if (depth >= maxD) {
      const tip = pts[n]
      if (p.tipClump > 0) {
        const rr = p.tipClump * (0.7 + r.next() * 0.6)
        m.clumps.push({ x: tip.x, y: tip.y, r: rr, shade: r.next(), birth: birth + span * 0.8 })
      }
      const fl = p.flower
      if (fl && r.next() < fl.p) {
        const fx = tip.x + (r.next() - 0.5) * 0.02
        const fy = tip.y + (r.next() - 0.5) * 0.02
        const fr = fl.r * (0.8 + r.next() * 0.5)
        m.flowers.push({ x: fx, y: fy, r: fr, birth: Math.max(fl.from, birth + span) + r.next() * (fl.spread ?? 0.2) })
      }
      const fr = p.fruit
      if (fr && r.next() < fr.p) {
        const [fx, fy] = polyAt(pts, 0.5 + r.next() * 0.5)
        const rr = fr.r * (0.8 + r.next() * 0.4)
        m.fruits.push({ x: fx, y: fy - (fr.hang ?? 0.015), r: rr, birth: Math.max(fr.from, birth + span) + r.next() * 0.12 })
      }
      return
    }
    const fl = p.flower
    if (fl && (fl.along ?? 0) > 0 && depth >= (fl.along ?? 0)) {
      for (let k = 0; k < 2; k++) {
        if (r.next() < fl.p) {
          const [fx, fy] = polyAt(pts, 0.3 + r.next() * 0.7)
          const fr = fl.r * (0.7 + r.next() * 0.5)
          m.flowers.push({ x: fx, y: fy, r: fr, birth: Math.max(fl.from, birth + span) + r.next() * (fl.spread ?? 0.2) })
        }
      }
    }
    const kids = depth === 0 ? p.trunkKids : p.kids + (r.next() < p.extraKid ? 1 : 0)
    const side = r.next() < 0.5 ? 1 : -1
    for (let i = 0; i < kids; i++) {
      const at = i === 0 ? 1 : p.atMin + r.next() * (1 - p.atMin - 0.1)
      const [px, py, pa] = polyAt(pts, at)
      const spread = p.spread[0] + r.next() * (p.spread[1] - p.spread[0])
      const dir = i === 0 ? (r.next() - 0.5) * p.mainJit : (i % 2 === 1 ? side : -side) * spread
      const lf = p.lenF[0] + r.next() * (p.lenF[1] - p.lenF[0])
      grow(px, py, pa + dir, len * lf * (depth === 0 && i > 0 ? p.sideBoost : 1), depth + 1, birth + span * at, spanD, w * p.wF)
    }
  }

  for (let k = 0; k < p.trunks; k++) {
    const off = p.trunks === 1 ? 0 : (k - (p.trunks - 1) / 2) * 0.025
    const ang = 90 + (p.trunks === 1 ? p.lean : (k - (p.trunks - 1) / 2) * p.trunkFan)
    grow(off, 0, ang, p.trunkLen, 0, k * 0.02, p.trunkSpan, p.trunkW)
  }
  return m
}

export interface PalmParams { seed: number; height: number; lean: number; trunkW: number; fronds: number; frondLen: number; droop: number }

export function palm(p: PalmParams): Model {
  const r = new Rng(p.seed)
  const m = new Model()
  const n = 24
  const pts: Pt[] = [{ x: 0, y: 0 }]
  for (let i = 1; i <= n; i++) {
    const f = i / n
    pts.push({ x: Math.sin(f * 2.2) * p.lean * f + (r.next() - 0.5) * 0.002, y: f * p.height })
  }
  m.palmPts = pts
  m.palmW = p.trunkW
  for (let i = 0; i < p.fronds; i++) {
    const a = -40 + 260 * (i / (p.fronds - 1)) + (r.next() - 0.5) * 14
    const len = p.frondLen * (0.75 + r.next() * 0.4)
    const droop = p.droop * (0.7 + r.next() * 0.6)
    const birth = 0.04 + (i % 4) * 0.05 + r.next() * 0.1 + (Math.abs(a - 90) > 90 ? 0.25 : 0)
    m.fronds.push({ a, len, droop, birth, dark: r.next() < 0.5 })
  }
  return m
}

export interface CedarParams { seed: number; height: number; trunkW: number; tiers: number; span: number; sag: number; pad: number; flat: number }

/** A young, cone-shaped cedar in tiers. */
export function cedar(p: CedarParams): Model {
  const r = new Rng(p.seed)
  const m = new Model()
  const h = p.height
  m.segs.push({ pts: Array.from({ length: 8 }, (_, i) => ({ x: (r.next() - 0.5) * 0.004 * i, y: (h * i) / 7 })), w: p.trunkW, birth: 0, span: 0.75, depth: 0 })
  for (let k = 0; k < p.tiers; k++) {
    const f = 0.22 + (0.74 * k) / (p.tiers - 1)
    const y = h * f
    const birth = 0.75 * f * 0.92
    const widthF = (1 - f) * 0.9 + 0.1
    for (const s of [-1, 1]) {
      const l = p.span * widthF * (0.65 + r.next() * 0.55)
      const up = 6 + r.next() * 10
      const pts = Array.from({ length: 7 }, (_, i) => {
        const u = i / 6
        return { x: s * l * u, y: y + Math.sin(rad(up)) * l * u - p.sag * u * u }
      })
      const seg: Seg = { pts, w: p.trunkW * 0.38, birth, span: 0.18, depth: 2 }
      m.segs.push(seg)
      const pads = 3 + Math.round(l * 12)
      for (let j = 0; j < pads; j++) {
        const u = 0.25 + (0.75 * j) / Math.max(1, pads - 1)
        const [px, py] = polyAt(pts, u)
        m.clumps.push({ x: px, y: py + 0.012, r: p.pad * (0.75 + r.next() * 0.5) * (1 - u * 0.25), shade: r.next(), birth: birth + 0.18 * u + 0.02, flat: p.flat })
      }
      if (k > 0 && k < p.tiers - 1) m.perches.push({ seg, pos: 0.7 })
    }
  }
  m.clumps.push({ x: 0, y: h + 0.01, r: p.pad * 0.9, shade: 0.2, birth: 0.82, flat: p.flat })
  return m
}

/**
 * The mustard tree exactly as the app has always drawn it (seed 7),
 * so the first tree looks the same before and after it moves into the garden.
 */
export function mustard(): Model {
  const m = new Model()
  const rnd = new KotlinRandom(7)
  const grow = (x: number, y: number, angle: number, len: number, depth: number, birth: number, span: number) => {
    const r = rad(angle)
    const x1 = x + Math.cos(r) * len
    const y1 = y + Math.sin(r) * len
    const w = Math.max(0.05 * (1 - depth * 0.17), 0.008)
    const seg: Seg = { pts: [{ x, y }, { x: x1, y: y1 }], w, birth, span, depth }
    m.segs.push(seg)
    if (depth === 1 || depth === 2) m.perches.push({ seg, pos: 0.75 })
    if (depth >= 1) {
      const n = 2 + rnd.nextIntUntil(3)
      for (let k = 0; k < n; k++) {
        const pos = 0.35 + rnd.nextFloat() * 0.65
        const a = angle + (rnd.nextBoolean() ? 1 : -1) * (35 + rnd.nextFloat() * 40)
        const size = 0.035 + rnd.nextFloat() * 0.025 - depth * 0.002
        const b = birth + span * (0.4 + rnd.nextFloat() * 0.6) + 0.03
        const dark = rnd.nextFloat() < 0.4
        m.leaves.push({ x: x + (x1 - x) * pos, y: y + (y1 - y) * pos, a, len: size, dark, birth: b, seg, pos })
      }
    }
    if (depth >= 4 && rnd.nextFloat() < 0.45) {
      const b = Math.max(0.72, birth + span) + rnd.nextFloat() * 0.22
      const size = 0.012 + rnd.nextFloat() * 0.008
      m.flowers.push({ x: x1, y: y1, r: size, birth: b, seg })
    }
    if (depth >= 5) return
    const children = depth === 0 ? 3 : 2 + (rnd.nextFloat() < 0.35 ? 1 : 0)
    const side = rnd.nextBoolean() ? 1 : -1
    for (let i = 0; i < children; i++) {
      const at = i === 0 ? 1 : 0.55 + rnd.nextFloat() * 0.35
      const spread = 18 + rnd.nextFloat() * 22
      const dir = children === 1 ? 0 : i === 0 ? (rnd.nextFloat() - 0.5) * 16 : i % 2 === 1 ? side * spread : -side * spread
      grow(x + (x1 - x) * at, y + (y1 - y) * at, angle + dir, len * (0.68 + rnd.nextFloat() * 0.12), depth + 1, birth + span * at, 0.15)
    }
  }
  grow(0, 0, 90, 0.3, 0, 0, 0.12)
  return m
}
