package dev.tobi.manna

import android.app.Application
import kotlinx.coroutines.launch
import dev.tobi.manna.data.bible.AssetTextProvider
import dev.tobi.manna.data.bible.TextProvider
import dev.tobi.manna.data.plan.PlanRepository
import dev.tobi.manna.data.progress.MannaDb
import dev.tobi.manna.data.progress.ProgressRepository
import dev.tobi.manna.data.settings.SettingsRepository

class AppContainer(app: Application) {
    val text: TextProvider = AssetTextProvider(app)
    val plans = PlanRepository(app)
    val progress = ProgressRepository(MannaDb.create(app).progress())
    val settings = SettingsRepository(app)
}

class MannaApp : Application() {
    lateinit var container: AppContainer
        private set

    override fun onCreate() {
        super.onCreate()
        container = AppContainer(this)
        kotlinx.coroutines.CoroutineScope(kotlinx.coroutines.Dispatchers.IO).launch { container.progress.migrate() }
    }
}
