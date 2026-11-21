<script lang="ts">
  import Icon from './Icon.svelte'
  import { answerBool, answerIndex, answerInt, type Quiz } from '../data/plan.ts'
  import type { Verse } from '../data/content.ts'
  import { feedback } from '../audio/feedback.ts'
  import { theme } from '../ui/theme.svelte.ts'
  import { shake } from '../ui/shake.ts'
  import { hashCode, shuffled } from '../util/random.ts'

  /**
   * One quiz question. Wrong answers never cost anything: a hint appears and the user tries again.
   * [onsolved] fires once with whether it was solved on the first attempt; [onnext] after the explanation.
   * Mount it inside {#key} per question.
   */
  let { quiz, qkey, verses = [], onsolved, onnext, nextLabel = 'Weiter' }: {
    quiz: Quiz; qkey: string; verses?: Verse[]; onsolved: (firstTry: boolean) => void; onnext: () => void; nextLabel?: string
  } = $props()

  let solved = $state(false)
  let mistakes = $state(0)
  let showVerse = $state(false)

  function wrong(el?: EventTarget | null) {
    mistakes++
    feedback.tryAgain()
    shake(el as Element)
  }
  function right() {
    if (solved) return
    solved = true
    feedback.correct()
    onsolved(mistakes === 0)
  }

  const title = $derived(({ whosaid: 'Wer hat’s gesagt?', truefalse: 'Stimmt das?', order: 'Bring in die richtige Reihenfolge', estimate: 'Schätzfrage' } as Record<string, string>)[quiz.type])
  const options = $derived(quiz.options ?? [])
  // svelte-ignore state_referenced_locally
  const seed = hashCode(qkey)

  // choice / whosaid
  // svelte-ignore state_referenced_locally
  const order = shuffled(options.map((_, i) => i), seed)
  let tried = $state<number[]>([])

  // truefalse
  let triedTF = $state<boolean[]>([])

  // order
  // svelte-ignore state_referenced_locally
  const items = quiz.items ?? []
  const orderShuffled = (() => {
    let s = shuffled(items, seed)
    let n = 1
    while (items.length > 1 && s.every((x, i) => x === items[i])) s = shuffled(items, seed + n++)
    return s
  })()
  let placed = $state<string[]>([])

  // error
  // svelte-ignore state_referenced_locally
  const tokens = (quiz.text ?? '').split(' ').filter((t) => t)
  let triedTok = $state<number[]>([])

  // estimate
  // svelte-ignore state_referenced_locally
  const min = quiz.min ?? 0, max = quiz.max ?? 10
  // svelte-ignore state_referenced_locally
  let value = $state(Math.trunc((min + max) / 2))
  let direction = $state<string | null>(null)

  const hintVerse = $derived(quiz.verse != null ? verses.find((v) => v.verse === quiz.verse) : undefined)

  function trailing(word: string) {
    const m = word.match(/[^\p{L}\p{N}]*$/u)
    return m ? m[0] : ''
  }
</script>

<div class="quiz stack-14">
  {#if title}<p class="t-ll primary">{title}</p>{/if}

  {#if quiz.type === 'whosaid'}
    <p class="t-tl italic">„{quiz.quote}“</p>
  {:else if quiz.type === 'order' || quiz.type === 'error'}
    {#if quiz.q}<p class="t-tm">{quiz.q}</p>{/if}
  {:else}
    <p class="t-tl" style="font-family:var(--ui-font);font-weight:400">{quiz.q ?? ''}</p>
  {/if}

  {#if quiz.type === 'truefalse'}
    <div class="tf">
      {#each [true, false] as v (v)}
        {@const st = solved && v === answerBool(quiz) ? 2 : triedTF.includes(v) ? 1 : 0}
        <button class="answer" class:wrong={st === 1} class:right={st === 2} disabled={solved || triedTF.includes(v)}
          onclick={(e) => { if (v === answerBool(quiz)) right(); else { triedTF = [...triedTF, v]; wrong(e.currentTarget) } }}>
          <span class="grow">{v ? 'Stimmt' : 'Stimmt nicht'}</span>
          {#if st === 2}<Icon name="check" color="var(--primary)" />{/if}
        </button>
      {/each}
    </div>
  {:else if quiz.type === 'order'}
    <p class="t-bm muted">{placed.length === 0 ? 'Tippe an, was zuerst kommt.' : 'Und dann?'}</p>
    {#each placed as item, i (item)}
      <div class="placed"><b class="primary">{i + 1}</b><span>{item}</span></div>
    {/each}
    {#each orderShuffled.filter((x) => !placed.includes(x)) as item (item)}
      <button class="answer" disabled={solved}
        onclick={(e) => {
          if (item === items[placed.length]) {
            placed = [...placed, item]
            if (placed.length === items.length) right(); else feedback.tick()
          } else wrong(e.currentTarget)
        }}>{item}</button>
    {/each}
  {:else if quiz.type === 'error'}
    <p class="t-bm muted">Tippe auf das Wort, das nicht stimmt.</p>
    <div class="error-text">
      {#each tokens as raw, i (i)}
        {@const isWrong = raw.includes('[')}
        {@const word = raw.replaceAll('[', '').replaceAll(']', '')}
        {#if solved && isWrong}
          {@const tr = trailing(word)}
          <span class="tok fixed"><s class="muted">{word.slice(0, word.length - tr.length)}</s> <b style="color:{theme.extra.success}">{(quiz.fix ?? '') + tr}</b></span>
        {:else}
          <button class="tok" class:bad={triedTok.includes(i)} disabled={solved || triedTok.includes(i)}
            onclick={(e) => { if (isWrong) right(); else { triedTok = [...triedTok, i]; wrong(e.currentTarget) } }}>{word}</button>
        {/if}
      {/each}
    </div>
  {:else if quiz.type === 'estimate'}
    <div class="estimate">
      <p class="t-ds value" style="color:{solved ? theme.extra.success : 'var(--on-surface)'}">{`${value} ${quiz.unit ?? ''}`.trim()}</p>
      <input type="range" {min} {max} step="1" bind:value disabled={solved} oninput={() => (direction = null)} aria-label="Schätzung" />
      <div class="row" style="justify-content:space-between;width:100%"><span class="muted">{min}</span><span class="muted">{max}</span></div>
      {#if direction}<p class="secondary" style="font-weight:500;margin:6px 0 0">{direction}</p>{/if}
      {#if !solved}
        <button class="btn outline" style="margin-top:10px"
          onclick={(e) => {
            const diff = value - answerInt(quiz)
            if (Math.abs(diff) <= (quiz.tolerance ?? 0)) right()
            else { direction = diff < 0 ? 'Etwas mehr' : 'Etwas weniger'; wrong((e.currentTarget as HTMLElement).parentElement?.querySelector('.value')) }
          }}>Prüfen</button>
      {/if}
    </div>
  {:else}
    {#each order as i (i)}
      {@const st = solved && i === answerIndex(quiz) ? 2 : tried.includes(i) ? 1 : 0}
      <button class="answer" class:wrong={st === 1} class:right={st === 2} disabled={solved || tried.includes(i)}
        onclick={(e) => { if (i === answerIndex(quiz)) right(); else { tried = [...tried, i]; wrong(e.currentTarget) } }}>
        <span class="grow">{options[i]}</span>
        {#if st === 2}<Icon name="check" color="var(--primary)" />{/if}
      </button>
    {/each}
  {/if}

  {#if !solved && mistakes > 0}
    <div class="hint enter stack-6">
      <div class="row" style="gap:8px"><Icon name="lightbulb" size={18} /><span>{quiz.hint ?? 'Kein Problem – versuch es nochmal.'}</span></div>
      {#if hintVerse}
        {#if showVerse}
          <p class="serif" style="margin:0">{hintVerse.verse} {hintVerse.text}</p>
        {:else}
          <button class="btn text small" style="align-self:flex-start" onclick={() => (showVerse = true)}>Vers {hintVerse.verse} ansehen</button>
        {/if}
      {/if}
    </div>
  {/if}

  {#if solved}
    <div class="enter stack-14">
      <div class="ok row" style="align-items:flex-start;gap:10px">
        <Icon name="check" />
        <div>
          <p style="margin:0;font-weight:600">{mistakes === 0 ? 'Richtig!' : 'Genau!'}</p>
          {#if quiz.explain}<p style="margin:0">{quiz.explain}</p>{/if}
        </div>
      </div>
      <button class="btn" style="height:54px" onclick={onnext}>{nextLabel}</button>
    </div>
  {/if}
</div>

<style>
  .stack-14 { display: flex; flex-direction: column; gap: 14px; }
  .stack-6 { display: flex; flex-direction: column; gap: 6px; }
  .answer {
    display: flex; align-items: center; gap: 8px; width: 100%; text-align: left; cursor: pointer;
    padding: 16px 18px; border-radius: 16px; font-size: 16px; line-height: 24px;
    background: var(--surface); color: var(--on-surface); border: 1px solid color-mix(in srgb, var(--outline) 60%, transparent);
    transition: background 0.2s;
  }
  .answer:disabled { cursor: default; }
  .answer.wrong { background: var(--surface-variant); color: color-mix(in srgb, var(--on-surface-variant) 55%, transparent); text-decoration: line-through; }
  .answer.right { background: var(--primary-container); color: var(--on-primary-container); border-color: var(--primary); }
  .tf { display: flex; gap: 10px; }
  .tf .answer { flex: 1; }
  .placed { display: flex; gap: 14px; align-items: center; padding: 14px 18px; border-radius: 16px; background: var(--primary-container); color: var(--on-primary-container); }
  .error-text { background: var(--surface-container); border-radius: 16px; padding: 14px; display: flex; flex-wrap: wrap; gap: 2px; }
  .tok { border: 0; background: transparent; padding: 6px 4px; border-radius: 8px; font-size: 16px; line-height: 24px; cursor: pointer; color: var(--on-surface); }
  .tok.bad { background: var(--surface-variant); }
  .tok:disabled { cursor: default; }
  .tok.fixed { cursor: default; }
  .estimate { display: flex; flex-direction: column; align-items: center; width: 100%; }
  .estimate .value { margin: 0; }
</style>
