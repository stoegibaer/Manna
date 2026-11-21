import { untrack } from 'svelte'

/** Cubic bezier easing (like Compose's CubicBezierEasing). */
function bezier(x1: number, y1: number, x2: number, y2: number) {
  const a = (a1: number, a2: number) => 1 - 3 * a2 + 3 * a1
  const b = (a1: number, a2: number) => 3 * a2 - 6 * a1
  const c = (a1: number) => 3 * a1
  const at = (t: number, a1: number, a2: number) => ((a(a1, a2) * t + b(a1, a2)) * t + c(a1)) * t
  const slope = (t: number, a1: number, a2: number) => 3 * a(a1, a2) * t * t + 2 * b(a1, a2) * t + c(a1)
  return (x: number) => {
    if (x <= 0 || x >= 1) return x
    let t = x
    for (let i = 0; i < 8; i++) {
      const s = slope(t, x1, x2)
      if (s === 0) break
      t -= (at(t, x1, x2) - x) / s
    }
    return at(t, y1, y2)
  }
}

export const FastOutSlowIn = bezier(0.4, 0, 0.2, 1)
export const Linear = (x: number) => x

/** An animated number (like Compose's Animatable). */
export class Anim {
  value = $state(0)
  private frame = 0

  constructor(initial: number) {
    this.value = initial
  }

  snapTo(v: number) {
    cancelAnimationFrame(this.frame)
    this.value = v
  }

  animateTo(target: number, ms: number, easing: (x: number) => number = FastOutSlowIn): Promise<void> {
    cancelAnimationFrame(this.frame)
    // read without tracking, so an effect that starts the animation does not re-run on every frame
    const from = untrack(() => this.value)
    if (ms <= 0 || from === target) { this.value = target; return Promise.resolve() }
    const start = performance.now()
    return new Promise((resolve) => {
      const step = (now: number) => {
        const f = Math.min(1, (now - start) / ms)
        this.value = from + (target - from) * easing(f)
        if (f < 1) this.frame = requestAnimationFrame(step)
        else resolve()
      }
      this.frame = requestAnimationFrame(step)
    })
  }

  stop() {
    cancelAnimationFrame(this.frame)
  }
}
