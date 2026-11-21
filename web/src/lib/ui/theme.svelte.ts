import { store } from '../data/store.svelte.ts'

/** Material color scheme of the Android app (ui/theme/Theme.kt). */
const LIGHT = {
  primary: '#2F6B4F', onPrimary: '#FFFFFF', primaryContainer: '#D3EADB', onPrimaryContainer: '#0E2C1E',
  secondary: '#B8860B', onSecondary: '#FFFFFF', secondaryContainer: '#F6E7B8', onSecondaryContainer: '#3A2B00',
  tertiary: '#7A5C3E', background: '#FAF7F0', onBackground: '#1F1D1A', surface: '#FFFDF8', onSurface: '#1F1D1A',
  surfaceVariant: '#EFEADF', onSurfaceVariant: '#55514A', surfaceContainer: '#F3EFE6', surfaceContainerHigh: '#ECE7DC',
  outline: '#B9B2A5', error: '#B4532A', errorContainer: '#FBE3D6', onErrorContainer: '#4A1A05',
}

const DARK: typeof LIGHT = {
  primary: '#8FCDAA', onPrimary: '#0B2A1C', primaryContainer: '#1E4A35', onPrimaryContainer: '#D3EADB',
  secondary: '#E7C15C', onSecondary: '#3A2B00', secondaryContainer: '#4D3C0C', onSecondaryContainer: '#F6E7B8',
  tertiary: '#D7B898', background: '#15171A', onBackground: '#E8E4DC', surface: '#1B1E21', onSurface: '#E8E4DC',
  surfaceVariant: '#2A2D30', onSurfaceVariant: '#BDB7AD', surfaceContainer: '#212427', surfaceContainerHigh: '#282B2F',
  outline: '#5C5953', error: '#F0A27E', errorContainer: '#5A2A14', onErrorContainer: '#FBE3D6',
}

/** Extra colors not covered by Material (plants, maps). */
export interface MannaColors {
  leaf: string; leafDark: string; trunk: string; blossom: string; ground: string; success: string
  sea: string; land: string; river: string; marker: string; dark: boolean
}

const LIGHT_EXTRA: MannaColors = {
  leaf: '#5E9E62', leafDark: '#3F7A4A', trunk: '#7A5C3E', blossom: '#E8B931', ground: '#D9CFBD', success: '#2F7D4F',
  sea: '#CFE0E8', land: '#F1E8D4', river: '#7FA7C2', marker: '#B4532A', dark: false,
}
const DARK_EXTRA: MannaColors = {
  leaf: '#7FBF84', leafDark: '#5A9B66', trunk: '#B08A63', blossom: '#F2C94C', ground: '#3A3631', success: '#8FCDAA',
  sea: '#15212B', land: '#3B372F', river: '#5B8BA8', marker: '#F0A27E', dark: true,
}

const media = typeof matchMedia === 'function' ? matchMedia('(prefers-color-scheme: dark)') : null

class Theme {
  systemDark = $state(media?.matches ?? false)
  dark = $derived(store.settings.theme === 'DARK' || (store.settings.theme === 'SYSTEM' && this.systemDark))
  scheme = $derived(this.dark ? DARK : LIGHT)
  extra = $derived(this.dark ? DARK_EXTRA : LIGHT_EXTRA)

  constructor() {
    media?.addEventListener('change', (e) => (this.systemDark = e.matches))
  }

  /** Writes the scheme as CSS variables (--primary, --on-primary, …) on the root element. */
  apply() {
    const root = document.documentElement
    for (const [k, v] of Object.entries({ ...this.scheme, ...this.extra })) {
      if (typeof v !== 'string') continue
      root.style.setProperty('--' + k.replace(/[A-Z]/g, (c) => '-' + c.toLowerCase()), v)
    }
    root.style.colorScheme = this.dark ? 'dark' : 'light'
    root.style.setProperty('--text-scale', String(store.settings.textScale))
    document.querySelector('meta[name="theme-color"]')?.setAttribute('content', this.scheme.background)
  }
}

export const theme = new Theme()

/** "#rrggbb" + alpha → rgba(). */
export function alpha(hex: string, a: number): string {
  const n = parseInt(hex.slice(1, 7), 16)
  return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`
}
