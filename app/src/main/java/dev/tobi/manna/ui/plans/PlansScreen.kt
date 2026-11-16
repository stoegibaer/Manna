package dev.tobi.manna.ui.plans

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowBack
import androidx.compose.material.icons.rounded.Check
import androidx.compose.material.icons.rounded.ExpandLess
import androidx.compose.material.icons.rounded.ExpandMore
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewModelScope
import dev.tobi.manna.AppContainer
import dev.tobi.manna.data.plan.Direction
import dev.tobi.manna.data.plan.PlanEntry
import dev.tobi.manna.data.plan.resolve
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn

data class PlanItem(val entry: PlanEntry, val sections: Int, val done: Int) {
    val finished get() = sections > 0 && done >= sections
}

data class PlansState(
    val loading: Boolean = true,
    val active: String = "",
    val start: PlanItem? = null,
    val directions: List<Pair<Direction, List<PlanItem>>> = emptyList(),
)

class PlansViewModel(private val c: AppContainer) : ViewModel() {
    val state = combine(c.settings.settings, c.progress.allSectionsDone) { s, done ->
        val index = c.plans.index()
        val byPlan = done.groupBy { it.planId }
        suspend fun item(e: PlanEntry) = PlanItem(
            e,
            sections = if (e.available) c.plans.plan(e.id).sections.size else 0,
            done = byPlan[e.id]?.size ?: 0,
        )
        PlansState(
            loading = false,
            active = index.resolve(s.activePlan),
            start = index.plans.firstOrNull { it.id == index.start }?.let { item(it) },
            directions = index.directions.map { d ->
                // never more than three plans per direction – too much choice makes starting harder.
                // Show what can be read now first: active plan, unfinished available ones, then "coming soon", finished last.
                val active = index.resolve(s.activePlan)
                d to index.plans.filter { it.direction == d.id }.map { item(it) }.sortedBy {
                    when {
                        it.entry.id == active -> 0
                        it.entry.available && it.done < it.sections -> 1
                        !it.entry.available -> 2
                        else -> 3
                    }
                }.take(3)
            },
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), PlansState())

    suspend fun choose(id: String) = c.settings.update { it.copy(activePlan = id) }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PlansScreen(vm: PlansViewModel, onChosen: (String) -> Unit, onBible: () -> Unit, onBack: () -> Unit) {
    val s by vm.state.collectAsStateWithLifecycle()
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Lesepläne") },
                navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Rounded.ArrowBack, "Zurück") } },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.background),
            )
        },
        containerColor = MaterialTheme.colorScheme.background,
    ) { pad ->
        if (s.loading) return@Scaffold
        Column(
            Modifier.fillMaxSize().padding(pad).verticalScroll(rememberScrollState()).padding(horizontal = 24.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            s.start?.let { start ->
                Text("Der Anfang", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary)
                PlanRow(start, active = s.active == start.entry.id, onChosen)
            }
            Spacer(Modifier.height(8.dp))
            Text("Wohin als Nächstes?", style = MaterialTheme.typography.headlineSmall)
            Text(
                "Wähl eine Richtung – darin warten höchstens drei Pläne.",
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            for ((dir, items) in s.directions) {
                DirectionCard(dir, items, s.active, onChosen)
            }
            Spacer(Modifier.height(8.dp))
            Surface(onClick = onBible, shape = RoundedCornerShape(20.dp), color = MaterialTheme.colorScheme.surfaceContainer, modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(18.dp)) {
                    Text("Frei lesen", style = MaterialTheme.typography.titleLarge)
                    Text("Die ganze Bibel, Buch für Buch – ohne Quiz.", color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
            Spacer(Modifier.height(32.dp))
        }
    }
}

@Composable
private fun DirectionCard(dir: Direction, items: List<PlanItem>, active: String, onChosen: (String) -> Unit) {
    var open by remember { mutableStateOf(items.any { it.entry.id == active }) }
    Surface(
        onClick = { open = !open },
        shape = RoundedCornerShape(20.dp),
        color = MaterialTheme.colorScheme.surfaceContainer,
        modifier = Modifier.fillMaxWidth(),
    ) {
        Column(Modifier.padding(18.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Column(Modifier.weight(1f)) {
                    Text(dir.title, style = MaterialTheme.typography.titleLarge)
                    Text(dir.subtitle, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                Icon(if (open) Icons.Rounded.ExpandLess else Icons.Rounded.ExpandMore, null)
            }
            AnimatedVisibility(open) {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    items.forEach { PlanRow(it, active = it.entry.id == active, onChosen) }
                }
            }
        }
    }
}

@Composable
private fun PlanRow(item: PlanItem, active: Boolean, onChosen: (String) -> Unit) {
    val e = item.entry
    val available = e.available
    Surface(
        onClick = { onChosen(e.id) },
        enabled = available && !active,
        shape = RoundedCornerShape(16.dp),
        color = if (active) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, if (active) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.outline.copy(alpha = 0.4f)),
        modifier = Modifier.fillMaxWidth(),
    ) {
        Row(Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
            Column(Modifier.weight(1f)) {
                Text(
                    e.title,
                    style = MaterialTheme.typography.titleMedium,
                    color = if (available) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.6f),
                )
                Text(
                    when {
                        !available -> "${e.subtitle} · bald verfügbar"
                        active -> "${e.subtitle} · liest du gerade"
                        item.finished -> "${e.subtitle} · gelesen"
                        item.done > 0 -> "${e.subtitle} · ${item.done} von ${item.sections} Abschnitten"
                        else -> "${e.subtitle} · ${item.sections} Abschnitte"
                    },
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = if (available) 1f else 0.6f),
                )
            }
            if (item.finished) Icon(Icons.Rounded.Check, "gelesen", Modifier.size(22.dp), tint = MaterialTheme.colorScheme.primary)
        }
    }
}
