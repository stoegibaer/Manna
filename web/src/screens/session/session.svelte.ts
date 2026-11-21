import { bookNames, places, plan as loadPlan, planIndex, TRANSLATION, verses as loadVerses, type Verse } from '../../lib/data/content.ts'
import { nextIndex, refLabel, resolvePlan, type Card, type Place, type Plan, type Quiz, type Ref, type Section } from '../../lib/data/plan.ts'
import { store } from '../../lib/data/store.svelte.ts'

export type Step = 'REVIEW' | 'READ' | 'QUIZ' | 'REWARD' | 'MEMORY' | 'RECAP' | 'DONE'

/** Reflection chips after a section. */
export const REFLECTION_TAGS: [string, string][] = [
  ['trost', 'hat mich getröstet'],
  ['herausfordernd', 'fordert mich heraus'],
  ['frage', 'verstehe ich noch nicht'],
  ['merken', 'will ich mir merken'],
]

/** A due question shown as „Erinnerst du dich?“ before reading. */
export interface ReviewItem { planId: string; sectionId: string; index: number; quiz: Quiz; sectionTitle: string }

/** A line in the reading view: a reference header (for multi-passage sections) or a verse. */
export type Line = { kind: 'header'; label: string } | { kind: 'verse'; verse: Verse }

/** One reading session (port of ui/session/SessionViewModel.kt). */
export class Session {
  loading = $state(true)
  plan = $state.raw<Plan | null>(null)
  section = $state.raw<Section | null>(null)
  sectionNumber = $state(0)
  refLabel = $state('')
  minutes = $state(1)
  place = $state.raw<Place | null>(null)
  /** Orientation point for the map (Jerusalem). */
  reference = $state.raw<Place | null>(null)
  lines = $state.raw<Line[]>([])
  step = $state<Step>('READ')
  quizIndex = $state(0)
  newCards = $state.raw<Card[]>([])
  totalBefore = $state(0)
  totalAfter = $state(0)
  planted = $state.raw<string[]>([])
  recap = $state.raw<Quiz | null>(null)
  recapStageTitle = $state<string | null>(null)
  next = $state.raw<Section | null>(null)
  /** Prayer text (Bible word or the historical prayer text). */
  prayerText = $state<string | null>(null)
  /** Quotes for whosaid questions, keyed by quiz index. */
  quotes = $state.raw<Record<number, string>>({})
  planFinished = $state(false)
  /** True when the user opened a session but every section of the plan was already done. */
  nothingLeft = $state(false)
  review = $state.raw<ReviewItem | null>(null)
  reflectionTags = $state.raw<Set<string>>(new Set())
  reflectionNote = $state('')

  private reviewOffered = false
  /** „Viel Energie“: keep going until the end of the stage. */
  readonly more: boolean

  constructor(more: boolean) {
    this.more = more
    void this.load().then(() => { if (this.step === 'READ') void this.offerReview() })
  }

  get verses(): Verse[] {
    return this.lines.flatMap((l) => (l.kind === 'verse' ? [l.verse] : []))
  }

  private reset() {
    Object.assign(this, {
      loading: true, plan: null, section: null, sectionNumber: 0, refLabel: '', minutes: 1, place: null, reference: null, lines: [],
      step: 'READ', quizIndex: 0, newCards: [], totalBefore: 0, totalAfter: 0, planted: [], recap: null, recapStageTitle: null,
      next: null, prayerText: null, quotes: {}, planFinished: false, nothingLeft: false, review: null, reflectionTags: new Set(), reflectionNote: '',
    })
  }

  private async load() {
    const settings = store.settings
    const planId = resolvePlan(await planIndex(), settings.activePlan)
    const plan = await loadPlan(planId)
    const idx = nextIndex(plan, store.doneIds(planId), settings.rereads[planId])
    if (idx < 0) {
      Object.assign(this, { loading: false, plan, nothingLeft: true, step: 'DONE', planFinished: true })
      return
    }
    const section = plan.sections[idx]
    const names = await bookNames()
    const name = (n: number) => names.get(n) ?? ''
    const lines: Line[] = []
    for (const r of section.refs) {
      if (section.refs.length > 1) lines.push({ kind: 'header', label: refLabel([r], name) })
      for (const v of await loadVerses(r.book, r.chapter, r.from, r.to)) lines.push({ kind: 'verse', verse: v })
    }
    const words = lines.reduce((n, l) => n + (l.kind === 'verse' ? l.verse.text.split(' ').length : 0), 0)
    const refText = async (r: Ref) => (await loadVerses(r.book, r.chapter, r.from, r.to)).map((v) => v.text).join(' ')
    const sameWording = (plan.basis ?? 'elbbk') === TRANSLATION
    const p = section.prayer
    const prayerText = p ? (p.ref ? await refText(p.ref) : p.text?.trim() ? p.text : null) : null
    // whosaid: the plan's fragment fits the basis translation; any other translation shows the whole verse
    const quotes: Record<number, string> = {}
    for (const [i, q] of (section.quiz ?? []).entries()) {
      if (q.type === 'whosaid') quotes[i] = sameWording || !q.quote_ref ? q.quote ?? '' : await refText(q.quote_ref)
    }
    const pl = await places()
    Object.assign(this, {
      loading: false, plan, section, sectionNumber: idx + 1,
      refLabel: refLabel(section.refs, name),
      minutes: Math.max(1, Math.ceil(words / 150)),
      place: (section.place && pl.get(section.place)) || null,
      reference: pl.get('jerusalem') ?? null,
      lines, next: plan.sections[idx + 1] ?? null, prayerText, quotes,
    })
  }

  toggleFavorite(v: Verse) {
    const on = !store.favoriteKeys().has(`${v.book}-${v.chapter}-${v.verse}`)
    store.setFavorite(v.book, v.chapter, v.verse, on)
  }

  toggleTag(tag: string) {
    const s = new Set(this.reflectionTags)
    if (s.has(tag)) s.delete(tag)
    else s.add(tag)
    this.reflectionTags = s
    this.saveReflection()
  }

  /** Saved on every chip tap and when leaving the done screen. Empty reflections are not stored. */
  saveReflection() {
    const plan = this.plan, section = this.section
    if (!plan || !section) return
    if (this.reflectionTags.size === 0 && !this.reflectionNote.trim()) return
    store.saveJournal(plan.id, section.id, section.title, this.reflectionTags, this.reflectionNote)
  }

  memoryDone(learned: boolean) {
    const mv = this.section?.memory_verse
    if (learned && mv) for (let v = mv.ref.from; v <= mv.ref.to; v++) store.setFavorite(mv.ref.book, mv.ref.chapter, v, true, 'memory')
    this.step = this.recap ? 'RECAP' : 'DONE'
  }

  finishReading() {
    store.logReading(this.verses.length, 0)
    if (!this.section?.quiz?.length) this.complete()
    else { this.quizIndex = 0; this.step = 'QUIZ' }
  }

  quizSolved(firstTry: boolean) {
    if (this.plan && this.section) store.recordQuiz(this.plan.id, this.section.id, this.quizIndex, firstTry)
  }

  nextQuiz() {
    const count = this.section?.quiz?.length ?? 0
    if (this.quizIndex + 1 < count) this.quizIndex++
    else this.complete()
  }

  private complete() {
    const plan = this.plan, section = this.section
    if (!plan || !section) return
    const before = store.totalSections
    store.completeSection(plan.id, section.id)
    // reading a finished plan again: advance the run (re-reads count for the garden as well)
    if (plan.id in store.settings.rereads) {
      const nextPos = plan.sections.indexOf(section) + 1
      store.updateSettings((st) => {
        const rereads = { ...st.rereads }
        if (nextPos < plan.sections.length) rereads[plan.id] = nextPos
        else delete rereads[plan.id]
        return { ...st, rereads }
      })
    }
    store.logReading(0, 1)
    const newCardIds = store.unlockCards(plan.id, section.cards ?? [])
    const [recap, stageTitle] = this.buildRecap(plan, section)
    const journal = store.journalFor(plan.id, section.id)
    Object.assign(this, {
      step: 'REWARD',
      newCards: newCardIds.map((id) => plan.cards?.find((c) => c.id === id)).filter(Boolean),
      totalBefore: before,
      totalAfter: before + 1,
      planted: store.planted,
      recap,
      recapStageTitle: stageTitle,
      planFinished: this.next === null,
      reflectionTags: new Set(journal?.tags.split(',').filter((t) => t.trim()) ?? []),
      reflectionNote: journal?.note ?? '',
    })
  }

  /** Plants the next tree in the garden (after one was fully grown). */
  plant(species: string) {
    store.plant(this.planted.length, species)
    this.planted = store.planted
  }

  /** At the end of a stage: order the titles of the stage's sections (whole-text retrieval). */
  private buildRecap(plan: Plan, section: Section): [Quiz | null, string | null] {
    const stageId = section.stage
    if (!stageId) return [null, null]
    const idx = plan.sections.indexOf(section)
    const next = plan.sections[idx + 1]
    if (next && next.stage === stageId) return [null, null]
    const inStage = plan.sections.filter((s) => s.stage === stageId)
    if (inStage.length < 3) return [null, null]
    const picked = inStage.length <= 5 ? inStage : Array.from({ length: 5 }, (_, i) => inStage[Math.floor((i * (inStage.length - 1)) / 4)])
    const title = plan.stages?.find((s) => s.id === stageId)?.title ?? null
    return [{
      type: 'order',
      q: `Rückblick${title ? `: ${title}` : ''}. Was kam wann?`,
      items: picked.map((s) => s.title),
      hint: 'Denk an den Verlauf: Was war zuerst?',
      explain: picked.map((s) => s.title).join(' → '),
    }, title]
  }

  /** At most one review per session, only before the first section. */
  private async offerReview() {
    if (this.reviewOffered) return
    this.reviewOffered = true
    const index = await planIndex()
    const available = new Set((index.plans ?? []).filter((p) => p.available).map((p) => p.id))
    for (const r of store.dueReviews()) {
      if (!available.has(r.planId)) continue
      const section = (await loadPlan(r.planId)).sections.find((s) => s.id === r.sectionId)
      const q = section?.quiz?.[r.quizIndex]
      if (!section || !q) continue
      this.review = { planId: r.planId, sectionId: r.sectionId, index: r.quizIndex, quiz: q, sectionTitle: section.title }
      this.step = 'REVIEW'
      return
    }
  }

  reviewSolved(firstTry: boolean) {
    const r = this.review
    if (r) store.recordReview(r.planId, r.sectionId, r.index, firstTry)
  }

  reviewDone() {
    this.step = 'READ'
    this.review = null
  }

  rewardContinue() {
    this.step = this.section?.memory_verse ? 'MEMORY' : this.recap ? 'RECAP' : 'DONE'
  }

  recapDone() {
    this.step = 'DONE'
  }

  /** "Noch einer?" – load the next section in place. */
  another() {
    this.saveReflection()
    this.reset()
    window.scrollTo(0, 0)
    void this.load()
  }
}
