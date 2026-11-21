<script lang="ts">
  import Icon from '../lib/components/Icon.svelte'
  import Dialog from '../lib/components/Dialog.svelte'
  import GardenView from '../lib/components/GardenView.svelte'
  import MustardTree from '../lib/components/MustardTree.svelte'
  import TreeChoice from '../lib/components/TreeChoice.svelte'
  import { bookNames, plan as loadPlan, planIndex } from '../lib/data/content.ts'
  import { ORDER, LIFE, choicePending, offers, progress } from '../lib/data/garden.ts'
  import { nextIndex, refLabel, resolvePlan, type Plan } from '../lib/data/plan.ts'
  import { store } from '../lib/data/store.svelte.ts'
  import { animations } from '../lib/data/types.ts'
  import { addDays, daysBetween, isoDate, mondayOf, parseIso, weekdayIndex } from '../lib/util/date.ts'
  import { router } from '../lib/router.svelte.ts'
  import { install } from '../lib/ui/install.svelte.ts'

  let plan = $state.raw<Plan | null>(null)
  let names = $state.raw<Map<number, string>>(new Map())
  let reEntrySection = $state.raw<{ title: string; summary: string } | null>(null)

  const settings = $derived(store.settings)
  const animate = $derived(animations(settings))

  // Dev only: ?debugTree=N previews the garden at N sections (all trees planted in order)
  const debugTree = import.meta.env.DEV ? Number(new URLSearchParams(location.search).get('debugTree') ?? -1) : -1

  $effect(() => {
    const chosen = settings.activePlan
    void planIndex().then((idx) => loadPlan(resolvePlan(idx, chosen))).then((p) => (plan = p))
    void bookNames().then((n) => (names = n))
  })

  const doneIds = $derived(plan ? store.doneIds(plan.id) : new Set<string>())
  const rereadPos = $derived(plan ? settings.rereads[plan.id] : undefined)
  const idx = $derived(plan ? nextIndex(plan, doneIds, rereadPos) : -1)
  const next = $derived(plan && idx >= 0 ? plan.sections[idx] : null)
  const nextRef = $derived(next ? refLabel(next.refs, (n) => names.get(n) ?? '') : '')
  // the curiosity question of the previous section leads into the next one
  const teaser = $derived(plan && idx > 0 ? plan.sections[idx - 1].teaser : null)
  const doneInPlan = $derived(rereadPos ?? doneIds.size)
  const total = $derived(store.totalSections)
  const planted = $derived(store.planted)

  const today = new Date()
  const activeDates = $derived(new Set(store.days.filter((d) => d.verses > 0 || d.sections > 0).map((d) => d.date)))
  const monday = mondayOf(today)
  const week = $derived(Array.from({ length: 7 }, (_, i) => activeDates.has(isoDate(addDays(monday, i)))))
  const weekCount = $derived(week.filter(Boolean).length)
  const readToday = $derived(activeDates.has(isoDate(today)))

  // back after a break (3+ days)? – welcome, no reproach
  const daysAway = $derived.by(() => {
    const since = isoDate(addDays(today, -14))
    const recent = [...activeDates].filter((d) => d >= since).sort()
    return recent.length ? daysBetween(parseIso(recent[recent.length - 1]), today) : 15
  })
  $effect(() => {
    if (total === 0 || daysAway < 3) { reEntrySection = null; return }
    const last = [...store.sections].sort((a, b) => b.completedAt - a.completedAt)[0]
    if (!last) return
    loadPlan(last.planId).then((p) => {
      const sec = p.sections.find((x) => x.id === last.sectionId)
      reEntrySection = sec ? { title: sec.title, summary: sec.summary } : null
    }).catch(() => (reEntrySection = null))
  })

  const shownTotal = $derived(debugTree >= 0 ? debugTree : total)
  const shownPlanted = $derived(debugTree >= 0 ? [...ORDER, LIFE] : planted)
  const firstTree = $derived(progress(shownTotal).done === 0)

  // a tree is grown but the next one is not chosen yet
  let choiceHidden = $state(false)
  const pending = $derived(debugTree < 0 && plan !== null && choicePending(total, planted))

  const labels = ['M', 'D', 'M', 'D', 'F', 'S', 'S']
</script>

<div class="page home">
  <header class="row top">
    <h1 class="t-hs grow">Manna</h1>
    <button class="icon-btn" onclick={() => router.go('album')} aria-label="Sammlung"><Icon name="cards" /></button>
    <button class="icon-btn" onclick={() => router.go('plans')} aria-label="Lesepläne"><Icon name="book" /></button>
    <button class="icon-btn" onclick={() => router.go('settings')} aria-label="Einstellungen"><Icon name="settings" /></button>
  </header>

  {#if firstTree}
    <MustardTree sections={shownTotal} {animate} style="flex:1;min-height:35dvh;margin:8px 0" />
  {:else}
    <GardenView total={shownTotal} planted={shownPlanted} {animate} corner={0} style="width:100%;aspect-ratio:1/1.02" />
  {/if}

  {#if plan}
    <div class="content bottom">
      <div class="row" style="justify-content:center;gap:10px">
        <span class="t-bl muted center">{total === 0 ? 'Ein Senfkorn. Mit jedem Abschnitt wächst es.' : total === 1 ? '1 Abschnitt gelesen' : `${total} Abschnitte gelesen`}</span>
        {#if readToday}
          <span class="today"><Icon name="check" size={14} color="var(--primary)" />heute</span>
        {/if}
      </div>

      <!-- seven dots for the week; read days are filled, nothing is ever marked as „missed“ -->
      <div class="row week">
        {#each week as read, i (i)}
          <div class="day">
            <span class="dot" class:read class:today={i === weekdayIndex(today)}></span>
            <span class="lbl" class:bold={i === weekdayIndex(today)}>{labels[i]}</span>
          </div>
        {/each}
        <span class="t-bm" style="margin-left:10px;color:{weekCount >= settings.weeklyGoal ? 'var(--primary)' : 'var(--on-surface-variant)'}">
          {weekCount >= settings.weeklyGoal ? 'Wochenziel erreicht' : `${weekCount} von ${settings.weeklyGoal} Tagen`}
        </span>
      </div>

      {#if !readToday && settings.anchorText.trim()}
        <p class="t-bm muted center anchor">Nach {settings.anchorText.trim()} lese ich einen Vers.</p>
      {/if}

      <!-- at most one hint at a time – too many cards make starting harder -->
      {#if reEntrySection}
        <div class="hintcard">
          <p class="t-tm">Schön, dass du da bist.</p>
          <p class="t-bm clamp">Zuletzt hast du „{reEntrySection.title}“ gelesen: {reEntrySection.summary}</p>
        </div>
      {:else if install.showHint && total > 0}
        <div class="hintcard">
          <p class="t-tm">Manna auf den Home-Bildschirm</p>
          <p class="t-bm">Dann startet Manna wie eine App – und dein Garten bleibt sicher gespeichert.</p>
          <div class="row" style="justify-content:flex-end">
            <button class="btn text" style="opacity:0.75;color:inherit" onclick={() => install.dismiss()}>Nicht jetzt</button>
            <button class="btn text" style="color:inherit" onclick={() => router.go('install')}>So geht’s</button>
          </div>
        </div>
      {/if}

      <div class="card-lg stack-8">
        <p class="t-ll primary">{plan.title}</p>
        {#if next}
          {#if teaser}<p class="t-bl serif italic muted">{teaser}</p>{/if}
          <p class="t-tl">{next.title}</p>
          <p class="t-bm muted">{nextRef}</p>
          <button class="btn tall" style="margin-top:4px" onclick={() => router.go('session')}>{doneInPlan === 0 ? 'Los geht’s' : 'Weiterlesen'}</button>
          <div class="row" style="justify-content:space-between">
            <button class="btn text" onclick={() => router.go('verse')}>Nur 1 Vers</button>
            <button class="btn text" onclick={() => router.go('session/more')}>Mehr am Stück</button>
          </div>
        {:else}
          <p class="t-tl">Plan abgeschlossen</p>
          <p class="muted" style="margin:0">Stark. Such dir aus, wie es weitergeht.</p>
          <button class="btn tall" style="margin-top:4px" onclick={() => router.go('plans')}>Wohin als Nächstes?</button>
        {/if}
      </div>
    </div>
  {/if}
</div>

{#if pending && !choiceHidden}
  <Dialog wide onclose={() => (choiceHidden = true)}>
    <div style="padding:20px">
      <TreeChoice grownId={planted[planted.length - 1]} offers={offers(planted)} {animate} onpick={(id) => store.plant(planted.length, id)} />
    </div>
  </Dialog>
{/if}

<style>
  .home { padding-bottom: calc(16px + var(--safe-bottom)); }
  .top { padding: calc(var(--safe-top) + 8px) 12px 0 24px; }
  .bottom { gap: 0; align-items: stretch; }
  .bottom > .row:first-child { margin-top: 4px; }
  .today {
    display: inline-flex; align-items: center; gap: 4px; padding: 3px 10px; border-radius: 100px;
    background: var(--primary-container); color: var(--on-primary-container); font-size: 12px; font-weight: 600;
  }
  .week { justify-content: center; margin: 10px 0 16px; }
  .day { display: flex; flex-direction: column; align-items: center; padding: 0 5px; }
  .dot { width: 14px; height: 14px; border-radius: 50%; border: 1.5px solid color-mix(in srgb, var(--outline) 50%, transparent); }
  .dot.today, .dot.read { border-color: var(--primary); }
  .dot.read { background: var(--primary); }
  .lbl { font-size: 10px; line-height: 14px; color: var(--on-surface-variant); }
  .lbl.bold { font-weight: 700; }
  .anchor { margin: -6px 0 14px; }
  .hintcard {
    background: var(--secondary-container); color: var(--on-secondary-container); border-radius: 20px; padding: 16px;
    margin-bottom: 12px; display: flex; flex-direction: column; gap: 4px;
  }
  .clamp { display: -webkit-box; -webkit-line-clamp: 3; line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
</style>
