<script lang="ts">
  import { onMount } from 'svelte'
  import CardTile from '../../lib/components/CardTile.svelte'
  import GardenView from '../../lib/components/GardenView.svelte'
  import MustardTree from '../../lib/components/MustardTree.svelte'
  import SingleTree from '../../lib/components/SingleTree.svelte'
  import TreeChoice from '../../lib/components/TreeChoice.svelte'
  import { feedback } from '../../lib/audio/feedback.ts'
  import { LIFE, PER_FRUIT, CITY_STEPS, TREES, choicePending, offers, progress } from '../../lib/data/garden.ts'
  import { store } from '../../lib/data/store.svelte.ts'
  import { animations } from '../../lib/data/types.ts'
  import { treeTitle } from '../../lib/garden/trees.ts'
  import { confetti } from '../../lib/ui/confetti.svelte.ts'
  import type { Session } from './session.svelte.ts'

  let { s }: { s: Session } = $props()
  const animate = $derived(animations(store.settings))
  const before = $derived(progress(s.totalBefore))
  const after = $derived(progress(s.totalAfter))
  const grew = $derived(s.totalAfter > s.totalBefore)
  let shownCards = $state(0)

  onMount(() => {
    feedback.sectionDone()
    confetti.fire(true)
    if (!animate) { shownCards = s.newCards.length; return }
    const timers = s.newCards.map((_, i) => setTimeout(() => (shownCards = i + 1), 500 + i * 350))
    return () => timers.forEach(clearTimeout)
  })

  /** Text for the finale of the tree of life and the fruits afterwards. */
  function fruitText(fruits: number) {
    if (fruits >= CITY_STEPS) return 'Die goldene Stadt steht am Horizont. Die Früchte reifen weiter, Monat für Monat.'
    if (fruits > 0) return 'Mit jeder Frucht kommt die goldene Stadt ein Stück näher (Offb 21,2).'
    return `Ab jetzt reift alle ${PER_FRUIT} Abschnitte eine Frucht.`
  }
</script>

<div class="content enter reward">
  {#if s.planted.length}
    {#if choicePending(s.totalAfter, s.planted)}
      <h2 class="t-hm center">Abschnitt geschafft</h2>
      <TreeChoice grownId={s.planted[s.planted.length - 1]} offers={offers(s.planted)} {animate} onpick={(id) => s.plant(id)} />
    {:else if after.done > TREES && before.done === TREES}
      <SingleTree id={LIFE} from={before.t} to={1} {animate} finale style="width:100%;height:260px" />
      <h2 class="t-hm center">Abschnitt geschafft</h2>
      <p class="t-bl muted center">Dein Baum des Lebens ist ausgewachsen. {fruitText(0)}</p>
    {:else if after.done > TREES}
      <GardenView total={s.totalAfter} planted={s.planted} {animate} style="width:100%;height:300px" />
      <h2 class="t-hm center">Abschnitt geschafft</h2>
      <p class="t-bl muted center">
        {after.fruits > before.fruits ? `Eine neue Frucht ist gereift. ${fruitText(after.fruits)}` : grew ? 'Die nächste Frucht reift schon.' : 'Nochmal gelesen – gut so.'}
      </p>
    {:else if after.done === 0}
      <!-- the first tree: the mustard tree alone -->
      <MustardTree sections={s.totalAfter} animateFrom={s.totalBefore} {animate} style="width:100%;height:260px" />
      <h2 class="t-hm center">Abschnitt geschafft</h2>
      <p class="t-bl muted center">{grew ? 'Dein Senfkorn ist gewachsen.' : 'Nochmal gelesen – gut so.'}</p>
    {:else if s.planted[after.done]}
      {@const id = s.planted[after.done]}
      <SingleTree {id} from={before.done === after.done ? before.t : 0} to={after.t} {animate} finale={false} style="width:100%;height:260px" />
      <h2 class="t-hm center">Abschnitt geschafft</h2>
      <p class="t-bl muted center">
        {after.done > before.done ? `${treeTitle(id)} ist gepflanzt.` : grew ? `${treeTitle(id)} ist gewachsen.` : 'Nochmal gelesen – gut so.'}
      </p>
    {/if}
  {/if}

  {#if s.newCards.length}
    <p class="t-ll primary" style="align-self:stretch;padding-top:8px">{s.newCards.length === 1 ? 'Neue Karte für deine Sammlung' : 'Neue Karten für deine Sammlung'}</p>
    {#each s.newCards.slice(0, shownCards) as card (card.id)}
      <div class="enter" style="width:100%"><CardTile {card} /></div>
    {/each}
  {/if}

  {#if s.section?.fact}
    <div class="card stack-6" style="width:100%">
      <p class="t-ll secondary">Wusstest du?</p>
      <p class="t-bl">{s.section.fact}</p>
    </div>
  {/if}
  <button class="btn" style="margin-top:4px" onclick={() => s.rewardContinue()}>Weiter</button>
</div>

<style>
  .reward { align-items: center; gap: 16px; padding-top: 8px; padding-bottom: 32px; }
  .stack-6 { display: flex; flex-direction: column; gap: 6px; }
</style>
