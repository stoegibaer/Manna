<script lang="ts">
  import { onDestroy, untrack } from 'svelte'
  import Icon from '../../lib/components/Icon.svelte'
  import VerseText from '../../lib/components/VerseText.svelte'
  import { Speaker, canSpeak } from '../../lib/audio/speaker.svelte.ts'
  import { feedback } from '../../lib/audio/feedback.ts'
  import { store } from '../../lib/data/store.svelte.ts'
  import type { Session } from './session.svelte.ts'

  let { s, onmap }: { s: Session; onmap: () => void } = $props()

  const section = $derived(s.section!)
  const focusMode = $derived(store.settings.focusMode)
  /** Line indices of the verses (headers are skipped by the focus). */
  const verseLines = $derived(s.lines.flatMap((l, i) => (l.kind === 'verse' ? [i] : [])))
  let focus = $state(0)
  const atEnd = $derived(!focusMode || focus >= verseLines.length - 1)
  const favorites = $derived(store.favoriteKeys())
  const speaker = new Speaker()
  onDestroy(() => speaker.stop())

  function scrollToLine(i: number) {
    const el = document.querySelector(`[data-line="${i}"]`)
    if (!el) return
    const top = el.getBoundingClientRect().top + window.scrollY - 76
    window.scrollTo({ top, behavior: store.settings.calm ? 'auto' : 'smooth' })
  }

  // while reading aloud, the focus follows the voice
  $effect(() => {
    const sp = speaker.current
    if (sp < 0) return
    if (focusMode) focus = Math.max(untrack(() => focus), sp)
    else scrollToLine(verseLines[sp])
  })

  // keep the previous line visible above the current verse
  $effect(() => {
    if (focusMode && focus > 0) scrollToLine(verseLines[focus] - 1)
  })

  function advance() {
    if (focusMode && focus < verseLines.length - 1) { focus++; feedback.tick() }
  }

  function opacity(pos: number) {
    if (!focusMode || pos === focus) return 1
    return pos < focus ? 0.5 : 0.16
  }
</script>

<div class="read" onclick={advance} role="presentation">
  <div class="head stack-8">
    {#if section.bridge}
      <div class="stack-4" style="padding-bottom:10px">
        <p class="t-lm secondary">Was dazwischen geschah</p>
        <p class="t-bl serif italic muted">{section.bridge}</p>
      </div>
    {/if}
    <h2 class="t-hm">{section.title}</h2>
    <div class="row wrap" style="gap:6px">
      <span class="t-bm muted">{s.refLabel} · ca. {s.minutes} Min.</span>
      {#if s.place}
        <button class="pill" onclick={(e) => { e.stopPropagation(); onmap() }}>
          <Icon name="place" size={16} color="var(--primary)" />{s.place.name}
        </button>
      {/if}
    </div>
    {#if canSpeak}
      <button class="pill" class:on={speaker.playing} style="align-self:flex-start"
        onclick={(e) => { e.stopPropagation(); speaker.toggle(s.verses, focusMode ? focus : 0) }}>
        <Icon name={speaker.playing ? 'stop' : 'volume'} size={18} color="var(--primary)" />{speaker.playing ? 'Stopp' : 'Vorlesen'}
      </button>
    {/if}
    {#if section.focus}
      <div class="hint t-bl" style="margin-top:6px">{section.focus}</div>
    {/if}
  </div>

  {#each s.lines as line, i (i)}
    <div data-line={i}>
      {#if line.kind === 'header'}
        <p class="t-ll primary" style="padding-top:10px">{line.label}</p>
      {:else}
        {@const pos = verseLines.indexOf(i)}
        {@const v = line.verse}
        <VerseText
          verse={v}
          opacity={opacity(pos)}
          highlighted={!focusMode && pos === speaker.current}
          favorite={favorites.has(`${v.book}-${v.chapter}-${v.verse}`)}
          ontap={advance}
          onlongpress={() => { s.toggleFavorite(v); feedback.correct() }}
        />
      {/if}
    </div>
  {/each}
</div>

<div class="cta">
  {#if atEnd}
    <button class="btn enter" onclick={() => { speaker.stop(); s.finishReading() }}>Fertig gelesen</button>
  {:else}
    <p class="tap muted center" onclick={advance} role="presentation">Tippe irgendwo, um weiterzulesen</p>
  {/if}
</div>

<style>
  .read { padding: 8px 24px 140px; display: flex; flex-direction: column; gap: 10px; min-height: 70dvh; }
  .head { padding-bottom: 12px; }
  .wrap { flex-wrap: wrap; }
  .cta {
    position: fixed; left: 0; right: 0; bottom: 0; z-index: 4; margin: 0 auto; max-width: var(--page-max);
    padding: 16px 24px calc(16px + var(--safe-bottom)); background: var(--background);
  }
  .tap { height: 56px; margin: 0; padding-top: 16px; }
</style>
