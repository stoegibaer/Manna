import { store } from '../data/store.svelte.ts'
import { playSound } from '../data/types.ts'

/**
 * Sound feedback, respecting the user's settings. Wrong answers get only a soft, non-punishing cue.
 * (Safari on the iPhone cannot vibrate, so there is no haptic feedback on the web.)
 * Web Audio only starts after a touch – the context is created and resumed on the first tap.
 */
const BASE = import.meta.env.BASE_URL + 'sounds/'
let ctx: AudioContext | null = null
const buffers = new Map<string, AudioBuffer>()

function context(): AudioContext | null {
  if (ctx) return ctx
  const AC = window.AudioContext ?? (window as unknown as { webkitAudioContext?: typeof AudioContext }).webkitAudioContext
  if (!AC) return null
  ctx = new AC()
  for (const name of ['chime_ok', 'chime_done', 'chime_soft']) {
    fetch(BASE + name + '.wav')
      .then((r) => r.arrayBuffer())
      .then((b) => ctx!.decodeAudioData(b))
      .then((buf) => buffers.set(name, buf))
      .catch(() => {})
  }
  return ctx
}

/** Call once at startup: unlocks audio on the first touch (iOS). */
export function unlockAudioOnFirstTouch() {
  const unlock = () => {
    const c = context()
    if (c && c.state !== 'running') void c.resume()
  }
  document.addEventListener('pointerdown', unlock, { capture: true })
  document.addEventListener('keydown', unlock, { capture: true })
}

function play(name: string, volume: number) {
  if (!playSound(store.settings)) return
  const c = context()
  const buf = buffers.get(name)
  if (!c || !buf) return
  if (c.state !== 'running') void c.resume()
  const src = c.createBufferSource()
  const gain = c.createGain()
  gain.gain.value = volume
  src.buffer = buf
  src.connect(gain).connect(c.destination)
  src.start()
}

export const feedback = {
  correct: () => play('chime_ok', 0.7),
  tryAgain: () => play('chime_soft', 0.4),
  sectionDone: () => play('chime_done', 0.8),
  tick: () => {},
}
