package dev.tobi.manna.ui.bible

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.GridItemSpan
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowBack
import androidx.compose.material.icons.automirrored.rounded.KeyboardArrowLeft
import androidx.compose.material.icons.automirrored.rounded.KeyboardArrowRight
import androidx.compose.material.icons.automirrored.rounded.VolumeUp
import androidx.compose.material.icons.rounded.Check
import androidx.compose.material.icons.rounded.Stop
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.ViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewModelScope
import dev.tobi.manna.AppContainer
import dev.tobi.manna.audio.rememberSpeaker
import dev.tobi.manna.data.bible.BookInfo
import dev.tobi.manna.data.bible.Verse
import dev.tobi.manna.data.settings.Settings
import dev.tobi.manna.ui.components.LocalFeedback
import dev.tobi.manna.ui.components.VerseText
import dev.tobi.manna.ui.components.key
import dev.tobi.manna.ui.theme.bibleTextStyle
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

/** Free reading in the whole Bible – no quiz, same reading aids. */
class BibleViewModel(private val c: AppContainer) : ViewModel() {
    val translationId = c.text.translationId
    val books = MutableStateFlow<List<BookInfo>>(emptyList())
    val translationName = MutableStateFlow("")
    val chapter = MutableStateFlow<List<Verse>>(emptyList())
    val chapterRead = MutableStateFlow(false)
    val favorites = c.progress.favorites.map { l -> l.map { Triple(it.book, it.chapter, it.verse) }.toSet() }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5000), emptySet())

    init {
        viewModelScope.launch {
            val info = c.text.info()
            books.value = info.books
            translationName.value = info.name
        }
    }

    fun load(book: Int, ch: Int) = viewModelScope.launch {
        chapter.value = c.text.chapter(book, ch)
        chapterRead.value = false
    }

    fun toggleFavorite(v: Verse) {
        val on = v.key() !in favorites.value
        viewModelScope.launch { c.progress.setFavorite(v.book, v.chapter, v.verse, on) }
    }

    /** Counts for the daily minimum and the week. */
    fun markRead() {
        if (chapterRead.value) return
        chapterRead.update { true }
        viewModelScope.launch { c.logReading(verses = chapter.value.size, sections = 0) }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun Bar(title: String, onBack: () -> Unit, actions: @Composable () -> Unit = {}) {
    TopAppBar(
        title = { Text(title) },
        navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Rounded.ArrowBack, "Zurück") } },
        actions = { actions() },
        colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.background),
    )
}

@Composable
fun BooksScreen(vm: BibleViewModel, onBook: (Int) -> Unit, onBack: () -> Unit) {
    val books by vm.books.collectAsStateWithLifecycle()
    val name by vm.translationName.collectAsStateWithLifecycle()
    Scaffold(topBar = { Bar("Ganze Bibel", onBack) }, containerColor = MaterialTheme.colorScheme.background) { pad ->
        LazyVerticalGrid(
            columns = GridCells.Fixed(2),
            modifier = Modifier.fillMaxSize().padding(pad),
            contentPadding = PaddingValues(start = 20.dp, end = 20.dp, bottom = 32.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            for ((label, range) in listOf("Altes Testament" to 1..39, "Neues Testament" to 40..66)) {
                item(span = { GridItemSpan(maxLineSpan) }) {
                    Text(label, style = MaterialTheme.typography.titleLarge, modifier = Modifier.padding(top = 12.dp, bottom = 4.dp))
                }
                items(books.filter { it.nr in range }, key = { it.nr }) { b ->
                    Surface(onClick = { onBook(b.nr) }, shape = RoundedCornerShape(14.dp), color = MaterialTheme.colorScheme.surfaceContainer) {
                        Text(b.name, Modifier.padding(horizontal = 16.dp, vertical = 14.dp), style = MaterialTheme.typography.bodyLarge)
                    }
                }
            }
            item(span = { GridItemSpan(maxLineSpan) }) {
                Text(name, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.padding(top = 16.dp))
            }
        }
    }
}

@Composable
fun ChaptersScreen(vm: BibleViewModel, book: Int, onChapter: (Int) -> Unit, onBack: () -> Unit) {
    val books by vm.books.collectAsStateWithLifecycle()
    val b = books.firstOrNull { it.nr == book }
    Scaffold(topBar = { Bar(b?.name.orEmpty(), onBack) }, containerColor = MaterialTheme.colorScheme.background) { pad ->
        if (b == null) return@Scaffold
        LazyVerticalGrid(
            columns = GridCells.Adaptive(64.dp),
            modifier = Modifier.fillMaxSize().padding(pad),
            contentPadding = PaddingValues(20.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            items((1..b.chapters).toList()) { ch ->
                Surface(onClick = { onChapter(ch) }, shape = RoundedCornerShape(14.dp), color = MaterialTheme.colorScheme.surfaceContainer, modifier = Modifier.aspectRatio(1f)) {
                    Box(contentAlignment = Alignment.Center) { Text("$ch", style = MaterialTheme.typography.titleMedium) }
                }
            }
        }
    }
}

@Composable
fun ChapterScreen(vm: BibleViewModel, settings: Settings, book: Int, chapter: Int, onChapter: (Int) -> Unit, onBack: () -> Unit) {
    LaunchedEffect(book, chapter) { vm.load(book, chapter) }
    val books by vm.books.collectAsStateWithLifecycle()
    val verses by vm.chapter.collectAsStateWithLifecycle()
    val favorites by vm.favorites.collectAsStateWithLifecycle()
    val read by vm.chapterRead.collectAsStateWithLifecycle()
    val b = books.firstOrNull { it.nr == book }
    val speaker = rememberSpeaker(vm.translationId, settings.ttsRate)
    val speaking by speaker.current.collectAsStateWithLifecycle()
    val playing by speaker.playing.collectAsStateWithLifecycle()
    val listState = rememberLazyListState()
    val fb = LocalFeedback.current
    LaunchedEffect(speaking) { if (speaking >= 0) listState.animateScrollToItem(speaking) }

    Scaffold(
        topBar = {
            Bar("${b?.name.orEmpty()} $chapter", onBack) {
                IconButton(onClick = { speaker.toggle(verses, 0) }) {
                    Icon(if (playing) Icons.Rounded.Stop else Icons.AutoMirrored.Rounded.VolumeUp, if (playing) "Stopp" else "Vorlesen")
                }
            }
        },
        containerColor = MaterialTheme.colorScheme.background,
    ) { pad ->
        if (verses.isEmpty()) { Box(Modifier.fillMaxSize().padding(pad)) { CircularProgressIndicator(Modifier.align(Alignment.Center)) }; return@Scaffold }
        LazyColumn(
            state = listState,
            modifier = Modifier.fillMaxSize().padding(pad),
            contentPadding = PaddingValues(start = 20.dp, end = 20.dp, top = 4.dp, bottom = 40.dp),
            verticalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            itemsIndexed(verses, key = { _, v -> v.verse }) { i, v ->
                VerseText(
                    v, bibleTextStyle(settings.textScale),
                    highlighted = i == speaking,
                    favorite = v.key() in favorites,
                    onLongPress = { vm.toggleFavorite(v); fb.correct() },
                )
            }
            item {
                Column(Modifier.padding(top = 20.dp)) {
                    if (read) {
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                            Icon(Icons.Rounded.Check, null, tint = MaterialTheme.colorScheme.primary)
                            Spacer(Modifier.width(8.dp))
                            Text("Gelesen – zählt für heute.", color = MaterialTheme.colorScheme.primary)
                        }
                    } else {
                        Button(onClick = { vm.markRead(); fb.sectionDone() }, modifier = Modifier.fillMaxWidth().height(52.dp)) { Text("Kapitel gelesen") }
                    }
                    Spacer(Modifier.height(12.dp))
                    Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        if (chapter > 1) OutlinedButton(onClick = { speaker.stop(); onChapter(chapter - 1) }) {
                            Icon(Icons.AutoMirrored.Rounded.KeyboardArrowLeft, null, Modifier.size(18.dp)); Text("Kapitel ${chapter - 1}")
                        } else Spacer(Modifier)
                        if (b != null && chapter < b.chapters) OutlinedButton(onClick = { speaker.stop(); onChapter(chapter + 1) }) {
                            Text("Kapitel ${chapter + 1}"); Icon(Icons.AutoMirrored.Rounded.KeyboardArrowRight, null, Modifier.size(18.dp))
                        }
                    }
                    Text(
                        "Tipp: Lange auf einen Vers drücken, um ihn zu speichern.",
                        style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant,
                        textAlign = TextAlign.Center, modifier = Modifier.fillMaxWidth().padding(top = 16.dp),
                    )
                }
            }
        }
    }
}
