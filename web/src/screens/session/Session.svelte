<script lang="ts">
  import TopBar from '../../lib/components/TopBar.svelte'
  import Icon from '../../lib/components/Icon.svelte'
  import QuizView from '../../lib/components/QuizView.svelte'
  import Sheet from '../../lib/components/Sheet.svelte'
  import MiniMap from '../../lib/components/MiniMap.svelte'
  import ReadStep from './ReadStep.svelte'
  import MemoryStep from './MemoryStep.svelte'
  import RewardStep from './RewardStep.svelte'
  import DoneStep from './DoneStep.svelte'
  import { Session } from './session.svelte.ts'
  import { TRANSLATION } from '../../lib/data/content.ts'
  import { confetti } from '../../lib/ui/confetti.svelte.ts'
  import { router } from '../../lib/router.svelte.ts'

  let { more = false }: { more?: boolean } = $props()

  // svelte-ignore state_referenced_locally
  const s = new Session(more)
  let showExplain = $state(false)
  let showMap = $state(false)
  let openExplain = $state(0)

  const close = () => { s.saveReflection(); router.home() }
  const explains = $derived((s.section?.explain ?? []).filter((e) => !e.translation || e.translation === TRANSLATION))
  const quizCount = $derived(s.section?.quiz?.length ?? 0)
  const quiz = $derived.by(() => {
    const q = s.section?.quiz?.[s.quizIndex]
    if (!q) return null
    const quote = s.quotes[s.quizIndex]
    return quote !== undefined ? { ...q, quote } : q
  })
</script>

<div class="page">
  <TopBar title={s.plan?.title ?? ''} close onback={close}>
    {#snippet actions()}
      {#if explains.length && s.step !== 'DONE' && s.step !== 'REVIEW'}
        <button class="btn text" onclick={() => { openExplain = 0; showExplain = true }}>
          <Icon name="help" size={18} />Versteh ich nicht
        </button>
      {/if}
    {/snippet}
  </TopBar>

  {#if s.loading}
    <div class="spinner"></div>
  {:else}
    {#key `${s.step}-${s.section?.id}`}
      {#if s.step === 'REVIEW' && s.review}
        {@const r = s.review}
        <div class="content stack-16 enter" style="padding-top:8px;padding-bottom:40px">
          <h2 class="t-hm">Erinnerst du dich?</h2>
          <p class="muted" style="margin:0">Eine Frage aus „{r.sectionTitle}“ – zum Warmwerden.</p>
          <QuizView quiz={r.quiz} qkey={`review-${r.planId}-${r.sectionId}-${r.index}`}
            onsolved={(first) => { s.reviewSolved(first); confetti.fire() }} onnext={() => s.reviewDone()} nextLabel="Jetzt lesen" />
          <button class="btn text" style="align-self:center" onclick={() => s.reviewDone()}>Überspringen</button>
        </div>
      {:else if s.step === 'READ'}
        <div class="enter"><ReadStep {s} onmap={() => (showMap = true)} /></div>
      {:else if s.step === 'QUIZ' && quiz}
        <div class="content stack-18 enter" style="padding-top:8px;padding-bottom:48px">
          {#if quizCount > 1}<p class="t-lm muted">Frage {s.quizIndex + 1} von {quizCount}</p>{/if}
          {#key s.quizIndex}
            <QuizView {quiz} qkey={`${s.section?.id}-${s.quizIndex}`} verses={s.verses}
              onsolved={(first) => { s.quizSolved(first); confetti.fire() }} onnext={() => s.nextQuiz()}
              nextLabel={s.quizIndex + 1 < quizCount ? 'Nächste Frage' : 'Weiter'} />
          {/key}
        </div>
      {:else if s.step === 'REWARD'}
        <RewardStep {s} />
      {:else if s.step === 'MEMORY'}
        <MemoryStep {s} />
      {:else if s.step === 'RECAP' && s.recap}
        <div class="content stack-18 enter" style="padding-top:8px;padding-bottom:48px">
          <h2 class="t-hm">Etappe geschafft</h2>
          <p class="muted" style="margin:0">Ein kurzer Blick zurück auf „{s.recapStageTitle ?? 'diese Etappe'}“ hilft, das Ganze zu behalten.</p>
          <QuizView quiz={s.recap} qkey={`recap-${s.section?.id}`} onsolved={() => confetti.fire()} onnext={() => s.recapDone()} />
        </div>
      {:else if s.step === 'DONE'}
        <DoneStep {s} onclose={close} onchooseplan={() => { s.saveReflection(); router.replace('plans') }} />
      {/if}
    {/key}
  {/if}
</div>

{#if showMap && s.place}
  <Sheet onclose={() => (showMap = false)}>
    <div class="stack-12">
      <h2 class="t-tl">Wo sind wir?</h2>
      <MiniMap place={s.place} reference={s.reference} style="width:100%;height:300px;border-radius:18px;overflow:hidden" />
      <p class="t-tm">{s.place.name}</p>
      {#if s.place.text}<p class="muted" style="margin:0">{s.place.text}</p>{/if}
    </div>
  </Sheet>
{/if}

{#if showExplain}
  <Sheet onclose={() => (showExplain = false)}>
    <h2 class="t-tl" style="padding-bottom:8px">Hilfe zum Abschnitt</h2>
    {#each explains as e, i (i)}
      <button class="explain" onclick={() => (openExplain = openExplain === i ? -1 : i)} aria-expanded={openExplain === i}>
        <span class="row" style="gap:8px">
          <span class="t-tm grow">{e.q}</span>
          <Icon name={openExplain === i ? 'expandLess' : 'expandMore'} />
        </span>
        {#if openExplain === i}<span class="t-bl muted enter" style="display:block;padding-top:6px">{e.a}</span>{/if}
      </button>
      {#if i < explains.length - 1}<hr class="divider" />{/if}
    {/each}
  </Sheet>
{/if}

<style>
  .explain { display: block; width: 100%; text-align: left; border: 0; background: transparent; padding: 10px 0; cursor: pointer; }
</style>
