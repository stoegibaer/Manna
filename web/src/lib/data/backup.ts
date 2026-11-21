import { store } from './store.svelte.ts'
import { DEFAULT_SETTINGS, type Settings } from './types.ts'
import { isoDate } from '../util/date.ts'

/**
 * Backup file (manna-sicherung-<date>.json) – the same format as the Android app (data/backup/Backup.kt),
 * so progress can move between iPhone and Android in both directions.
 */
const FORMAT = 'manna-backup'
export const WEB_VERSION = '0.1.0'

export class BackupError extends Error {}

export const suggestedFileName = () => `manna-sicherung-${isoDate()}.json`

export function exportJson(): string {
  const file = {
    format: FORMAT,
    version: 1,
    appVersion: `web-${WEB_VERSION}`,
    exportedAt: Date.now(),
    sections: store.sections,
    rereads: store.rereads,
    quiz: store.quiz,
    cards: store.cards,
    days: store.days,
    favorites: store.favorites,
    journal: store.journal,
    garden: store.garden,
    settings: store.settings,
  }
  return JSON.stringify(file, null, 2)
}

/** Saves the backup: share sheet on the iPhone (→ „In Dateien sichern“), download elsewhere. */
export async function saveBackup(): Promise<string> {
  const name = suggestedFileName()
  const blob = new Blob([exportJson()], { type: 'application/json' })
  const file = new File([blob], name, { type: 'application/json' })
  const nav = navigator as Navigator & { canShare?: (d: ShareData) => boolean }
  if (nav.canShare?.({ files: [file] }) && /iPhone|iPad|iPod|Android/i.test(navigator.userAgent)) {
    try {
      await nav.share({ files: [file], title: name })
      return 'Sicherung erstellt.'
    } catch (e) {
      if ((e as DOMException).name === 'AbortError') return 'Abgebrochen – nichts gespeichert.'
    }
  }
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = name
  document.body.appendChild(a)
  a.click()
  a.remove()
  setTimeout(() => URL.revokeObjectURL(url), 10_000)
  return 'Sicherung gespeichert.'
}

const n = (x: number, one: string, many: string) => `${x} ${x === 1 ? one : many}`

/** Import **merges**: nothing already on the device is lost. Settings are taken from the file. */
export async function importBackup(f: File): Promise<string> {
  let text: string
  try { text = await f.text() } catch { throw new BackupError('Die Datei konnte nicht gelesen werden.') }
  let file: Record<string, unknown>
  try { file = JSON.parse(text) } catch { throw new BackupError('Diese Datei ist keine Manna-Sicherung.') }
  if (!file || file.format !== FORMAT) throw new BackupError('Diese Datei ist keine Manna-Sicherung.')
  if (typeof file.version === 'number' && file.version > 1) {
    throw new BackupError('Diese Sicherung stammt aus einer neueren Version von Manna. Bitte lade die Seite neu, um zu aktualisieren.')
  }
  const list = <T>(k: string) => (Array.isArray(file[k]) ? (file[k] as T[]) : [])
  const r = store.mergeBackup({
    sections: list('sections'), rereads: list('rereads'), quiz: list('quiz'), cards: list('cards'), days: list('days'),
    favorites: list('favorites'), journal: list('journal'), garden: list('garden'),
  })
  const s = file.settings as Partial<Settings> | undefined
  if (s && typeof s === 'object') {
    store.updateSettings((cur) => ({ ...DEFAULT_SETTINGS, ...s, rereads: { ...(s.rereads ?? {}) }, energyDate: cur.energyDate, energy: cur.energy }))
  }
  const parts = [
    r.sections && n(r.sections, 'neuer Abschnitt', 'neue Abschnitte'),
    r.cards && n(r.cards, 'Karte', 'Karten'),
    r.favorites && n(r.favorites, 'Vers', 'Verse'),
    r.journal && n(r.journal, 'Tagebucheintrag', 'Tagebucheinträge'),
  ].filter(Boolean)
  const what = parts.length ? `Sicherung eingelesen: ${parts.join(', ')}.` : 'Sicherung eingelesen – es war schon alles auf dem Gerät.'
  return what + (s ? ' Einstellungen übernommen.' : '')
}
