<script lang="ts">
  import Canvas from './Canvas.svelte'
  import { Anim, Linear } from '../util/anim.svelte.ts'
  import { drawTree, sceneColors } from '../garden/treeDraw.ts'
  import { treeById } from '../garden/trees.ts'
  import { LIFE, ORDER } from '../data/garden.ts'
  import { theme } from '../ui/theme.svelte.ts'

  /**
   * One tree on its own, zoomed so even a sprout fills the frame. Grows from [from] to [to] (0..1).
   * With [finale] the tree's finale moment plays once it is grown.
   */
  let { id, from, to, animate, finale, style = '' }: { id: string; from: number; to: number; animate: boolean; finale: boolean; style?: string } = $props()

  // svelte-ignore state_referenced_locally
  const grow = new Anim(animate ? from : to)
  // svelte-ignore state_referenced_locally
  const fin = new Anim(finale && !animate ? 1 : 0)

  $effect(() => {
    const target = to, f = finale, a = animate
    let alive = true
    ;(async () => {
      if (a) await grow.animateTo(target, 1600)
      else grow.snapTo(target)
      if (f && alive) { if (a) await fin.animateTo(1, 2400, Linear); else fin.snapTo(1) }
    })()
    return () => { alive = false; grow.stop(); fin.stop() }
  })

  function draw(ctx: CanvasRenderingContext2D, w: number, h: number) {
    const sp = treeById(id)
    const sc = sceneColors(theme.extra)
    const t = grow.value
    const unit = Math.min(w * 1.05, h) * 0.95
    // the mustard tree keeps the size it always had, so it does not jump when grown
    const mustard = id === ORDER[0]
    const scale = unit * (mustard ? 1.55 - 0.75 * t : (1.5 - 0.8 * t) * 0.92)
    const rootX = w / 2 - (sp.water ? w * 0.06 : 0)
    ctx.save()
    ctx.beginPath()
    ctx.rect(0, 0, w, h)
    ctx.clip()
    drawTree(ctx, sp, t, rootX, h * 0.93, scale, sc, {
      fin: finale ? fin.value : null,
      water: !!sp.water && t >= 1,
      groundR: mustard ? (0.32 * unit) / scale : 0.3,
      groundRy: mustard ? (0.03 * unit) / scale : undefined,
      fruitN: id === LIFE ? 0 : null,
    })
    ctx.restore()
  }
</script>

<div {style}>
  <Canvas label={treeById(id).name} {draw} />
</div>
