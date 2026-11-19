package dev.tobi.manna.ui.garden

import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.graphics.drawscope.scale
import androidx.compose.ui.graphics.drawscope.translate
import androidx.compose.ui.graphics.drawscope.withTransform
import dev.tobi.manna.ui.theme.MannaColors
import kotlin.math.PI
import kotlin.math.abs
import kotlin.math.ceil
import kotlin.math.cos
import kotlin.math.floor
import kotlin.math.max
import kotlin.math.min
import kotlin.math.pow
import kotlin.math.sign
import kotlin.math.sin

/** Colors of the surroundings (ground, sky, water, birds). */
internal class SceneColors(
    val dark: Boolean, val trunk: Color, val trunkDark: Color, val blossom: Color, val ground: Color,
    val sky: Color, val hill: Color, val hill2: Color, val water: Color, val water2: Color, val bank: Color, val reed: Color,
    val bird: Color, val birdWing: Color, val white: Color,
)

private fun hex(v: Long) = Color(0xFF000000 or v)

internal fun sceneColors(c: MannaColors) = if (c.dark) SceneColors(
    true, c.trunk, hex(0x8C6C4C), c.blossom, c.ground, hex(0x1A1E22), hex(0x24272A), hex(0x2C2E30),
    hex(0x4F7F9C), hex(0x7FA9C2), hex(0x33383A), hex(0x7FA06A), hex(0xD9CFC2), hex(0xA89886), hex(0xF3EEE6),
) else SceneColors(
    false, c.trunk, hex(0x5E4630), c.blossom, c.ground, hex(0xF4EFE3), hex(0xE7DECB), hex(0xDED3BD),
    hex(0x8FB4CC), hex(0xC9DEEA), hex(0xD3CDB4), hex(0x7E9A5A), hex(0x5A4E44), hex(0x8C7B6B), hex(0xFFFFFF),
)

internal class TreeOpts(
    /** Progress of the finale moment 0..1, or null for none. */
    val fin: Double? = null,
    val ground: Boolean = true,
    val groundColor: Color? = null,
    val groundR: Double = 0.3,
    /** Height of the ground shadow; default follows [groundR]. */
    val groundRy: Double? = null,
    /** Brook at the foot (only when shown alone). */
    val water: Boolean = false,
    /** Only this many fruits, in ripening order, colored by [fruitColor] (tree of life). */
    val fruitN: Int? = null,
    val fruitColor: ((Int) -> Color)? = null,
)

private fun DrawScope.oval(color: Color, cx: Float, cy: Float, rx: Float, ry: Float, rotRad: Double = 0.0, alpha: Float = 1f) {
    if (rx <= 0f || ry <= 0f) return
    val tl = Offset(cx - rx, cy - ry)
    val sz = Size(rx * 2, ry * 2)
    if (rotRad == 0.0) drawOval(color, tl, sz, alpha = alpha)
    else rotate((rotRad * 180 / PI).toFloat(), pivot = Offset(cx, cy)) { drawOval(color, tl, sz, alpha = alpha) }
}

private fun DrawScope.line(color: Color, a: Offset, b: Offset, width: Float, alpha: Float = 1f) =
    drawLine(color, a, b, strokeWidth = width, cap = StrokeCap.Round, alpha = alpha)

/** A leaf pointing in direction [angDeg] (math angle, y up) from (x, y). */
private fun DrawScope.leaf(x: Float, y: Float, angDeg: Double, len: Float, shape: LeafShape, wr: Double, color: Color) {
    if (len <= 0.3f) return
    val path = Path()
    fun lobe(rotDeg: Double, l: Float, w: Double) {
        val c = cos(rad(rotDeg)).toFloat(); val s = sin(rad(rotDeg)).toFloat()
        fun px(x0: Float, y0: Float) = x0 * c - y0 * s
        fun py(x0: Float, y0: Float) = x0 * s + y0 * c
        val wl = (l * w).toFloat()
        path.moveTo(0f, 0f)
        path.quadraticTo(px(l * 0.5f, -wl), py(l * 0.5f, -wl), px(l, 0f), py(l, 0f))
        path.quadraticTo(px(l * 0.5f, wl), py(l * 0.5f, wl), 0f, 0f)
    }
    when (shape) {
        LeafShape.LOBED -> { lobe(-38.0, len * 0.78f, 0.34); lobe(0.0, len, 0.34); lobe(38.0, len * 0.78f, 0.34) }
        LeafShape.ROUND -> path.addOval(androidx.compose.ui.geometry.Rect(0f, -len * 0.36f, len, len * 0.36f))
        else -> lobe(0.0, len, wr)
    }
    withTransform({ translate(x, y); rotate((-angDeg).toFloat(), pivot = Offset.Zero) }) { drawPath(path, color) }
}

private fun DrawScope.blossom(x: Float, y: Float, r: Float, color: Color, center: Color?, petals: Int) {
    for (k in 0 until petals) {
        val a = k * 2 * PI / petals + 0.4
        drawCircle(color, r * 0.55f, Offset(x + (cos(a) * r * 0.55).toFloat(), y + (sin(a) * r * 0.55).toFloat()))
    }
    center?.let { drawCircle(it, r * 0.3f, Offset(x, y)) }
}

/** A small bird, sitting or (while [flying]) as a flapping silhouette. */
private fun DrawScope.bird(x: Float, y: Float, s: Float, flap: Double, facing: Float, body: Color, wing: Color, beak: Color, flying: Boolean) {
    withTransform({ translate(x, y); scale(facing, 1f, pivot = Offset.Zero) }) {
        if (flying) {
            val wy = (sin(flap) * s * 0.5).toFloat()
            val p = Path().apply {
                moveTo(-s, wy); quadraticTo(-s * 0.4f, -s * 0.2f + wy * 0.3f, 0f, 0f); quadraticTo(s * 0.4f, -s * 0.2f + wy * 0.3f, s, wy)
            }
            drawPath(p, body, style = Stroke(max(1f, s * 0.18f), cap = StrokeCap.Round))
        } else {
            oval(body, 0f, -s * 0.35f, s * 0.55f, s * 0.36f, -0.25)
            drawCircle(body, s * 0.24f, Offset(s * 0.45f, -s * 0.72f))
            drawPath(Path().apply { moveTo(-s * 0.4f, -s * 0.3f); lineTo(-s * 0.95f, -s * 0.05f); lineTo(-s * 0.85f, -s * 0.38f); close() }, body)
            drawPath(Path().apply { moveTo(s * 0.66f, -s * 0.76f); lineTo(s * 0.88f, -s * 0.7f); lineTo(s * 0.66f, -s * 0.64f); close() }, beak)
            oval(wing, -s * 0.08f, -s * 0.38f, s * 0.32f, s * 0.16f, -0.35)
        }
    }
}

/**
 * Draws one tree with its root at ([rootX], [rootY]). [t] = growth 0..1, [scale] = pixels per tree unit.
 */
internal fun DrawScope.drawTree(sp: TreeSpecies, t: Double, rootX: Float, rootY: Float, scale: Float, sc: SceneColors, o: TreeOpts = TreeOpts()) {
    val m = sp.model
    val col = if (sc.dark) sp.dark else sp.light
    fun px(x: Double) = (rootX + x * scale).toFloat()
    fun py(y: Double) = (rootY - y * scale).toFloat()

    if (o.ground) oval(o.groundColor ?: sc.ground, rootX, rootY, scale * o.groundR.toFloat(), (scale * (o.groundRy ?: (0.028 * (o.groundR / 0.3) * 1.3))).toFloat())
    if (o.water) {
        oval(sc.water, rootX + scale * 0.28f, rootY + scale * 0.012f, scale * 0.2f, scale * 0.024f)
        oval(sc.water2, rootX + scale * 0.3f, rootY + scale * 0.008f, scale * 0.08f, scale * 0.007f)
    }
    if (t < 0.012) { // the seed
        oval(sc.trunk, rootX, rootY - scale * 0.016f, scale * 0.02f, scale * 0.014f)
        return
    }

    if (m.palmPts != null) drawPalm(m, t, ::px, ::py, scale, col)
    else {
        for (s in m.segs) {
            val f = frac(t, s.birth, s.span)
            if (f <= 0) continue
            val pts = s.pts
            val upto = f * (pts.size - 1)
            val path = Path().apply { moveTo(px(pts[0].x), py(pts[0].y)) }
            for (i in 1..ceil(upto).toInt()) {
                val u = min(1.0, upto - (i - 1))
                val q = pts[i - 1]; val w = pts[i]
                path.lineTo(px(lerp(q.x, w.x, u)), py(lerp(q.y, w.y, u)))
            }
            val width = max(0.6, s.w * scale * (0.6 + 0.4 * f) * (0.45 + 0.55 * t)).toFloat()
            drawPath(path, col.trunk, style = Stroke(width, cap = StrokeCap.Round, join = StrokeJoin.Round))
        }
        // seed leaves while it is a sprout
        val sprout = (1 - frac(t, 0.22, 0.2)) * frac(t, 0.012, 0.02)
        if (sprout > 0 && m.segs.isNotEmpty()) {
            val s0 = m.segs[0]
            val (x, y) = polyAt(s0.pts, frac(t, s0.birth, s0.span))
            leaf(px(x), py(y), 55.0, (0.11 * scale * sprout).toFloat(), LeafShape.ELLIPSE, 0.38, col.leaf)
            leaf(px(x), py(y), 125.0, (0.11 * scale * sprout).toFloat(), LeafShape.ELLIPSE, 0.38, col.leafDark)
        }
        for (st in m.strands) {
            val f = frac(t, st.birth, 0.1)
            if (f <= 0) continue
            val x = px(st.x); val y = py(st.y); val l = (st.len * scale * f).toFloat(); val sw = (st.sway * scale).toFloat()
            val p = Path().apply { moveTo(x, y); quadraticTo(x + sw, y + l * 0.5f, x + sw * 1.6f, y + l) }
            drawPath(p, if (st.dark) col.leafDark else col.leaf, style = Stroke(max(0.8f, scale * sp.strandW.toFloat()), cap = StrokeCap.Round))
        }
        for (c in m.clumps) {
            val f = frac(t, c.birth, 0.08)
            if (f <= 0) continue
            val rr = (c.r * scale * f).toFloat()
            val color = if (c.shade < 0.33) col.leafDark else if (c.shade < 0.8) col.leaf else col.leafLight ?: col.leaf
            oval(color, px(c.x), py(c.y), rr, rr * (c.flat ?: sp.flat).toFloat())
        }
        if (sp.leafShape != LeafShape.NONE) for (l in m.leaves) {
            val f = frac(t, l.birth, 0.05)
            if (f <= 0) continue
            leaf(px(l.x), py(l.y), l.a, (l.len * scale * 1.6 * f).toFloat(), sp.leafShape, sp.leafW, if (l.dark) col.leafDark else col.leaf)
        }
        col.flower?.let { fc ->
            for (b in m.flowers) {
                val f = frac(t, b.birth, 0.06)
                if (f <= 0) continue
                val x = px(b.x); val y = py(b.y); val rr = (b.r * scale * f).toFloat()
                when (sp.flowerKind) {
                    FlowerKind.BALL -> drawCircle(fc, rr * 0.7f, Offset(x, y))
                    FlowerKind.PLUME -> line(fc, Offset(x, y), Offset(x + rr * 0.3f, y - rr * 1.6f), max(1f, rr * 0.5f))
                    FlowerKind.BLOSSOM -> blossom(x, y, rr, fc, col.flowerCenter, sp.petals)
                    FlowerKind.CROSS -> for (k in 0 until 4) {
                        val a = rad(k * 90 + 45.0)
                        drawCircle(fc, rr * 0.62f, Offset(x + (cos(a) * rr * 0.55).toFloat(), y + (sin(a) * rr * 0.55).toFloat()))
                    }
                }
            }
        }
        col.fruit?.let { defaultFruit ->
            val list = o.fruitN?.let { n -> m.fruitOrder.take(min(n, m.fruits.size)).map { m.fruits[it] } } ?: m.fruits
            list.forEachIndexed { k, fr ->
                val f = if (o.fruitN != null) 1.0 else frac(t, fr.birth, 0.06)
                if (f <= 0) return@forEachIndexed
                val x = px(fr.x); val y = py(fr.y); val rr = (fr.r * scale * f).toFloat()
                val fc = o.fruitColor?.invoke(k) ?: defaultFruit
                when (sp.fruitKind) {
                    FruitKind.OVAL -> oval(fc, x, y, rr * 0.7f, rr, 0.3)
                    FruitKind.PEAR -> oval(fc, x, y + rr * 0.2f, rr, rr * 1.05f)
                    else -> drawCircle(fc, rr, Offset(x, y))
                }
                if (sp.fruitKind == FruitKind.CROWN) {
                    drawPath(Path().apply { moveTo(x - rr * 0.3f, y - rr * 0.9f); lineTo(x, y - rr * 1.35f); lineTo(x + rr * 0.3f, y - rr * 0.9f); close() }, col.fruitDark ?: fc)
                }
                if (o.fruitN != null) drawCircle(Color.White.copy(alpha = 0.55f), rr * 0.3f, Offset(x - rr * 0.3f, y - rr * 0.3f))
            }
        }
    }
    val fin = o.fin
    if (fin != null && fin > 0 && sp.finale != null) drawFinale(sp, m, fin, ::px, ::py, scale, col, sc)
}

private fun DrawScope.drawPalm(m: Model, t: Double, px: (Double) -> Float, py: (Double) -> Float, scale: Float, col: TreeColors) {
    val pts = m.palmPts ?: return
    val trunkF = frac(t, 0.0, 0.8)
    val n = pts.size - 1
    val upto = max(0.02, trunkF) * n
    var tip = pts[0]
    val path = Path().apply { moveTo(px(0.0), py(0.0)) }
    for (i in 1..ceil(upto).toInt()) {
        val u = min(1.0, upto - (i - 1))
        val q = pts[i - 1]; val w = pts[i]
        tip = Pt(lerp(q.x, w.x, u), lerp(q.y, w.y, u))
        path.lineTo(px(tip.x), py(tip.y))
    }
    val tw = (m.palmW * scale * (0.5 + 0.5 * t)).toFloat()
    drawPath(path, col.trunk, style = Stroke(max(1f, tw), cap = StrokeCap.Round, join = StrokeJoin.Round))
    val ring = col.trunkDark ?: col.trunk
    for (i in 2 until floor(upto).toInt()) {
        val q = pts[i]; val x = px(q.x); val y = py(q.y); val hw = tw * 0.5f
        line(ring, Offset(x - hw, y + 1), Offset(x + hw, y - 1), max(0.6f, scale * 0.005f))
    }
    val tx = px(tip.x); val ty = py(tip.y)
    for (fr in m.fronds) {
        val f = frac(t, fr.birth, 0.3)
        if (f <= 0) continue
        val l = fr.len * scale * f * (0.45 + 0.55 * t)
        val a = rad(fr.a)
        val ex = (tx + cos(a) * l).toFloat(); val ey = (ty - sin(a) * l * 0.7 + fr.droop * l).toFloat()
        val cx = (tx + cos(a) * l * 0.5).toFloat(); val cy = (ty - sin(a) * l * 0.7 - l * 0.12).toFloat()
        val c = if (fr.dark) col.leafDark else col.leaf
        drawPath(Path().apply { moveTo(tx, ty); quadraticTo(cx, cy, ex, ey) }, c, style = Stroke(max(1f, scale * 0.006f), cap = StrokeCap.Round))
        val lw = max(0.7f, scale * 0.0045f)
        val cs = cos(a).let { if (it == 0.0) 1.0 else it }.sign
        for (k in 2..12) {
            val u = k / 13.0
            val bx = ((1 - u) * (1 - u) * tx + 2 * (1 - u) * u * cx + u * u * ex).toFloat()
            val by = ((1 - u) * (1 - u) * ty + 2 * (1 - u) * u * cy + u * u * ey).toFloat()
            val ll = l * 0.2 * sin(u * PI) + l * 0.03
            for (sd in intArrayOf(-1, 1)) {
                val aa = a + sd * 1.1 - 0.3 * cs
                line(c, Offset(bx, by), Offset((bx + cos(aa) * ll * 0.6).toFloat(), (by + abs(sin(aa)) * ll * 0.9 + ll * 0.3).toFloat()), lw)
            }
        }
    }
    m.palmTip = tip
}

private fun perchPoint(m: Model, i: Int): Pair<Double, Double> {
    val p = m.perches[(i * 7) % m.perches.size]
    val (x, y) = polyAt(p.seg.pts, p.pos)
    return x to y
}

private fun ease(lf: Double) = 1 - (1 - lf).pow(3)

private fun DrawScope.drawFinale(sp: TreeSpecies, m: Model, fin: Double, px: (Double) -> Float, py: (Double) -> Float, scale: Float, col: TreeColors, sc: SceneColors) {
    when (sp.finale) {
        Finale.BIRDS_NEST, Finale.CEDAR_BIRDS -> birdsIn(m, fin, 3, true, px, py, scale, sc)
        Finale.PALM_BIRDS -> { birdsIn(m, fin, 2, false, px, py, scale, sc); sparkle(m, fin, hex(0xE8B931), px, py, scale) }
        Finale.DOVE -> {
            if (m.perches.isEmpty()) return
            val lf = (fin * 1.3).coerceIn(0.0, 1.0)
            val (qx, qy) = perchPoint(m, 1)
            val tx = px(qx); val ty = py(qy)
            val e = ease(lf)
            val x = lerp(tx - scale * 0.9, tx.toDouble(), e).toFloat()
            val y = (lerp(ty - scale * 0.5, ty.toDouble(), e) - sin(e * PI) * scale * 0.06).toFloat()
            val s = scale * 0.065f
            bird(x, y, s, fin * 30, 1f, sc.white, hex(0xC9D1D6), hex(0xC98A2E), lf < 1)
            if (lf > 0.1) leaf(x + s * 0.8f, y - s * 0.7f, -20.0, s * 0.9f, LeafShape.ELLIPSE, 0.25, col.leafDark)
        }
        Finale.FIGS -> col.ripe?.let { ripe ->
            val a = (fin * 1.5).coerceIn(0.0, 1.0).toFloat()
            for (fr in m.fruits) oval(ripe, px(fr.x), py(fr.y) + (fr.r * scale * 0.2).toFloat(), (fr.r * scale).toFloat(), (fr.r * scale * 1.05).toFloat(), alpha = a)
        }
        Finale.PETALS -> {
            val r = Rng(3)
            val c = col.flower ?: return
            for (i in 0 until 14) {
                val fx = (r.next() - 0.5) * 0.8; val fy0 = 0.3 + r.next() * 0.5; val fall = (fin * 0.6 + r.next()) % 1.0
                val a = ((fin * 3).coerceIn(0.0, 1.0) * (1 - fall * 0.6)).toFloat()
                oval(c, px(fx + sin(fall * 6 + i) * 0.03), py(fy0 - fall * fy0), scale * 0.008f, scale * 0.005f, fall * 5, a)
            }
        }
        Finale.SPARKLE_WHITE -> sparkle(m, fin, Color.White, px, py, scale)
        Finale.SPARKLE_GOLD -> sparkle(m, fin, hex(0xF2C94C), px, py, scale)
        Finale.SPARKLE_PINK -> sparkle(m, fin, hex(0xE7A6C0), px, py, scale)
        Finale.TENT -> {
            val a = (fin * 1.5).coerceIn(0.0, 1.0).toFloat()
            val x = px(0.34); val y = py(0.0); val w = scale * 0.13f * a; val h = scale * 0.1f * a
            drawPath(Path().apply { moveTo(x - w, y); lineTo(x, y - h); lineTo(x + w, y); close() }, if (sc.dark) hex(0x8C7458) else hex(0xB79A73))
            drawPath(Path().apply { moveTo(x - w * 0.25f, y); lineTo(x, y - h * 0.62f); lineTo(x + w * 0.25f, y); close() }, if (sc.dark) hex(0x3C3227) else hex(0x6E5A41))
        }
        Finale.ZACCHAEUS -> {
            val a = (fin * 1.4).coerceIn(0.0, 1.0).toFloat()
            if (a <= 0f || m.perches.isEmpty()) return
            val (qx, qy) = perchPoint(m, 0)
            val x = px(qx); val y = py(qy); val s = scale * 0.03f
            val body = if (sc.dark) hex(0xD7B898) else hex(0x8B5E3C)
            drawCircle(body, s * 0.55f, Offset(x, y - s * 2.1f), alpha = a)
            drawPath(Path().apply { moveTo(x - s * 0.7f, y); quadraticTo(x, y - s * 2.2f, x + s * 0.7f, y); close() }, body, alpha = a)
            drawRect(if (sc.dark) hex(0xC9A23A) else hex(0xB8860B), Offset(x - s * 0.75f, y - s * 1.2f), Size(s * 1.5f, s * 0.25f), alpha = a)
        }
        null -> {}
    }
}

private fun DrawScope.birdsIn(m: Model, fin: Double, count: Int, nest: Boolean, px: (Double) -> Float, py: (Double) -> Float, scale: Float, sc: SceneColors) {
    val isPalm = m.palmPts != null
    if (m.perches.isEmpty() && !isPalm) return
    for (i in 0 until count) {
        val lf = (fin * 1.6 - i * 0.2).coerceIn(0.0, 1.0)
        if (lf <= 0) continue
        val (tx, ty) = if (isPalm) px(m.palmTip.x + (i - 1) * 0.12) to py(m.palmTip.y - 0.02) else perchPoint(m, i).let { (x, y) -> px(x) to py(y) }
        val sx = tx + (if (i % 2 == 1) 1 else -1) * scale * 0.9f
        val sy = ty - scale * 0.55f
        val e = ease(lf)
        val x = lerp(sx.toDouble(), tx.toDouble(), e).toFloat()
        val y = (lerp(sy.toDouble(), ty.toDouble(), e) - sin(e * PI) * scale * 0.08).toFloat()
        val sz = scale * 0.055f
        if (nest && i == 0 && lf >= 1) oval(sc.trunkDark, tx, ty + sz * 0.1f, sz * 0.9f, sz * 0.38f)
        bird(x, y, sz, fin * 40 + i, if (i % 2 == 1) -1f else 1f, sc.bird, sc.birdWing, sc.blossom, lf < 1)
    }
}

private fun DrawScope.sparkle(m: Model, fin: Double, color: Color, px: (Double) -> Float, py: (Double) -> Float, scale: Float) {
    val pts = m.flowers + m.fruits
    if (pts.isEmpty()) return
    val k = min(pts.size, 14)
    for (i in 0 until k) {
        val q = pts[(i * 5) % pts.size]
        val x = px(q.x); val y = py(q.y)
        val a = ((fin * 2 - i.toDouble() / k).coerceIn(0.0, 1.0) * (0.5 + 0.5 * sin(fin * 12 + i))).toFloat() * 0.8f
        val r = scale * 0.022f
        val w = 1.2f * density
        line(color, Offset(x - r, y), Offset(x + r, y), w, a)
        line(color, Offset(x, y - r), Offset(x, y + r), w, a)
    }
}
