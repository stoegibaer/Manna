package dev.tobi.manna.ui.album

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.GridItemSpan
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowBack
import androidx.compose.material.icons.outlined.Lock
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
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items as listItems
import androidx.compose.foundation.layout.Row
import androidx.compose.material3.PrimaryTabRow
import androidx.compose.material3.Tab
import androidx.compose.material3.TextButton
import dev.tobi.manna.data.progress.JournalEntry
import dev.tobi.manna.ui.session.REFLECTION_TAGS
import kotlinx.coroutines.launch
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.lifecycle.ViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewModelScope
import dev.tobi.manna.AppContainer
import dev.tobi.manna.data.plan.Card
import dev.tobi.manna.ui.components.CardTile
import dev.tobi.manna.ui.components.cardColors
import dev.tobi.manna.ui.components.cardLabel
import dev.tobi.manna.ui.theme.BibleFont
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn

data class AlbumGroup(val planTitle: String, val cards: List<Pair<Card, Boolean>>)
data class AlbumState(val loading: Boolean = true, val groups: List<AlbumGroup> = emptyList()) {
    val total get() = groups.sumOf { it.cards.size }
    val found get() = groups.sumOf { g -> g.cards.count { it.second } }
}

data class SavedVerse(val book: Int, val chapter: Int, val verse: Int, val ref: String, val text: String, val memory: Boolean)

class AlbumViewModel(private val c: AppContainer) : ViewModel() {
    val verses = c.progress.favorites.map { favs ->
        val books = c.text.info().books.associateBy { it.nr }
        favs.mapNotNull { f ->
            val v = c.text.verses(f.book, f.chapter, f.verse, f.verse).firstOrNull() ?: return@mapNotNull null
            SavedVerse(f.book, f.chapter, f.verse, "${books[f.book]?.name} ${f.chapter},${f.verse}", v.text, f.source == "memory")
        }
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    val journal = c.progress.journal.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    fun removeVerse(v: SavedVerse) = viewModelScope.launch { c.progress.setFavorite(v.book, v.chapter, v.verse, false) }

    val atlas = c.progress.allSectionsDone.map { done ->
        val have = done.map { it.planId to it.sectionId }.toSet()
        val places = c.plans.places()
        val occ = LinkedHashMap<String, MutableList<AtlasOccurrence>>()
        for (e in c.plans.index().plans.filter { it.available }) {
            val plan = c.plans.plan(e.id)
            for (sec in plan.sections) {
                val id = sec.place ?: continue
                if (id !in places) continue
                occ.getOrPut(id) { mutableListOf() } += AtlasOccurrence(plan.title, sec.title, (plan.id to sec.id) in have)
            }
        }
        val collator = java.text.Collator.getInstance(java.util.Locale.GERMAN)
        occ.map { (id, list) -> AtlasPlace(places.getValue(id), list) }.sortedWith(compareBy(collator) { it.place.name })
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptyList())

    val state = c.progress.cards.map { unlocked ->
        val have = unlocked.map { it.planId to it.cardId }.toSet()
        val groups = c.plans.index().plans.filter { it.available }.map { e ->
            val plan = c.plans.plan(e.id)
            AlbumGroup(plan.title, plan.cards.map { it to ((plan.id to it.id) in have) })
        }.filter { it.cards.isNotEmpty() }.sortedByDescending { g -> g.cards.count { it.second } } // started collections first
        AlbumState(false, groups)
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), AlbumState())
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AlbumScreen(vm: AlbumViewModel, onBack: () -> Unit) {
    val s by vm.state.collectAsStateWithLifecycle()
    val verses by vm.verses.collectAsStateWithLifecycle()
    val journal by vm.journal.collectAsStateWithLifecycle()
    val atlas by vm.atlas.collectAsStateWithLifecycle()
    var open by remember { mutableStateOf<Card?>(null) }
    var tab by rememberSaveable { mutableIntStateOf(0) }
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Sammlung") },
                navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Rounded.ArrowBack, "Zurück") } },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.background),
            )
        },
        containerColor = MaterialTheme.colorScheme.background,
    ) { pad ->
        if (s.loading) return@Scaffold
        Column(Modifier.fillMaxSize().padding(pad)) {
        PrimaryTabRow(selectedTabIndex = tab, containerColor = MaterialTheme.colorScheme.background) {
            listOf("Karten", "Verse", "Tagebuch", "Atlas").forEachIndexed { i, t ->
                Tab(selected = tab == i, onClick = { tab = i }, text = { Text(t) })
            }
        }
        when (tab) {
            1 -> VersesTab(verses, vm::removeVerse)
            2 -> JournalTab(journal)
            3 -> AtlasTab(atlas)
            else -> LazyVerticalGrid(
            columns = GridCells.Fixed(2),
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(start = 20.dp, end = 20.dp, top = 12.dp, bottom = 32.dp),
            horizontalArrangement = Arrangement.spacedBy(12.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            item(span = { GridItemSpan(maxLineSpan) }) {
                Text(
                    "${s.found} von ${s.total} Karten entdeckt",
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(bottom = 4.dp),
                )
            }
            for (g in s.groups) {
                item(span = { GridItemSpan(maxLineSpan) }) {
                    Text(g.planTitle, style = MaterialTheme.typography.titleLarge, modifier = Modifier.padding(top = 12.dp))
                }
                items(g.cards, key = { g.planTitle + it.first.id }) { (card, unlocked) ->
                    MiniCard(card, unlocked) { open = card }
                }
            }
        }
        }
        }
    }
    open?.let { card ->
        Dialog(onDismissRequest = { open = null }) { CardTile(card) }
    }
}

@Composable
private fun VersesTab(verses: List<SavedVerse>, onRemove: (SavedVerse) -> Unit) {
    if (verses.isEmpty()) {
        Empty("Noch keine Verse gespeichert.", "Drück beim Lesen lange auf einen Vers, um ihn hier zu sammeln. Gelernte Merkverse landen automatisch hier.")
        return
    }
    LazyColumn(contentPadding = PaddingValues(20.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        listItems(verses, key = { "${it.book}-${it.chapter}-${it.verse}" }) { v ->
            Surface(color = MaterialTheme.colorScheme.surfaceContainer, shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text(v.text, fontFamily = BibleFont, style = MaterialTheme.typography.bodyLarge)
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(v.ref + if (v.memory) " · Merkvers" else "", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f))
                        TextButton(onClick = { onRemove(v) }) { Text("Entfernen") }
                    }
                }
            }
        }
    }
}

@Composable
private fun JournalTab(entries: List<JournalEntry>) {
    if (entries.isEmpty()) {
        Empty("Dein Tagebuch ist noch leer.", "Nach jedem Abschnitt kannst du mit einem Tipp festhalten, was du mitnimmst.")
        return
    }
    val labels = REFLECTION_TAGS.toMap()
    val fmt = remember { java.time.format.DateTimeFormatter.ofPattern("d. MMMM yyyy", java.util.Locale.GERMAN) }
    LazyColumn(contentPadding = PaddingValues(20.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        listItems(entries, key = { it.planId + it.sectionId }) { e ->
            Surface(color = MaterialTheme.colorScheme.surfaceContainer, shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text(e.sectionTitle, style = MaterialTheme.typography.titleMedium)
                    val date = java.time.Instant.ofEpochMilli(e.savedAt).atZone(java.time.ZoneId.systemDefault()).toLocalDate()
                    Text(fmt.format(date), style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    val tags = e.tags.split(',').mapNotNull { labels[it] }
                    if (tags.isNotEmpty()) Text(tags.joinToString(" · "), color = MaterialTheme.colorScheme.secondary, style = MaterialTheme.typography.bodyMedium)
                    if (e.note.isNotBlank()) Text(e.note, style = MaterialTheme.typography.bodyLarge)
                }
            }
        }
    }
}

@Composable
private fun Empty(title: String, text: String) {
    Column(Modifier.fillMaxSize().padding(32.dp), verticalArrangement = Arrangement.Center, horizontalAlignment = Alignment.CenterHorizontally) {
        Text(title, style = MaterialTheme.typography.titleMedium)
        Text(text, color = MaterialTheme.colorScheme.onSurfaceVariant, textAlign = androidx.compose.ui.text.style.TextAlign.Center, modifier = Modifier.padding(top = 8.dp))
    }
}

@Composable
private fun MiniCard(card: Card, unlocked: Boolean, onClick: () -> Unit) {
    val (a, b) = cardColors(card.type)
    Surface(
        onClick = onClick,
        enabled = unlocked,
        shape = RoundedCornerShape(16.dp),
        color = MaterialTheme.colorScheme.surface,
        border = BorderStroke(1.dp, if (unlocked) a.copy(alpha = 0.4f) else MaterialTheme.colorScheme.outline.copy(alpha = 0.3f)),
        modifier = Modifier.fillMaxWidth().height(118.dp),
    ) {
        if (unlocked) {
            Column {
                Box(Modifier.fillMaxWidth().height(10.dp).background(Brush.horizontalGradient(listOf(a, b))))
                Column(Modifier.padding(14.dp)) {
                    Text(cardLabel(card.type), fontSize = 10.sp, fontWeight = FontWeight.Bold, letterSpacing = 1.4.sp, color = a)
                    Text(card.name, fontFamily = BibleFont, fontWeight = FontWeight.SemiBold, fontSize = 18.sp, maxLines = 2, overflow = TextOverflow.Ellipsis)
                }
            }
        } else {
            Box(Modifier.fillMaxSize().background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(Icons.Outlined.Lock, null, Modifier.size(22.dp), tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.6f))
                    Text(cardLabel(card.type), fontSize = 10.sp, fontWeight = FontWeight.Bold, letterSpacing = 1.4.sp, color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.6f), modifier = Modifier.padding(top = 6.dp))
                }
            }
        }
    }
}
