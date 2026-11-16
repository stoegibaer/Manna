package dev.tobi.manna.ui.home

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.navigationBarsPadding
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.Settings
import androidx.compose.material.icons.outlined.Style
import androidx.compose.material.icons.automirrored.outlined.MenuBook
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewModelScope
import dev.tobi.manna.AppContainer
import dev.tobi.manna.data.settings.Settings
import dev.tobi.manna.ui.components.MustardTree
import dev.tobi.manna.ui.session.refLabel
import dev.tobi.manna.ui.theme.BibleFont
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.distinctUntilChanged
import dev.tobi.manna.data.plan.resolve
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn

data class HomeState(
    val loading: Boolean = true,
    val planTitle: String = "",
    val nextTitle: String? = null,
    val nextRef: String = "",
    val teaser: String? = null,
    val total: Int = 0,
    val doneInPlan: Int = 0,
)

@OptIn(ExperimentalCoroutinesApi::class)
class HomeViewModel(c: AppContainer) : ViewModel() {
    val state = c.settings.settings.map { c.plans.index().resolve(it.activePlan) }.distinctUntilChanged().flatMapLatest { planId ->
        combine(c.progress.sectionsDone(planId), c.progress.totalSections) { done, total ->
            val plan = c.plans.plan(planId)
            val doneIds = done.map { it.sectionId }.toSet()
            val idx = plan.sections.indexOfFirst { it.id !in doneIds }
            val next = plan.sections.getOrNull(idx)
            val books = c.text.info().books.associateBy { it.nr }
            HomeState(
                loading = false,
                planTitle = plan.title,
                nextTitle = next?.title,
                nextRef = next?.let { refLabel(it.refs) { n -> books[n]?.name ?: "" } }.orEmpty(),
                // the curiosity question of the previous section leads into the next one
                teaser = if (idx > 0) plan.sections[idx - 1].teaser else null,
                total = total,
                doneInPlan = doneIds.size,
            )
        }
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), HomeState())
}

@Composable
fun HomeScreen(
    vm: HomeViewModel, settings: Settings, debugTree: Int = -1,
    onStart: () -> Unit, onSettings: () -> Unit, onPlans: () -> Unit, onAlbum: () -> Unit,
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
            Spacer(Modifier.height(20.dp))

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
            Spacer(Modifier.height(20.dp))
        }
    }
}
