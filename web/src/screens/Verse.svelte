<script lang="ts">
  import Icon from '../lib/components/Icon.svelte'
  import { bookNames, plan as loadPlan, planIndex, verses } from '../lib/data/content.ts'
  import { nextIndex, resolvePlan } from '../lib/data/plan.ts'
  import { store } from '../lib/data/store.svelte.ts'
  import { feedback } from '../lib/audio/feedback.ts'
  import { confetti } from '../lib/ui/confetti.svelte.ts'
  import { router } from '../lib/router.svelte.ts'

  /** „Nur 1 Vers“ – the lowest possible bar: the first verse of the next section. Reading it fulfils the daily minimum. */
  let st = $state<{ loading: boolean; text: string; ref: string; sectionTitle: string; planFinished: boolean }>({ loading: true, text: '', ref: '', sectionTitle: '', planFinished: false })
  let done = $state(false)

  $effect(() => {
    void (async () => {
      const settings = store.settings
      const planId = resolvePlan(await planIndex(), settings.activePlan)
      const plan = await loadPlan(planId)
      const section = plan.sections[nextIndex(plan, store.doneIds(planId), settings.rereads[planId])]
      if (!section) { st = { ...st, loading: false, planFinished: true }; return }
      const r = section.refs[0]
      const v = (await verses(r.book, r.chapter, r.from, r.to))[0]
      const names = await bookNames()
      st = { loading: false, text: v.text, ref: `${names.get(v.book)} ${v.chapter},${v.verse}`, sectionTitle: section.title, planFinished: false }
    })()
  })

  function markRead() {
    if (done) return
    done = true
    store.logReading(1, 0)
    feedback.sectionDone()
    confetti.fire()
  }
</script>

<div class="page">
  <div class="bar"><button class="icon-btn" onclick={() => router.home()} aria-label="Schließen"><Icon name="close" /></button></div>
  {#if st.loading}
    <div class="spinner"></div>
  {:else if st.planFinished}
    <div class="content stack-16" style="align-items:center;padding-top:30dvh">
      <p class="t-tl center">Dieser Plan ist schon ganz gelesen.</p>
      <button class="btn" style="width:auto" onclick={() => router.replace('plans')}>Wohin als Nächstes?</button>
    </div>
  {:else}
    <div class="content stack-20" style="padding:16px 28px 24px">
      <p class="t-ll primary">Dein Vers für heute</p>
      <p class="bible" style="font-size:calc(22.8px * var(--text-scale));line-height:calc(36px * var(--text-scale));margin:0">{st.text}</p>
      <p class="t-bm muted">{st.ref}</p>
      <div style="height:8px"></div>
      {#if !done}
        <button class="btn tall" onclick={markRead}><Icon name="check" />Gelesen</button>
      {:else}
        <div class="stack-12 enter">
          <p class="t-tl">Geschafft – das reicht für heute.</p>
          <p class="muted" style="margin:0">Wenn du magst: Der Vers gehört zum Abschnitt „{st.sectionTitle}“.</p>
          <button class="btn outline" onclick={() => router.replace('session')}>Ganzen Abschnitt lesen</button>
          <button class="btn text" style="align-self:center" onclick={() => router.home()}>Fertig</button>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .bar { padding: calc(var(--safe-top) + 8px) 8px 0; }
  .stack-20 { display: flex; flex-direction: column; gap: 20px; }
</style>
