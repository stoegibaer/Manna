package dev.tobi.manna.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import dev.tobi.manna.data.plan.Card
import dev.tobi.manna.ui.theme.BibleFont

private data class CardStyle(val label: String, val a: Color, val b: Color)

fun cardColors(type: String): Pair<Color, Color> = styleFor(type).let { it.a to it.b }
fun cardLabel(type: String): String = styleFor(type).label

private fun styleFor(type: String) = when (type) {
    "person" -> CardStyle("PERSON", Color(0xFF7A4E2D), Color(0xFFC08A55))
    "ort" -> CardStyle("ORT", Color(0xFF2D5E6E), Color(0xFF6FA3A8))
    "ereignis" -> CardStyle("EREIGNIS", Color(0xFF6B2F4F), Color(0xFFB0698A))
    else -> CardStyle("BEGRIFF", Color(0xFF2F6B4F), Color(0xFF7FB08A))
}

/** A collectible card: colored band by type, an ornamental pattern, name and short text. */
@Composable
fun CardTile(card: Card, modifier: Modifier = Modifier) {
    val st = styleFor(card.type)
    val shape = RoundedCornerShape(18.dp)
    Column(
        modifier
            .fillMaxWidth()
            .clip(shape)
            .background(MaterialTheme.colorScheme.surface)
            .border(1.dp, st.a.copy(alpha = 0.35f), shape),
    ) {
        Box(Modifier.fillMaxWidth().height(64.dp).clipToBounds().background(Brush.linearGradient(listOf(st.a, st.b)))) {
            // subtle ornament: concentric arcs, different per card id
            val seed = card.id.hashCode()
            Canvas(Modifier.matchParentSize()) {
                val cx = size.width * (0.62f + ((seed and 0xff) / 255f) * 0.3f)
                val cy = size.height * (0.2f + (((seed shr 8) and 0xff) / 255f) * 0.6f)
                for (i in 1..6) {
                    drawCircle(Color.White.copy(alpha = 0.10f), radius = i * 16.dp.toPx(), center = Offset(cx, cy), style = Stroke(1.2.dp.toPx()))
                }
            }
            Row(Modifier.padding(horizontal = 16.dp, vertical = 10.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Text(st.label, color = Color.White.copy(alpha = 0.85f), fontSize = 11.sp, fontWeight = FontWeight.Bold, letterSpacing = 1.6.sp)
            }
            Text(
                card.name,
                color = Color.White,
                fontFamily = BibleFont,
                fontWeight = FontWeight.SemiBold,
                fontSize = 22.sp,
                modifier = Modifier.padding(start = 16.dp, top = 28.dp),
            )
        }
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
            Text(card.text, style = MaterialTheme.typography.bodyMedium)
            if (card.refs.isNotBlank()) {
                Text(card.refs, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }
        }
    }
}
