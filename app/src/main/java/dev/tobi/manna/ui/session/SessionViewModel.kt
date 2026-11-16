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
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import kotlin.math.ceil

enum class Step { READ, QUIZ, REWARD, RECAP, DONE }

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

class SessionViewModel(private val c: AppContainer) : ViewModel() {
    private val _state = MutableStateFlow(SessionState())
    val state: StateFlow<SessionState> = _state

    init {
        viewModelScope.launch { load() }
    }

    private suspend fun load() {
        val planId = c.plans.index().resolve(c.settings.settings.first().activePlan)
        val plan = c.plans.plan(planId)
        val done = c.progress.sectionsDone(planId).first().map { it.sectionId }.toSet()
        val idx = plan.sections.indexOfFirst { it.id !in done }
        if (idx < 0) {
            _state.value = SessionState(loading = false, plan = plan, nothingLeft = true, step = Step.DONE, planFinished = true)
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
            prayerText = prayerText,
            quotes = quotes,
        )
    }

    fun finishReading() {
        val s = _state.value
        viewModelScope.launch {
            c.progress.logReading(verses = s.verses.size, sections = 0)
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
        val isNew = c.progress.completeSection(plan.id, section.id)
        if (isNew) c.progress.logReading(verses = 0, sections = 1)
        val newCardIds = c.progress.unlockCards(plan.id, section.cards)
        val (recap, stageTitle) = buildRecap(plan, section)
        _state.update {
            it.copy(
                step = Step.REWARD,
                newCards = newCardIds.mapNotNull { id -> plan.card(id) },
                totalBefore = before,
                totalAfter = if (isNew) before + 1 else before,
                recap = recap,
                recapStageTitle = stageTitle,
                planFinished = it.next == null,
            )
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

    fun rewardContinue() = _state.update { it.copy(step = if (it.recap != null) Step.RECAP else Step.DONE) }

    fun recapDone() = _state.update { it.copy(step = Step.DONE) }

    /** "Noch einer?" – load the next section in place. */
    fun another() {
        _state.value = SessionState()
        viewModelScope.launch { load() }
    }
}
