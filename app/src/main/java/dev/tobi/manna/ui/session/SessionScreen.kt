package dev.tobi.manna.ui.session

import androidx.activity.compose.BackHandler
import androidx.compose.animation.AnimatedContent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.slideInVertically
import androidx.compose.animation.togetherWith
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.HelpOutline
import androidx.compose.material.icons.outlined.Place
import androidx.compose.material.icons.rounded.Check
import androidx.compose.material.icons.rounded.Close
import androidx.compose.material.icons.rounded.ExpandLess
import androidx.compose.material.icons.rounded.ExpandMore
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.text.SpanStyle
import androidx.compose.ui.text.buildAnnotatedString
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.BaselineShift
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.withStyle
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.em
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import dev.tobi.manna.data.plan.Explain
import dev.tobi.manna.data.settings.Settings
import dev.tobi.manna.ui.components.CardTile
import dev.tobi.manna.ui.components.Confetti
import dev.tobi.manna.ui.components.LocalFeedback
import dev.tobi.manna.ui.components.MiniMap
import androidx.compose.ui.draw.clip
import dev.tobi.manna.ui.components.MustardTree
import dev.tobi.manna.ui.theme.BibleFont
import dev.tobi.manna.ui.theme.bibleTextStyle

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SessionScreen(vm: SessionViewModel, settings: Settings, onClose: () -> Unit, onChoosePlan: () -> Unit) {
    val state by vm.state.collectAsStateWithLifecycle()
    var showExplain by remember { mutableStateOf(false) }
    var showMap by remember { mutableStateOf(false) }
    var confetti by remember { mutableIntStateOf(0) }
    var bigConfetti by remember { mutableStateOf(false) }
    BackHandler(onBack = onClose)

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Text(state.plan?.title.orEmpty(), style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                },
                navigationIcon = { IconButton(onClick = onClose) { Icon(Icons.Rounded.Close, "Schließen") } },
                actions = {
                    if (state.section?.explain?.isNotEmpty() == true && state.step != Step.DONE && state.step != Step.REVIEW) {
                        TextButton(onClick = { showExplain = true }) {
                            Icon(Icons.AutoMirrored.Outlined.HelpOutline, null, Modifier.size(18.dp))
                            Spacer(Modifier.width(6.dp))
                            Text("Versteh ich nicht")
                        }
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.background),
            )
        },
        containerColor = MaterialTheme.colorScheme.background,
    ) { pad ->
        Box(Modifier.fillMaxSize().padding(pad)) {
            if (state.loading) {
                CircularProgressIndicator(Modifier.align(Alignment.Center))
            } else {
                AnimatedContent(
                    targetState = state.step to state.section?.id,
                    transitionSpec = {
                        (fadeIn(tween(260)) + slideInVertically(tween(260)) { it / 12 }) togetherWith fadeOut(tween(160))
                    },
                    label = "step",
                ) { (step, _) ->
                    when (step) {
                        Step.REVIEW -> ReviewStep(state, onSolved = { first -> vm.reviewSolved(first); bigConfetti = false; confetti++ }, onDone = vm::reviewDone)
                        Step.READ -> ReadStep(state, settings, onMap = { showMap = true }, onDone = vm::finishReading)
                        Step.QUIZ -> QuizStep(state, onSolved = { first -> vm.quizSolved(first); bigConfetti = false; confetti++ }, onNext = vm::nextQuiz)
                        Step.REWARD -> RewardStep(state, settings, onShown = { bigConfetti = true; confetti++ }, onNext = vm::rewardContinue)
                        Step.RECAP -> RecapStep(state, onSolved = { bigConfetti = false; confetti++ }, onNext = vm::recapDone)
                        Step.DONE -> DoneStep(state, onClose = onClose, onAnother = vm::another, onChoosePlan = onChoosePlan)
                    }
                }
            }
            Confetti(confetti, enabled = settings.showConfetti, big = bigConfetti)
        }
    }

    if (showMap) {
        state.place?.let { MapSheet(it, state.reference, onDismiss = { showMap = false }) }
    }
    if (showExplain) {
        ExplainSheet(state.section?.explain.orEmpty().filter { it.translation == null || it.translation == state.translationId }, onDismiss = { showExplain = false })
    }
}

// ───────────────────────── Reading ─────────────────────────

@Composable
private fun ReadStep(state: SessionState, settings: Settings, onMap: () -> Unit, onDone: () -> Unit) {
    val section = state.section ?: return
    val lines = state.lines
    val verseLineIdx = remember(lines) { lines.indices.filter { lines[it] is Line.V } }
    val focusMode = settings.focusMode
    var focus by rememberSaveable(section.id) { mutableIntStateOf(0) } // index into verseLineIdx
    val atEnd = !focusMode || focus >= verseLineIdx.lastIndex
    val listState = rememberLazyListState()
    val fb = LocalFeedback.current
    val textStyle = bibleTextStyle(settings.textScale)

    LaunchedEffect(focus) {
        if (focusMode && focus > 0) {
            // keep the previous verse visible above the current one (item 0 is the header block)
            val item = verseLineIdx[focus] // line index; list item = line index + 1
            listState.animateScrollToItem(item.coerceAtLeast(0))
        }
    }

    val advance: () -> Unit = {
        if (focusMode && focus < verseLineIdx.lastIndex) { focus++; fb.tick() }
    }

    Column(Modifier.fillMaxSize()) {
        LazyColumn(
            state = listState,
            modifier = Modifier
                .weight(1f)
                .fillMaxWidth()
                .clickable(interactionSource = remember { MutableInteractionSource() }, indication = null, onClick = advance),
            contentPadding = PaddingValues(start = 24.dp, end = 24.dp, top = 8.dp, bottom = 120.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            item {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp), modifier = Modifier.padding(bottom = 12.dp)) {
                    section.bridge?.let {
                        Column(Modifier.padding(bottom = 10.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
                            Text("Was dazwischen geschah", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.secondary)
                            Text(it, style = MaterialTheme.typography.bodyLarge, fontFamily = BibleFont, fontStyle = FontStyle.Italic, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                    Text(section.title, style = MaterialTheme.typography.headlineMedium)
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("${state.refLabel} · ca. ${state.minutes} Min.", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        state.place?.let {
                            Spacer(Modifier.width(6.dp))
                            Surface(
                                onClick = onMap,
                                shape = RoundedCornerShape(50),
                                color = MaterialTheme.colorScheme.surfaceContainer,
                            ) {
                                Row(Modifier.padding(horizontal = 10.dp, vertical = 4.dp), verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Outlined.Place, null, Modifier.size(16.dp), tint = MaterialTheme.colorScheme.primary)
                                    Spacer(Modifier.width(4.dp))
                                    Text(it.name, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.primary)
                                }
                            }
                        }
                    }
                    section.focus?.let {
                        Surface(color = MaterialTheme.colorScheme.secondaryContainer, shape = RoundedCornerShape(14.dp), modifier = Modifier.padding(top = 6.dp)) {
                            Text(it, Modifier.padding(14.dp), color = MaterialTheme.colorScheme.onSecondaryContainer, style = MaterialTheme.typography.bodyLarge)
                        }
                    }
                }
            }
            itemsIndexed(lines) { i, line ->
                when (line) {
                    is Line.Header -> Text(line.label, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(top = 10.dp))
                    is Line.V -> {
                        val pos = verseLineIdx.indexOf(i)
                        val target = when {
                            !focusMode -> 1f
                            pos == focus -> 1f
                            pos < focus -> 0.5f
                            else -> 0.16f
                        }
                        val a by animateFloatAsState(target, tween(if (settings.animations) 280 else 0), label = "a")
                        Text(
                            buildAnnotatedString {
                                withStyle(SpanStyle(fontSize = 0.62.em, color = MaterialTheme.colorScheme.primary, baselineShift = BaselineShift(0.35f), fontWeight = FontWeight.Bold)) {
                                    append("${line.verse.verse} ")
                                }
                                append(line.verse.text)
                            },
                            style = textStyle,
                            color = MaterialTheme.colorScheme.onBackground,
                            modifier = Modifier.alpha(a),
                        )
                    }
                }
            }
        }

        Box(
            Modifier
                .fillMaxWidth()
                .background(MaterialTheme.colorScheme.background)
                .padding(horizontal = 24.dp, vertical = 16.dp)
                .navigationBarsPadding(),
        ) {
            AnimatedContent(atEnd, label = "cta") { end ->
                if (end) {
                    Button(onClick = onDone, modifier = Modifier.fillMaxWidth().height(56.dp)) {
                        Text("Fertig gelesen", style = MaterialTheme.typography.titleMedium)
                    }
                } else {
                    Text(
                        "Tippe irgendwo, um weiterzulesen",
                        modifier = Modifier.fillMaxWidth().height(56.dp).padding(top = 16.dp),
                        textAlign = TextAlign.Center,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }
        }
    }
}

// ───────────────────────── Review ─────────────────────────

@Composable
private fun ReviewStep(state: SessionState, onSolved: (Boolean) -> Unit, onDone: () -> Unit) {
    val r = state.review ?: return
    Column(
        Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(horizontal = 24.dp, vertical = 8.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        Text("Erinnerst du dich?", style = MaterialTheme.typography.headlineMedium)
        Text("Eine Frage aus „${r.sectionTitle}“ – zum Warmwerden.", color = MaterialTheme.colorScheme.onSurfaceVariant)
        QuizView(r.quiz, key = "review-${r.planId}-${r.sectionId}-${r.index}", verses = emptyList(), onSolved = onSolved, onNext = onDone, nextLabel = "Jetzt lesen")
        TextButton(onClick = onDone, modifier = Modifier.align(Alignment.CenterHorizontally)) { Text("Überspringen") }
        Spacer(Modifier.height(32.dp))
    }
}

// ───────────────────────── Quiz ─────────────────────────

@Composable
private fun QuizStep(state: SessionState, onSolved: (Boolean) -> Unit, onNext: () -> Unit) {
    val section = state.section ?: return
    val quiz = section.quiz.getOrNull(state.quizIndex) ?: return
    val count = section.quiz.size
    Column(
        Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(horizontal = 24.dp, vertical = 8.dp),
        verticalArrangement = Arrangement.spacedBy(18.dp),
    ) {
        if (count > 1) {
            Text("Frage ${state.quizIndex + 1} von $count", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        QuizView(
            quiz = state.quotes[state.quizIndex]?.let { quiz.copy(quote = it) } ?: quiz,
            key = "${section.id}-${state.quizIndex}",
            verses = state.verses,
            onSolved = onSolved,
            onNext = onNext,
            nextLabel = if (state.quizIndex + 1 < count) "Nächste Frage" else "Weiter",
        )
        Spacer(Modifier.height(40.dp))
    }
}

// ───────────────────────── Reward ─────────────────────────

@Composable
private fun RewardStep(state: SessionState, settings: Settings, onShown: () -> Unit, onNext: () -> Unit) {
    val fb = LocalFeedback.current
    LaunchedEffect(Unit) { fb.sectionDone(); onShown() }
    val grew = state.totalAfter > state.totalBefore
    Column(
        Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(horizontal = 24.dp, vertical = 8.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        MustardTree(
            sections = state.totalAfter.toFloat(),
            animateFrom = state.totalBefore.toFloat(),
            animate = settings.animations,
            modifier = Modifier.fillMaxWidth().height(260.dp),
        )
        Text("Abschnitt geschafft", style = MaterialTheme.typography.headlineMedium, textAlign = TextAlign.Center)
        Text(
            if (grew) "Dein Senfkorn ist gewachsen." else "Nochmal gelesen – gut so.",
            style = MaterialTheme.typography.bodyLarge,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        if (state.newCards.isNotEmpty()) {
            Text(
                if (state.newCards.size == 1) "Neue Karte für deine Sammlung" else "Neue Karten für deine Sammlung",
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
            )
            state.newCards.forEachIndexed { i, card ->
                var visible by remember { mutableStateOf(!settings.animations) }
                LaunchedEffect(Unit) { kotlinx.coroutines.delay(500L + i * 350L); visible = true }
                AnimatedVisibility(visible, enter = fadeIn(tween(400)) + slideInVertically(tween(400)) { it / 3 }) {
                    CardTile(card)
                }
            }
        }
        state.section?.fact?.let { fact ->
            Surface(color = MaterialTheme.colorScheme.surfaceContainer, shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text("Wusstest du?", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.secondary)
                    Text(fact, style = MaterialTheme.typography.bodyLarge)
                }
            }
        }
        Button(onClick = onNext, modifier = Modifier.fillMaxWidth().height(56.dp).padding(top = 4.dp)) { Text("Weiter") }
        Spacer(Modifier.height(24.dp))
    }
}

// ───────────────────────── Recap ─────────────────────────

@Composable
private fun RecapStep(state: SessionState, onSolved: () -> Unit, onNext: () -> Unit) {
    val recap = state.recap ?: return
    Column(
        Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(horizontal = 24.dp, vertical = 8.dp),
        verticalArrangement = Arrangement.spacedBy(18.dp),
    ) {
        Text("Etappe geschafft", style = MaterialTheme.typography.headlineMedium)
        Text(
            "Ein kurzer Blick zurück auf „${state.recapStageTitle ?: "diese Etappe"}“ hilft, das Ganze zu behalten.",
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        QuizView(recap, key = "recap-${state.section?.id}", verses = emptyList(), onSolved = { onSolved() }, onNext = onNext)
        Spacer(Modifier.height(40.dp))
    }
}

// ───────────────────────── Done ─────────────────────────

@Composable
private fun DoneStep(state: SessionState, onClose: () -> Unit, onAnother: () -> Unit, onChoosePlan: () -> Unit) {
    val section = state.section
    Column(
        Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(horizontal = 24.dp, vertical = 8.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(16.dp),
    ) {
        Spacer(Modifier.height(12.dp))
        Box(
            Modifier.size(84.dp).background(MaterialTheme.colorScheme.primaryContainer, CircleShape),
            contentAlignment = Alignment.Center,
        ) { Icon(Icons.Rounded.Check, null, Modifier.size(46.dp), tint = MaterialTheme.colorScheme.primary) }

        if (state.planFinished) {
            Text("${state.plan?.title} abgeschlossen", style = MaterialTheme.typography.headlineMedium, textAlign = TextAlign.Center)
            Text(
                if (state.nothingLeft) "Du hast alle Abschnitte dieses Plans gelesen."
                else "Du hast den ganzen Plan gelesen. Stark.",
                textAlign = TextAlign.Center, color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        } else {
            Text("Für heute geschafft", style = MaterialTheme.typography.headlineMedium, textAlign = TextAlign.Center)
            section?.let { Text("„${it.title}“ gelesen.", color = MaterialTheme.colorScheme.onSurfaceVariant) }
        }

        section?.tryIt?.let {
            InfoCard("Heute ausprobieren", it)
        }
        val prayerText = state.prayerText
        section?.prayer?.takeIf { prayerText != null }?.let { p ->
            Surface(color = MaterialTheme.colorScheme.surfaceContainer, shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text("Als Gebet", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.secondary)
                    Text(prayerText.orEmpty(), fontFamily = BibleFont, fontStyle = FontStyle.Italic, style = MaterialTheme.typography.bodyLarge)
                    Text("— ${p.source}", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }

        Spacer(Modifier.height(4.dp))
        if (state.planFinished) {
            Button(onClick = onChoosePlan, modifier = Modifier.fillMaxWidth().height(56.dp)) { Text("Wohin als Nächstes?", style = MaterialTheme.typography.titleMedium) }
            TextButton(onClick = onClose) { Text("Fertig für heute") }
        } else if (state.more && state.next != null && state.next.stage == section?.stage) {
            // „Viel Energie“: keep going within the stage – but stopping is always fine
            Button(onClick = onAnother, modifier = Modifier.fillMaxWidth().height(56.dp)) { Text("Nächster Abschnitt", style = MaterialTheme.typography.titleMedium) }
            TextButton(onClick = onClose) { Text("Für heute genug") }
        } else {
            Button(onClick = onClose, modifier = Modifier.fillMaxWidth().height(56.dp)) { Text("Fertig", style = MaterialTheme.typography.titleMedium) }
        }

        val next = state.next
        if (!state.planFinished && next != null && !(state.more && next.stage == section?.stage)) {
            HorizontalDivider(Modifier.padding(vertical = 6.dp), color = MaterialTheme.colorScheme.outline.copy(alpha = 0.3f))
            section?.teaser?.let {
                Text(it, style = MaterialTheme.typography.bodyLarge, fontFamily = BibleFont, fontStyle = FontStyle.Italic, textAlign = TextAlign.Center, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
            TextButton(onClick = onAnother) { Text("Noch ein Abschnitt") }
        }
        Spacer(Modifier.height(24.dp))
    }
}

@Composable
private fun InfoCard(label: String, text: String) {
    Surface(color = MaterialTheme.colorScheme.surfaceContainer, shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth()) {
        Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Text(label, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.secondary)
            Text(text, style = MaterialTheme.typography.bodyLarge)
        }
    }
}

// ───────────────────────── Map ─────────────────────────

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun MapSheet(place: dev.tobi.manna.data.plan.Place, reference: dev.tobi.manna.data.plan.Place?, onDismiss: () -> Unit) {
    ModalBottomSheet(onDismissRequest = onDismiss, containerColor = MaterialTheme.colorScheme.surface) {
        Column(Modifier.fillMaxWidth().verticalScroll(rememberScrollState()).padding(horizontal = 24.dp).padding(bottom = 32.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
            Text("Wo sind wir?", style = MaterialTheme.typography.titleLarge)
            MiniMap(
                place, reference,
                Modifier.fillMaxWidth().height(300.dp).clip(RoundedCornerShape(18.dp)),
            )
            Text(place.name, style = MaterialTheme.typography.titleMedium)
            if (place.text.isNotBlank()) Text(place.text, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
    }
}

// ───────────────────────── Explanations ─────────────────────────

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun ExplainSheet(items: List<Explain>, onDismiss: () -> Unit) {
    ModalBottomSheet(onDismissRequest = onDismiss, containerColor = MaterialTheme.colorScheme.surface) {
        Column(
            Modifier.fillMaxWidth().verticalScroll(rememberScrollState()).padding(horizontal = 24.dp).padding(bottom = 32.dp),
            verticalArrangement = Arrangement.spacedBy(4.dp),
        ) {
            Text("Hilfe zum Abschnitt", style = MaterialTheme.typography.titleLarge, modifier = Modifier.padding(bottom = 8.dp))
            items.forEachIndexed { i, e ->
                var open by remember { mutableStateOf(i == 0) }
                Column(Modifier.fillMaxWidth().clickable { open = !open }.padding(vertical = 10.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(e.q, style = MaterialTheme.typography.titleMedium, modifier = Modifier.weight(1f))
                        Icon(if (open) Icons.Rounded.ExpandLess else Icons.Rounded.ExpandMore, null)
                    }
                    AnimatedVisibility(open) {
                        Text(e.a, style = MaterialTheme.typography.bodyLarge, modifier = Modifier.padding(top = 6.dp), color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
                if (i < items.lastIndex) HorizontalDivider(color = MaterialTheme.colorScheme.outline.copy(alpha = 0.3f))
            }
        }
    }
}
