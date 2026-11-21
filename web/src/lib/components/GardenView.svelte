<script lang="ts">
  import Canvas from './Canvas.svelte'
  import { untrack } from 'svelte'
  import { Anim } from '../util/anim.svelte.ts'
  import { drawGarden, SCENE_ASPECT } from '../garden/scene.ts'
  import { sceneColors } from '../garden/treeDraw.ts'
  import { treeName } from '../garden/trees.ts'
  import { progress, TREES } from '../data/garden.ts'
  import { theme } from '../ui/theme.svelte.ts'

  /** The garden. Grows (animated) when [total] changes; keeps the scene's proportions, centered. */
  let { total, planted, animate, corner = 18, style = '' }: { total: number; planted: string[]; animate: boolean; corner?: number; style?: string } = $props()

  // svelte-ignore state_referenced_locally
  const anim = new Anim(total)
  $effect(() => {
    const target = total
    // only animate growth within one tree; a new tree or a jump is shown directly
    const current = untrack(() => anim.value)
    const same = progress(current).done === progress(target).done
    if (animate && same && target > current) void anim.animateTo(target, 1600)
    else anim.snapTo(target)
    return () => anim.stop()
  })

  const description = $derived.by(() => {
    const g = progress(total)
    const trees = Math.min(g.done, TREES)
    const growing = g.done < TREES
      ? (planted[g.done] ? `Es wächst: ${treeName(planted[g.done])}.` : 'Ein Samenkorn wartet.')
      : g.done === TREES ? 'Am Wasser wächst der Baum des Lebens.' : `Der Baum des Lebens trägt ${g.fruits} Früchte.`
    return `Garten mit ${trees} ${trees === 1 ? 'Baum' : 'Bäumen'}. ${growing}`
  })

  function draw(ctx: CanvasRenderingContext2D, w: number, h: number) {
    const gw = Math.min(w, h / SCENE_ASPECT)
    const gh = gw * SCENE_ASPECT
    const left = (w - gw) / 2, top = (h - gh) / 2
    ctx.save()
    ctx.beginPath()
    ctx.roundRect(left, top, gw, gh, corner)
    ctx.clip()
    ctx.translate(left, top)
    drawGarden(ctx, gw, gh, anim.value, planted, sceneColors(theme.extra))
    ctx.restore()
  }
</script>

<div {style}>
  <Canvas label={description} {draw} />
</div>
