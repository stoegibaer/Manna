package dev.tobi.manna

import android.app.Application
import dev.tobi.manna.data.bible.AssetTextProvider
import dev.tobi.manna.data.bible.TextProvider
import dev.tobi.manna.data.plan.PlanRepository
import dev.tobi.manna.data.progress.MannaDb
import dev.tobi.manna.data.progress.ProgressRepository
import dev.tobi.manna.data.settings.SettingsRepository
import dev.tobi.manna.reminder.Dnd
import dev.tobi.manna.reminder.Reminders
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.SupervisorJob
import kotlinx.coroutines.launch

class AppContainer(private val app: Application) {
    val text: TextProvider = AssetTextProvider(app)
    val plans = PlanRepository(app)
    val progress = ProgressRepository(MannaDb.create(app).progress())
    val settings = SettingsRepository(app)
    /** Lives as long as the process – for small fire-and-forget jobs like rescheduling. */
    val scope = CoroutineScope(SupervisorJob() + Dispatchers.IO)

    /** Call whenever something was read or reminder settings changed. */
    fun rescheduleReminders() {
        scope.launch { Reminders.reschedule(app, this@AppContainer) }
    }

    suspend fun logReading(verses: Int, sections: Int) {
        progress.logReading(verses, sections)
        Reminders.reschedule(app, this)
    }
}

class MannaApp : Application() {
    lateinit var container: AppContainer
        private set

    override fun onCreate() {
        super.onCreate()
        container = AppContainer(this)
        Reminders.ensureChannel(this)
        container.scope.launch {
            container.progress.migrate()
            Dnd.end(this@MannaApp, container) // restore DND if the app died while reading
            Reminders.reschedule(this@MannaApp, container)
        }
    }
}
