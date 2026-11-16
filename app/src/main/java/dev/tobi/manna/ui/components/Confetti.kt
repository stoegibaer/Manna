package dev.tobi.manna.ui.components

import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.drawscope.rotate
import dev.tobi.manna.ui.theme.LocalMannaColors
import kotlin.math.cos
import kotlin.math.sin
import kotlin.random.Random

private class Particle(val angle: Float, val speed: Float, val spin: Float, val colorIdx: Int, val w: Float, val h: Float)

/**
 * Burst of confetti every time [trigger] changes (and is > 0). [big] for completed sections.
 * Draws nothing when [enabled] is false.
 */
@Composable
fun Confetti(trigger: Int, enabled: Boolean, big: Boolean = false, modifier: Modifier = Modifier.fillMaxSize()) {
    if (!enabled) return
    val extra = LocalMannaColors.current
    val palette = listOf(MaterialTheme.colorScheme.primary, extra.blossom, extra.leaf, MaterialTheme.colorScheme.tertiary, MaterialTheme.colorScheme.secondary)
    val progress = remember { Animatable(1f) }
    val particles = remember(trigger) {
        val rnd = Random(trigger * 31 + 7)
        List(if (big) 90 else 36) {
            Particle(
                angle = (-90f + (rnd.nextFloat() - 0.5f) * (if (big) 150f else 110f)),
                speed = 0.55f + rnd.nextFloat() * 0.75f,
                spin = (rnd.nextFloat() - 0.5f) * 900f,
                colorIdx = rnd.nextInt(5),
                w = 6f + rnd.nextFloat() * 7f,
                h = 4f + rnd.nextFloat() * 4f,
            )
        }
    }
    LaunchedEffect(trigger) {
        if (trigger > 0) {
            progress.snapTo(0f)
            progress.animateTo(1f, tween(if (big) 2200 else 1400, easing = LinearEasing))
        }
    }
    Canvas(modifier) {
        val t = progress.value
        if (t >= 1f) return@Canvas
        val origin = Offset(size.width / 2f, size.height * (if (big) 0.45f else 0.55f))
        val reach = size.height * 0.9f
        for (p in particles) {
            val rad = Math.toRadians(p.angle.toDouble())
            val x = origin.x + (cos(rad) * p.speed * reach * t).toFloat()
            val y = origin.y + (sin(rad) * p.speed * reach * t).toFloat() + 0.9f * reach * t * t
            val alpha = (1.6f - 1.6f * t).coerceIn(0f, 1f)
            rotate(p.spin * t, Offset(x, y)) {
                val w = p.w * density; val h = p.h * density
                drawRect(palette[p.colorIdx].copy(alpha = alpha), Offset(x - w / 2, y - h / 2), Size(w, h))
            }
        }
    }
}
