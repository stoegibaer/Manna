package dev.tobi.manna.ui.home

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.MenuBook
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material.icons.outlined.Style
import androidx.compose.material.icons.rounded.Check
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewModelScope
import dev.tobi.manna.AppContainer
import dev.tobi.manna.data.plan.resolve
import dev.tobi.manna.data.progress.ReadingDay
import dev.tobi.manna.data.settings.Settings
import dev.tobi.manna.ui.components.MustardTree
import dev.tobi.manna.ui.session.refLabel
import dev.tobi.manna.ui.settings.formatMinute
import dev.tobi.manna.ui.theme.BibleFont
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import java.time.DayOfWeek
import java.time.LocalDate
import java.time.temporal.ChronoUnit
import kotlin.math.abs

data class ReEntry(val daysAway: Int, val lastTitle: String, val lastSummary: String)

data class HomeState(
    val loading: Boolean = true,
    val planTitle: String = "",
    val nextTitle: String? = null,
    val nextRef: String = "",
    val teaser: String? = null,
    val total: Int = 0,
    val doneInPlan: Int = 0,
    val readToday: Boolean = false,
    /** Monday..Sunday of the current week: read on that day? */
    val week: List<Boolean> = List(7) { false },
    val todayIndex: Int = 0,
    val weeklyGoal: Int = 4,
    val reEntry: ReEntry? = null,
    val showReminderInvite: Boolean = false,
    /** Suggested reminder minute based on when the user actually reads. */
    val suggestMinute: Int? = null,
) {
    val weekCount get() = week.count { it }
}

@OptIn(ExperimentalCoroutinesApi::class)
class HomeViewModel(private val c: AppContainer) : ViewModel() {
    val state = c.settings.settings.flatMapLatest { s ->
        val planId = c.plans.index().resolve(s.activePlan)
        val today = LocalDate.now()
        combine(
            c.progress.sectionsDone(planId),
            c.progress.totalSections,
            c.progress.daysSince(today.minusDays(14)),
            c.progress.allSectionsDone,
        ) { done, total, days, all ->
            val plan = c.plans.plan(planId)
            val doneIds = done.map { it.sectionId }.toSet()
            val idx = plan.sections.indexOfFirst { it.id !in doneIds }
            val next = plan.sections.getOrNull(idx)
            val books = c.text.info().books.associateBy { it.nr }
            val active = days.filter { it.verses > 0 || it.sections > 0 }
            val activeDates = active.map { it.date }.toSet()
            val monday = today.with(DayOfWeek.MONDAY)

            // back after a break (3+ days, or nothing in the last two weeks)? – welcome, no reproach
            val lastActive = active.maxOfOrNull { it.date }?.let { LocalDate.parse(it) }
            val daysAway = lastActive?.let { ChronoUnit.DAYS.between(it, today).toInt() } ?: 15
            val reEntry = if (total > 0 && daysAway >= 3) {
                all.maxByOrNull { it.completedAt }?.let { last ->
                    val sec = runCatching { c.plans.plan(last.planId) }.getOrNull()?.sections?.firstOrNull { it.id == last.sectionId }
                    sec?.let { ReEntry(daysAway, it.title, it.summary) }
                }
            } else null

            HomeState(
                loading = false,
                planTitle = plan.title,
                nextTitle = next?.title,
                nextRef = next?.let { refLabel(it.refs) { n -> books[n]?.name ?: "" } }.orEmpty(),
                // the curiosity question of the previous section leads into the next one
                teaser = if (idx > 0) plan.sections[idx - 1].teaser else null,
                total = total,
                doneInPlan = doneIds.size,
                readToday = today.toString() in activeDates,
                week = List(7) { monday.plusDays(it.toLong()).toString() in activeDates },
                todayIndex = today.dayOfWeek.value - 1,
                weeklyGoal = s.weeklyGoal,
                reEntry = reEntry,
                showReminderInvite = !s.reminderSetupSeen && total > 0,
                suggestMinute = suggestion(s, active, today),
            )
        }
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), HomeState())

    /** After a week or two of real reading: if the user usually reads at another time, offer to move the reminder. */
    private fun suggestion(s: Settings, active: List<ReadingDay>, today: LocalDate): Int? {
        if (!s.remindersOn || s.suggestionHiddenUntil > today.toString()) return null
        val minutes = active.map { it.firstMinute }.filter { it >= 0 }.sorted()
        if (minutes.size < 7) return null
        val median = minutes[minutes.size / 2]
        val rounded = (median + 2) / 5 * 5
        return rounded.takeIf { abs(it - s.anchorMinute) >= 45 }
    }

    fun dismissInvite() = viewModelScope.launch { c.settings.update { it.copy(reminderSetupSeen = true) } }

    fun acceptSuggestion(minute: Int) = viewModelScope.launch {
        c.settings.update { it.copy(anchorMinute = minute) }
        c.rescheduleReminders()
    }

    fun hideSuggestion() = viewModelScope.launch {
        c.settings.update { it.copy(suggestionHiddenUntil = LocalDate.now().plusDays(14).toString()) }
    }
}

@Composable
fun HomeScreen(
    vm: HomeViewModel, settings: Settings, debugTree: Int = -1,
    onStart: () -> Unit, onStartMore: () -> Unit, onOneVerse: () -> Unit,
    onSettings: () -> Unit, onPlans: () -> Unit, onAlbum: () -> Unit, onReminders: () -> Unit,
) {
    val s by vm.state.collectAsStateWithLifecycle()
    Column(
        Modifier.fillMaxSize().statusBarsPadding().navigationBarsPadding().padding(horizontal = 24.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Row(Modifier.fillMaxWidth().padding(top = 8.dp), verticalAlignment = Alignment.CenterVertically) {
            Text("Manna", style = MaterialTheme.typography.headlineSmall, modifier = Modifier.weight(1f))
            IconButton(onClick = onAlbum) { Icon(Icons.Outlined.Style, "Sammlung") }
            IconButton(onClick = onPlans) { Icon(Icons.AutoMirrored.Outlined.MenuBook, "Lesepläne") }
            IconButton(onClick = onSettings) { Icon(Icons.Outlined.Settings, "Einstellungen") }
        }

        MustardTree(
            sections = (if (debugTree >= 0) debugTree else s.total).toFloat(),
            animate = settings.animations,
            modifier = Modifier.fillMaxWidth().weight(1f).padding(vertical = 8.dp),
        )

        if (!s.loading) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    when (s.total) {
                        0 -> "Ein Senfkorn. Mit jedem Abschnitt wächst es."
                        1 -> "1 Abschnitt gelesen"
                        else -> "${s.total} Abschnitte gelesen"
                    },
                    style = MaterialTheme.typography.bodyLarge,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    textAlign = TextAlign.Center,
                )
                if (s.readToday) {
                    Spacer(Modifier.width(10.dp))
                    Surface(color = MaterialTheme.colorScheme.primaryContainer, shape = RoundedCornerShape(50)) {
                        Row(Modifier.padding(horizontal = 10.dp, vertical = 3.dp), verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Rounded.Check, null, Modifier.size(14.dp), tint = MaterialTheme.colorScheme.primary)
                            Spacer(Modifier.width(4.dp))
                            Text("heute", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onPrimaryContainer)
                        }
                    }
                }
            }
            Spacer(Modifier.height(10.dp))
            WeekRow(s)
            Spacer(Modifier.height(16.dp))

            // at most one hint at a time – too many cards make starting harder
            when {
                s.reEntry != null -> HintCard(
                    title = "Schön, dass du da bist.",
                    text = "Zuletzt hast du „${s.reEntry!!.lastTitle}“ gelesen: ${s.reEntry!!.lastSummary}",
                )
                s.suggestMinute != null -> HintCard(
                    title = "Du liest meistens gegen ${formatMinute(s.suggestMinute!!)} Uhr.",
                    text = "Soll die Erinnerung dorthin wandern?",
                    primary = "Ja, verschieben" to { vm.acceptSuggestion(s.suggestMinute!!) },
                    secondary = "Nein danke" to { vm.hideSuggestion() },
                )
                s.showReminderInvite -> HintCard(
                    title = "Soll Manna dich erinnern?",
                    text = "Ein Vers am Tag reicht. Leg fest, wann du liest – Manna erinnert dich freundlich.",
                    primary = "Einrichten" to onReminders,
                    secondary = "Nicht jetzt" to { vm.dismissInvite() },
                )
            }

            Surface(
                color = MaterialTheme.colorScheme.surfaceContainer,
                shape = RoundedCornerShape(24.dp),
                modifier = Modifier.fillMaxWidth(),
            ) {
                Column(Modifier.padding(20.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(s.planTitle, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                    if (s.nextTitle != null) {
                        s.teaser?.let {
                            Text(it, fontFamily = BibleFont, fontStyle = FontStyle.Italic, style = MaterialTheme.typography.bodyLarge, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                        Text(s.nextTitle!!, style = MaterialTheme.typography.titleLarge)
                        Text(s.nextRef, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        Spacer(Modifier.height(4.dp))
                        Button(onClick = onStart, modifier = Modifier.fillMaxWidth().height(60.dp)) {
                            Text(if (s.doneInPlan == 0) "Los geht’s" else "Weiterlesen", style = MaterialTheme.typography.titleMedium)
                        }
                        // energy check without an extra step: the big button is „normal“
                        Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                            TextButton(onClick = onOneVerse) { Text("Wenig Kraft: 1 Vers") }
                            TextButton(onClick = onStartMore) { Text("Viel Energie: mehr") }
                        }
                    } else {
                        Text("Plan abgeschlossen", style = MaterialTheme.typography.titleLarge)
                        Text("Stark. Such dir aus, wie es weitergeht.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                        Spacer(Modifier.height(4.dp))
                        Button(onClick = onPlans, modifier = Modifier.fillMaxWidth().height(60.dp)) {
                            Text("Wohin als Nächstes?", style = MaterialTheme.typography.titleMedium)
                        }
                    }
                }
            }
            Spacer(Modifier.height(16.dp))
        }
    }
}

/** Seven dots for the week. Read days are filled, nothing is ever marked as „missed“. */
@Composable
private fun WeekRow(s: HomeState) {
    val labels = listOf("M", "D", "M", "D", "F", "S", "S")
    Row(verticalAlignment = Alignment.CenterVertically) {
        s.week.forEachIndexed { i, read ->
            Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.padding(horizontal = 5.dp)) {
                Box(
                    Modifier.size(14.dp)
                        .then(if (read) Modifier.background(MaterialTheme.colorScheme.primary, CircleShape) else Modifier)
                        .border(
                            BorderStroke(1.5.dp, if (i == s.todayIndex || read) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outline.copy(alpha = 0.5f)),
                            CircleShape,
                        )
                )
                Text(labels[i], fontSize = 10.sp, color = MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = if (i == s.todayIndex) FontWeight.Bold else FontWeight.Normal)
            }
        }
        Spacer(Modifier.width(10.dp))
        Text(
            if (s.weekCount >= s.weeklyGoal) "Wochenziel erreicht" else "${s.weekCount} von ${s.weeklyGoal} Tagen",
            style = MaterialTheme.typography.bodyMedium,
            color = if (s.weekCount >= s.weeklyGoal) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}

@Composable
private fun HintCard(title: String, text: String, primary: Pair<String, () -> Unit>? = null, secondary: Pair<String, () -> Unit>? = null) {
    Surface(color = MaterialTheme.colorScheme.secondaryContainer, shape = RoundedCornerShape(20.dp), modifier = Modifier.fillMaxWidth().padding(bottom = 12.dp)) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Text(title, style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onSecondaryContainer)
            Text(text, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSecondaryContainer, maxLines = 3)
            if (primary != null || secondary != null) {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
                    val c = MaterialTheme.colorScheme.onSecondaryContainer
                    secondary?.let { (l, a) -> TextButton(onClick = a) { Text(l, color = c.copy(alpha = 0.75f)) } }
                    primary?.let { (l, a) -> TextButton(onClick = a) { Text(l, color = c, fontWeight = FontWeight.Bold) } }
                }
            }
        }
    }
}
