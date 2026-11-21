<script lang="ts">
  import TopBar from '../lib/components/TopBar.svelte'
  import Icon from '../lib/components/Icon.svelte'
  import Dialog from '../lib/components/Dialog.svelte'
  import { plan as loadPlan, planIndex } from '../lib/data/content.ts'
  import { resolvePlan, type Direction, type PlanEntry, type PlanIndex } from '../lib/data/plan.ts'
  import { store } from '../lib/data/store.svelte.ts'
  import { router } from '../lib/router.svelte.ts'

  /** [reread] = position in a second (third …) run through a finished plan. */
  interface Item { entry: PlanEntry; sections: number; done: number; reread?: number; finished: boolean }

  let index = $state.raw<PlanIndex | null>(null)
  let sizes = $state.raw<Map<string, number>>(new Map())
  $effect(() => {
    void planIndex().then(async (idx) => {
      const avail = (idx.plans ?? []).filter((p) => p.available)
      const plans = await Promise.all(avail.map((p) => loadPlan(p.id)))
      sizes = new Map(plans.map((p) => [p.id, p.sections.length]))
      index = idx
    })
  })

  const active = $derived(index ? resolvePlan(index, store.settings.activePlan) : '')

  function item(e: PlanEntry): Item {
    const sections = e.available ? sizes.get(e.id) ?? 0 : 0
    const done = store.sections.filter((s) => s.planId === e.id).length
    const reread = store.settings.rereads[e.id]
    return { entry: e, sections, done, reread, finished: reread === undefined && sections > 0 && done >= sections }
  }

  const start = $derived(index ? (index.plans ?? []).find((p) => p.id === index!.start) : undefined)
  // Show what can be read now first: active plan, unfinished available ones, finished ones, then "coming soon".
  const directions = $derived.by((): [Direction, Item[]][] => {
    if (!index) return []
    const rank = (it: Item) => (it.entry.id === active ? 0 : it.entry.available && !it.finished ? 1 : it.entry.available ? 2 : 3)
    return (index.directions ?? []).map((d) => [d, (index!.plans ?? []).filter((p) => p.direction === d.id).map(item).sort((a, b) => rank(a) - rank(b))])
  })

  let open = $state<Record<string, boolean>>({})
  let more = $state<Record<string, boolean>>({})
  let askReread = $state<PlanEntry | null>(null)

  /** Choosing a finished plan starts reading it again; progress, cards and garden stay as they are. */
  async function choose(id: string) {
    const p = await loadPlan(id)
    const done = store.doneIds(id)
    const finished = p.sections.every((s) => done.has(s.id))
    store.updateSettings((st) => ({
      ...st, activePlan: id, rereads: finished && !(id in st.rereads) ? { ...st.rereads, [id]: 0 } : st.rereads,
    }))
    router.home()
  }

  function subtitle(it: Item) {
    const e = it.entry, sub = e.subtitle ?? ''
    if (!e.available) return `${sub} · bald verfügbar`
    if (it.entry.id === active && !it.finished) return `${sub} · liest du gerade`
    if (it.finished) return `${sub} · gelesen · nochmal lesen?`
    if (it.reread !== undefined) return `${sub} · nochmal: ${it.reread} von ${it.sections}`
    if (it.done > 0) return `${sub} · ${it.done} von ${it.sections} Abschnitten`
    return `${sub} · ${it.sections} Abschnitte`
  }
</script>

{#snippet planRow(it: Item)}
  {@const isActive = it.entry.id === active}
  <button class="plan" class:active={isActive} class:finished={it.finished} class:soon={!it.entry.available}
    disabled={!it.entry.available || (isActive && !it.finished)}
    onclick={(e) => { e.stopPropagation(); if (it.finished) askReread = it.entry; else void choose(it.entry.id) }}>
    <span class="grow">
      <span class="t-tm" style="display:block">{it.entry.title}</span>
      <span class="t-bm sub" style="display:block">{subtitle(it)}</span>
    </span>
    {#if it.finished}<Icon name="check" size={22} color="var(--primary)" label="gelesen" />{/if}
  </button>
{/snippet}

<div class="page">
  <TopBar title="Lesepläne" onback={() => router.back()} />
  {#if index}
    <div class="content stack-12" style="padding-bottom:40px">
      {#if start}
        <p class="t-ll primary">Der Anfang</p>
        {@render planRow(item(start))}
      {/if}
      <div style="height:8px"></div>
      <h2 class="t-hs">Wohin als Nächstes?</h2>
      <p class="muted" style="margin:0">Wähl eine Richtung – darin warten drei Pläne, weitere auf Wunsch.</p>
      {#each directions as [dir, items] (dir.id)}
        {@const isOpen = open[dir.id] ?? items.some((i) => i.entry.id === active)}
        <div class="direction">
          <button class="dir-head" onclick={() => (open[dir.id] = !isOpen)} aria-expanded={isOpen}>
            <span class="grow">
              <span class="t-tl" style="display:block">{dir.title}</span>
              <span class="muted" style="display:block">{dir.subtitle ?? ''}</span>
            </span>
            <Icon name={isOpen ? 'expandLess' : 'expandMore'} />
          </button>
          {#if isOpen}
            <div class="stack-8 enter" style="padding:0 18px 18px">
              {#each more[dir.id] ? items : items.slice(0, 3) as it (it.entry.id)}{@render planRow(it)}{/each}
              {#if items.length > 3}
                <button class="btn text" style="align-self:center" onclick={() => (more[dir.id] = !more[dir.id])}>
                  {more[dir.id] ? 'Weniger anzeigen' : `Weitere Pläne (${items.length - 3})`}
                </button>
              {/if}
            </div>
          {/if}
        </div>
      {/each}
      <div style="height:8px"></div>
      <button class="tile" onclick={() => router.go('bible')}>
        <span class="t-tl" style="display:block">Frei lesen</span>
        <span class="muted">Die ganze Bibel, Buch für Buch – ohne Quiz.</span>
      </button>
    </div>
  {:else}
    <div class="spinner"></div>
  {/if}
</div>

{#if askReread}
  {@const e = askReread}
  <Dialog onclose={() => (askReread = null)}>
    <div class="stack-16" style="padding:24px">
      <h2 class="t-hs">{e.title} nochmal lesen?</h2>
      <p class="muted" style="margin:0">Du startest wieder beim ersten Abschnitt. Deine Karten, dein Garten und alles Gelesene bleiben erhalten.</p>
      <div class="row" style="justify-content:flex-end">
        <button class="btn text" onclick={() => (askReread = null)}>Abbrechen</button>
        <button class="btn text" onclick={() => { askReread = null; void choose(e.id) }}>Nochmal lesen</button>
      </div>
    </div>
  </Dialog>
{/if}

<style>
  .direction { background: var(--surface-container); border-radius: 20px; }
  .dir-head { display: flex; align-items: center; gap: 8px; width: 100%; padding: 18px; border: 0; background: transparent; text-align: left; cursor: pointer; }
  .plan {
    display: flex; align-items: center; gap: 8px; width: 100%; text-align: left; padding: 16px; border-radius: 16px; cursor: pointer;
    background: var(--surface); border: 1px solid color-mix(in srgb, var(--outline) 40%, transparent); color: var(--on-surface);
  }
  .plan:disabled { cursor: default; }
  .plan.active { background: var(--primary-container); border-color: var(--primary); }
  .plan.finished { background: color-mix(in srgb, var(--primary) 8%, var(--surface)); border-color: color-mix(in srgb, var(--primary) 35%, transparent); }
  .plan .sub { color: var(--on-surface-variant); }
  .plan.finished .sub { color: var(--primary); }
  .plan.soon { color: color-mix(in srgb, var(--on-surface-variant) 60%, transparent); }
  .plan.soon .sub { opacity: 0.6; }
</style>
