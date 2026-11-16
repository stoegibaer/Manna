package dev.tobi.manna.ui.components

import android.content.Context
import androidx.compose.foundation.Canvas
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.sp
import dev.tobi.manna.data.plan.Place
import dev.tobi.manna.ui.theme.LocalMannaColors
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import kotlin.math.cos
import kotlin.math.max

/** Base map built by tools/build_map.py from Natural Earth (public domain). Coordinates are [lon, lat]. */
@Serializable
data class MapData(
    val bbox: List<Double>,
    val land: List<List<List<Double>>>,
    val lakes: List<List<List<Double>>>,
    val rivers: List<River>,
)

@Serializable
data class River(val name: String, val line: List<List<Double>>)

private object MapCache {
    var data: MapData? = null
    suspend fun load(context: Context): MapData = data ?: withContext(Dispatchers.IO) {
        Json { ignoreUnknownKeys = true }.decodeFromString<MapData>(
            context.assets.open("map.json").bufferedReader().use { it.readText() }
        )
    }.also { data = it }
}

/**
 * Simple map centered on [place]. [reference] (usually Jerusalem) is shown as a small orientation dot
 * and included in the view, so the user sees how far away the place is.
 */
@Composable
fun MiniMap(place: Place, reference: Place?, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    var data by remember { mutableStateOf(MapCache.data) }
    LaunchedEffect(Unit) { if (data == null) data = MapCache.load(context) }
    val colors = LocalMannaColors.current
    val measurer = rememberTextMeasurer()
    val labelColor = colors.marker

    Canvas(modifier) {
        drawRect(colors.sea)
        val map = data ?: return@Canvas

        // viewport: place (+ reference) with padding, at least ~4° wide, matching the canvas aspect
        val pts = listOfNotNull(place, reference?.takeIf { it.id != place.id })
        var minLon = pts.minOf { it.lon }; var maxLon = pts.maxOf { it.lon }
        var minLat = pts.minOf { it.lat }; var maxLat = pts.maxOf { it.lat }
        val cLat = (minLat + maxLat) / 2
        val k = cos(Math.toRadians(cLat)) // shrink longitude so the map isn't stretched
        var spanX = max((maxLon - minLon) * k * 1.6, 3.2)
        var spanY = max((maxLat - minLat) * 1.6, 3.2 * size.height / size.width)
        val aspect = size.width / size.height
        if (spanX / spanY > aspect) spanY = spanX / aspect else spanX = spanY * aspect
        val cx = (minLon + maxLon) / 2 * k
        val cy = (minLat + maxLat) / 2
        fun p(lon: Double, lat: Double) = Offset(
            ((lon * k - (cx - spanX / 2)) / spanX * size.width).toFloat(),
            (((cy + spanY / 2) - lat) / spanY * size.height).toFloat(),
        )
        fun path(poly: List<List<Double>>, close: Boolean) = Path().apply {
            poly.forEachIndexed { i, c -> val o = p(c[0], c[1]); if (i == 0) moveTo(o.x, o.y) else lineTo(o.x, o.y) }
            if (close) close()
        }

        for (poly in map.land) drawPath(path(poly, true), colors.land)
        for (r in map.rivers) drawPath(path(r.line, false), colors.river, style = Stroke(width = 2.2f * density, cap = StrokeCap.Round))
        for (poly in map.lakes) drawPath(path(poly, true), colors.river)

        val style = TextStyle(fontSize = 13.sp, fontWeight = FontWeight.SemiBold, color = labelColor)
        if (reference != null && reference.id != place.id) {
            val r = p(reference.lon, reference.lat)
            drawCircle(labelColor.copy(alpha = 0.6f), 3.5f * density, r)
            val t = measurer.measure(reference.name, style.copy(fontWeight = FontWeight.Normal, color = labelColor.copy(alpha = 0.8f)))
            drawText(t, topLeft = Offset(r.x + 6 * density, r.y - t.size.height / 2f))
        }
        val m = p(place.lon, place.lat)
        drawCircle(labelColor.copy(alpha = 0.22f), 16f * density, m)
        drawCircle(labelColor, 6f * density, m)
        drawCircle(colors.land, 2.4f * density, m)
        val t = measurer.measure(place.name, style)
        val left = (m.x + 12 * density).coerceAtMost(size.width - t.size.width - 4 * density)
        drawText(t, topLeft = Offset(left, m.y - t.size.height - 6 * density))
    }
}
