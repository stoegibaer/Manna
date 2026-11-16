package dev.tobi.manna.data.settings

import android.content.Context
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.floatPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

enum class ThemeMode { SYSTEM, LIGHT, DARK }

data class Settings(
    val focusMode: Boolean = true,
    val haptics: Boolean = true,
    val sound: Boolean = true,
    val confetti: Boolean = true,
    val calm: Boolean = false,
    val textScale: Float = 1f,
    val theme: ThemeMode = ThemeMode.SYSTEM,
    /** Empty = not chosen yet; resolved via PlanIndex.resolve(). */
    val activePlan: String = "",
) {
    val showConfetti get() = confetti && !calm
    val playSound get() = sound && !calm
    val animations get() = !calm
}

private val Context.dataStore by preferencesDataStore("settings")

class SettingsRepository(private val context: Context) {
    private object K {
        val focus = booleanPreferencesKey("focus_mode")
        val haptics = booleanPreferencesKey("haptics")
        val sound = booleanPreferencesKey("sound")
        val confetti = booleanPreferencesKey("confetti")
        val calm = booleanPreferencesKey("calm")
        val textScale = floatPreferencesKey("text_scale")
        val theme = stringPreferencesKey("theme")
        val activePlan = stringPreferencesKey("active_plan")
    }

    val settings: Flow<Settings> = context.dataStore.data.map { read(it) }

    suspend fun update(transform: (Settings) -> Settings) {
        context.dataStore.edit { p ->
            val cur = read(p)
            val n = transform(cur)
            p[K.focus] = n.focusMode
            p[K.haptics] = n.haptics
            p[K.sound] = n.sound
            p[K.confetti] = n.confetti
            p[K.calm] = n.calm
            p[K.textScale] = n.textScale
            p[K.theme] = n.theme.name
            p[K.activePlan] = n.activePlan
        }
    }

    private fun read(p: Preferences): Settings {
        val d = Settings()
        return Settings(
            focusMode = p[K.focus] ?: d.focusMode,
            haptics = p[K.haptics] ?: d.haptics,
            sound = p[K.sound] ?: d.sound,
            confetti = p[K.confetti] ?: d.confetti,
            calm = p[K.calm] ?: d.calm,
            textScale = p[K.textScale] ?: d.textScale,
            theme = p[K.theme]?.let { runCatching { ThemeMode.valueOf(it) }.getOrNull() } ?: d.theme,
            activePlan = p[K.activePlan] ?: d.activePlan,
        )
    }
}
