package dev.tobi.manna.ui.album

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.ModalBottomSheet
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.unit.dp
import dev.tobi.manna.data.plan.Place
import dev.tobi.manna.ui.components.AtlasMap
import dev.tobi.manna.ui.components.AtlasPoint

/** A section of a plan that takes place at a place. */
data class AtlasOccurrence(val planTitle: String, val sectionTitle: String, val done: Boolean)

/** A place used by at least one available plan; visited once one of its sections is done. */
data class AtlasPlace(val place: Place, val occurrences: List<AtlasOccurrence>) {
    val visited get() = occurrences.any { it.done }
}

@Composable
fun AtlasTab(places: List<AtlasPlace>) {
    var selected by rememberSaveable { mutableStateOf<String?>(null) }
    val visited = places.filter { it.visited }
    val points = places.map { AtlasPoint(it.place.id, it.place.name, it.place.lat, it.place.lon, it.visited, it.occurrences.size) }

    Column(Modifier.fillMaxSize()) {
        AtlasMap(
            points, selected, onSelect = { selected = it },
            Modifier.padding(start = 20.dp, end = 20.dp, top = 12.dp).fillMaxWidth().aspectRatio(1.45f).clip(RoundedCornerShape(18.dp)),
        )
        LazyColumn(
            Modifier.fillMaxWidth().weight(1f),
            contentPadding = PaddingValues(start = 20.dp, end = 20.dp, top = 12.dp, bottom = 32.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            item {
                Text(
                    "${visited.size} von ${places.size} Orten besucht",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(bottom = 4.dp),
                )
            }
            if (visited.isEmpty()) item {
                Text(
                    "Wenn du einen Abschnitt abschließt, der an einem Ort spielt, erscheint der Ort hier und auf der Karte.",
                    style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            items(visited, key = { it.place.id }) { p ->
                Surface(
                    onClick = { selected = p.place.id },
                    color = MaterialTheme.colorScheme.surfaceContainer,
                    shape = RoundedCornerShape(14.dp),
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    Column(Modifier.padding(horizontal = 16.dp, vertical = 12.dp)) {
                        Text(p.place.name, style = MaterialTheme.typography.titleMedium)
                        Text(
                            p.occurrences.filter { it.done }.map { it.planTitle }.distinct().joinToString(" · "),
                            style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant,
                        )
                    }
                }
            }
        }
    }

    places.firstOrNull { it.place.id == selected }?.let { PlaceSheet(it, onDismiss = { selected = null }) }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun PlaceSheet(p: AtlasPlace, onDismiss: () -> Unit) {
    ModalBottomSheet(onDismissRequest = onDismiss, containerColor = MaterialTheme.colorScheme.surface) {
        Column(
            Modifier.fillMaxWidth().verticalScroll(rememberScrollState()).padding(horizontal = 24.dp).padding(bottom = 32.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            if (!p.visited) {
                Text("Noch nicht entdeckt", style = MaterialTheme.typography.titleLarge)
                Text(
                    "Dieser Ort kommt vor in: " + p.occurrences.map { it.planTitle }.distinct().joinToString(", ") + ".",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
                return@Column
            }
            Text(p.place.name, style = MaterialTheme.typography.titleLarge)
            if (p.place.text.isNotBlank()) Text(p.place.text, color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text("Kommt vor in", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(top = 8.dp))
            p.occurrences.filter { it.done }.forEach { o ->
                Text("${o.planTitle} · ${o.sectionTitle}", style = MaterialTheme.typography.bodyLarge)
            }
            val more = p.occurrences.count { !it.done }
            if (more > 0) Text(
                if (more == 1) "und in einem weiteren Abschnitt" else "und in $more weiteren Abschnitten",
                style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
    }
}
