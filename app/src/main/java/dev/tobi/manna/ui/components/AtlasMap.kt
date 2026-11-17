package dev.tobi.manna.ui.components

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.gestures.detectTransformGestures
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.ZoomOutMap
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Rect
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.drawText
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.rememberTextMeasurer
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import dev.tobi.manna.ui.theme.LocalMannaColors
import kotlin.math.cos
import kotlin.math.max

/**
 * A place on the atlas. Places not [visited] yet are drawn as faint dots without a name.
 * [weight] (e.g. number of sections) decides which of two nearby places stays visible when zoomed out.
 */
data class AtlasPoint(val id: String, val name: String, val lat: Double, val lon: Double, val visited: Boolean, val weight: Int = 0)

/**
 * Points shown at the current zoom, with their screen position: a point is hidden while it is closer than
 * [minDist] px to a more important one (selected > visited > weight), and appears when zooming in far enough.
 * Depends only on the zoom, not on panning, so points don't flicker while dragging.
 */
private fun declutter(points: List<AtlasPoint>, pr: Projection, selected: String?, minDist: Float): List<Pair<AtlasPoint, Offset>> {
    val ordered = points.sortedWith(compareBy<AtlasPoint>({ it.id != selected }, { !it.visited }, { -it.weight }, { it.id }))
    val shown = mutableListOf<Pair<AtlasPoint, Offset>>()
    for (pt in ordered) {
        val o = pr.p(pt.lon, pt.lat)
        if (shown.none { (it.second - o).getDistance() < minDist }) shown += pt to o
    }
    return shown
}

private const val MAX_ZOOM = 150f
/** Minimum distance between two shown dots. */
private const val MIN_DIST_DP = 16f

/**
 * Viewport that fits all [pts] into a canvas of [w]×[h] (equirectangular, longitude shrunk by cos(lat)),
 * then applies the user's zoom [scale] and pan [offset].
 */
private class Projection(pts: List<AtlasPoint>, bbox: List<Double>, private val w: Float, private val h: Float, private val scale: Float, private val offset: Offset) {
    private val k: Double
    private val cx: Double
    private val cy: Double
    private val spanX: Double
    private val spanY: Double

    init {
        val minLon = pts.minOf { it.lon }; val maxLon = pts.maxOf { it.lon }
        val minLat = pts.minOf { it.lat }; val maxLat = pts.maxOf { it.lat }
        k = cos(Math.toRadians((minLat + maxLat) / 2))
        var sx = max((maxLon - minLon) * k * 1.15, 4.0)
        var sy = max((maxLat - minLat) * 1.15, 4.0 * h / w)
        val aspect = w / h
        if (sx / sy > aspect) sy = sx / aspect else sx = sy * aspect
        spanX = sx; spanY = sy
        // keep the view inside the base map (bbox = [minLon, minLat, maxLon, maxLat]) where it fits
        fun keep(c: Double, half: Double, lo: Double, hi: Double) = if (hi - lo >= 2 * half) c.coerceIn(lo + half, hi - half) else (lo + hi) / 2
        cx = keep((minLon + maxLon) / 2 * k, sx / 2, bbox[0] * k, bbox[2] * k)
        cy = keep((minLat + maxLat) / 2, sy / 2, bbox[1], bbox[3])
    }

    fun p(lon: Double, lat: Double) = Offset(
        ((lon * k - (cx - spanX / 2)) / spanX * w).toFloat() * scale + offset.x,
        (((cy + spanY / 2) - lat) / spanY * h).toFloat() * scale + offset.y,
    )
}

/** The zoomed content must always cover the whole canvas. */
private fun clampOffset(o: Offset, scale: Float, size: Size) = Offset(
    o.x.coerceIn(size.width * (1 - scale), 0f),
    o.y.coerceIn(size.height * (1 - scale), 0f),
)

/** Zoomable map of all [points]; pinch to zoom, drag to pan, double tap to zoom in, tap a dot to select it. */
@Composable
fun AtlasMap(points: List<AtlasPoint>, selected: String?, onSelect: (String) -> Unit, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    var data by remember { mutableStateOf(MapCache.data) }
    LaunchedEffect(Unit) { if (data == null) data = MapCache.load(context) }
    val colors = LocalMannaColors.current
    val measurer = rememberTextMeasurer()
    var scale by remember { mutableFloatStateOf(1f) }
    var offset by remember { mutableStateOf(Offset.Zero) }
    val currentPoints by rememberUpdatedState(points)
    val select by rememberUpdatedState(onSelect)
    val currentSelected by rememberUpdatedState(selected)

    Box(modifier) {
        Canvas(
            Modifier.fillMaxSize()
                .pointerInput(Unit) {
                    detectTransformGestures { centroid, pan, zoom, _ ->
                        val sz = Size(size.width.toFloat(), size.height.toFloat())
                        val ns = (scale * zoom).coerceIn(1f, MAX_ZOOM)
                        offset = clampOffset((offset - centroid) * (ns / scale) + centroid + pan, ns, sz)
                        scale = ns
                    }
                }
                .pointerInput(Unit) {
                    detectTapGestures(
                        onDoubleTap = { pos ->
                            val sz = Size(size.width.toFloat(), size.height.toFloat())
                            val ns = (scale * 2.5f).coerceAtMost(MAX_ZOOM)
                            offset = clampOffset((offset - pos) * (ns / scale) + pos, ns, sz)
                            scale = ns
                        },
                        onTap = { pos ->
                            val pts = currentPoints
                            val bbox = MapCache.data?.bbox
                            if (pts.isEmpty() || bbox == null) return@detectTapGestures
                            val pr = Projection(pts, bbox, size.width.toFloat(), size.height.toFloat(), scale, offset)
                            val hit = declutter(pts, pr, currentSelected, MIN_DIST_DP.dp.toPx())
                                .map { (pt, o) -> pt to (o - pos).getDistance() }.minByOrNull { it.second }
                            if (hit != null && hit.second < 28.dp.toPx()) select(hit.first.id)
                        },
                    )
                },
        ) {
            drawRect(colors.sea)
            val map = data ?: return@Canvas
            if (points.isEmpty()) return@Canvas
            val pr = Projection(points, map.bbox, size.width, size.height, scale, offset)
            fun path(poly: List<List<Double>>, close: Boolean) = Path().apply {
                poly.forEachIndexed { i, c -> val o = pr.p(c[0], c[1]); if (i == 0) moveTo(o.x, o.y) else lineTo(o.x, o.y) }
                if (close) close()
            }
            for (poly in map.land) drawPath(path(poly, true), colors.land)
            for (r in map.rivers) drawPath(path(r.line, false), colors.river, style = Stroke(width = 2f * density, cap = StrokeCap.Round))
            for (poly in map.lakes) drawPath(path(poly, true), colors.river)

            val bounds = Rect(Offset.Zero, size).inflate(24 * density)
            val style = TextStyle(fontSize = 12.sp, fontWeight = FontWeight.SemiBold, color = colors.marker)
            val shown = declutter(points, pr, selected, MIN_DIST_DP * density)
            // faint dots first, then visited markers, selected one on top
            for ((pt, o) in shown) {
                if (!pt.visited && bounds.contains(o)) drawCircle(colors.marker.copy(alpha = 0.3f), 3.5f * density, o)
            }
            val visited = shown.filter { it.first.visited }
            for ((pt, o) in visited.reversed()) {
                if (!bounds.contains(o)) continue
                if (pt.id == selected) drawCircle(colors.marker.copy(alpha = 0.22f), 15f * density, o)
                drawCircle(colors.marker, 5.5f * density, o)
                drawCircle(colors.land, 2.2f * density, o)
            }
            // labels: selected first; right of the dot, else left; skipped if they would cover another label or dot
            // only visited markers block labels; faint dots may sit underneath a name
            val dots = visited.map { it.second }
            val taken = mutableListOf<Rect>()
            for ((i, v) in visited.withIndex()) {
                val (pt, o) = v
                if (!bounds.contains(o)) continue
                val t = measurer.measure(pt.name, style)
                val sz = Size(t.size.width.toFloat(), t.size.height.toFloat())
                val gap = 9 * density
                val r = listOf(
                    Rect(Offset(o.x + gap, o.y - sz.height / 2f), sz),
                    Rect(Offset(o.x - gap - sz.width, o.y - sz.height / 2f), sz),
                ).firstOrNull { c ->
                    c.left >= 0 && c.right <= size.width && taken.none { it.overlaps(c) } &&
                        dots.withIndex().none { (j, d) -> j != i && c.inflate(4 * density).contains(d) }
                } ?: continue
                taken += r
                drawText(t, topLeft = r.topLeft)
            }
        }
        if (scale > 1.01f) {
            Surface(
                onClick = { scale = 1f; offset = Offset.Zero },
                shape = CircleShape,
                color = MaterialTheme.colorScheme.surface.copy(alpha = 0.9f),
                modifier = Modifier.align(Alignment.TopEnd).padding(10.dp),
            ) {
                Icon(Icons.Outlined.ZoomOutMap, "Ganze Karte zeigen", Modifier.padding(8.dp), tint = MaterialTheme.colorScheme.primary)
            }
        }
    }
}
