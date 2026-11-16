package dev.tobi.manna.ui.session

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.Spring
import androidx.compose.animation.core.spring
import androidx.compose.animation.core.tween
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.rounded.Check
import androidx.compose.material.icons.rounded.Lightbulb
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.LocalMinimumInteractiveComponentSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Slider
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import dev.tobi.manna.data.bible.Verse
import dev.tobi.manna.data.plan.Quiz
import dev.tobi.manna.ui.components.LocalFeedback
import dev.tobi.manna.ui.theme.BibleFont
import dev.tobi.manna.ui.theme.LocalMannaColors
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.launch
import kotlin.math.roundToInt
import kotlin.random.Random

/** Small horizontal shake for a wrong tap – a gentle "nope", no penalty. */
private class Shaker(private val scope: CoroutineScope) {
    val offset = Animatable(0f)
    fun shake() = scope.launch {
        for (x in listOf(14f, -12f, 8f, -5f, 0f)) offset.animateTo(x, tween(55))
    }
}

@Composable
private fun rememberShaker(): Shaker {
    val scope = rememberCoroutineScope()
    return remember { Shaker(scope) }
}

/**
 * Renders one quiz question. Wrong answers never cost anything: a hint appears and the user tries again.
 * [onSolved] fires once with whether it was solved on the first attempt; [onNext] after the explanation.
 */
@Composable
fun QuizView(
    quiz: Quiz,
    key: String,
    verses: List<Verse>,
    onSolved: (firstTry: Boolean) -> Unit,
    onNext: () -> Unit,
    nextLabel: String = "Weiter",
) {
    val fb = LocalFeedback.current
    var solved by remember(key) { mutableStateOf(false) }
    var mistakes by remember(key) { mutableIntStateOf(0) }
    var showVerse by remember(key) { mutableStateOf(false) }

    val wrong: () -> Unit = { mistakes++; fb.tryAgain() }
    val right: () -> Unit = {
        if (!solved) {
            solved = true
            fb.correct()
            onSolved(mistakes == 0)
        }
    }

    Column(Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(14.dp)) {
        val title = when (quiz.type) {
            "whosaid" -> "Wer hat’s gesagt?"
            "truefalse" -> "Stimmt das?"
            "order" -> "Bring in die richtige Reihenfolge"
            "estimate" -> "Schätzfrage"
            else -> null
        }
        if (title != null) Text(title, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)

        when (quiz.type) {
            "whosaid" -> {
                Text("„${quiz.quote}“", style = MaterialTheme.typography.titleLarge.copy(fontFamily = BibleFont, fontStyle = FontStyle.Italic))
                ChoiceQuiz(quiz, key, solved, right, wrong)
            }
            "truefalse" -> {
                Text(quiz.q.orEmpty(), style = MaterialTheme.typography.titleLarge)
                TrueFalseQuiz(quiz, key, solved, right, wrong)
            }
            "order" -> {
                quiz.q?.let { Text(it, style = MaterialTheme.typography.titleMedium) }
                OrderQuiz(quiz, key, solved, right, wrong)
            }
            "error" -> {
                quiz.q?.let { Text(it, style = MaterialTheme.typography.titleMedium) }
                ErrorQuiz(quiz, key, solved, right, wrong)
            }
            "estimate" -> {
                Text(quiz.q.orEmpty(), style = MaterialTheme.typography.titleLarge)
                EstimateQuiz(quiz, key, solved, right, wrong)
            }
            else -> {
                Text(quiz.q.orEmpty(), style = MaterialTheme.typography.titleLarge)
                ChoiceQuiz(quiz, key, solved, right, wrong)
            }
        }

        // Hint after a mistake – friendly, with the option to look at the verse.
        AnimatedVisibility(!solved && mistakes > 0, enter = fadeIn() + expandVertically()) {
            Surface(color = MaterialTheme.colorScheme.secondaryContainer, shape = RoundedCornerShape(14.dp), modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Rounded.Lightbulb, null, Modifier.size(18.dp), tint = MaterialTheme.colorScheme.onSecondaryContainer)
                        Spacer(Modifier.width(8.dp))
                        Text(quiz.hint ?: "Kein Problem – versuch es nochmal.", color = MaterialTheme.colorScheme.onSecondaryContainer)
                    }
                    val v = quiz.verse?.let { n -> verses.firstOrNull { it.verse == n } }
                    if (v != null) {
                        if (showVerse) {
                            Text("${v.verse} ${v.text}", fontFamily = BibleFont, color = MaterialTheme.colorScheme.onSecondaryContainer)
                        } else {
                            TextButton(onClick = { showVerse = true }, contentPadding = androidx.compose.foundation.layout.PaddingValues(0.dp)) {
                                Text("Vers ${v.verse} ansehen")
                            }
                        }
                    }
                }
            }
        }

        AnimatedVisibility(solved, enter = fadeIn(tween(300)) + expandVertically()) {
            Column(verticalArrangement = Arrangement.spacedBy(14.dp)) {
                Surface(color = MaterialTheme.colorScheme.primaryContainer, shape = RoundedCornerShape(14.dp), modifier = Modifier.fillMaxWidth()) {
                    Row(Modifier.padding(14.dp)) {
                        Icon(Icons.Rounded.Check, null, tint = MaterialTheme.colorScheme.onPrimaryContainer)
                        Spacer(Modifier.width(10.dp))
                        Column {
                            Text(if (mistakes == 0) "Richtig!" else "Genau!", fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onPrimaryContainer)
                            if (quiz.explain.isNotBlank()) Text(quiz.explain, color = MaterialTheme.colorScheme.onPrimaryContainer)
                        }
                    }
                }
                Button(onClick = onNext, modifier = Modifier.fillMaxWidth().height(54.dp)) { Text(nextLabel) }
            }
        }
    }
}

@Composable
private fun answerColors(state: Int): Pair<Color, Color> {
    // 0 = neutral, 1 = wrong (tried), 2 = correct
    val cs = MaterialTheme.colorScheme
    val container by animateColorAsState(
        when (state) { 2 -> cs.primaryContainer; 1 -> cs.surfaceVariant; else -> cs.surface }, label = "c",
    )
    val content = when (state) { 2 -> cs.onPrimaryContainer; 1 -> cs.onSurfaceVariant.copy(alpha = 0.55f); else -> cs.onSurface }
    return container to content
}

@Composable
private fun AnswerButton(text: String, state: Int, enabled: Boolean, shaker: Shaker?, onClick: () -> Unit) {
    val (container, content) = answerColors(state)
    Surface(
        onClick = onClick,
        enabled = enabled,
        shape = RoundedCornerShape(16.dp),
        color = container,
        contentColor = content,
        border = BorderStroke(1.dp, if (state == 2) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outline.copy(alpha = 0.6f)),
        modifier = Modifier
            .fillMaxWidth()
            .offset { IntOffset((shaker?.offset?.value ?: 0f).roundToInt(), 0) },
    ) {
        Row(Modifier.padding(horizontal = 18.dp, vertical = 16.dp), verticalAlignment = Alignment.CenterVertically) {
            Text(
                text,
                modifier = Modifier.weight(1f),
                style = MaterialTheme.typography.bodyLarge,
                textDecoration = if (state == 1) TextDecoration.LineThrough else null,
            )
            if (state == 2) Icon(Icons.Rounded.Check, null, tint = MaterialTheme.colorScheme.primary)
        }
    }
}

@Composable
private fun ChoiceQuiz(quiz: Quiz, key: String, solved: Boolean, right: () -> Unit, wrong: () -> Unit) {
    val order = remember(key) { quiz.options.indices.shuffled(Random(key.hashCode())) }
    val tried = remember(key) { mutableStateListOf<Int>() }
    val shakers = order.associateWith { rememberShaker() }
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        for (i in order) {
            val state = when {
                solved && i == quiz.answerIndex -> 2
                i in tried -> 1
                else -> 0
            }
            AnswerButton(quiz.options[i], state, enabled = !solved && i !in tried, shaker = shakers[i]) {
                if (i == quiz.answerIndex) right() else { tried += i; shakers[i]?.shake(); wrong() }
            }
        }
    }
}

@Composable
private fun TrueFalseQuiz(quiz: Quiz, key: String, solved: Boolean, right: () -> Unit, wrong: () -> Unit) {
    val tried = remember(key) { mutableStateListOf<Boolean>() }
    val shakeT = rememberShaker()
    val shakeF = rememberShaker()
    Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
        for (value in listOf(true, false)) {
            val state = when {
                solved && value == quiz.answerBool -> 2
                value in tried -> 1
                else -> 0
            }
            Column(Modifier.weight(1f)) {
                AnswerButton(if (value) "Stimmt" else "Stimmt nicht", state, !solved && value !in tried, if (value) shakeT else shakeF) {
                    if (value == quiz.answerBool) right() else { tried += value; (if (value) shakeT else shakeF).shake(); wrong() }
                }
            }
        }
    }
}

@Composable
private fun OrderQuiz(quiz: Quiz, key: String, solved: Boolean, right: () -> Unit, wrong: () -> Unit) {
    val fb = LocalFeedback.current
    val shuffled = remember(key) {
        val rnd = Random(key.hashCode())
        var s = quiz.items.shuffled(rnd)
        while (s == quiz.items && quiz.items.size > 1) s = quiz.items.shuffled(rnd)
        s
    }
    val placed = remember(key) { mutableStateListOf<String>() }
    val shakers = shuffled.associateWith { rememberShaker() }
    Column(verticalArrangement = Arrangement.spacedBy(10.dp)) {
        Text(
            if (placed.isEmpty()) "Tippe an, was zuerst kommt." else "Und dann?",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        placed.forEachIndexed { i, item ->
            Surface(shape = RoundedCornerShape(16.dp), color = MaterialTheme.colorScheme.primaryContainer, modifier = Modifier.fillMaxWidth()) {
                Row(Modifier.padding(horizontal = 18.dp, vertical = 14.dp), verticalAlignment = Alignment.CenterVertically) {
                    Text("${i + 1}", fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary)
                    Spacer(Modifier.width(14.dp))
                    Text(item, color = MaterialTheme.colorScheme.onPrimaryContainer)
                }
            }
        }
        for (item in shuffled) {
            if (item in placed) continue
            AnswerButton(item, 0, enabled = !solved, shaker = shakers[item]) {
                if (item == quiz.items[placed.size]) {
                    placed += item
                    if (placed.size == quiz.items.size) right() else fb.tick()
                } else {
                    shakers[item]?.shake(); wrong()
                }
            }
        }
    }
}

@Composable
private fun ErrorQuiz(quiz: Quiz, key: String, solved: Boolean, right: () -> Unit, wrong: () -> Unit) {
    val tokens = remember(key) { quiz.text.orEmpty().split(" ").filter { it.isNotEmpty() } }
    val tried = remember(key) { mutableStateListOf<Int>() }
    val shakers = tokens.indices.associateWith { rememberShaker() }
    Text("Tippe auf das Wort, das nicht stimmt.", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
    Surface(shape = RoundedCornerShape(16.dp), color = MaterialTheme.colorScheme.surfaceContainer, modifier = Modifier.fillMaxWidth()) {
        // words sit close together like normal text; disable the 48dp minimum touch size that would spread the lines apart
        CompositionLocalProvider(LocalMinimumInteractiveComponentSize provides 0.dp) {
        FlowRow(Modifier.padding(14.dp), horizontalArrangement = Arrangement.spacedBy(2.dp), verticalArrangement = Arrangement.spacedBy(2.dp)) {
            tokens.forEachIndexed { i, raw ->
                val isWrong = raw.contains('[')
                val word = raw.replace("[", "").replace("]", "")
                if (solved && isWrong) {
                    val trailing = word.takeLastWhile { !it.isLetterOrDigit() }
                    Row(Modifier.padding(horizontal = 4.dp, vertical = 6.dp), verticalAlignment = Alignment.CenterVertically) {
                        Text(word.dropLast(trailing.length), textDecoration = TextDecoration.LineThrough, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodyLarge)
                        Spacer(Modifier.width(4.dp))
                        Text(quiz.fix.orEmpty() + trailing, color = LocalMannaColors.current.success, fontWeight = FontWeight.Bold, style = MaterialTheme.typography.bodyLarge)
                    }
                } else {
                    val bad = i in tried
                    Surface(
                        onClick = { if (isWrong) right() else { tried += i; shakers[i]?.shake(); wrong() } },
                        enabled = !solved && !bad,
                        shape = RoundedCornerShape(8.dp),
                        color = if (bad) MaterialTheme.colorScheme.surfaceVariant else Color.Transparent,
                        modifier = Modifier.offset { IntOffset((shakers[i]?.offset?.value ?: 0f).roundToInt(), 0) },
                    ) {
                        Text(word, Modifier.padding(horizontal = 4.dp, vertical = 6.dp), style = MaterialTheme.typography.bodyLarge)
                    }
                }
            }
        }
        }
    }
}

@Composable
private fun EstimateQuiz(quiz: Quiz, key: String, solved: Boolean, right: () -> Unit, wrong: () -> Unit) {
    val fb = LocalFeedback.current
    var value by remember(key) { mutableIntStateOf((quiz.min + quiz.max) / 2) }
    var direction by remember(key) { mutableStateOf<String?>(null) }
    val shaker = rememberShaker()
    val anim = remember(key) { Animatable(1f) }
    val scope = rememberCoroutineScope()
    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.fillMaxWidth()) {
        Text(
            "$value ${quiz.unit}".trim(),
            style = MaterialTheme.typography.displaySmall,
            fontWeight = FontWeight.SemiBold,
            color = if (solved) LocalMannaColors.current.success else MaterialTheme.colorScheme.onSurface,
            modifier = Modifier.offset { IntOffset(shaker.offset.value.roundToInt(), 0) },
        )
        Slider(
            value = value.toFloat(),
            onValueChange = {
                val n = it.roundToInt()
                if (n != value) { value = n; fb.tick() }
                direction = null
            },
            valueRange = quiz.min.toFloat()..quiz.max.toFloat(),
            steps = (quiz.max - quiz.min - 1).coerceAtLeast(0),
            enabled = !solved,
        )
        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
            Text("${quiz.min}", color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text("${quiz.max}", color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        direction?.let {
            Spacer(Modifier.height(6.dp))
            Text(it, color = MaterialTheme.colorScheme.secondary, fontWeight = FontWeight.Medium)
        }
        if (!solved) {
            Spacer(Modifier.height(10.dp))
            OutlinedButton(onClick = {
                val diff = value - quiz.answerInt
                if (kotlin.math.abs(diff) <= quiz.tolerance) {
                    right()
                    scope.launch { anim.snapTo(1.2f); anim.animateTo(1f, spring(Spring.DampingRatioMediumBouncy)) }
                } else {
                    direction = if (diff < 0) "Etwas mehr" else "Etwas weniger"
                    shaker.shake(); wrong()
                }
            }, modifier = Modifier.fillMaxWidth().height(52.dp)) { Text("Prüfen") }
        }
    }
}
