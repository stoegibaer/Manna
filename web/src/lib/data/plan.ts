// Types of the plan files; format documented in .claude/skills/leseplan-schreiben/format.md

export interface Direction { id: string; title: string; subtitle?: string }
export interface PlanEntry { id: string; title: string; subtitle?: string; direction: string; available?: boolean }
export interface PlanIndex { start: string; directions?: Direction[]; plans?: PlanEntry[] }

export interface Ref { book: number; chapter: number; from: number; to: number }
export interface Stage { id: string; title: string }
export interface Card { id: string; type: string; name: string; text: string; refs?: string }

export interface Quiz {
  type: string
  q?: string | null
  options?: string[]
  answer?: number | boolean | string | null
  quote?: string | null
  quote_ref?: Ref | null
  items?: string[]
  text?: string | null
  fix?: string | null
  min?: number
  max?: number
  tolerance?: number
  unit?: string
  hint?: string | null
  verse?: number | null
  explain?: string
}

export interface Explain { q: string; a: string; translation?: string | null }
export interface MemoryVerse { ref: Ref; text: string }
export interface Prayer { source: string; text?: string; ref?: Ref | null }

export interface Section {
  id: string
  stage?: string | null
  refs: Ref[]
  title: string
  summary: string
  bridge?: string | null
  place?: string | null
  focus?: string | null
  quiz?: Quiz[]
  explain?: Explain[]
  cards?: string[]
  fact?: string | null
  teaser?: string | null
  memory_verse?: MemoryVerse | null
  try?: string | null
  prayer?: Prayer | null
}

export interface Plan {
  id: string
  title: string
  subtitle?: string
  description?: string
  direction?: string
  /** Translation whose wording quote/memory texts use. */
  basis?: string
  stages?: Stage[]
  cards?: Card[]
  sections: Section[]
}

export interface Place { id: string; name: string; lat: number; lon: number; text?: string }

/** The plan to read now: the chosen one if available, else the start plan, else the first available. */
export function resolvePlan(index: PlanIndex, chosen: string): string {
  const avail = (index.plans ?? []).filter((p) => p.available).map((p) => p.id)
  if (avail.includes(chosen)) return chosen
  if (avail.includes(index.start)) return index.start
  return avail[0]
}

/**
 * Index of the next section to read, or -1 if the plan is finished.
 * [rereadPos] is set while a finished plan is read again from the start.
 */
export function nextIndex(plan: Plan, done: Set<string>, rereadPos: number | undefined): number {
  if (rereadPos !== undefined) return rereadPos >= 0 && rereadPos < plan.sections.length ? rereadPos : -1
  return plan.sections.findIndex((s) => !done.has(s.id))
}

export const answerIndex = (q: Quiz): number => (typeof q.answer === 'number' ? q.answer : parseInt(String(q.answer ?? '0'), 10) || 0)
export const answerBool = (q: Quiz): boolean => q.answer === true || q.answer === 'true'
export const answerInt = answerIndex

/** German reference label, e.g. "Habakuk 1,1–4" or "Habakuk 1,1–4; 2,1". */
export function refLabel(refs: Ref[], bookName: (nr: number) => string): string {
  const parts: string[] = []
  let lastBook = -1
  for (const r of refs) {
    const range = r.from === r.to ? `${r.chapter},${r.from}` : `${r.chapter},${r.from}–${r.to}`
    parts.push(r.book === lastBook ? range : `${bookName(r.book)} ${range}`)
    lastBook = r.book
  }
  return parts.join('; ')
}
