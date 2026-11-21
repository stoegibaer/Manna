<script lang="ts">
  import Canvas from './Canvas.svelte'
  import SingleTree from './SingleTree.svelte'
  import { drawTree, sceneColors } from '../garden/treeDraw.ts'
  import { treeById } from '../garden/trees.ts'
  import { lifeFruitColor } from '../garden/scene.ts'
  import { LIFE } from '../data/garden.ts'
  import { theme } from '../ui/theme.svelte.ts'

  /**
   * The moment a tree is fully grown: its finale, its verse, and the choice of the next tree.
   * Also shown when fewer than three trees are left, so one always knows what comes next.
   */
  let { grownId, offers, animate, onpick }: { grownId: string; offers: string[]; animate: boolean; onpick: (id: string) => void } = $props()

  const grown = $derived(treeById(grownId))
  const shortVerse = (v: string) => (v.length <= 90 ? v : v.slice(0, 88).replace(/\s\S*$/, '') + ' …')

  function thumb(id: string) {
    return (ctx: CanvasRenderingContext2D, w: number, h: number) =>
      drawTree(ctx, treeById(id), 1, w / 2, h * 0.94, h * 0.95, sceneColors(theme.extra), {
        fruitN: id === LIFE ? 12 : null,
        fruitColor: id === LIFE ? lifeFruitColor(12) : undefined,
      })
  }
</script>

<div class="choice">
  <SingleTree id={grownId} from={1} to={1} {animate} finale style="width:100%;height:240px" />
  <h2 class="t-hs center">{grown.article} {grown.name} ist ausgewachsen</h2>
  <p class="t-bm serif italic muted center">„{grown.verse}“ {grown.ref}</p>
  {#if offers.length}
    <p class="t-ll primary" style="margin-top:8px">
      {offers[0] === LIFE ? 'Zum Schluss wächst am Wasser' : offers.length === 1 ? 'Als Letztes im Garten wächst' : offers.length === 2 ? 'Noch zwei Bäume zur Wahl' : 'Was pflanzt du als Nächstes?'}
    </p>
    {#each offers as id (id)}
      {@const sp = treeById(id)}
      <button class="offer" onclick={() => onpick(id)}>
        <div class="thumb"><Canvas draw={thumb(id)} /></div>
        <div class="grow stack-2">
          <p class="t-tm">{sp.name}</p>
          <p class="t-bs serif italic muted clamp">„{shortVerse(sp.verse)}“</p>
          <p class="t-ls muted">{sp.ref}</p>
          {#if offers.length === 1}<p class="t-lm primary">Antippen zum Pflanzen</p>{/if}
        </div>
      </button>
    {/each}
  {/if}
</div>

<style>
  .choice { display: flex; flex-direction: column; align-items: center; gap: 10px; width: 100%; }
  .offer {
    display: flex; align-items: center; gap: 12px; width: 100%; padding: 8px; border: 0; border-radius: 18px;
    background: var(--surface-container); text-align: left; cursor: pointer;
  }
  .thumb { width: 76px; height: 76px; border-radius: 12px; overflow: hidden; flex: none; }
  .stack-2 { display: flex; flex-direction: column; gap: 2px; }
  .clamp { display: -webkit-box; -webkit-line-clamp: 3; line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
</style>
