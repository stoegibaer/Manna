package dev.tobi.manna.ui.quick

import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Check
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewModelScope
import dev.tobi.manna.AppContainer
import dev.tobi.manna.data.plan.Quiz
import dev.tobi.manna.data.plan.resolve
import dev.tobi.manna.data.settings.Settings
import dev.tobi.manna.reminder.Reminders
import dev.tobi.manna.ui.components.Confetti
import dev.tobi.manna.ui.components.LocalFeedback
import dev.tobi.manna.ui.session.refLabel
import dev.tobi.manna.ui.theme.BibleFont
import dev.tobi.manna.ui.theme.LocalMannaColors
import dev.tobi.manna.ui.theme.bibleTextStyle
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

// ───────────────────────── „Nur 1 Vers“ ─────────────────────────

data class VerseState(
    val loading: Boolean = true,
    val text: String = "",
    val ref: String = "",
    val sectionTitle: String = "",
    val done: Boolean = false,
    val planFinished: Boolean = false,
)

/** The lowest possible bar: the first verse of the next section. Reading it fulfils the daily minimum. */
class VerseViewModel(private val c: AppContainer) : ViewModel() {
    val state = MutableStateFlow(VerseState())

    init {
        viewModelScope.launch {
            val planId = c.plans.index().resolve(c.settings.current().activePlan)
            val plan = c.plans.plan(planId)
            val done = c.progress.sectionsDone(planId).first().map { it.sectionId }.toSet()
            val section = plan.sections.firstOrNull { it.id !in done }
            if (section == null) {
                state.value = VerseState(loading = false, planFinished = true)
                return@launch
            }
            val r = section.refs.first()
            val v = c.text.verses(r.book, r.chapter, r.from, r.to).first()
            val books = c.text.info().books.associateBy { it.nr }
            state.value = VerseState(
                loading = false,
                text = v.text,
                ref = "${books[v.book]?.name} ${v.chapter},${v.verse}",
                sectionTitle = section.title,
            )
        }
    }

    fun markRead() {
        if (state.value.done) return
        state.update { it.copy(done = true) }
        viewModelScope.launch { c.logReading(verses = 1, sections = 0) }
    }
}

@Composable
fun VerseScreen(vm: VerseViewModel, settings: Settings, onMore: () -> Unit, onClose: () -> Unit, onPlans: () -> Unit) {
    val s by vm.state.collectAsStateWithLifecycle()
    val fb = LocalFeedback.current
    var confetti by remember { mutableIntStateOf(0) }
    BackHandler(onBack = onClose)
    Box(Modifier.fillMaxSize().statusBarsPadding().navigationBarsPadding()) {
        if (s.loading) {
            CircularProgressIndicator(Modifier.align(Alignment.Center))
        } else if (s.planFinished) {
            Column(Modifier.align(Alignment.Center).padding(24.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                Text("Dieser Plan ist schon ganz gelesen.", style = MaterialTheme.typography.titleLarge, textAlign = TextAlign.Center)
                Spacer(Modifier.height(16.dp))
                Button(onClick = onPlans) { Text("Wohin als Nächstes?") }
            }
        } else {
            Column(
                Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(horizontal = 28.dp).padding(top = 72.dp, bottom = 24.dp),
                verticalArrangement = Arrangement.spacedBy(20.dp),
            ) {
                Text("Dein Vers für heute", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                Text(s.text, style = bibleTextStyle(settings.textScale * 1.2f))
                Text(s.ref, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                Spacer(Modifier.height(8.dp))
                AnimatedContent(s.done, label = "done") { done ->
                    if (!done) {
                        Button(onClick = { vm.markRead(); fb.sectionDone(); confetti++ }, modifier = Modifier.fillMaxWidth().height(60.dp)) {
                            Icon(Icons.Rounded.Check, null)
                            Spacer(Modifier.width(8.dp))
                            Text("Gelesen", style = MaterialTheme.typography.titleMedium)
                        }
                    } else {
                        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                            Text("Geschafft – das reicht für heute.", style = MaterialTheme.typography.titleLarge)
                            Text("Wenn du magst: Der Vers gehört zum Abschnitt „${s.sectionTitle}“.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                            OutlinedButton(onClick = onMore, modifier = Modifier.fillMaxWidth().height(52.dp)) { Text("Ganzen Abschnitt lesen") }
                            TextButton(onClick = onClose, modifier = Modifier.align(Alignment.CenterHorizontally)) { Text("Fertig") }
                        }
                    }
                }
            }
        }
        Confetti(confetti, enabled = settings.showConfetti)
        IconButton(onClick = onClose, modifier = Modifier.padding(8.dp)) { Icon(Icons.Rounded.Close, "Schließen") }
    }
}

// ───────────────────────── Answer from the notification ─────────────────────────

data class AnswerState(
    val loading: Boolean = true,
    val quiz: Quiz? = null,
    /** Passage and section title, e.g. "Habakuk 1,1–4 · Wie lange noch?" – the question needs this context. */
    val where: String = "",
    /** Not answered yet: the options to choose from (label, value). */
    val asking: List<Pair<String, Int>> = emptyList(),
    val chosen: String = "",
    val correctText: String = "",
    val correct: Boolean = false,
)

/**
 * A review question from the reminder. Either the user already tapped an answer button (show the result right away –
 * a small win before reading), or the answers were too long for buttons ([Reminders.ASK]): then ask here first.
 */
class AnswerViewModel(private val c: AppContainer, private val planId: String, private val sectionId: String, private val index: Int, answer: Int) : ViewModel() {
    val state = MutableStateFlow(AnswerState())

    init {
        viewModelScope.launch {
            val section = c.plans.plan(planId).sections.firstOrNull { it.id == sectionId }
            val q = section?.quiz?.getOrNull(index) ?: return@launch
            val books = c.text.info().books.associateBy { it.nr }
            val where = refLabel(section.refs) { books[it]?.name ?: "" } + " · " + section.title
            if (answer == Reminders.ASK) {
                val options = if (q.type == "truefalse") listOf("Stimmt" to 1, "Stimmt nicht" to 0)
                    else q.options.mapIndexed { i, o -> o to i }.shuffled()
                state.value = AnswerState(false, q, where, asking = options)
            } else answer(q, where, answer)
        }
    }

    fun choose(value: Int) {
        val q = state.value.quiz ?: return
        viewModelScope.launch { answer(q, state.value.where, value) }
    }

    private suspend fun answer(q: Quiz, where: String, answer: Int) {
        val correct = if (q.type == "truefalse") (answer == 1) == q.answerBool else answer == q.answerIndex
        val chosen = if (q.type == "truefalse") (if (answer == 1) "Stimmt" else "Stimmt nicht") else q.options.getOrElse(answer) { "" }
        val right = if (q.type == "truefalse") (if (q.answerBool) "Stimmt" else "Stimmt nicht") else q.options.getOrElse(q.answerIndex) { "" }
        c.progress.recordReview(planId, sectionId, index, correct)
        state.value = AnswerState(false, q, where, chosen = chosen, correctText = right, correct = correct)
    }
}

@Composable
fun AnswerScreen(vm: AnswerViewModel, settings: Settings, onRead: () -> Unit, onVerse: () -> Unit, onClose: () -> Unit) {
    val s by vm.state.collectAsStateWithLifecycle()
    val fb = LocalFeedback.current
    var confetti by remember { mutableIntStateOf(0) }
    val answered = !s.loading && s.quiz != null && s.asking.isEmpty()
    LaunchedEffect(answered) { if (answered) { if (s.correct) { fb.correct(); confetti++ } else fb.tryAgain() } }
    BackHandler(onBack = onClose)
    Box(Modifier.fillMaxSize().statusBarsPadding().navigationBarsPadding()) {
        val q = s.quiz
        if (s.loading || q == null) {
            if (s.loading) CircularProgressIndicator(Modifier.align(Alignment.Center))
        } else {
            val ok = LocalMannaColors.current.success
            Column(
                Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(horizontal = 24.dp).padding(top = 72.dp, bottom = 24.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
            ) {
                Text("Erinnerst du dich?", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                Text(s.where, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                if (q.type == "whosaid") {
                    Text("Wer hat das gesagt?", style = MaterialTheme.typography.titleMedium)
                    Text("„${q.quote}“", style = MaterialTheme.typography.titleLarge.copy(fontFamily = BibleFont, fontStyle = FontStyle.Italic))
                } else Text(q.q.orEmpty(), style = MaterialTheme.typography.titleLarge)
                if (s.asking.isNotEmpty()) {
                    for ((label, value) in s.asking) {
                        OutlinedButton(onClick = { vm.choose(value) }, modifier = Modifier.fillMaxWidth()) {
                            Text(label, modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp), textAlign = TextAlign.Start)
                        }
                    }
                    TextButton(onClick = onClose, modifier = Modifier.align(Alignment.CenterHorizontally)) { Text("Später") }
                    return@Column
                }
                Surface(
                    color = if (s.correct) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.secondaryContainer,
                    shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth(),
                ) {
                    Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Box(Modifier.size(28.dp).background(if (s.correct) ok else MaterialTheme.colorScheme.secondary, CircleShape), contentAlignment = Alignment.Center) {
                                Icon(if (s.correct) Icons.Rounded.Check else Icons.Rounded.Close, null, Modifier.size(18.dp), tint = MaterialTheme.colorScheme.surface)
                            }
                            Spacer(Modifier.width(10.dp))
                            Text(if (s.correct) "Richtig!" else "Knapp daneben – kein Problem.", fontWeight = FontWeight.SemiBold)
                        }
                        if (!s.correct) Text("Richtig ist: ${s.correctText}")
                        if (q.explain.isNotBlank()) Text(q.explain)
                    }
                }
                Spacer(Modifier.height(4.dp))
                Button(onClick = onRead, modifier = Modifier.fillMaxWidth().height(58.dp)) { Text("Weiterlesen", style = MaterialTheme.typography.titleMedium) }
                OutlinedButton(onClick = onVerse, modifier = Modifier.fillMaxWidth().height(52.dp)) { Text("Nur 1 Vers") }
                TextButton(onClick = onClose, modifier = Modifier.align(Alignment.CenterHorizontally)) { Text("Später") }
            }
        }
        Confetti(confetti, enabled = settings.showConfetti)
        IconButton(onClick = onClose, modifier = Modifier.padding(8.dp)) { Icon(Icons.Rounded.Close, "Schließen") }
    }
}
