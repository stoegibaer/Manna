package dev.tobi.manna.ui.components

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.FastOutSlowInEasing
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.rotate
import androidx.compose.ui.graphics.drawscope.translate
import dev.tobi.manna.ui.theme.LocalMannaColors
import kotlin.math.cos
import kotlin.math.exp
import kotlin.math.sin
import kotlin.random.Random

/** Growth 0..1 from number of completed sections. Never shrinks. */
fun treeGrowth(sections: Float): Float = (1f - exp(-sections / 22f)).coerceIn(0f, 1f)

private class Branch(
    val x0: Float, val y0: Float, val x1: Float, val y1: Float,
    val depth: Int, val birth: Float, val span: Float, val parent: Branch?, val atParent: Float,
)

private class Leaf(val branch: Branch, val pos: Float, val angle: Float, val size: Float, val birth: Float, val dark: Boolean)
private class Blossom(val branch: Branch, val birth: Float, val size: Float)

private class TreeModel(seed: Int) {
    val branches = ArrayList<Branch>()
    val leaves = ArrayList<Leaf>()
    val blossoms = ArrayList<Blossom>()

    init {
        val rnd = Random(seed)
        fun grow(x: Float, y: Float, angle: Float, len: Float, depth: Int, birth: Float, span: Float, parent: Branch?, at: Float) {
            val rad = Math.toRadians(angle.toDouble())
            val x1 = x + (cos(rad) * len).toFloat()
            val y1 = y + (sin(rad) * len).toFloat()
            val b = Branch(x, y, x1, y1, depth, birth, span, parent, at)
            branches += b
            if (depth >= 1) {
                val n = 2 + rnd.nextInt(3)
                repeat(n) {
                    leaves += Leaf(
                        b, 0.35f + rnd.nextFloat() * 0.65f,
                        angle + (if (rnd.nextBoolean()) 1 else -1) * (35f + rnd.nextFloat() * 40f),
                        0.035f + rnd.nextFloat() * 0.025f - depth * 0.002f,
                        birth + span * (0.4f + rnd.nextFloat() * 0.6f) + 0.03f,
                        rnd.nextFloat() < 0.4f,
                    )
                }
            }
            if (depth >= 4 && rnd.nextFloat() < 0.45f) blossoms += Blossom(b, maxOf(0.72f, birth + span) + rnd.nextFloat() * 0.22f, 0.012f + rnd.nextFloat() * 0.008f)
            if (depth >= 5) return
            val children = if (depth == 0) 3 else 2 + (if (rnd.nextFloat() < 0.35f) 1 else 0)
            val side = if (rnd.nextBoolean()) 1f else -1f // which side the first side-branch goes, so the tree stays balanced
            repeat(children) { i ->
                val at = if (i == 0) 1f else 0.55f + rnd.nextFloat() * 0.35f
                val spread = 18f + rnd.nextFloat() * 22f
                val dir = when {
                    children == 1 -> 0f
                    i == 0 -> (rnd.nextFloat() - 0.5f) * 16f
                    i % 2 == 1 -> side * spread
                    else -> -side * spread
                }
                val cx = x + (x1 - x) * at
                val cy = y + (y1 - y) * at
                grow(cx, cy, angle + dir, len * (0.68f + rnd.nextFloat() * 0.12f), depth + 1, birth + span * at, 0.15f, b, at)
            }
        }
        grow(0f, 0f, 90f, 0.30f, 0, 0f, 0.12f, null, 0f)
    }
}

private fun frac(t: Float, birth: Float, span: Float) = ((t - birth) / span).coerceIn(0f, 1f)

/**
 * The mustard seed (Mk 4,30–32) that grows into a tree with every completed section.
 * [sections] may be fractional while animating.
 */
@Composable
fun MustardTree(sections: Float, modifier: Modifier = Modifier, animateFrom: Float? = null, animate: Boolean = true) {
    val colors = LocalMannaColors.current
    val model = remember { TreeModel(seed = 7) }
    val anim = remember { Animatable(animateFrom ?: sections) }
    LaunchedEffect(sections) {
        if (animate) anim.animateTo(sections, tween(1600, easing = FastOutSlowInEasing)) else anim.snapTo(sections)
    }
    Canvas(modifier) {
        val t = treeGrowth(anim.value)
        val unit = minOf(size.width * 1.05f, size.height) * 0.95f
        // zoom in while the plant is small so even a sprout fills the frame
        val scale = unit * (1.55f - 0.75f * t)
        val root = Offset(size.width / 2f, size.height * 0.93f)
        fun p(x: Float, y: Float) = Offset(root.x + x * scale, root.y - y * scale)

        // ground
        drawOval(colors.ground, topLeft = Offset(root.x - unit * 0.32f, root.y - unit * 0.025f), size = Size(unit * 0.64f, unit * 0.06f))

        if (t < 0.012f) {
            // the seed
            drawOval(colors.trunk, topLeft = Offset(root.x - scale * 0.02f, root.y - scale * 0.032f), size = Size(scale * 0.04f, scale * 0.028f))
            return@Canvas
        }

        // visible end point of a branch
        fun tip(b: Branch): Offset {
            val f = frac(t, b.birth, b.span)
            return p(b.x0 + (b.x1 - b.x0) * f, b.y0 + (b.y1 - b.y0) * f)
        }

        for (b in model.branches) {
            val f = frac(t, b.birth, b.span)
            if (f <= 0f) continue
            val w = (0.05f * (1f - b.depth * 0.17f)).coerceAtLeast(0.008f) * scale * (0.6f + 0.4f * f) * (0.4f + 0.6f * t)
            drawLine(colors.trunk, p(b.x0, b.y0), tip(b), strokeWidth = w, cap = StrokeCap.Round)
        }

        // first two seed leaves while the plant is a sprout
        val sprout = (1f - frac(t, 0.22f, 0.2f)) * frac(t, 0.012f, 0.02f)
        if (sprout > 0f) {
            val top = tip(model.branches[0])
            leaf(top, 55f, 0.11f * scale * sprout, colors.leaf)
            leaf(top, 125f, 0.11f * scale * sprout, colors.leafDark)
        }

        for (l in model.leaves) {
            val f = frac(t, l.birth, 0.05f)
            if (f <= 0f || frac(t, l.branch.birth, l.branch.span) < l.pos) continue
            val b = l.branch
            val at = p(b.x0 + (b.x1 - b.x0) * l.pos, b.y0 + (b.y1 - b.y0) * l.pos)
            leaf(at, l.angle, l.size * scale * 1.6f * f, if (l.dark) colors.leafDark else colors.leaf)
        }

        for (bl in model.blossoms) {
            val f = frac(t, bl.birth, 0.06f)
            if (f <= 0f || frac(t, bl.branch.birth, bl.branch.span) < 1f) continue
            val at = p(bl.branch.x1, bl.branch.y1)
            val r = bl.size * scale * f
            for (k in 0 until 4) {
                val a = Math.toRadians((k * 90 + 45).toDouble())
                drawCircle(colors.blossom, r * 0.62f, Offset(at.x + (cos(a) * r * 0.55f).toFloat(), at.y + (sin(a) * r * 0.55f).toFloat()))
            }
        }
    }
}

private fun DrawScope.leaf(at: Offset, angleDeg: Float, length: Float, color: androidx.compose.ui.graphics.Color) {
    if (length <= 0.5f) return
    val path = Path().apply {
        moveTo(0f, 0f)
        quadraticTo(length * 0.5f, -length * 0.38f, length, 0f)
        quadraticTo(length * 0.5f, length * 0.38f, 0f, 0f)
        close()
    }
    // canvas y points down, so a math angle maps to -angle
    rotate(-angleDeg, pivot = at) {
        translate(left = at.x, top = at.y) { drawPath(path, color) }
    }
}
