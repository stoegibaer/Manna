import { openDB, type IDBPDatabase } from 'idb'
import { ORDER } from './garden.ts'
import { isoDate, minuteOfDay } from '../util/date.ts'
import {
  DEFAULT_SETTINGS,
  type CardUnlock, type FavoriteVerse, type GardenTree, type JournalEntry, type QuizResult,
  type ReadingDay, type SectionDone, type SectionReread, type Settings,
} from './types.ts'

/** Leitner intervals in days per box. */
const INTERVAL_DAYS = [1, 3, 7, 21, 60]
const DAY_MS = 86_400_000

export const STORES = {
  sections: ['planId', 'sectionId'],
  rereads: ['planId', 'sectionId', 'readAt'],
  quiz: ['planId', 'sectionId', 'quizIndex'],
  cards: ['planId', 'cardId'],
  days: 'date',
  favorites: ['book', 'chapter', 'verse'],
  journal: ['planId', 'sectionId'],
  garden: 'position',
} as const
type StoreName = keyof typeof STORES | 'kv'

const keyOf = (name: keyof typeof STORES, r: object): string => {
  const kp = STORES[name]
  const rec = r as Record<string, unknown>
  return (typeof kp === 'string' ? [kp] : kp).map((k) => String(rec[k])).join('|')
}

/**
 * All user data, held in memory (reactive) and written through to IndexedDB.
 * Mirrors the Android ProgressRepository / SettingsRepository. If IndexedDB is unavailable
 * (e.g. a private window) the app still works for the session.
 */
class Store {
  ready = $state(false)
  /** false when the browser refused IndexedDB – nothing will be kept after closing. */
  persistent = $state(true)

  sections = $state.raw<SectionDone[]>([])
  rereads = $state.raw<SectionReread[]>([])
  quiz = $state.raw<QuizResult[]>([])
  cards = $state.raw<CardUnlock[]>([])
  days = $state.raw<ReadingDay[]>([])
  favorites = $state.raw<FavoriteVerse[]>([])
  journal = $state.raw<JournalEntry[]>([])
  garden = $state.raw<GardenTree[]>([])
  settings = $state.raw<Settings>(DEFAULT_SETTINGS)

  private db: IDBPDatabase | null = null

  async init() {
    try {
      this.db = await openDB('manna', 1, {
        upgrade(db) {
          for (const [name, keyPath] of Object.entries(STORES)) db.createObjectStore(name, { keyPath: keyPath as string | string[] })
          db.createObjectStore('kv')
        },
      })
      const [sections, rereads, quiz, cards, days, favorites, journal, garden, settings] = await Promise.all([
        this.db.getAll('sections'), this.db.getAll('rereads'), this.db.getAll('quiz'), this.db.getAll('cards'),
        this.db.getAll('days'), this.db.getAll('favorites'), this.db.getAll('journal'), this.db.getAll('garden'),
        this.db.get('kv', 'settings'),
      ])
      Object.assign(this, { sections, rereads, quiz, cards, days, favorites, journal, garden })
      this.settings = { ...DEFAULT_SETTINGS, ...(settings ?? {}) }
    } catch (e) {
      console.warn('IndexedDB unavailable', e)
      this.db = null
      this.persistent = false
    }
    this.migrate()
    this.ready = true
  }

  private async put(name: StoreName, value: object, key?: string) {
    try { await this.db?.put(name, value, key) } catch (e) { console.warn('save failed', e) }
  }

  private async del(name: StoreName, key: IDBValidKey) {
    try { await this.db?.delete(name, key) } catch (e) { console.warn('delete failed', e) }
  }

  /** Replaces or inserts [rec] in an in-memory list (by primary key) and stores it. */
  private upsert<K extends keyof typeof STORES>(name: K, rec: Store[K][number]) {
    const list = this[name] as object[]
    const k = keyOf(name, rec)
    const i = list.findIndex((r) => keyOf(name, r) === k)
    const next = i < 0 ? [...list, rec] : list.map((r, j) => (j === i ? rec : r))
    ;(this as unknown as Record<string, object[]>)[name] = next
    void this.put(name, rec)
  }

  /** Inserts [rec] unless its key exists already (OnConflictStrategy.IGNORE). @return true if inserted. */
  private insert<K extends keyof typeof STORES>(name: K, rec: Store[K][number]): boolean {
    const k = keyOf(name, rec)
    if ((this[name] as object[]).some((r) => keyOf(name, r) === k)) return false
    this.upsert(name, rec)
    return true
  }

  // ── settings ──

  updateSettings(f: (s: Settings) => Settings) {
    this.settings = f(this.settings)
    void this.put('kv', { ...this.settings, rereads: { ...this.settings.rereads } }, 'settings')
  }

  // ── progress ──

  /** All sections ever read, re-reads included – the garden grows with every one of them. */
  get totalSections() { return this.sections.length + this.rereads.length }

  doneIds(planId: string): Set<string> {
    return new Set(this.sections.filter((s) => s.planId === planId).map((s) => s.sectionId))
  }

  /**
   * Marks a section as read. A section read before is logged as a re-read, so it still counts for the garden.
   * @return true if the section was newly completed.
   */
  completeSection(planId: string, sectionId: string): boolean {
    const now = Date.now()
    const isNew = this.insert('sections', { planId, sectionId, completedAt: now })
    if (!isNew) this.insert('rereads', { planId, sectionId, readAt: now })
    return isNew
  }

  private quizFor(planId: string, sectionId: string, quizIndex: number) {
    return this.quiz.find((q) => q.planId === planId && q.sectionId === sectionId && q.quizIndex === quizIndex)
  }

  /** Answer in a reading session: new questions come back for review tomorrow; re-reads keep the review progress. */
  recordQuiz(planId: string, sectionId: string, quizIndex: number, firstTry: boolean) {
    const now = Date.now()
    const old = this.quizFor(planId, sectionId, quizIndex)
    this.upsert('quiz', old ? { ...old, firstTry, answeredAt: now } : { planId, sectionId, quizIndex, firstTry, answeredAt: now, box: 0, dueAt: now + DAY_MS })
  }

  /** A review („Erinnerst du dich?“): right on first try moves to the next box, otherwise back to box 0. */
  recordReview(planId: string, sectionId: string, quizIndex: number, correct: boolean) {
    const now = Date.now()
    const old = this.quizFor(planId, sectionId, quizIndex) ?? { planId, sectionId, quizIndex, firstTry: correct, answeredAt: now, box: 0, dueAt: 0 }
    const box = correct ? Math.min(old.box + 1, INTERVAL_DAYS.length - 1) : 0
    this.upsert('quiz', { ...old, box, answeredAt: now, dueAt: now + INTERVAL_DAYS[box] * DAY_MS })
  }

  dueReviews(limit = 20): QuizResult[] {
    const now = Date.now()
    return this.quiz.filter((q) => q.dueAt <= now).sort((a, b) => a.dueAt - b.dueAt).slice(0, limit)
  }

  /** @return ids of cards that were newly unlocked. */
  unlockCards(planId: string, cardIds: string[]): string[] {
    const now = Date.now()
    return cardIds.filter((cardId) => this.insert('cards', { planId, cardId, unlockedAt: now }))
  }

  /** Small data migrations after content updates. Idempotent. */
  private migrate() {
    for (const c of this.cards.filter((c) => c.planId === 'habakuk' && c.cardId === 'jehova')) {
      void this.del('cards', [c.planId, c.cardId])
      this.cards = this.cards.filter((x) => x !== c)
      this.insert('cards', { ...c, cardId: 'gottesname' })
    }
  }

  logReading(verses: number, sections: number) {
    const today = isoDate()
    const d = this.days.find((x) => x.date === today) ?? { date: today, verses: 0, sections: 0, firstMinute: -1 }
    const minute = d.firstMinute < 0 && verses + sections > 0 ? minuteOfDay() : d.firstMinute
    this.upsert('days', { ...d, verses: d.verses + verses, sections: d.sections + sections, firstMinute: minute })
  }

  get readToday(): boolean {
    const d = this.days.find((x) => x.date === isoDate())
    return !!d && (d.verses > 0 || d.sections > 0)
  }

  // ── favorites & journal ──

  favoriteKeys(): Set<string> {
    return new Set(this.favorites.map((f) => `${f.book}-${f.chapter}-${f.verse}`))
  }

  setFavorite(book: number, chapter: number, verse: number, on: boolean, source = 'favorite') {
    if (on) this.upsert('favorites', { book, chapter, verse, savedAt: Date.now(), source })
    else {
      this.favorites = this.favorites.filter((f) => !(f.book === book && f.chapter === chapter && f.verse === verse))
      void this.del('favorites', [book, chapter, verse])
    }
  }

  journalFor(planId: string, sectionId: string) {
    return this.journal.find((j) => j.planId === planId && j.sectionId === sectionId)
  }

  saveJournal(planId: string, sectionId: string, sectionTitle: string, tags: Set<string>, note: string) {
    this.upsert('journal', { planId, sectionId, sectionTitle, tags: [...tags].join(','), note: note.trim(), savedAt: Date.now() })
  }

  // ── garden ──

  /** Planted species by position, starting with the mustard tree. */
  get planted(): string[] {
    return [ORDER[0], ...[...this.garden].sort((a, b) => a.position - b.position).map((t) => t.species)]
  }

  /** Plants [species] at [position]. Ignored if that position is already planted (e.g. a double tap). */
  plant(position: number, species: string) {
    this.insert('garden', { position, species, plantedAt: Date.now() })
  }

  // ── backup ──

  /** Merges records from a backup: nothing on the device is lost; for entries on both sides the more recent one wins. */
  mergeBackup(f: {
    sections: SectionDone[]; rereads: SectionReread[]; quiz: QuizResult[]; cards: CardUnlock[]; days: ReadingDay[]
    favorites: FavoriteVerse[]; journal: JournalEntry[]; garden: GardenTree[]
  }) {
    const sections = f.sections.filter((s) => this.insert('sections', s)).length + f.rereads.filter((r) => this.insert('rereads', r)).length
    const cards = f.cards.filter((c) => this.insert('cards', c)).length
    for (const t of f.garden) this.insert('garden', t)
    for (const q of f.quiz) {
      const old = this.quizFor(q.planId, q.sectionId, q.quizIndex)
      if (!old || q.answeredAt > old.answeredAt) this.upsert('quiz', { ...q, box: q.box ?? 0, dueAt: q.dueAt ?? 0 })
    }
    for (const d of f.days) {
      const old = this.days.find((x) => x.date === d.date)
      const firstMinute = d.firstMinute ?? -1
      if (!old) this.upsert('days', { ...d, firstMinute })
      else {
        const mins = [old.firstMinute, firstMinute].filter((m) => m >= 0)
        this.upsert('days', { date: d.date, verses: Math.max(old.verses, d.verses), sections: Math.max(old.sections, d.sections), firstMinute: mins.length ? Math.min(...mins) : -1 })
      }
    }
    let favorites = 0
    for (const v of f.favorites) {
      const old = this.favorites.find((x) => x.book === v.book && x.chapter === v.chapter && x.verse === v.verse)
      if (!old) favorites++
      if (!old || v.savedAt > old.savedAt) this.upsert('favorites', { ...v, source: v.source ?? 'favorite' })
    }
    let journal = 0
    for (const j of f.journal) {
      const old = this.journalFor(j.planId, j.sectionId)
      if (!old) journal++
      if (!old || j.savedAt > old.savedAt) this.upsert('journal', j)
    }
    return { sections, cards, favorites, journal }
  }
}

export const store = new Store()
