<script lang="ts">
  import TopBar from '../lib/components/TopBar.svelte'
  import Icon from '../lib/components/Icon.svelte'
  import VerseText from '../lib/components/VerseText.svelte'
  import { onDestroy } from 'svelte'
  import { bibleInfo, chapterVerses, type TranslationInfo, type Verse } from '../lib/data/content.ts'
  import { store } from '../lib/data/store.svelte.ts'
  import { Speaker, canSpeak } from '../lib/audio/speaker.svelte.ts'
  import { feedback } from '../lib/audio/feedback.ts'
  import { router } from '../lib/router.svelte.ts'

  /** Free reading in the whole Bible – no quiz, same reading aids. Books → chapters → chapter. */
  let { book, chapter }: { book?: number; chapter?: number } = $props()

  let info = $state.raw<TranslationInfo | null>(null)
  $effect(() => { void bibleInfo().then((i) => (info = i)) })
  const b = $derived(info?.books.find((x) => x.nr === book))

  let verses = $state.raw<Verse[]>([])
  let read = $state(false)
  $effect(() => {
    if (book && chapter) {
      verses = []
      read = false
      void chapterVerses(book, chapter).then((v) => (verses = v))
    }
  })

  const favorites = $derived(store.favoriteKeys())
  const speaker = new Speaker()
  onDestroy(() => speaker.stop())
  $effect(() => {
    const i = speaker.current
    const el = i >= 0 ? document.querySelector(`[data-verse="${i}"]`) : null
    if (el) window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - 90, behavior: 'smooth' })
  })

  function toggleFavorite(v: Verse) {
    store.setFavorite(v.book, v.chapter, v.verse, !favorites.has(`${v.book}-${v.chapter}-${v.verse}`))
    feedback.correct()
  }

  /** Counts for the daily minimum and the week. */
  function markRead() {
    if (read) return
    read = true
    store.logReading(verses.length, 0)
    feedback.sectionDone()
  }

  function goChapter(ch: number) {
    speaker.stop()
    router.replace(`bible/${book}/${ch}`)
  }
</script>

<div class="page">
  {#if !book}
    <TopBar title="Ganze Bibel" onback={() => router.back()} />
    <div class="content" style="padding:0 20px 32px">
      {#each [['Altes Testament', 1, 39], ['Neues Testament', 40, 66]] as [label, from, to] (label)}
        <h2 class="t-tl" style="padding:12px 0 4px">{label}</h2>
        <div class="grid2">
          {#each (info?.books ?? []).filter((x) => x.nr >= (from as number) && x.nr <= (to as number)) as bk (bk.nr)}
            <button class="book" onclick={() => router.go(`bible/${bk.nr}`)}>{bk.name}</button>
          {/each}
        </div>
      {/each}
      {#if info}<p class="t-bs muted" style="padding-top:16px">{info.name}</p>{/if}
    </div>
  {:else if !chapter}
    <TopBar title={b?.name ?? ''} onback={() => router.back()} />
    {#if b}
      <div class="chapters">
        {#each Array.from({ length: b.chapters }, (_, i) => i + 1) as ch (ch)}
          <button class="ch t-tm" onclick={() => router.go(`bible/${book}/${ch}`)}>{ch}</button>
        {/each}
      </div>
    {/if}
  {:else}
    <TopBar title={`${b?.name ?? ''} ${chapter}`} onback={() => router.back()}>
      {#snippet actions()}
        {#if canSpeak}
          <button class="icon-btn" onclick={() => speaker.toggle(verses, 0)} aria-label={speaker.playing ? 'Stopp' : 'Vorlesen'}>
            <Icon name={speaker.playing ? 'stop' : 'volume'} />
          </button>
        {/if}
      {/snippet}
    </TopBar>
    {#if !verses.length}
      <div class="spinner"></div>
    {:else}
      <div class="verses">
        {#each verses as v, i (v.verse)}
          <div data-verse={i}>
            <VerseText verse={v} highlighted={i === speaker.current} favorite={favorites.has(`${v.book}-${v.chapter}-${v.verse}`)} onlongpress={() => toggleFavorite(v)} />
          </div>
        {/each}
        <div style="padding-top:20px" class="stack-12">
          {#if read}
            <div class="row primary" style="gap:8px"><Icon name="check" />Gelesen – zählt für heute.</div>
          {:else}
            <button class="btn" style="height:52px" onclick={markRead}>Kapitel gelesen</button>
          {/if}
          <div class="row" style="justify-content:space-between">
            {#if chapter > 1}
              <button class="btn outline navb" onclick={() => goChapter(chapter - 1)}><Icon name="left" size={18} />Kapitel {chapter - 1}</button>
            {:else}<span></span>{/if}
            {#if b && chapter < b.chapters}
              <button class="btn outline navb" onclick={() => goChapter(chapter + 1)}>Kapitel {chapter + 1}<Icon name="right" size={18} /></button>
            {/if}
          </div>
          <p class="t-bs muted center" style="padding-top:4px">Tipp: Lange auf einen Vers drücken, um ihn zu speichern.</p>
        </div>
      </div>
    {/if}
  {/if}
</div>

<style>
  .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .book { border: 0; text-align: left; padding: 14px 16px; border-radius: 14px; background: var(--surface-container); font-size: 16px; cursor: pointer; }
  .chapters { display: grid; grid-template-columns: repeat(auto-fill, minmax(64px, 1fr)); gap: 8px; padding: 20px; }
  .ch { aspect-ratio: 1; border: 0; border-radius: 14px; background: var(--surface-container); cursor: pointer; }
  .verses { padding: 4px 20px calc(40px + var(--safe-bottom)); display: flex; flex-direction: column; gap: 10px; }
  .navb { width: auto; height: 40px; padding: 0 16px; font-size: 14px; }
</style>
