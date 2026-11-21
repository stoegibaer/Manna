import type { Verse } from '../data/content.ts'
import { store } from '../data/store.svelte.ts'

const synth: SpeechSynthesis | null = typeof speechSynthesis !== 'undefined' ? speechSynthesis : null

export const canSpeak = synth !== null

function germanVoice(): SpeechSynthesisVoice | null {
  const voices = synth?.getVoices() ?? []
  return voices.find((v) => v.lang === 'de-DE' && v.localService) ?? voices.find((v) => v.lang.toLowerCase().startsWith('de')) ?? null
}

/**
 * Reads verses aloud with the device's voice and reports the verse currently spoken (for highlighting).
 * One utterance per verse, with a short breath in between – like the Android app.
 */
export class Speaker {
  /** Index into the verse list being read, -1 when idle. */
  current = $state(-1)
  playing = $state(false)

  private verses: Verse[] = []
  private timer: ReturnType<typeof setTimeout> | undefined
  private run = 0
  /** Safari drops utterances that are garbage-collected while speaking – keep a reference. */
  private utterance: SpeechSynthesisUtterance | null = null

  play(list: Verse[], from = 0) {
    this.stop()
    this.verses = list
    if (!list.length || !synth) return
    this.playing = true
    this.playAt(Math.min(Math.max(from, 0), list.length - 1), ++this.run)
  }

  toggle(list: Verse[], from: number) {
    if (this.playing) this.stop()
    else this.play(list, from)
  }

  private playAt(i: number, run: number) {
    if (!this.playing || run !== this.run || !synth) return
    if (i >= this.verses.length) { this.finish(); return }
    this.current = i
    const u = new SpeechSynthesisUtterance(this.verses[i].text)
    u.lang = 'de-DE'
    const voice = germanVoice()
    if (voice) u.voice = voice
    u.rate = store.settings.ttsRate
    u.onend = () => { if (run === this.run) this.timer = setTimeout(() => this.playAt(i + 1, run), 250) }
    u.onerror = (e) => {
      if (run !== this.run) return
      if (e.error === 'interrupted' || e.error === 'canceled') return
      this.timer = setTimeout(() => this.playAt(i + 1, run), 50)
    }
    this.utterance = u
    synth.speak(u)
  }

  private finish() {
    this.playing = false
    this.current = -1
  }

  stop() {
    this.run++
    clearTimeout(this.timer)
    this.playing = false
    this.current = -1
    this.utterance = null
    synth?.cancel()
  }
}
