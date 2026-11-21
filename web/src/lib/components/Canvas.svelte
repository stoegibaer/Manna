<script lang="ts">
  /**
   * A canvas in CSS pixels (sharp on retina). [draw] runs inside an effect, so every reactive value it
   * reads (animations, theme, data) repaints it automatically.
   */
  let { draw, class: cls = '', style = '', label, onpointerdown, onclick, ondblclick, ontouchstart, onwheel, el = $bindable() }: {
    draw: (ctx: CanvasRenderingContext2D, w: number, h: number) => void
    class?: string; style?: string; label?: string
    onpointerdown?: (e: PointerEvent) => void
    onclick?: (e: MouseEvent) => void
    ondblclick?: (e: MouseEvent) => void
    ontouchstart?: (e: TouchEvent) => void
    onwheel?: (e: WheelEvent) => void
    el?: HTMLCanvasElement
  } = $props()

  let canvas: HTMLCanvasElement
  let w = $state(0)
  let h = $state(0)

  $effect(() => {
    el = canvas
    const ro = new ResizeObserver(() => {
      w = canvas.clientWidth
      h = canvas.clientHeight
    })
    ro.observe(canvas)
    return () => ro.disconnect()
  })

  $effect(() => {
    if (!w || !h) return
    const dpr = Math.min(3, window.devicePixelRatio || 1)
    const pw = Math.round(w * dpr), ph = Math.round(h * dpr)
    if (canvas.width !== pw) canvas.width = pw
    if (canvas.height !== ph) canvas.height = ph
    const ctx = canvas.getContext('2d')
    if (!ctx) return
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
    ctx.clearRect(0, 0, w, h)
    draw(ctx, w, h)
  })
</script>

<canvas bind:this={canvas} class={cls} {style} role={label ? 'img' : undefined} aria-label={label} {onpointerdown} {onclick} {ondblclick} {ontouchstart} {onwheel}></canvas>

<style>
  canvas { display: block; width: 100%; height: 100%; }
</style>
