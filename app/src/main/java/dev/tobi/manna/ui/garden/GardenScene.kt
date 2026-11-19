package dev.tobi.manna.ui.garden

import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.translate
import dev.tobi.manna.data.garden.Garden
import kotlin.math.PI
import kotlin.math.ceil
import kotlin.math.floor
import kotlin.math.hypot
import kotlin.math.max
import kotlin.math.min
import kotlin.math.pow
import kotlin.math.sin
import kotlin.math.sqrt

/*
 * The garden as seen on the home screen. All positions are fractions of the scene's width/height
 * (the scene is 1 : 1.02). Tree places were arranged by hand in the design mockup.
 */

/** Height : width of the garden scene. */
const val SCENE_ASPECT = 1.02f
private const val HORIZON = 0.24

/** [x, y, size] per garden place, in the order in which they are filled. */
private val SLOTS = listOf(
    Triple(0.16, 0.961, 0.69), Triple(0.7, 0.579, 0.46), Triple(0.32, 0.645, 0.57), Triple(0.882, 0.798, 0.68),
    Triple(0.091, 0.628, 0.48), Triple(0.922, 0.495, 0.46), Triple(0.383, 0.459, 0.39), Triple(0.608, 0.409, 0.36),
    Triple(0.177, 0.396, 0.44), Triple(0.803, 0.362, 0.38), Triple(0.296, 0.286, 0.43), Triple(0.676, 0.275, 0.46),
)
/** The growing tree in front … */
private val FRONT = Triple(0.516, 0.98, 0.55)
/** … and the tree of life, which grows at the water and stays there. */
private val LIFE_PLACE = Triple(0.513, 0.979, 0.9)

/** Center line of the river: from the source at the horizon to the front right. */
private val RIVER = listOf(0.5 to 0.262, 0.505 to 0.34, 0.49 to 0.44, 0.5 to 0.55, 0.575 to 0.66, 0.68 to 0.78, 0.75 to 0.9, 0.79 to 1.03)

private fun riverPt(u: Double): Pair<Double, Double> {
    val n = RIVER.size - 1
    val x = u.coerceIn(0.0, 1.0) * n
    val i = min(n - 1, floor(x).toInt())
    val f = x - i
    val p0 = RIVER[max(0, i - 1)]; val p1 = RIVER[i]; val p2 = RIVER[i + 1]; val p3 = RIVER[min(n, i + 2)]
    fun cr(a: Double, b: Double, c: Double, d: Double) = 0.5 * (2 * b + (-a + c) * f + (2 * a - 5 * b + 4 * c - d) * f * f + (-a + 3 * b - 3 * c + d) * f * f * f)
    return cr(p0.first, p1.first, p2.first, p3.first) to cr(p0.second, p1.second, p2.second, p3.second)
}

/** Hes 47,3–5: the water gets deeper with every grown tree. [reach] = length 0..1, [w] = width. */
private class RiverStage(val reach: Double, val w: Double)

private fun riverStage(done: Int): RiverStage? {
    val k = min(done, Garden.TREES)
    if (k <= 0) return null
    val f = (k - 1) / 11.0
    return RiverStage(min(1.0, 0.16 + 0.84 * f.pow(0.7)), 0.007 + 0.078 * f.pow(1.2))
}

/** Name of the river stage for texts. */
fun riverName(done: Int): String? = when (min(done, Garden.TREES)) {
    0 -> null
    1, 2 -> "eine Quelle, knöcheltief"
    3, 4, 5 -> "ein Bach, knietief"
    6, 7, 8 -> "ein Fluss, hüfttief"
    in 9..11 -> "ein Fluss, tief"
    else -> "ein Strom"
}

/** After 36 fruits every fruit changes in turn to the fruit of the next „month“. */
internal fun lifeFruitColor(n: Int): (Int) -> Color = { k ->
    val extra = n - Garden.CITY_STEPS
    val g = if (extra > k) (extra - 1 - k) / Garden.CITY_STEPS + 1 else 0
    Trees.lifeFruits[(k + g * 5) % 12]
}

// ── the golden city (Offb 21): comes down from heaven with every fruit ──

private val STONES = listOf(0x7FB89A, 0x3E64B5, 0x8FA9B8, 0x2E9E6A, 0xC8644A, 0xB0303A, 0xC9C04A, 0x5FB5B0, 0xE0A030, 0x8CCB6A, 0x5A6FD0, 0x8E5BB5)
    .map { Color(0xFF000000 or it.toLong()) }

private class Building(val x: Double, val wd: Double, val ht: Double, val dome: Boolean)

private val BUILDINGS: List<Building> = run {
    val r = Rng(42)
    List(12) { i ->
        val side = if (i % 2 == 1) 1 else -1
        val rank = ceil(i / 2.0)
        val x = side * rank * 0.07 + (if (i == 0) 0.0 else (r.next() - 0.5) * 0.02)
        val wd = 0.075 + r.next() * 0.03
        val ht = 1 - rank * 0.13 - r.next() * 0.08
        Building(x, wd, ht, r.next() < 0.4)
    }
}

private val GOLD_LIGHT = Color(0xFFF7DA7C)
private val GOLD_DARK = Color(0xFFD9A520)

private fun DrawScope.drawCity(w: Float, h: Float, fruits: Int, sc: SceneColors) {
    if (fruits <= 0) return
    val p = (fruits.toFloat() / Garden.CITY_STEPS).coerceIn(0f, 1f)
    val cx = 0.5f * w; val cw = 0.42f * w; val base = 0.264f * h; val fh = 0.014f * h; val wallH = 0.05f * h; val cityH = 0.2f * h
    val alpha = 0.1f + 0.9f * p
    translate(0f, -(1 - p) * 0.045f * h) {
        // its radiance (21,11.23)
        drawRect(
            Brush.radialGradient(listOf(GOLD_LIGHT.copy(alpha = 0.6f * p * alpha), GOLD_LIGHT.copy(alpha = 0f)), Offset(cx, base - cityH * 0.5f), cw * 0.95f),
            Offset(cx - cw, base - cityH * 2.2f), Size(2 * cw, cityH * 2.6f),
        )
        // golden buildings (21,18)
        for (i in BUILDINGS.indices.reversed()) {
            val b = BUILDINGS[i]
            val bw = (b.wd * cw).toFloat(); val bh = (b.ht * cityH).toFloat()
            val bx = (cx + b.x * cw - bw / 2).toFloat(); val by = base - fh - bh
            val brush = Brush.horizontalGradient(listOf(GOLD_LIGHT, GOLD_DARK), bx, bx + bw)
            drawRect(brush, Offset(bx, by), Size(bw, bh), alpha = alpha)
            if (b.dome) drawArc(brush, 180f, 180f, true, Offset(bx, by - bw / 2), Size(bw, bw), alpha = alpha)
            for (k in 0 until 3) drawRect(Color(0xB3FFFAE6), Offset(bx + bw * (0.2f + k * 0.25f), by + bh * 0.25f), Size(bw * 0.1f, bh * 0.25f), alpha = alpha)
        }
        // jasper wall with twelve pearl gates (21,12.18.21)
        drawRect(Color(0xFFA9D9C4), Offset(cx - cw / 2, base - fh - wallH), Size(cw, wallH), alpha = alpha)
        drawRect(Color(0xFFCDEBDD), Offset(cx - cw / 2, base - fh - wallH), Size(cw, max(1f, wallH * 0.12f)), alpha = alpha)
        for (i in 0 until 12) {
            val gx = cx - cw / 2 + (i + 0.5f) * cw / 12; val gw = cw / 12 * 0.46f; val gh = wallH * 0.72f
            val gate = Path().apply {
                moveTo(gx - gw / 2, base - fh); lineTo(gx - gw / 2, base - fh - gh + gw / 2)
                arcTo(androidx.compose.ui.geometry.Rect(gx - gw / 2, base - fh - gh, gx + gw / 2, base - fh - gh + gw), 180f, 180f, false)
                lineTo(gx + gw / 2, base - fh); close()
            }
            drawPath(gate, Color(0xFFF6F1E7), alpha = alpha)
            drawRect(Color(0x8CC8BEAA), Offset(gx - gw * 0.08f, base - fh - gh * 0.75f), Size(gw * 0.16f, gh * 0.75f), alpha = alpha)
        }
        // twelve foundation stones (21,19–20)
        for (i in 0 until 12) {
            val x = cx - cw / 2 + i * cw / 12 + 0.5f
            drawRect(STONES[i], Offset(x, base - fh), Size(cw / 12 - 1, fh), alpha = alpha)
            drawRect(Color.White.copy(alpha = 0.35f), Offset(x, base - fh), Size(cw / 12 - 1, fh * 0.3f), alpha = alpha)
        }
        // clouds while it comes down (21,2)
        if (p < 1f) for (k in -3..3) {
            val rx = cw * 0.13f; val ry = 0.02f * h; val ox = cx + k * cw * 0.15f; val oy = base + 0.004f * h
            drawOval(sc.white, Offset(ox - rx, oy - ry), Size(rx * 2, ry * 2), alpha = (1 - p) * 0.9f)
        }
    }
}

private fun DrawScope.drawRiver(w: Float, h: Float, done: Int, sc: SceneColors) {
    val st = riverStage(done) ?: return
    class M(val x: Float, val y: Float, val hw: Float, val nx: Float, val ny: Float)
    val n = 90
    val mid = List(n + 1) { i ->
        val u = st.reach * i / n
        val (x, y) = riverPt(u)
        val (x2, y2) = riverPt(min(1.0, u + 0.004))
        var nx = -(y2 - y) * h; var ny = (x2 - x) * w
        val ln = hypot(nx, ny).let { if (it == 0.0) 1.0 else it }
        nx /= ln; ny /= ln
        val tip = min(1.0, (st.reach - u) / 0.04 + 0.1)
        val hw = w * st.w * (0.12 + (y - HORIZON) / 0.6) * sqrt(tip)
        M((x * w).toFloat(), (y * h).toFloat(), hw.toFloat(), nx.toFloat(), ny.toFloat())
    }
    fun band(grow: Float, color: Color) {
        val path = Path()
        mid.forEachIndexed { i, m ->
            val k = m.hw + grow * (0.5f + m.y / h)
            if (i == 0) path.moveTo(m.x + m.nx * k, m.y + m.ny * k) else path.lineTo(m.x + m.nx * k, m.y + m.ny * k)
        }
        for (i in mid.indices.reversed()) { val m = mid[i]; val k = m.hw + grow * (0.5f + m.y / h); path.lineTo(m.x - m.nx * k, m.y - m.ny * k) }
        path.close()
        drawPath(path, color)
    }
    band(w * min(0.012, 0.004 + st.w * 0.15).toFloat(), sc.bank)
    band(0f, sc.water)
    // light current lines – more of them the wider it gets
    val lanes = if (done <= 2) 1 else if (done <= 6) 2 else 3
    for (j in 0 until lanes) {
        val off = if (lanes == 1) 0f else (j.toFloat() / (lanes - 1) - 0.5f) * 0.9f
        var i = 3 + j * 4
        while (i < n - 3) {
            val a = mid[i]; val b = mid[i + 4]
            drawLine(sc.water2, Offset(a.x + a.nx * a.hw * off, a.y + a.ny * a.hw * off), Offset(b.x + b.nx * b.hw * off, b.y + b.ny * b.hw * off),
                strokeWidth = max(0.8f * density, w * 0.005f * (a.y / h)), cap = StrokeCap.Round)
            i += 11
        }
    }
    // reeds from the brook on
    if (done >= 3) {
        val r = Rng(5)
        val tall = 0.6f + min(done, Garden.TREES) / 12f
        var i = 10
        while (i < n) {
            val m = mid[i]
            if (r.next() >= 0.5) {
                val sd = if (r.next() < 0.5) 1 else -1
                val k = m.hw + w * 0.012f
                val bx = m.x + sd * m.nx * k; val by = m.y + sd * m.ny * k; val s = m.y / h
                for (q in -1..1) drawLine(sc.reed, Offset(bx + q * w * 0.006f * s, by), Offset(bx + q * w * 0.011f * s, by - h * (0.03f + 0.008f * (q and 1)) * s * tall),
                    strokeWidth = max(0.7f * density, w * 0.003f * s), cap = StrokeCap.Round)
            }
            i += 6
        }
    }
    // the source
    val (sx, sy) = RIVER[0]
    val rx = w * (0.012 + st.w * 0.5).toFloat(); val ry = h * (0.004 + st.w * 0.06).toFloat()
    drawOval(sc.water, Offset((sx * w).toFloat() - rx, (sy * h).toFloat() - ry), Size(rx * 2, ry * 2))
}

/**
 * Paints the whole garden into a [w] × [h] area at the origin.
 * [total] may be fractional while the front tree grows. [planted] = species by position.
 */
internal fun DrawScope.drawGarden(w: Float, h: Float, total: Float, planted: List<String>, sc: SceneColors) {
    val g = Garden.progress(total)
    val done = g.done
    // sky, far hills, meadow
    drawRect(sc.sky, Offset.Zero, Size(w, h))
    val hills = Path().apply {
        moveTo(0f, h * HORIZON.toFloat())
        var x = 0f
        while (x <= w) {
            val f = x / w
            lineTo(x, (h * HORIZON - (sin(f * PI * 2.1 + 0.7) * 0.012 + sin(f * PI) * 0.025 + 0.01) * h).toFloat())
            x += 4f
        }
        lineTo(w, h); lineTo(0f, h); close()
    }
    drawPath(hills, sc.hill2)
    drawRect(sc.hill, Offset(0f, h * (HORIZON + 0.012).toFloat()), Size(w, h * (1 - HORIZON.toFloat())))
    drawCity(w, h, g.fruits, sc)
    drawRiver(w, h, done, sc)

    // garden trees, back to front
    val items = (0 until min(done, Garden.TREES)).mapNotNull { i -> planted.getOrNull(i)?.let { i to Trees.byId(it) } }.sortedBy { SLOTS[it.first].second }
    for ((i, sp) in items) {
        val (x, y, s) = SLOTS[i]
        drawTree(sp, 1.0, (x * w).toFloat(), (y * h).toFloat(), (h * 0.5 * s).toFloat(), sc, TreeOpts(fin = 1.0, groundColor = sc.hill2, groundR = 0.2))
    }
    // the growing tree in front; a seed while the next tree is not chosen yet
    val t = g.t.toDouble()
    if (done < Garden.TREES) {
        val (x, y, s) = FRONT
        val sp = planted.getOrNull(done)?.let { Trees.byId(it) }
        val tt = if (sp == null) 0.0 else max(t, 0.0001)
        drawTree(sp ?: Trees.all.first(), tt, (w * x).toFloat(), (h * y).toFloat(), (h * s * (1.3 - 0.3 * tt)).toFloat(), sc, TreeOpts(groundColor = sc.ground, groundR = 0.17))
    } else {
        val (x, y, s) = LIFE_PLACE
        val chosen = Garden.LIFE in planted
        val tt = if (done > Garden.TREES) 1.0 else if (!chosen) 0.0 else max(t, 0.0001)
        drawTree(
            Trees.life, tt, (w * x).toFloat(), (h * y).toFloat(), (h * 0.5 * s * (1.3 - 0.3 * tt)).toFloat(), sc,
            TreeOpts(groundColor = sc.ground, groundR = 0.17, fruitN = if (done > Garden.TREES) g.fruits else 0, fruitColor = lifeFruitColor(g.fruits)),
        )
    }
}
