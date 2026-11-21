/**
 * kotlin.random.Random(seed) (XorWow) – the same sequence as on Android, so the mustard tree
 * grows exactly like in the Android app.
 */
export class KotlinRandom {
  private x: number
  private y: number
  private z: number
  private w: number
  private v: number
  private addend: number

  constructor(seed: number) {
    const s1 = seed | 0
    const s2 = s1 >> 31
    this.x = s1
    this.y = s2
    this.z = 0
    this.w = 0
    this.v = ~s1
    this.addend = (s1 << 10) ^ (s2 >>> 4)
    for (let i = 0; i < 64; i++) this.nextInt()
  }

  nextInt(): number {
    let t = this.x
    t = t ^ (t >>> 2)
    this.x = this.y
    this.y = this.z
    this.z = this.w
    const v0 = this.v
    this.w = v0
    t = t ^ (t << 1) ^ v0 ^ (v0 << 4)
    this.v = t | 0
    this.addend = (this.addend + 362437) | 0
    return (t + this.addend) | 0
  }

  private nextBits(bitCount: number): number {
    return (this.nextInt() >>> (32 - bitCount)) & (-bitCount >> 31)
  }

  nextFloat(): number {
    return this.nextBits(24) / 16777216
  }

  nextBoolean(): boolean {
    return this.nextBits(1) !== 0
  }

  /** nextInt(until) for 0 < until. */
  nextIntUntil(n: number): number {
    if ((n & -n) === n) return this.nextBits(31 - Math.clz32(n))
    let bits: number
    let v: number
    do {
      bits = this.nextInt() >>> 1
      v = bits % n
    } while (((bits - v + (n - 1)) | 0) < 0)
    return v
  }
}

/** xorshift32 – the generator of the garden's tree shapes (ui/garden/TreeModel.kt). */
export class Rng {
  private s: number
  constructor(seed: number) {
    const s = Math.imul(seed, 2654435761 | 0)
    this.s = s === 0 ? 1 : s
  }
  next(): number {
    let s = this.s
    s ^= s << 13
    s ^= s >>> 17
    s ^= s << 5
    this.s = s
    return (s >>> 0) / 4294967296
  }
}

/** Java's String.hashCode, for stable per-question shuffles. */
export function hashCode(s: string): number {
  let h = 0
  for (let i = 0; i < s.length; i++) h = (Math.imul(31, h) + s.charCodeAt(i)) | 0
  return h
}

/** Deterministic shuffle (same order every time for the same seed). */
export function shuffled<T>(list: readonly T[], seed: number): T[] {
  const r = new Rng(seed)
  const a = list.slice()
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(r.next() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}
