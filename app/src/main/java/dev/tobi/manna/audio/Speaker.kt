package dev.tobi.manna.audio

import android.content.Context
import android.media.AudioAttributes
import android.media.MediaPlayer
import android.os.Handler
import android.os.Looper
import android.speech.tts.TextToSpeech
import android.speech.tts.UtteranceProgressListener
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.platform.LocalContext
import dev.tobi.manna.data.bible.Verse
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import java.util.Locale

/**
 * Reads verses aloud and reports the verse currently spoken (for highlighting).
 * Uses pre-generated audio from assets/audio/<translation>/<BB_CCC_VVV>.ogg when present
 * (made on the TTS server, see docs/tts-server-auftrag.md), otherwise Android's TextToSpeech.
 */
class Speaker(context: Context, private val translationId: String) {
    private val app = context.applicationContext
    private val main = Handler(Looper.getMainLooper())
    private val _current = MutableStateFlow(-1)
    /** Index into the verse list being read, -1 when idle. */
    val current: StateFlow<Int> = _current
    private val _playing = MutableStateFlow(false)
    val playing: StateFlow<Boolean> = _playing

    var rate: Float = 1f
    private var verses: List<Verse> = emptyList()
    private var player: MediaPlayer? = null
    private var tts: TextToSpeech? = null
    private var ttsReady = false
    private var pendingStart: Int? = null
    private val audioFiles: Set<String> by lazy {
        runCatching { app.assets.list("audio/$translationId")?.toSet() }.getOrNull().orEmpty()
    }

    private fun fileFor(v: Verse) = "%02d_%03d_%03d.ogg".format(v.book, v.chapter, v.verse).takeIf { it in audioFiles }

    fun play(list: List<Verse>, from: Int = 0) {
        stop()
        verses = list
        if (list.isEmpty()) return
        _playing.value = true
        playAt(from.coerceIn(0, list.lastIndex))
    }

    fun toggle(list: List<Verse>, from: Int) = if (_playing.value) stop() else play(list, from)

    private fun playAt(i: Int) {
        if (!_playing.value) return
        if (i > verses.lastIndex) { finish(); return }
        _current.value = i
        val file = fileFor(verses[i])
        if (file != null) playFile(i, "audio/$translationId/$file") else speak(i)
    }

    private fun playFile(i: Int, path: String) {
        runCatching {
            val afd = app.assets.openFd(path)
            player?.release()
            player = MediaPlayer().apply {
                setAudioAttributes(AudioAttributes.Builder().setUsage(AudioAttributes.USAGE_MEDIA).setContentType(AudioAttributes.CONTENT_TYPE_SPEECH).build())
                setDataSource(afd.fileDescriptor, afd.startOffset, afd.length)
                afd.close()
                setOnPreparedListener {
                    runCatching { it.playbackParams = it.playbackParams.setSpeed(rate) }
                    it.start()
                }
                // short breath between verses
                setOnCompletionListener { main.postDelayed({ playAt(i + 1) }, 350) }
                prepareAsync()
            }
        }.onFailure { speak(i) }
    }

    private fun speak(i: Int) {
        val engine = tts ?: TextToSpeech(app) { status ->
            ttsReady = status == TextToSpeech.SUCCESS
            if (ttsReady) {
                tts?.language = Locale.GERMAN
                pendingStart?.let { main.post { speak(it) } }
            } else main.post { finish() }
            pendingStart = null
        }.also { t ->
            tts = t
            t.setOnUtteranceProgressListener(object : UtteranceProgressListener() {
                override fun onStart(id: String) {}
                override fun onDone(id: String) { main.postDelayed({ playAt(id.toInt() + 1) }, 250) }
                @Deprecated("Deprecated in Java") override fun onError(id: String) { main.post { playAt(id.toInt() + 1) } }
            })
        }
        if (!ttsReady) { pendingStart = i; return }
        engine.setSpeechRate(rate)
        engine.speak(verses[i].text, TextToSpeech.QUEUE_FLUSH, null, i.toString())
    }

    private fun finish() {
        _playing.value = false
        _current.value = -1
    }

    fun stop() {
        main.removeCallbacksAndMessages(null)
        _playing.value = false
        _current.value = -1
        player?.run { runCatching { stop() }; release() }
        player = null
        tts?.stop()
    }

    fun release() {
        stop()
        tts?.shutdown()
        tts = null
    }
}

@Composable
fun rememberSpeaker(translationId: String, rate: Float): Speaker {
    val context = LocalContext.current
    val speaker = remember(translationId) { Speaker(context, translationId) }
    speaker.rate = rate
    DisposableEffect(speaker) { onDispose { speaker.release() } }
    return speaker
}
