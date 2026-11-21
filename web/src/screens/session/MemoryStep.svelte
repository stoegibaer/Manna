<script lang="ts">
  import { feedback } from '../../lib/audio/feedback.ts'
  import { confetti } from '../../lib/ui/confetti.svelte.ts'
  import { shake } from '../../lib/ui/shake.ts'
  import { hashCode, shuffled } from '../../lib/util/random.ts'
  import type { Session } from './session.svelte.ts'

  /** Tap the words of the memory verse in the right order. Wrong taps only shake – no penalty. */
  let { s }: { s: Session } = $props()
  // svelte-ignore state_referenced_locally
  const mv = s.section!.memory_verse!
  const words = mv.text.split(' ').filter((w) => w.trim())
  const order = shuffled(words.map((_, i) => i), hashCode(mv.text))
  let placed = $state(0)
  const done = $derived(placed === words.length)
  // svelte-ignore state_referenced_locally
  const bookName = s.refLabel.split(';')[0].replace(/\s+\S+$/, '')
  const ref = `${bookName} ${mv.ref.chapter},${mv.ref.from}${mv.ref.to !== mv.ref.from ? `–${mv.ref.to}` : ''}`

  function tap(i: number, el: EventTarget | null) {
    // equal words (e.g. „und“) are interchangeable
    if (words[i] === words[placed]) {
      placed++
      feedback.tick()
      if (placed === words.length) { feedback.sectionDone(); confetti.fire(true) }
    } else { shake(el as Element); feedback.tryAgain() }
  }
</script>

<div class="content stack-16 enter" style="padding-top:8px;padding-bottom:40px">
  <h2 class="t-hm">Merkvers</h2>
  <p class="muted" style="margin:0">{done ? 'Gemerkt – er ist jetzt bei deinen Lieblingsversen.' : 'Tippe die Wörter in der richtigen Reihenfolge an.'}</p>
  <div class="card"><p class="t-tl" style="margin:2px">{words.slice(0, placed).join(' ') || '…'}</p></div>
  <p class="t-bs muted">{ref}</p>
  {#if !done}
    <div class="words">
      {#each order.filter((i) => i >= placed) as i (i)}
        <button class="word" onclick={(e) => tap(i, e.currentTarget)}>{words[i]}</button>
      {/each}
    </div>
    <button class="btn text" style="align-self:center" onclick={() => s.memoryDone(false)}>Überspringen</button>
  {:else}
    <button class="btn" onclick={() => s.memoryDone(true)}>Weiter</button>
  {/if}
</div>

<style>
  .words { display: flex; flex-wrap: wrap; gap: 8px; }
  .word {
    padding: 10px 14px; border-radius: 12px; font-size: 16px; cursor: pointer;
    background: var(--surface); color: var(--on-surface); border: 1px solid color-mix(in srgb, var(--outline) 60%, transparent);
  }
</style>
