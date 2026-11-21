<script lang="ts">
  import Icon from './Icon.svelte'
  import type { Verse } from '../data/content.ts'

  /**
   * One verse with a small verse number. Long-press saves it as a favorite (bookmark at the end);
   * [highlighted] marks the verse that is being read aloud.
   */
  let { verse, opacity = 1, highlighted = false, favorite = false, ontap, onlongpress, dim = false }: {
    verse: Verse; opacity?: number; highlighted?: boolean; favorite?: boolean; dim?: boolean
    ontap?: () => void; onlongpress?: () => void
  } = $props()

  let timer: ReturnType<typeof setTimeout> | undefined
  let start: { x: number; y: number } | null = null
  let longFired = false

  function down(e: PointerEvent) {
    longFired = false
    start = { x: e.clientX, y: e.clientY }
    clearTimeout(timer)
    timer = setTimeout(() => { longFired = true; onlongpress?.() }, 520)
  }
  function move(e: PointerEvent) {
    if (start && Math.hypot(e.clientX - start.x, e.clientY - start.y) > 10) { clearTimeout(timer); start = null }
  }
  function up() { clearTimeout(timer) }
  function click(e: MouseEvent) {
    if (longFired) { e.stopPropagation(); longFired = false; return }
    if (ontap) { e.stopPropagation(); ontap() }
  }
</script>

<!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_noninteractive_element_interactions -->
<p
  class="verse bible"
  class:hl={highlighted}
  class:dim
  style="opacity:{opacity}"
  onpointerdown={down}
  onpointermove={move}
  onpointerup={up}
  onpointercancel={up}
  onclick={click}
  oncontextmenu={(e) => e.preventDefault()}
>
  <sup class="nr">{verse.verse}</sup> {verse.text}{#if favorite}&nbsp;<span class="fav"><Icon name="bookmark" size={17} color="var(--secondary)" label="Lieblingsvers" /></span>{/if}
</p>

<style>
  .verse {
    margin: 0; padding: 2px 4px; border-radius: 8px; color: var(--on-background); cursor: default;
    transition: opacity 0.28s, background 0.2s;
    -webkit-user-select: none; user-select: none; -webkit-touch-callout: none;
  }
  :global(.calm) .verse { transition: none; }
  .hl { background: color-mix(in srgb, var(--secondary-container) 55%, transparent); }
  .nr { font-size: 0.62em; font-weight: 700; color: var(--primary); vertical-align: 0.5em; line-height: 0; font-family: var(--ui-font); }
  .fav { display: inline-flex; vertical-align: -2px; }
</style>
