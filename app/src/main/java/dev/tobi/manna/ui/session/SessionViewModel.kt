package dev.tobi.manna.ui.session

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dev.tobi.manna.AppContainer
import dev.tobi.manna.data.bible.Verse
import dev.tobi.manna.data.plan.Card
import dev.tobi.manna.data.plan.Place
import dev.tobi.manna.data.plan.Plan
import dev.tobi.manna.data.plan.Quiz
import dev.tobi.manna.data.plan.Ref
import dev.tobi.manna.data.plan.Section
import dev.tobi.manna.data.plan.resolve
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import dev.tobi.manna.ui.components.key
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlin.math.ceil

enum class Step { REVIEW, READ, QUIZ, REWARD, MEMORY, RECAP, DONE }

/** Reflection chips after a section. */
val REFLECTION_TAGS = listOf(
    "trost" to "hat mich getröstet",
    "herausfordernd" to "fordert mich heraus",
    "frage" to "verstehe ich noch nicht",
    "merken" to "will ich mir merken",
)

/** A due question shown as „Erinnerst du dich?“ before reading. */
data class ReviewItem(val planId: String, val sectionId: String, val index: Int, val quiz: Quiz, val sectionTitle: String)

/** A line in the reading view: either a reference header (for multi-passage sections) or a verse. */
sealed interface Line {
    data class Header(val label: String) : Line
    data class V(val verse: Verse) : Line
}

data class SessionState(
    val loading: Boolean = true,
    val plan: Plan? = null,
    val section: Section? = null,
    val sectionNumber: Int = 0,
    val refLabel: String = "",
    val minutes: Int = 1,
    val place: Place? = null,
    /** Orientation point for the map (Jerusalem). */
    val reference: Place? = null,
    val lines: List<Line> = emptyList(),
    val step: Step = Step.READ,
    val quizIndex: Int = 0,
    val newCards: List<Card> = emptyList(),
    val totalBefore: Int = 0,
    val totalAfter: Int = 0,
    /** Garden: planted species by position (see Garden). */
    val planted: List<String> = emptyList(),
    val recap: Quiz? = null,
    val recapStageTitle: String? = null,
    val next: Section? = null,
    val translationId: String = "",
    /** Prayer text in the active translation (Bible word) or the historical prayer text. */
    val prayerText: String? = null,
    /** Quotes for whosaid questions, keyed by quiz index, in the active translation. */
    val quotes: Map<Int, String> = emptyMap(),
    val planFinished: Boolean = false,
    /** True when the user opened a session but every section of the plan was already done. */
    val nothingLeft: Boolean = false,
    /** „Viel Energie“: keep going until the end of the stage. */
    val more: Boolean = false,
    val review: ReviewItem? = null,
    val reflectionTags: Set<String> = emptySet(),
    val reflectionNote: String = "",
) {
    val verses: List<Verse> get() = lines.filterIsInstance<Line.V>().map { it.verse }
}

/** German reference label, e.g. "Habakuk 1,1–4" or "Habakuk 1,1–4; 2,1". */
fun refLabel(refs: List<Ref>, bookName: (Int) -> String): String {
    val parts = ArrayList<String>()
    var lastBook = -1
    for (r in refs) {
        val range = if (r.from == r.to) "${r.chapter},${r.from}" else "${r.chapter},${r.from}–${r.to}"
        parts += if (r.book == lastBook) range else "${bookName(r.book)} $range"
        lastBook = r.book
    }
    return parts.joinToString("; ")
}

class SessionViewModel(private val c: AppContainer, private val more: Boolean = false) : ViewModel() {
    private var reviewOffered = false

    val favorites = c.progress.favorites
        .map { list -> list.map { Triple(it.book, it.chapter, it.verse) }.toSet() }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptySet())

    fun toggleFavorite(v: Verse) {
        val on = v.key() !in favorites.value
        viewModelScope.launch { c.progress.setFavorite(v.book, v.chapter, v.verse, on) }
    }

    fun toggleTag(tag: String) {
        _state.update { s -> s.copy(reflectionTags = if (tag in s.reflectionTags) s.reflectionTags - tag else s.reflectionTags + tag) }
        saveReflection()
    }

    fun setNote(note: String) = _state.update { it.copy(reflectionNote = note) }

    /** Saved on every chip tap and when leaving the done screen. Empty reflections are not stored. */
    fun saveReflection() {
        val s = _state.value
        val plan = s.plan ?: return
        val section = s.section ?: return
        if (s.reflectionTags.isEmpty() && s.reflectionNote.isBlank()) return
        viewModelScope.launch { c.progress.saveJournal(plan.id, section.id, section.title, s.reflectionTags, s.reflectionNote) }
    }

    fun memoryDone(learned: Boolean) {
        val mv = _state.value.section?.memoryVerse
        if (learned && mv != null) viewModelScope.launch {
            for (v in mv.ref.from..mv.ref.to) c.progress.setFavorite(mv.ref.book, mv.ref.chapter, v, true, "memory")
        }
        _state.update { it.copy(step = if (it.recap != null) Step.RECAP else Step.DONE) }
    }
    private val _state = MutableStateFlow(SessionState())
    val state: StateFlow<SessionState> = _state

    init {
        viewModelScope.launch { load(); if (_state.value.step == Step.READ) offerReview() }
    }

    private suspend fun load() {
        val settings = c.settings.settings.first()
        val planId = c.plans.index().resolve(settings.activePlan)
        val plan = c.plans.plan(planId)
        val done = c.progress.sectionsDone(planId).first().map { it.sectionId }.toSet()
        val idx = plan.nextIndex(done, settings.rereads[planId])
        if (idx < 0) {
            _state.value = SessionState(loading = false, plan = plan, nothingLeft = true, step = Step.DONE, planFinished = true, more = more)
            return
        }
        val section = plan.sections[idx]
        val books = c.text.info().books.associateBy { it.nr }
        val lines = ArrayList<Line>()
        for (r in section.refs) {
            if (section.refs.size > 1) lines += Line.Header(refLabel(listOf(r)) { books[it]?.name ?: "" })
            c.text.verses(r.book, r.chapter, r.from, r.to).forEach { lines += Line.V(it) }
        }
        val words = lines.filterIsInstance<Line.V>().sumOf { it.verse.text.split(' ').size }
        suspend fun refText(r: Ref) = c.text.verses(r.book, r.chapter, r.from, r.to).joinToString(" ") { it.text }
        val sameWording = plan.basis == c.text.translationId
        val prayerText = section.prayer?.let { p -> p.ref?.let { refText(it) } ?: p.text.takeIf { it.isNotBlank() } }
        // whosaid: the plan's fragment fits the basis translation; any other translation shows the whole verse
        val quotes = section.quiz.withIndex().filter { it.value.type == "whosaid" }.associate { (i, q) ->
            i to (if (sameWording || q.quoteRef == null) q.quote.orEmpty() else refText(q.quoteRef))
        }
        _state.value = SessionState(
            loading = false,
            plan = plan,
            section = section,
            sectionNumber = idx + 1,
            refLabel = refLabel(section.refs) { books[it]?.name ?: "" },
            minutes = ceil(words / 150.0).toInt().coerceAtLeast(1),
            place = c.plans.place(section.place),
            reference = c.plans.place("jerusalem"),
            lines = lines,
            next = plan.sections.getOrNull(idx + 1),
            translationId = c.text.translationId,
            more = more,
            prayerText = prayerText,
            quotes = quotes,
        )
    }

    fun finishReading() {
        val s = _state.value
        viewModelScope.launch {
            c.logReading(verses = s.verses.size, sections = 0)
            if (s.section?.quiz.isNullOrEmpty()) complete() else _state.update { it.copy(step = Step.QUIZ, quizIndex = 0) }
        }
    }

    fun quizSolved(firstTry: Boolean) {
        val s = _state.value
        val plan = s.plan ?: return
        val section = s.section ?: return
        viewModelScope.launch { c.progress.recordQuiz(plan.id, section.id, s.quizIndex, firstTry) }
    }

    fun nextQuiz() {
        val s = _state.value
        val count = s.section?.quiz?.size ?: 0
        if (s.quizIndex + 1 < count) _state.update { it.copy(quizIndex = it.quizIndex + 1) } else viewModelScope.launch { complete() }
    }

    private suspend fun complete() {
        val s = _state.value
        val plan = s.plan ?: return
        val section = s.section ?: return
        val before = c.progress.totalSections.first()
        c.progress.completeSection(plan.id, section.id)
        // reading a finished plan again: advance the run (re-reads count for the garden as well)
        val rereading = plan.id in c.settings.current().rereads
        if (rereading) {
            val nextPos = plan.sections.indexOf(section) + 1
            c.settings.update { st -> st.copy(rereads = if (nextPos < plan.sections.size) st.rereads + (plan.id to nextPos) else st.rereads - plan.id) }
        }
        c.logReading(verses = 0, sections = 1)
        val newCardIds = c.progress.unlockCards(plan.id, section.cards)
        val (recap, stageTitle) = buildRecap(plan, section)
        val journal = c.progress.journalFor(plan.id, section.id)
        val planted = c.progress.garden.first()
        _state.update {
            it.copy(
                step = Step.REWARD,
                newCards = newCardIds.mapNotNull { id -> plan.card(id) },
                totalBefore = before,
                totalAfter = before + 1,
                planted = planted,
                recap = recap,
                recapStageTitle = stageTitle,
                planFinished = it.next == null,
                reflectionTags = journal?.tags?.split(',')?.filter { t -> t.isNotBlank() }?.toSet().orEmpty(),
                reflectionNote = journal?.note.orEmpty(),
            )
        }
    }

    /** Plants the next tree in the garden (after one was fully grown). */
    fun plant(species: String) {
        val planted = _state.value.planted
        viewModelScope.launch {
            c.progress.plant(planted.size, species)
            _state.update { it.copy(planted = c.progress.garden.first()) }
        }
    }

    /** At the end of a stage: order the titles of the stage's sections (whole-text retrieval). */
    private fun buildRecap(plan: Plan, section: Section): Pair<Quiz?, String?> {
        val stageId = section.stage ?: return null to null
        val idx = plan.sections.indexOf(section)
        val next = plan.sections.getOrNull(idx + 1)
        if (next != null && next.stage == stageId) return null to null
        val inStage = plan.sections.filter { it.stage == stageId }
        if (inStage.size < 3) return null to null
        val picked = if (inStage.size <= 5) inStage else List(5) { i -> inStage[i * (inStage.size - 1) / 4] }
        val title = plan.stage(stageId)?.title
        return Quiz(
            type = "order",
            q = "Rückblick${title?.let { ": $it" } ?: ""}. Was kam wann?",
            items = picked.map { it.title },
            hint = "Denk an den Verlauf: Was war zuerst?",
            explain = picked.joinToString(" → ") { it.title },
        ) to title
    }

    /** At most one review per session, only before the first section. */
    private suspend fun offerReview() {
        if (reviewOffered) return
        reviewOffered = true
        val available = c.plans.index().plans.filter { it.available }.map { it.id }.toSet()
        for (r in c.progress.dueReviews()) {
            if (r.planId !in available) continue
            val section = c.plans.plan(r.planId).sections.firstOrNull { it.id == r.sectionId } ?: continue
            val q = section.quiz.getOrNull(r.quizIndex) ?: continue
            _state.update { it.copy(step = Step.REVIEW, review = ReviewItem(r.planId, r.sectionId, r.quizIndex, q, section.title)) }
            return
        }
    }

    fun reviewSolved(firstTry: Boolean) {
        val r = _state.value.review ?: return
        viewModelScope.launch { c.progress.recordReview(r.planId, r.sectionId, r.index, firstTry) }
    }

    fun reviewDone() = _state.update { it.copy(step = Step.READ, review = null) }

    fun rewardContinue() = _state.update {
        it.copy(step = when {
            it.section?.memoryVerse != null -> Step.MEMORY
            it.recap != null -> Step.RECAP
            else -> Step.DONE
        })
    }

    fun recapDone() = _state.update { it.copy(step = Step.DONE) }

    /** "Noch einer?" – load the next section in place. */
    fun another() {
        saveReflection()
        _state.value = SessionState()
        viewModelScope.launch { load() }
    }
}
