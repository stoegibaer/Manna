// Records stored on the device – same shape as the Android Room entities, so backups move between both apps.

export interface SectionDone { planId: string; sectionId: string; completedAt: number }
/** A section read again (e.g. a finished plan read a second time). Counts for the garden like a new one. */
export interface SectionReread { planId: string; sectionId: string; readAt: number }
/** One answered quiz question, also used for spaced repetition (Leitner boxes). */
export interface QuizResult { planId: string; sectionId: string; quizIndex: number; firstTry: boolean; answeredAt: number; box: number; dueAt: number }
export interface CardUnlock { planId: string; cardId: string; unlockedAt: number }
/** Per-day reading log (date = ISO yyyy-MM-dd). [firstMinute] = minute of the first reading, -1 unknown. */
export interface ReadingDay { date: string; verses: number; sections: number; firstMinute: number }
/** [source] = "favorite" (long-press) or "memory" (learned memory verse). */
export interface FavoriteVerse { book: number; chapter: number; verse: number; savedAt: number; source: string }
/** [tags] comma separated chip ids. */
export interface JournalEntry { planId: string; sectionId: string; sectionTitle: string; tags: string; note: string; savedAt: number }
/** A tree planted in the garden. Position 0 (mustard tree) is implicit and never stored. */
export interface GardenTree { position: number; species: string; plantedAt: number }

export type ThemeMode = 'SYSTEM' | 'LIGHT' | 'DARK'

/**
 * Same fields as the Android app's Settings. Reminder-related fields have no effect on the web
 * (no notifications there) but are kept so a backup keeps them when moving back to Android.
 */
export interface Settings {
  focusMode: boolean
  haptics: boolean
  sound: boolean
  confetti: boolean
  calm: boolean
  textScale: number
  theme: ThemeMode
  ttsRate: number
  activePlan: string
  remindersOn: boolean
  reminderSetupSeen: boolean
  anchorText: string
  anchorMinute: number
  planB: string
  quietMinute: number
  weeklyGoal: number
  pausedDate: string
  suggestionHiddenUntil: string
  dndWhileReading: boolean
  energyDate: string
  energy: string
  /** Finished plans read again: plan id → index of the next section in this run. */
  rereads: Record<string, number>
}

export const DEFAULT_SETTINGS: Settings = {
  focusMode: true,
  haptics: true,
  sound: true,
  confetti: true,
  calm: false,
  textScale: 1,
  theme: 'SYSTEM',
  ttsRate: 1,
  activePlan: '',
  remindersOn: false,
  reminderSetupSeen: false,
  anchorText: '',
  anchorMinute: 7 * 60 + 30,
  planB: '',
  quietMinute: 22 * 60,
  weeklyGoal: 4,
  pausedDate: '',
  suggestionHiddenUntil: '',
  dndWhileReading: false,
  energyDate: '',
  energy: 'normal',
  rereads: {},
}

export const showConfetti = (s: Settings) => s.confetti && !s.calm
export const playSound = (s: Settings) => s.sound && !s.calm
export const animations = (s: Settings) => !s.calm
