/**
 * Tiny hash router. Every screen has its own back button (an installed web app on the iPhone has no
 * browser back button), and the browser's back still works where there is one.
 * history.state.depth counts the screens above the home screen.
 */
function current(): string {
  return decodeURI(location.hash.replace(/^#\/?/, ''))
}

class Router {
  path = $state(current())

  constructor() {
    window.addEventListener('popstate', () => (this.path = current()))
    window.addEventListener('hashchange', () => (this.path = current()))
  }

  private get depth(): number {
    return (history.state?.depth as number | undefined) ?? (this.path ? 1 : 0)
  }

  /** Opens a screen on top of the current one. */
  go(path: string) {
    history.pushState({ depth: this.depth + 1 }, '', '#/' + path)
    this.path = path
    window.scrollTo(0, 0)
  }

  /** Replaces the current screen (like popUpTo on Android): back then leads to the screen below. */
  replace(path: string) {
    history.replaceState({ depth: this.depth }, '', path ? '#/' + path : location.pathname + location.search)
    this.path = path
    window.scrollTo(0, 0)
  }

  back() {
    if (((history.state?.depth as number | undefined) ?? 0) > 0) history.back()
    else this.replace('')
  }

  home() {
    const d = (history.state?.depth as number | undefined) ?? 0
    if (d > 0) history.go(-d)
    else this.replace('')
  }
}

export const router = new Router()
