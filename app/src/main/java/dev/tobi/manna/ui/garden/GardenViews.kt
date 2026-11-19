package dev.tobi.manna.ui.garden

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.drawscope.clipPath
import androidx.compose.ui.graphics.drawscope.clipRect
import androidx.compose.ui.graphics.drawscope.translate
import androidx.compose.ui.semantics.contentDescription
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import dev.tobi.manna.data.garden.Garden
import dev.tobi.manna.ui.theme.BibleFont
import dev.tobi.manna.ui.theme.LocalMannaColors
import kotlin.math.min

/** „Dein Senfbaum“, „Deine Palme“ … */
fun treeTitle(id: String): String = Trees.byId(id).let { "${it.article} ${it.name}" }
fun treeName(id: String): String = Trees.byId(id).name

/**
 * The garden on the home screen. Grows (animated) when [total] changes.
 * Keeps the scene's proportions and centers it in the available space.
 */
@Composable
fun GardenView(total: Int, planted: List<String>, animate: Boolean, modifier: Modifier = Modifier, corner: Dp = 18.dp) {
    val sc = sceneColors(LocalMannaColors.current)
    val anim = remember { Animatable(total.toFloat()) }
    LaunchedEffect(total) {
        // only animate growth within one tree; a new tree or a jump is shown directly
        val same = Garden.progress(anim.value).done == Garden.progress(total).done
        if (animate && same && total > anim.value) anim.animateTo(total.toFloat(), tween(1600, easing = FastOutSlowInEasing)) else anim.snapTo(total.toFloat())
    }
    val g = Garden.progress(total)
    Canvas(modifier.semantics { contentDescription = gardenDescription(g, planted) }) {
        val gw = min(size.width, size.height / SCENE_ASPECT)
        val gh = gw * SCENE_ASPECT
        val left = (size.width - gw) / 2
        val top = (size.height - gh) / 2
        val corner = corner.toPx()
        val clip = androidx.compose.ui.graphics.Path().apply {
            addRoundRect(androidx.compose.ui.geometry.RoundRect(left, top, left + gw, top + gh, corner, corner))
        }
        clipPath(clip) {
            translate(left, top) { drawGarden(gw, gh, anim.value, planted, sc) }
        }
    }
}

private fun gardenDescription(g: Garden.Progress, planted: List<String>): String {
    val trees = min(g.done, Garden.TREES)
    val growing = when {
        g.done < Garden.TREES -> planted.getOrNull(g.done)?.let { "Es wächst: ${treeName(it)}." } ?: "Ein Samenkorn wartet."
        g.done == Garden.TREES -> "Am Wasser wächst der Baum des Lebens."
        else -> "Der Baum des Lebens trägt ${g.fruits} Früchte."
    }
    return "Garten mit $trees ${if (trees == 1) "Baum" else "Bäumen"}. $growing"
}

/**
 * One tree on its own, zoomed so even a sprout fills the frame. Grows from [from] to [to] (0..1).
 * With [finale] the tree's finale moment plays once it is grown.
 */
@Composable
fun SingleTree(id: String, from: Float, to: Float, animate: Boolean, finale: Boolean, modifier: Modifier = Modifier) {
    val sp = Trees.byId(id)
    val sc = sceneColors(LocalMannaColors.current)
    val grow = remember(id) { Animatable(if (animate) from else to) }
    val fin = remember(id) { Animatable(if (finale && !animate) 1f else 0f) }
    LaunchedEffect(id, to, finale) {
        if (animate) grow.animateTo(to, tween(1600, easing = FastOutSlowInEasing)) else grow.snapTo(to)
        if (finale) { if (animate) fin.animateTo(1f, tween(2400, easing = LinearEasing)) else fin.snapTo(1f) }
    }
    Canvas(modifier.semantics { contentDescription = sp.name }) {
        val t = grow.value.toDouble()
        val unit = min(size.width * 1.05f, size.height) * 0.95f
        // the mustard tree keeps the size it always had (ui.components.MustardTree), so it does not jump when grown
        val mustard = id == Garden.ORDER.first()
        val scale = unit * if (mustard) 1.55f - 0.75f * t.toFloat() else (1.5f - 0.8f * t.toFloat()) * 0.92f
        val rootX = size.width / 2 - if (sp.water) size.width * 0.06f else 0f
        clipRect {
            drawTree(
                sp, t, rootX, size.height * 0.93f, scale, sc,
                TreeOpts(fin = if (finale) fin.value.toDouble() else null, water = sp.water && t >= 1.0,
                    groundR = if (mustard) 0.32 * unit / scale else 0.3, groundRy = if (mustard) 0.03 * unit / scale else null,
                    fruitN = if (id == Garden.LIFE) 0 else null),
            )
        }
    }
}

/** A grown tree as a small picture (choice cards). */
@Composable
private fun TreeThumb(id: String, modifier: Modifier = Modifier) {
    val sp = Trees.byId(id)
    val sc = sceneColors(LocalMannaColors.current)
    Canvas(modifier) {
        drawTree(sp, 1.0, size.width / 2, size.height * 0.94f, size.height * 0.95f, sc,
            TreeOpts(fruitN = if (id == Garden.LIFE) 12 else null, fruitColor = if (id == Garden.LIFE) lifeFruitColor(12) else null))
    }
}

/**
 * The moment a tree is fully grown: its finale, its verse, and the choice of the next tree.
 * Also shown when fewer than three trees are left, so one always knows what comes next.
 */
@Composable
fun TreeChoice(grownId: String, offers: List<String>, animate: Boolean, onPick: (String) -> Unit, modifier: Modifier = Modifier) {
    val grown = Trees.byId(grownId)
    Column(modifier, horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.spacedBy(10.dp)) {
        SingleTree(grownId, from = 1f, to = 1f, animate = animate, finale = true, modifier = Modifier.fillMaxWidth().height(240.dp))
        Text("${grown.article} ${grown.name} ist ausgewachsen", style = MaterialTheme.typography.headlineSmall, textAlign = TextAlign.Center)
        Text(
            "„${grown.verse}“ ${grown.ref}",
            fontFamily = BibleFont, fontStyle = FontStyle.Italic, textAlign = TextAlign.Center,
            style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        if (offers.isEmpty()) return@Column
        Text(
            when {
                offers.first() == Garden.LIFE -> "Zum Schluss wächst am Wasser"
                offers.size == 1 -> "Als Letztes im Garten wächst"
                offers.size == 2 -> "Noch zwei Bäume zur Wahl"
                else -> "Was pflanzt du als Nächstes?"
            },
            style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary,
            modifier = Modifier.padding(top = 8.dp),
        )
        offers.forEach { id ->
            val sp = Trees.byId(id)
            Surface(
                onClick = { onPick(id) },
                shape = RoundedCornerShape(18.dp),
                color = MaterialTheme.colorScheme.surfaceContainer,
                modifier = Modifier.fillMaxWidth(),
            ) {
                Row(Modifier.padding(8.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    TreeThumb(id, Modifier.size(76.dp).clip(RoundedCornerShape(12.dp)))
                    Column(Modifier.weight(1f), verticalArrangement = Arrangement.spacedBy(2.dp)) {
                        Text(sp.name, style = MaterialTheme.typography.titleMedium)
                        Text(
                            "„${shortVerse(sp.verse)}“",
                            fontFamily = BibleFont, fontStyle = FontStyle.Italic,
                            style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant,
                            maxLines = 3, overflow = TextOverflow.Ellipsis,
                        )
                        Text(sp.ref, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        if (offers.size == 1) Text("Antippen zum Pflanzen", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.primary)
                    }
                }
            }
        }
    }
}

private fun shortVerse(v: String) = if (v.length <= 90) v else v.take(88).replace(Regex("\\s\\S*$"), "") + " …"

/** Text for the finale of the tree of life and the fruits afterwards. */
fun fruitText(fruits: Int): String = when {
    fruits >= Garden.CITY_STEPS -> "Die goldene Stadt steht am Horizont. Die Früchte reifen weiter, Monat für Monat."
    fruits > 0 -> "Mit jeder Frucht kommt die goldene Stadt ein Stück näher (Offb 21,2)."
    else -> "Ab jetzt reift alle ${Garden.PER_FRUIT} Abschnitte eine Frucht."
}
