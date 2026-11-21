<script lang="ts">
  import Canvas from './Canvas.svelte'
  import { Anim } from '../util/anim.svelte.ts'
  import { drawMustard } from '../garden/mustard.ts'
  import { theme } from '../ui/theme.svelte.ts'

  /** The mustard seed that grows with every section (shown alone while the first tree grows). */
  let { sections, animateFrom, animate = true, style = '' }: { sections: number; animateFrom?: number; animate?: boolean; style?: string } = $props()

  // svelte-ignore state_referenced_locally
  const anim = new Anim(animateFrom ?? sections)
  $effect(() => {
    const target = sections
    if (animate) void anim.animateTo(target, 1600)
    else anim.snapTo(target)
    return () => anim.stop()
  })
</script>

<div {style}>
  <Canvas label="Senfbaum" draw={(ctx, w, h) => drawMustard(ctx, w, h, anim.value, theme.extra)} />
</div>
