/** Whether Manna runs as an installed app, and the „Zum Home-Bildschirm“ hint. */
const KEY = 'manna.installHintDismissed'

function read(): boolean {
  try { return localStorage.getItem(KEY) === '1' } catch { return false }
}

interface BeforeInstallPrompt extends Event { prompt: () => Promise<void> }

class Install {
  standalone = $state(
    (typeof matchMedia === 'function' && matchMedia('(display-mode: standalone)').matches) ||
      (navigator as Navigator & { standalone?: boolean }).standalone === true,
  )
  dismissed = $state(read())
  /** Chrome/Android: the browser's own install dialog. */
  prompt = $state.raw<BeforeInstallPrompt | null>(null)
  readonly ios = /iPhone|iPad|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)

  get showHint() { return !this.standalone && !this.dismissed }

  constructor() {
    window.addEventListener('beforeinstallprompt', (e) => { e.preventDefault(); this.prompt = e as BeforeInstallPrompt })
    window.addEventListener('appinstalled', () => (this.standalone = true))
  }

  dismiss() {
    this.dismissed = true
    try { localStorage.setItem(KEY, '1') } catch { /* private mode */ }
  }
}

export const install = new Install()
