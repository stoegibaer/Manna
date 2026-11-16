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

class AlbumViewModel(c: AppContainer) : ViewModel() {
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
    var open by remember { mutableStateOf<Card?>(null) }
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
        LazyVerticalGrid(
            columns = GridCells.Fixed(2),
            modifier = Modifier.fillMaxSize().padding(pad),
            contentPadding = PaddingValues(start = 20.dp, end = 20.dp, bottom = 32.dp),
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
    open?.let { card ->
        Dialog(onDismissRequest = { open = null }) { CardTile(card) }
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
