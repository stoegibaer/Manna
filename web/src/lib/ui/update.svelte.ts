import { registerSW } from 'virtual:pwa-register'

/** Service worker: works offline; offers „Neu laden“ when a new version was published. */
class Update {
  needed = $state(false)
  private reload: ((reload?: boolean) => Promise<void>) | null = null

  start() {
    if (!('serviceWorker' in navigator)) return
    this.reload = registerSW({
      immediate: true,
      onNeedRefresh: () => (this.needed = true),
      onRegisteredSW: (_url, reg) => {
        // look for a new version now and then (installed apps stay open for a long time)
        if (reg) setInterval(() => void reg.update(), 60 * 60 * 1000)
      },
    })
  }

  apply() {
    this.needed = false
    void this.reload?.(true)
  }
}

export const update = new Update()
