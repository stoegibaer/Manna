package dev.tobi.manna.data.settings

import android.content.Context
import androidx.datastore.preferences.core.MutablePreferences
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.floatPreferencesKey
import androidx.datastore.preferences.core.intPreferencesKey
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.flow.map

enum class ThemeMode { SYSTEM, LIGHT, DARK }

data class Settings(
    // reading & feedback
    val focusMode: Boolean = true,
    val haptics: Boolean = true,
    val sound: Boolean = true,
    val confetti: Boolean = true,
    val calm: Boolean = false,
    val textScale: Float = 1f,
    val theme: ThemeMode = ThemeMode.SYSTEM,
    /** Read-aloud speed (0.7–1.4). */
    val ttsRate: Float = 1f,
    /** Empty = not chosen yet; resolved via PlanIndex.resolve(). */
    val activePlan: String = "",

    // reminders & habit
    val remindersOn: Boolean = false,
    /** True once the user went through the reminder setup or dismissed the invitation. */
    val reminderSetupSeen: Boolean = false,
    /** „Nach dem ___ lese ich“ */
    val anchorText: String = "",
    /** Minute of the day of the anchor (first reminder). */
    val anchorMinute: Int = 7 * 60 + 30,
    /** „Wenn ich es verpasse, dann ___“ */
    val planB: String = "",
    /** No reminders after this minute of the day. */
    val quietMinute: Int = 22 * 60,
    /** Reading days per week (1–7). */
    val weeklyGoal: Int = 4,
    /** ISO date on which the user chose „Heute aussetzen“. */
    val pausedDate: String = "",
    /** ISO date until which the reminder-time suggestion stays hidden. */
    val suggestionHiddenUntil: String = "",
    /** Mute notifications (Do not disturb) while reading. */
    val dndWhileReading: Boolean = false,
    /** ISO date of today's energy answer and the answer itself: low | normal | high. */
    val energyDate: String = "",
    val energy: String = "normal",
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
        val ttsRate = floatPreferencesKey("tts_rate")
        val activePlan = stringPreferencesKey("active_plan")
        val remindersOn = booleanPreferencesKey("reminders_on")
        val reminderSetupSeen = booleanPreferencesKey("reminder_setup_seen")
        val anchorText = stringPreferencesKey("anchor_text")
        val anchorMinute = intPreferencesKey("anchor_minute")
        val planB = stringPreferencesKey("plan_b")
        val quietMinute = intPreferencesKey("quiet_minute")
        val weeklyGoal = intPreferencesKey("weekly_goal")
        val pausedDate = stringPreferencesKey("paused_date")
        val suggestionHiddenUntil = stringPreferencesKey("suggestion_hidden_until")
        val dnd = booleanPreferencesKey("dnd_while_reading")
        val energyDate = stringPreferencesKey("energy_date")
        val energy = stringPreferencesKey("energy")
        // internal state, not part of Settings
        val dndRestore = intPreferencesKey("dnd_restore_filter")
        val reminderDate = stringPreferencesKey("reminder_last_date")
        val reminderCount = intPreferencesKey("reminder_count_today")
    }

    val settings: Flow<Settings> = context.dataStore.data.map { read(it) }

    suspend fun current(): Settings = settings.first()

    suspend fun update(transform: (Settings) -> Settings) {
        context.dataStore.edit { p -> write(p, transform(read(p))) }
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
            ttsRate = p[K.ttsRate] ?: d.ttsRate,
            activePlan = p[K.activePlan] ?: d.activePlan,
            remindersOn = p[K.remindersOn] ?: d.remindersOn,
            reminderSetupSeen = p[K.reminderSetupSeen] ?: d.reminderSetupSeen,
            anchorText = p[K.anchorText] ?: d.anchorText,
            anchorMinute = p[K.anchorMinute] ?: d.anchorMinute,
            planB = p[K.planB] ?: d.planB,
            quietMinute = p[K.quietMinute] ?: d.quietMinute,
            weeklyGoal = p[K.weeklyGoal] ?: d.weeklyGoal,
            pausedDate = p[K.pausedDate] ?: d.pausedDate,
            suggestionHiddenUntil = p[K.suggestionHiddenUntil] ?: d.suggestionHiddenUntil,
            dndWhileReading = p[K.dnd] ?: d.dndWhileReading,
            energyDate = p[K.energyDate] ?: d.energyDate,
            energy = p[K.energy] ?: d.energy,
        )
    }

    private fun write(p: MutablePreferences, n: Settings) {
        p[K.focus] = n.focusMode
        p[K.haptics] = n.haptics
        p[K.sound] = n.sound
        p[K.confetti] = n.confetti
        p[K.calm] = n.calm
        p[K.textScale] = n.textScale
        p[K.theme] = n.theme.name
        p[K.ttsRate] = n.ttsRate
        p[K.activePlan] = n.activePlan
        p[K.remindersOn] = n.remindersOn
        p[K.reminderSetupSeen] = n.reminderSetupSeen
        p[K.anchorText] = n.anchorText
        p[K.anchorMinute] = n.anchorMinute
        p[K.planB] = n.planB
        p[K.quietMinute] = n.quietMinute
        p[K.weeklyGoal] = n.weeklyGoal
        p[K.pausedDate] = n.pausedDate
        p[K.suggestionHiddenUntil] = n.suggestionHiddenUntil
        p[K.dnd] = n.dndWhileReading
        p[K.energyDate] = n.energyDate
        p[K.energy] = n.energy
    }

    // ── internal state ──

    /** Interruption filter to restore after reading, or null if nothing to restore. */
    suspend fun dndRestore(): Int? = context.dataStore.data.first()[K.dndRestore]?.takeIf { it >= 0 }
    suspend fun setDndRestore(filter: Int?) = context.dataStore.edit { it[K.dndRestore] = filter ?: -1 }

    /** Counts reminders per day so the first one can be the quiz and later ones the teaser. */
    suspend fun nextReminderNumber(today: String): Int {
        var n = 0
        context.dataStore.edit { p ->
            n = if (p[K.reminderDate] == today) (p[K.reminderCount] ?: 0) + 1 else 1
            p[K.reminderDate] = today
            p[K.reminderCount] = n
        }
        return n
    }
}
