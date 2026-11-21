<script lang="ts">
  import TopBar from '../lib/components/TopBar.svelte'
  import Icon from '../lib/components/Icon.svelte'
  import Dialog from '../lib/components/Dialog.svelte'
  import Sheet from '../lib/components/Sheet.svelte'
  import CardTile, { cardStyle } from '../lib/components/CardTile.svelte'
  import AtlasMap, { type AtlasPoint } from '../lib/components/AtlasMap.svelte'
  import { availablePlans, bookNames, places as loadPlaces, verses as loadVerses } from '../lib/data/content.ts'
  import type { Card, Place, Plan } from '../lib/data/plan.ts'
  import { store } from '../lib/data/store.svelte.ts'
  import { REFLECTION_TAGS } from './session/session.svelte.ts'
  import { formatLongDate } from '../lib/util/date.ts'
  import { router } from '../lib/router.svelte.ts'

  const TAB_KEY = 'manna.albumTab'
  let tab = $state((() => { try { return Number(sessionStorage.getItem(TAB_KEY) ?? 0) } catch { return 0 } })())
  $effect(() => { try { sessionStorage.setItem(TAB_KEY, String(tab)) } catch { /* ignore */ } })

  let plans = $state.raw<Plan[] | null>(null)
  let placeMap = $state.raw<Map<string, Place>>(new Map())
  let names = $state.raw<Map<number, string>>(new Map())
  $effect(() => {
    void Promise.all([availablePlans(), loadPlaces(), bookNames()]).then(([p, pl, n]) => { plans = p; placeMap = pl; names = n })
  })

  // ── cards ──
  const groups = $derived.by(() => {
    if (!plans) return []
    const have = new Set(store.cards.map((c) => `${c.planId}|${c.cardId}`))
    return plans
      .map((p) => ({ title: p.title, cards: (p.cards ?? []).map((c) => [c, have.has(`${p.id}|${c.id}`)] as [Card, boolean]) }))
      .filter((g) => g.cards.length)
      .sort((a, b) => b.cards.filter((c) => c[1]).length - a.cards.filter((c) => c[1]).length) // started collections first
  })
  const totalCards = $derived(groups.reduce((n, g) => n + g.cards.length, 0))
  const found = $derived(groups.reduce((n, g) => n + g.cards.filter((c) => c[1]).length, 0))
  let openCard = $state<Card | null>(null)

  // ── verses ──
  let saved = $state.raw<{ book: number; chapter: number; verse: number; ref: string; text: string; memory: boolean }[]>([])
  $effect(() => {
    const favs = [...store.favorites].sort((a, b) => b.savedAt - a.savedAt)
    const n = names
    void Promise.all(favs.map(async (f) => {
      const v = (await loadVerses(f.book, f.chapter, f.verse, f.verse))[0]
      return v ? { book: f.book, chapter: f.chapter, verse: f.verse, ref: `${n.get(f.book) ?? ''} ${f.chapter},${f.verse}`, text: v.text, memory: f.source === 'memory' } : null
    })).then((list) => (saved = list.filter((x) => x !== null)))
  })

  // ── journal ──
  const labels = new Map(REFLECTION_TAGS)
  const journal = $derived([...store.journal].sort((a, b) => b.savedAt - a.savedAt))

  // ── atlas ──
  interface Occ { planTitle: string; sectionTitle: string; done: boolean }
  const atlas = $derived.by(() => {
    if (!plans) return []
    const have = new Set(store.sections.map((s) => `${s.planId}|${s.sectionId}`))
    const occ = new Map<string, Occ[]>()
    for (const p of plans) for (const sec of p.sections) {
      if (!sec.place || !placeMap.has(sec.place)) continue
      if (!occ.has(sec.place)) occ.set(sec.place, [])
      occ.get(sec.place)!.push({ planTitle: p.title, sectionTitle: sec.title, done: have.has(`${p.id}|${sec.id}`) })
    }
    return [...occ].map(([id, list]) => ({ place: placeMap.get(id)!, occ: list, visited: list.some((o) => o.done) }))
      .sort((a, b) => a.place.name.localeCompare(b.place.name, 'de'))
  })
  const visited = $derived(atlas.filter((a) => a.visited))
  const points = $derived<AtlasPoint[]>(atlas.map((a) => ({ id: a.place.id, name: a.place.name, lat: a.place.lat, lon: a.place.lon, visited: a.visited, weight: a.occ.length })))
  let selected = $state<string | null>(null)
  const selectedPlace = $derived(atlas.find((a) => a.place.id === selected))
  const distinct = (xs: string[]) => [...new Set(xs)]
</script>

{#snippet empty(title: string, text: string)}
  <div class="empty">
    <p class="t-tm">{title}</p>
    <p class="muted center" style="margin:8px 0 0">{text}</p>
  </div>
{/snippet}

<div class="page">
  <TopBar title="Sammlung" onback={() => router.back()} />
  <div class="tabs" role="tablist">
    {#each ['Karten', 'Verse', 'Tagebuch', 'Atlas'] as t, i (t)}
      <button role="tab" class="tab" class:on={tab === i} aria-selected={tab === i} onclick={() => (tab = i)}>{t}</button>
    {/each}
  </div>

  {#if !plans}
    <div class="spinner"></div>
  {:else if tab === 0}
    <div class="pad">
      <p class="muted" style="margin:0 0 4px">{found} von {totalCards} Karten entdeckt</p>
      {#each groups as g (g.title)}
        <h2 class="t-tl" style="padding-top:12px;margin-bottom:12px">{g.title}</h2>
        <div class="grid2">
          {#each g.cards as [card, unlocked] (card.id)}
            {@const st = cardStyle(card.type)}
            <button class="mini" class:locked={!unlocked} disabled={!unlocked} onclick={() => (openCard = card)}
              style="border-color:{unlocked ? st[1] + '66' : 'color-mix(in srgb, var(--outline) 30%, transparent)'}">
              {#if unlocked}
                <span class="mini-band" style="background:linear-gradient(90deg,{st[1]},{st[2]})"></span>
                <span class="mini-body">
                  <span class="mini-label" style="color:{st[1]}">{st[0]}</span>
                  <span class="mini-name">{card.name}</span>
                </span>
              {:else}
                <span class="mini-lock">
                  <Icon name="lock" size={22} color="color-mix(in srgb, var(--on-surface-variant) 60%, transparent)" />
                  <span class="mini-label">{st[0]}</span>
                </span>
              {/if}
            </button>
          {/each}
        </div>
      {/each}
    </div>
  {:else if tab === 1}
    {#if !store.favorites.length}
      {@render empty('Noch keine Verse gespeichert.', 'Drück beim Lesen lange auf einen Vers, um ihn hier zu sammeln. Gelernte Merkverse landen automatisch hier.')}
    {:else}
      <div class="pad stack-12">
        {#each saved as v (`${v.book}-${v.chapter}-${v.verse}`)}
          <div class="card stack-6">
            <p class="t-bl serif">{v.text}</p>
            <div class="row">
              <span class="t-lm muted grow">{v.ref}{v.memory ? ' · Merkvers' : ''}</span>
              <button class="btn text" onclick={() => store.setFavorite(v.book, v.chapter, v.verse, false)}>Entfernen</button>
            </div>
          </div>
        {/each}
      </div>
    {/if}
  {:else if tab === 2}
    {#if !journal.length}
      {@render empty('Dein Tagebuch ist noch leer.', 'Nach jedem Abschnitt kannst du mit einem Tipp festhalten, was du mitnimmst.')}
    {:else}
      <div class="pad stack-12">
        {#each journal as e (e.planId + e.sectionId)}
          {@const tags = e.tags.split(',').map((t) => labels.get(t)).filter(Boolean)}
          <div class="card stack-6">
            <p class="t-tm">{e.sectionTitle}</p>
            <p class="t-ls muted">{formatLongDate(e.savedAt)}</p>
            {#if tags.length}<p class="t-bm secondary">{tags.join(' · ')}</p>{/if}
            {#if e.note.trim()}<p class="t-bl">{e.note}</p>{/if}
          </div>
        {/each}
      </div>
    {/if}
  {:else}
    <div style="padding:12px 20px 0">
      <AtlasMap {points} {selected} onselect={(id) => (selected = id)} style="width:100%;aspect-ratio:1.45;border-radius:18px" />
    </div>
    <div class="pad stack-8">
      <p class="muted" style="margin:0 0 4px">{visited.length} von {atlas.length} Orten besucht</p>
      {#if !visited.length}
        <p class="t-bm muted">Wenn du einen Abschnitt abschließt, der an einem Ort spielt, erscheint der Ort hier und auf der Karte.</p>
      {/if}
      {#each visited as p (p.place.id)}
        <button class="place" onclick={() => (selected = p.place.id)}>
          <span class="t-tm" style="display:block">{p.place.name}</span>
          <span class="t-bs muted" style="display:block">{distinct(p.occ.filter((o) => o.done).map((o) => o.planTitle)).join(' · ')}</span>
        </button>
      {/each}
    </div>
  {/if}
</div>

{#if openCard}
  <Dialog onclose={() => (openCard = null)}><CardTile card={openCard} /></Dialog>
{/if}

{#if selectedPlace}
  {@const p = selectedPlace}
  <Sheet onclose={() => (selected = null)}>
    <div class="stack-10">
      {#if !p.visited}
        <h2 class="t-tl">Noch nicht entdeckt</h2>
        <p class="muted" style="margin:0">Dieser Ort kommt vor in: {distinct(p.occ.map((o) => o.planTitle)).join(', ')}.</p>
      {:else}
        <h2 class="t-tl">{p.place.name}</h2>
        {#if p.place.text}<p class="muted" style="margin:0">{p.place.text}</p>{/if}
        <p class="t-ll primary" style="padding-top:8px">Kommt vor in</p>
        {#each p.occ.filter((o) => o.done) as o, i (i)}<p class="t-bl">{o.planTitle} · {o.sectionTitle}</p>{/each}
        {@const more = p.occ.filter((o) => !o.done).length}
        {#if more > 0}<p class="t-bm muted">{more === 1 ? 'und in einem weiteren Abschnitt' : `und in ${more} weiteren Abschnitten`}</p>{/if}
      {/if}
    </div>
  </Sheet>
{/if}

<style>
  .tabs { display: flex; position: sticky; top: calc(64px + var(--safe-top)); z-index: 4; background: var(--background); border-bottom: 1px solid color-mix(in srgb, var(--outline) 30%, transparent); }
  .tab { flex: 1; border: 0; background: transparent; padding: 14px 4px; font-size: 14px; font-weight: 600; color: var(--on-surface-variant); cursor: pointer; border-bottom: 3px solid transparent; }
  .tab.on { color: var(--primary); border-bottom-color: var(--primary); }
  .pad { padding: 12px 20px calc(32px + var(--safe-bottom)); }
  .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .mini { height: 118px; border-radius: 16px; border: 1px solid; background: var(--surface); padding: 0; overflow: hidden; display: flex; flex-direction: column; text-align: left; cursor: pointer; }
  .mini:disabled { cursor: default; }
  .mini-band { height: 10px; width: 100%; flex: none; }
  .mini-body { padding: 14px; display: flex; flex-direction: column; }
  .mini-label { font-size: 10px; font-weight: 700; letter-spacing: 1.4px; }
  .mini-name { font-family: var(--bible-font); font-weight: 600; font-size: 18px; line-height: 24px; display: -webkit-box; -webkit-line-clamp: 2; line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
  .mini-lock { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 6px; background: color-mix(in srgb, var(--surface-variant) 50%, transparent); color: color-mix(in srgb, var(--on-surface-variant) 60%, transparent); }
  .place { display: block; width: 100%; text-align: left; border: 0; border-radius: 14px; padding: 12px 16px; background: var(--surface-container); cursor: pointer; }
  .empty { padding: 64px 32px; display: flex; flex-direction: column; align-items: center; }
  .stack-6 { display: flex; flex-direction: column; gap: 6px; }
  .stack-10 { display: flex; flex-direction: column; gap: 10px; }
</style>
