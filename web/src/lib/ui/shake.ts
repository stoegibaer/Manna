/** Small horizontal shake for a wrong tap – a gentle "nope", no penalty. */
export function shake(el: Element | null | undefined) {
  if (!el || !(el as HTMLElement).animate || document.documentElement.classList.contains('calm')) return
  ;(el as HTMLElement).animate(
    [{ transform: 'translateX(0)' }, { transform: 'translateX(14px)' }, { transform: 'translateX(-12px)' }, { transform: 'translateX(8px)' }, { transform: 'translateX(-5px)' }, { transform: 'translateX(0)' }],
    { duration: 275, easing: 'linear' },
  )
}
