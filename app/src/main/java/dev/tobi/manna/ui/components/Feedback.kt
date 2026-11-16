package dev.tobi.manna.ui.components

import android.content.Context
import android.media.AudioAttributes
import android.media.SoundPool
import android.os.Build
import android.view.HapticFeedbackConstants
import android.view.View
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.remember
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalView
import dev.tobi.manna.R
import dev.tobi.manna.data.settings.Settings

/** Haptic + sound feedback, respecting the user's settings. Wrong answers get only a soft, non-punishing cue. */
class Feedback(context: Context, private val view: View) {
    var settings: Settings = Settings()

    private val pool = SoundPool.Builder()
        .setMaxStreams(2)
        .setAudioAttributes(
            AudioAttributes.Builder()
                .setUsage(AudioAttributes.USAGE_ASSISTANCE_SONIFICATION)
                .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                .build()
        ).build()
    private val ok = pool.load(context, R.raw.chime_ok, 1)
    private val done = pool.load(context, R.raw.chime_done, 1)
    private val soft = pool.load(context, R.raw.chime_soft, 1)

    fun correct() {
        haptic(if (Build.VERSION.SDK_INT >= 30) HapticFeedbackConstants.CONFIRM else HapticFeedbackConstants.VIRTUAL_KEY)
        sound(ok, 0.7f)
    }

    fun tryAgain() {
        haptic(HapticFeedbackConstants.CLOCK_TICK)
        sound(soft, 0.4f)
    }

    fun sectionDone() {
        haptic(HapticFeedbackConstants.LONG_PRESS)
        sound(done, 0.8f)
    }

    fun tick() = haptic(HapticFeedbackConstants.CLOCK_TICK)

    private fun haptic(type: Int) {
        if (settings.haptics) view.performHapticFeedback(type)
    }

    private fun sound(id: Int, vol: Float) {
        if (settings.playSound) pool.play(id, vol, vol, 1, 0, 1f)
    }

    fun release() = pool.release()
}

val LocalFeedback = staticCompositionLocalOf<Feedback> { error("Feedback not provided") }

@Composable
fun rememberFeedback(settings: Settings): Feedback {
    val context = LocalContext.current
    val view = LocalView.current
    val fb = remember { Feedback(context, view) }
    fb.settings = settings
    DisposableEffect(Unit) { onDispose { fb.release() } }
    return fb
}
