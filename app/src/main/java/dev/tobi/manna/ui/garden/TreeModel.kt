package dev.tobi.manna.ui.garden

import kotlin.math.PI
import kotlin.math.atan2
import kotlin.math.cos
import kotlin.math.floor
import kotlin.math.max
import kotlin.math.min
import kotlin.math.roundToInt
import kotlin.math.sin

/*
 * Procedural tree shapes. Units: the root is at (0, 0), y points up, a grown tree is about 1 high.
 * Every element has a birth time in growth t (0..1), so a tree grows a little with every section.
 * The generators follow the approved design mockup exactly (same random sequence per seed).
 */

/** xorshift32 – same sequence as the design mockup for the same seed. */
internal class Rng(seed: Int) {
    private var s: Int = ((seed.toLong() * 2654435761L) and 0xFFFFFFFFL).toInt().let { if (it == 0) 1 else it }
    fun next(): Double {
        s = s xor (s shl 13)
        s = s xor (s ushr 17)
        s = s xor (s shl 5)
        return (s.toLong() and 0xFFFFFFFFL) / 4294967296.0
    }
}

internal fun rad(d: Double) = d * PI / 180.0
internal fun lerp(a: Double, b: Double, f: Double) = a + (b - a) * f
internal fun frac(t: Double, birth: Double, span: Double) = ((t - birth) / span).coerceIn(0.0, 1.0)

internal class Pt(val x: Double, val y: Double)

internal class Seg(val pts: List<Pt>, val w: Double, val birth: Double, val span: Double, val depth: Int)
internal class Leaf(val x: Double, val y: Double, val a: Double, val len: Double, val dark: Boolean, val birth: Double)
internal class Clump(val x: Double, val y: Double, val r: Double, val shade: Double, val birth: Double, val flat: Double? = null)
internal class Dot(val x: Double, val y: Double, val r: Double, val birth: Double)
internal class Strand(val x: Double, val y: Double, val len: Double, val sway: Double, val birth: Double, val dark: Boolean)
internal class Perch(val seg: Seg, val pos: Double)
internal class Frond(val a: Double, val len: Double, val droop: Double, val birth: Double, val dark: Boolean)

internal class Model {
    val segs = ArrayList<Seg>()
    val leaves = ArrayList<Leaf>()
    val clumps = ArrayList<Clump>()
    val flowers = ArrayList<Dot>()
    val fruits = ArrayList<Dot>()
    val strands = ArrayList<Strand>()
    val perches = ArrayList<Perch>()

    // palm only
    var palmPts: List<Pt>? = null
    val fronds = ArrayList<Frond>()
    var palmW = 0.0
    /** Visible top of the palm trunk from the last draw (for the finale). */
    var palmTip = Pt(0.0, 0.0)

    /** Fruits in a scattered order, for ripening one after the other. */
    val fruitOrder: List<Int> by lazy {
        val r = Rng(91)
        fruits.indices.map { r.next() to it }.sortedBy { it.first }.map { it.second }
    }
}

/** Point and direction (degrees) at fraction [f] along a polyline. */
internal fun polyAt(pts: List<Pt>, f: Double): Triple<Double, Double, Double> {
    val n = pts.size - 1
    val x = f * n
    val i = min(n - 1, floor(x).toInt())
    val u = x - i
    val a = pts[i]; val b = pts[i + 1]
    return Triple(lerp(a.x, b.x, u), lerp(a.y, b.y, u), atan2(b.y - a.y, b.x - a.x) * 180 / PI)
}

internal class Flower(val p: Double, val r: Double, val from: Double, val spread: Double = 0.2, val along: Int = 0)
internal class Fruit(val p: Double, val r: Double, val from: Double, val hang: Double = 0.015)

/** Parameters of the branching generator; defaults as in the mockup. */
internal class Branchy(
    val seed: Int,
    val depth: Int,
    val trunkLen: Double = 0.3,
    val trunkW: Double = 0.05,
    val trunkSpan: Double = 0.12,
    val trunkCurve: Double = 20.0,
    val curve: Double = 16.0,
    val up: Double = 0.0,
    val droop: Double = 0.0,
    val droopFrom: Int = 2,
    val gnarl: Double = 0.0,
    val squash: Double = 0.0,
    val leaf: Boolean = false,
    val leafFrom: Int = 1,
    val leafCount: Double = 3.0,
    val leafLen: Double = 0.05,
    val clumpAlong: Int = 0,
    val clumpFrom: Int = 2,
    val clumpR: Double = 0.06,
    val strands: Int = 0,
    val strandFrom: Int = 0,
    val strandLen: Double = 0.0,
    val tipClump: Double = 0.0,
    val flower: Flower? = null,
    val fruit: Fruit? = null,
    val trunkKids: Int = 3,
    val kids: Int = 2,
    val extraKid: Double = 0.35,
    val atMin: Double = 0.55,
    val spread: Pair<Double, Double> = 18.0 to 40.0,
    val mainJit: Double = 16.0,
    val lenF: Pair<Double, Double> = 0.68 to 0.8,
    val sideBoost: Double = 1.0,
    val wF: Double = 0.68,
    val trunks: Int = 1,
    val lean: Double = 0.0,
    val trunkFan: Double = 14.0,
)

internal fun branchy(p: Branchy): Model {
    val r = Rng(p.seed)
    val m = Model()
    val maxD = p.depth
    val spanD = (0.86 - p.trunkSpan) / maxD

    fun grow(x: Double, y: Double, ang: Double, len: Double, depth: Int, birth: Double, span: Double, w: Double) {
        val n = 7
        val pts = ArrayList<Pt>(n + 1).apply { add(Pt(x, y)) }
        var a = ang
        var cx = x
        var cy = y
        val bend = (r.next() - 0.5) * (if (depth == 0) p.trunkCurve else p.curve)
        repeat(n) {
            a += bend / n
            a += (90 - a) * p.up / n
            if (p.droop != 0.0 && depth >= p.droopFrom) {
                val tgt = if (cos(rad(a)) >= 0) -90.0 else 270.0
                a += (tgt - a) * p.droop * (depth.toDouble() / maxD) / n
            }
            if (p.gnarl != 0.0 && depth <= 1) a += (r.next() - 0.5) * p.gnarl
            cx += cos(rad(a)) * len / n
            cy += sin(rad(a)) * len / n * (if (p.squash != 0.0 && depth > 0) p.squash else 1.0)
            pts.add(Pt(cx, cy))
        }
        val seg = Seg(pts, w, birth, span, depth)
        m.segs.add(seg)
        if (depth == 1 || depth == 2) m.perches.add(Perch(seg, 0.55 + r.next() * 0.35))
        if (p.leaf && depth >= p.leafFrom) {
            val cnt = (p.leafCount * (0.7 + r.next() * 0.6)).roundToInt()
            repeat(cnt) {
                val pos = 0.3 + r.next() * 0.7
                val (lx, ly, la) = polyAt(pts, pos)
                val la2 = la + (if (r.next() < 0.5) 1 else -1) * (35 + r.next() * 40)
                val l = p.leafLen * (0.75 + r.next() * 0.5) * (1 - depth * 0.03)
                val dark = r.next() < 0.4
                m.leaves.add(Leaf(lx, ly, la2, l, dark, birth + span * pos + 0.02 + r.next() * 0.04))
            }
        }
        if (p.clumpAlong > 0 && depth >= p.clumpFrom) {
            repeat(p.clumpAlong) {
                val pos = 0.4 + r.next() * 0.6
                val (lx, ly) = polyAt(pts, pos)
                val qx = lx + (r.next() - 0.5) * 0.03
                val qy = ly + (r.next() - 0.3) * 0.03
                val rr = p.clumpR * (0.6 + r.next() * 0.5) * (1.15 - depth * 0.06)
                m.clumps.add(Clump(qx, qy, rr, r.next(), birth + span * pos + 0.02))
            }
        }
        if (p.strands > 0 && depth >= p.strandFrom) {
            repeat(p.strands) {
                val pos = 0.4 + r.next() * 0.6
                val (lx, ly) = polyAt(pts, pos)
                val l = p.strandLen * (0.6 + r.next() * 0.6)
                val sway = (r.next() - 0.5) * 0.04
                m.strands.add(Strand(lx, ly, l, sway, birth + span * pos + 0.03, r.next() < 0.45))
            }
        }
        if (depth >= maxD) {
            val tip = pts[n]
            if (p.tipClump > 0) {
                val rr = p.tipClump * (0.7 + r.next() * 0.6)
                m.clumps.add(Clump(tip.x, tip.y, rr, r.next(), birth + span * 0.8))
            }
            p.flower?.let { fl ->
                if (r.next() < fl.p) {
                    val fx = tip.x + (r.next() - 0.5) * 0.02
                    val fy = tip.y + (r.next() - 0.5) * 0.02
                    val fr = fl.r * (0.8 + r.next() * 0.5)
                    m.flowers.add(Dot(fx, fy, fr, max(fl.from, birth + span) + r.next() * fl.spread))
                }
            }
            p.fruit?.let { fr ->
                if (r.next() < fr.p) {
                    val (fx, fy) = polyAt(pts, 0.5 + r.next() * 0.5)
                    val rr = fr.r * (0.8 + r.next() * 0.4)
                    m.fruits.add(Dot(fx, fy - fr.hang, rr, max(fr.from, birth + span) + r.next() * 0.12))
                }
            }
            return
        }
        p.flower?.let { fl ->
            if (fl.along > 0 && depth >= fl.along) repeat(2) {
                if (r.next() < fl.p) {
                    val (fx, fy) = polyAt(pts, 0.3 + r.next() * 0.7)
                    val fr = fl.r * (0.7 + r.next() * 0.5)
                    m.flowers.add(Dot(fx, fy, fr, max(fl.from, birth + span) + r.next() * fl.spread))
                }
            }
        }
        val kids = if (depth == 0) p.trunkKids else p.kids + (if (r.next() < p.extraKid) 1 else 0)
        val side = if (r.next() < 0.5) 1 else -1
        for (i in 0 until kids) {
            val at = if (i == 0) 1.0 else p.atMin + r.next() * (1 - p.atMin - 0.1)
            val (px, py, pa) = polyAt(pts, at)
            val spread = p.spread.first + r.next() * (p.spread.second - p.spread.first)
            val dir = if (i == 0) (r.next() - 0.5) * p.mainJit else (if (i % 2 == 1) side else -side) * spread
            val lf = p.lenF.first + r.next() * (p.lenF.second - p.lenF.first)
            grow(px, py, pa + dir, len * lf * (if (depth == 0 && i > 0) p.sideBoost else 1.0), depth + 1, birth + span * at, spanD, w * p.wF)
        }
    }

    for (k in 0 until p.trunks) {
        val off = if (p.trunks == 1) 0.0 else (k - (p.trunks - 1) / 2.0) * 0.025
        val ang = 90 + if (p.trunks == 1) p.lean else (k - (p.trunks - 1) / 2.0) * p.trunkFan
        grow(off, 0.0, ang, p.trunkLen, 0, k * 0.02, p.trunkSpan, p.trunkW)
    }
    return m
}

internal class PalmParams(val seed: Int, val height: Double, val lean: Double, val trunkW: Double, val fronds: Int, val frondLen: Double, val droop: Double)

internal fun palm(p: PalmParams): Model {
    val r = Rng(p.seed)
    val m = Model()
    val n = 24
    val pts = ArrayList<Pt>().apply { add(Pt(0.0, 0.0)) }
    for (i in 1..n) {
        val f = i.toDouble() / n
        pts.add(Pt(sin(f * 2.2) * p.lean * f + (r.next() - 0.5) * 0.002, f * p.height))
    }
    m.palmPts = pts
    m.palmW = p.trunkW
    for (i in 0 until p.fronds) {
        val a = -40 + 260 * (i.toDouble() / (p.fronds - 1)) + (r.next() - 0.5) * 14
        val len = p.frondLen * (0.75 + r.next() * 0.4)
        val droop = p.droop * (0.7 + r.next() * 0.6)
        val birth = 0.04 + (i % 4) * 0.05 + r.next() * 0.1 + (if (kotlin.math.abs(a - 90) > 90) 0.25 else 0.0)
        m.fronds.add(Frond(a, len, droop, birth, r.next() < 0.5))
    }
    return m
}

internal class CedarParams(val seed: Int, val height: Double, val trunkW: Double, val tiers: Int, val span: Double, val sag: Double, val pad: Double, val flat: Double)

/** A young, cone-shaped cedar in tiers. */
internal fun cedar(p: CedarParams): Model {
    val r = Rng(p.seed)
    val m = Model()
    val h = p.height
    m.segs.add(Seg(List(8) { i -> Pt((r.next() - 0.5) * 0.004 * i, h * i / 7) }, p.trunkW, 0.0, 0.75, 0))
    for (k in 0 until p.tiers) {
        val f = 0.22 + 0.74 * k / (p.tiers - 1)
        val y = h * f
        val birth = 0.75 * f * 0.92
        val widthF = (1 - f) * 0.9 + 0.1
        for (s in intArrayOf(-1, 1)) {
            val l = p.span * widthF * (0.65 + r.next() * 0.55)
            val up = 6 + r.next() * 10
            val pts = List(7) { i -> val u = i / 6.0; Pt(s * l * u, y + sin(rad(up)) * l * u - p.sag * u * u) }
            val seg = Seg(pts, p.trunkW * 0.38, birth, 0.18, 2)
            m.segs.add(seg)
            val pads = 3 + (l * 12).roundToInt()
            for (j in 0 until pads) {
                val u = 0.25 + 0.75 * j / max(1, pads - 1)
                val (px, py) = polyAt(pts, u)
                m.clumps.add(Clump(px, py + 0.012, p.pad * (0.75 + r.next() * 0.5) * (1 - u * 0.25), r.next(), birth + 0.18 * u + 0.02, p.flat))
            }
            if (k > 0 && k < p.tiers - 1) m.perches.add(Perch(seg, 0.7))
        }
    }
    m.clumps.add(Clump(0.0, h + 0.01, p.pad * 0.9, 0.2, 0.82, p.flat))
    return m
}

/**
 * The mustard tree exactly as the app has always drawn it (ui.components.MustardTree, seed 7),
 * so the first tree looks the same before and after it moves into the garden.
 */
internal fun mustard(): Model {
    val m = Model()
    val rnd = kotlin.random.Random(7)
    fun grow(x: Float, y: Float, angle: Float, len: Float, depth: Int, birth: Float, span: Float) {
        val r = Math.toRadians(angle.toDouble())
        val x1 = x + (cos(r) * len).toFloat()
        val y1 = y + (sin(r) * len).toFloat()
        val w = (0.05f * (1f - depth * 0.17f)).coerceAtLeast(0.008f).toDouble()
        val seg = Seg(listOf(Pt(x.toDouble(), y.toDouble()), Pt(x1.toDouble(), y1.toDouble())), w, birth.toDouble(), span.toDouble(), depth)
        m.segs.add(seg)
        if (depth == 1 || depth == 2) m.perches.add(Perch(seg, 0.75))
        if (depth >= 1) {
            val n = 2 + rnd.nextInt(3)
            repeat(n) {
                val pos = 0.35f + rnd.nextFloat() * 0.65f
                val a = angle + (if (rnd.nextBoolean()) 1 else -1) * (35f + rnd.nextFloat() * 40f)
                val size = 0.035f + rnd.nextFloat() * 0.025f - depth * 0.002f
                val b = birth + span * (0.4f + rnd.nextFloat() * 0.6f) + 0.03f
                val dark = rnd.nextFloat() < 0.4f
                m.leaves.add(Leaf((x + (x1 - x) * pos).toDouble(), (y + (y1 - y) * pos).toDouble(), a.toDouble(), size.toDouble(), dark, b.toDouble()))
            }
        }
        if (depth >= 4 && rnd.nextFloat() < 0.45f) {
            val b = maxOf(0.72f, birth + span) + rnd.nextFloat() * 0.22f
            val size = 0.012f + rnd.nextFloat() * 0.008f
            m.flowers.add(Dot(x1.toDouble(), y1.toDouble(), size.toDouble(), b.toDouble()))
        }
        if (depth >= 5) return
        val children = if (depth == 0) 3 else 2 + (if (rnd.nextFloat() < 0.35f) 1 else 0)
        val side = if (rnd.nextBoolean()) 1f else -1f
        repeat(children) { i ->
            val at = if (i == 0) 1f else 0.55f + rnd.nextFloat() * 0.35f
            val spread = 18f + rnd.nextFloat() * 22f
            val dir = when {
                children == 1 -> 0f
                i == 0 -> (rnd.nextFloat() - 0.5f) * 16f
                i % 2 == 1 -> side * spread
                else -> -side * spread
            }
            grow(x + (x1 - x) * at, y + (y1 - y) * at, angle + dir, len * (0.68f + rnd.nextFloat() * 0.12f), depth + 1, birth + span * at, 0.15f)
        }
    }
    grow(0f, 0f, 90f, 0.30f, 0, 0f, 0.12f)
    return m
}
