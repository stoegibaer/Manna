package dev.tobi.manna.ui.home

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
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
import androidx.compose.ui.layout.Layout
import androidx.compose.ui.unit.Constraints
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import kotlin.math.roundToInt
import androidx.lifecycle.ViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewModelScope
import dev.tobi.manna.AppContainer
import dev.tobi.manna.data.plan.resolve
import dev.tobi.manna.data.progress.ReadingDay
import dev.tobi.manna.data.settings.Settings
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import dev.tobi.manna.data.garden.Garden
import dev.tobi.manna.ui.components.MustardTree
import dev.tobi.manna.ui.garden.GardenView
import dev.tobi.manna.ui.garden.SCENE_ASPECT
import dev.tobi.manna.ui.garden.TreeChoice
import dev.tobi.manna.ui.session.refLabel
import dev.tobi.manna.ui.settings.formatMinute
import dev.tobi.manna.ui.theme.BibleFont
import dev.tobi.manna.update.UpdateCard
import dev.tobi.manna.update.UpdateState
import dev.tobi.manna.update.Updater
import dev.tobi.manna.update.showOnHome
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
    /** Garden: planted species by position. */
    val planted: List<String> = listOf(Garden.ORDER.first()),
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
            combine(c.progress.allSectionsDone, c.progress.garden, ::Pair),
        ) { done, total, days, (all, planted) ->
            val plan = c.plans.plan(planId)
            val doneIds = done.map { it.sectionId }.toSet()
            val rereadPos = s.rereads[planId]
            val idx = plan.nextIndex(doneIds, rereadPos)
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
                planted = planted,
                doneInPlan = rereadPos ?: doneIds.size,
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

    /** Plants the next tree after one was fully grown. */
    fun plant(species: String) = viewModelScope.launch { c.progress.plant(state.value.planted.size, species) }

    fun acceptSuggestion(minute: Int) = viewModelScope.launch {
        c.settings.update { it.copy(anchorMinute = minute) }
        c.rescheduleReminders()
    }

    /** „Später“ on the update hint: back tomorrow. */
    fun hideUpdate() = viewModelScope.launch {
        c.settings.update { it.copy(updateHiddenUntil = LocalDate.now().plusDays(1).toString()) }
    }

    fun hideSuggestion() = viewModelScope.launch {
        c.settings.update { it.copy(suggestionHiddenUntil = LocalDate.now().plusDays(14).toString()) }
    }
}

@Composable
fun HomeScreen(
    vm: HomeViewModel, settings: Settings, updater: Updater, debugTree: Int = -1, debugChoice: Boolean = false,
    onStart: () -> Unit, onStartMore: () -> Unit, onOneVerse: () -> Unit,
    onSettings: () -> Unit, onPlans: () -> Unit, onAlbum: () -> Unit, onReminders: () -> Unit,
) {
    val s by vm.state.collectAsStateWithLifecycle()
    val update by updater.state.collectAsStateWithLifecycle()
    // „Später“ hides an offered update until tomorrow; a running download stays visible
    val waiting = update is UpdateState.Available || update is UpdateState.Failed
    val showUpdate = update.showOnHome() && !(waiting && settings.updateHiddenUntil > LocalDate.now().toString())
    // a tree is grown but the next one is not chosen yet (e.g. after an update with many sections read)
    var choiceHidden by rememberSaveable { mutableStateOf(false) }
    val debugPlanted = if (debugChoice) s.planted else Garden.ORDER + Garden.LIFE
    val pending = if (debugTree >= 0) debugChoice && Garden.choicePending(debugTree, s.planted) else Garden.choicePending(s.total, s.planted)
    if (!s.loading && !choiceHidden && pending) {
        Dialog(onDismissRequest = { choiceHidden = true }, properties = DialogProperties(usePlatformDefaultWidth = false)) {
            Surface(shape = RoundedCornerShape(28.dp), color = MaterialTheme.colorScheme.surface, modifier = Modifier.padding(16.dp)) {
                TreeChoice(
                    s.planted.last(), Garden.offers(s.planted), settings.animations, onPick = { vm.plant(it) },
                    modifier = Modifier.verticalScroll(rememberScrollState()).padding(20.dp),
                )
            }
        }
    }
    val shownTotal = if (debugTree >= 0) debugTree else s.total
    // while the first tree grows, the mustard tree is shown alone, as before; then the garden
    val firstTree = Garden.progress(shownTotal).done == 0
    BoxWithConstraints(Modifier.fillMaxSize().statusBarsPadding().navigationBarsPadding()) {
        val viewport = constraints.maxHeight
        Layout(
            modifier = Modifier.fillMaxWidth().verticalScroll(rememberScrollState()).padding(horizontal = 24.dp),
            content = {
                Row(Modifier.fillMaxWidth().padding(top = 8.dp), verticalAlignment = Alignment.CenterVertically) {
                    Text("Manna", style = MaterialTheme.typography.headlineSmall, modifier = Modifier.weight(1f))
                    IconButton(onClick = onAlbum) { Icon(Icons.Outlined.Style, "Sammlung") }
                    IconButton(onClick = onPlans) { Icon(Icons.AutoMirrored.Outlined.MenuBook, "Lesepläne") }
                    IconButton(onClick = onSettings) { Icon(Icons.Outlined.Settings, "Einstellungen") }
                }

                // debug preview (--ei debugTree N): a garden with all trees in their usual order
                if (firstTree) MustardTree(
                    sections = shownTotal.toFloat(),
                    animate = settings.animations,
                    modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp),
                ) else GardenView(
                    total = shownTotal,
                    planted = if (debugTree >= 0) debugPlanted else s.planted,
                    animate = settings.animations,
                    corner = 0.dp,
                    modifier = Modifier.fillMaxWidth(),
                )

                Column(Modifier.fillMaxWidth(), horizontalAlignment = Alignment.CenterHorizontally) {
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
                            showUpdate -> UpdateCard(update, updater, onLater = { vm.hideUpdate() }, modifier = Modifier.padding(bottom = 12.dp))
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
                                    val mainLabel = if (s.doneInPlan == 0) "Los geht’s" else "Weiterlesen"
                                    Button(onClick = onStart, modifier = Modifier.fillMaxWidth().height(60.dp)) {
                                        Text(mainLabel, style = MaterialTheme.typography.titleMedium)
                                    }
                                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                                        TextButton(onClick = onOneVerse) { Text("Nur 1 Vers") }
                                        TextButton(onClick = onStartMore) { Text("Mehr am Stück") }
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
            },
        ) { m, c ->
            val w = c.maxWidth
            val loose = Constraints(minWidth = w, maxWidth = w)
            val header = m[0].measure(loose)
            val bottom = m[2].measure(loose)
            // the mustard tree takes the free space, but never less than a third of the screen;
            // the garden spans the full screen width (beyond the side padding) in its own proportions.
            // If hint and plan card need more room, the page scrolls instead of squeezing the plant.
            val pad = if (firstTree) 0 else 24.dp.roundToPx()
            val treeW = w + 2 * pad
            val treeH = if (firstTree) maxOf((viewport * 0.35f).roundToInt(), viewport - header.height - bottom.height)
                else (treeW * SCENE_ASPECT).roundToInt()
            val tree = m[1].measure(Constraints.fixed(treeW, treeH))
            layout(w, header.height + treeH + bottom.height) {
                header.place(0, 0)
                tree.place(-pad, header.height)
                bottom.place(0, header.height + treeH)
            }
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
