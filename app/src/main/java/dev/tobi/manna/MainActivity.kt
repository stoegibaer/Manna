package dev.tobi.manna

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import dev.tobi.manna.data.settings.Settings
import dev.tobi.manna.reminder.Dnd
import dev.tobi.manna.reminder.Reminders
import dev.tobi.manna.ui.album.AlbumScreen
import dev.tobi.manna.ui.bible.BibleViewModel
import dev.tobi.manna.ui.bible.BooksScreen
import dev.tobi.manna.ui.bible.ChapterScreen
import dev.tobi.manna.ui.bible.ChaptersScreen
import dev.tobi.manna.ui.album.AlbumViewModel
import dev.tobi.manna.ui.components.LocalFeedback
import dev.tobi.manna.ui.components.rememberFeedback
import dev.tobi.manna.ui.home.HomeScreen
import dev.tobi.manna.ui.home.HomeViewModel
import dev.tobi.manna.ui.plans.PlansScreen
import dev.tobi.manna.ui.plans.PlansViewModel
import dev.tobi.manna.ui.quick.AnswerScreen
import dev.tobi.manna.ui.quick.AnswerViewModel
import dev.tobi.manna.ui.quick.VerseScreen
import dev.tobi.manna.ui.quick.VerseViewModel
import dev.tobi.manna.ui.session.SessionScreen
import dev.tobi.manna.ui.session.SessionViewModel
import dev.tobi.manna.ui.settings.ReminderSetupScreen
import dev.tobi.manna.ui.settings.SettingsScreen
import dev.tobi.manna.ui.theme.MannaTheme
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    /** Route requested by a notification tap, consumed once by the NavHost. */
    private val pendingRoute = MutableStateFlow<String?>(null)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        val c = (application as MannaApp).container
        // Debug-only: `adb shell am start -n dev.tobi.manna/.MainActivity --ei debugTree 40` previews the tree at 40 sections.
        val debuggable = (applicationInfo.flags and android.content.pm.ApplicationInfo.FLAG_DEBUGGABLE) != 0
        val debugTree = if (debuggable) intent.getIntExtra("debugTree", -1) else -1
        if (savedInstanceState == null) pendingRoute.value = routeFor(intent)
        // Debug-only: `--ei debugReminder 1` shows the quiz reminder, `2` the teaser reminder (for testing the notifications).
        if (debuggable && intent.hasExtra("debugReminder")) {
            val n = intent.getIntExtra("debugReminder", 1)
            // `--es debugQuiz plan/section/index` forces a specific review question
            val forced = intent.getStringExtra("debugQuiz")?.split("/")
            c.scope.launch {
                val pick = forced?.let { (p, sec, i) ->
                    c.plans.plan(p).sections.firstOrNull { it.id == sec }?.quiz?.getOrNull(i.toInt())?.let { Reminders.ReviewPick(p, sec, i.toInt(), it) }
                }
                Reminders.show(this@MainActivity, c, n, isLast = true, anyReview = true, forced = pick)
            }
        }

        setContent {
            val settings by c.settings.settings.collectAsStateWithLifecycle(initialValue = Settings())
            val scope = rememberCoroutineScope()
            val route by pendingRoute.collectAsStateWithLifecycle()
            MannaTheme(settings.theme) {
                CompositionLocalProvider(LocalFeedback provides rememberFeedback(settings)) {
                    Surface(Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
                        val nav = rememberNavController()
                        LaunchedEffect(route) {
                            route?.let { r -> nav.navigate(r) { popUpTo("home") }; pendingRoute.value = null }
                        }
                        val home: () -> Unit = { if (!nav.popBackStack("home", inclusive = false)) nav.navigate("home") }
                        NavHost(nav, startDestination = "home") {
                            composable("home") {
                                val vm: HomeViewModel = viewModel(factory = viewModelFactory { initializer { HomeViewModel(c) } })
                                HomeScreen(
                                    vm, settings, debugTree = debugTree,
                                    onStart = { nav.navigate("session") },
                                    onStartMore = { nav.navigate("session?more=true") },
                                    onOneVerse = { nav.navigate("verse") },
                                    onSettings = { nav.navigate("settings") },
                                    onPlans = { nav.navigate("plans") },
                                    onAlbum = { nav.navigate("album") },
                                    onReminders = { nav.navigate("reminders") },
                                )
                            }
                            composable(
                                "session?more={more}",
                                arguments = listOf(navArgument("more") { type = NavType.BoolType; defaultValue = false }),
                            ) { entry ->
                                val more = entry.arguments?.getBoolean("more") == true
                                val vm: SessionViewModel = viewModel(factory = viewModelFactory { initializer { SessionViewModel(c, more) } })
                                DndWhileReading(c)
                                SessionScreen(vm, settings, onClose = home, onChoosePlan = { nav.navigate("plans") { popUpTo("home") } })
                            }
                            composable("verse") {
                                val vm: VerseViewModel = viewModel(factory = viewModelFactory { initializer { VerseViewModel(c) } })
                                VerseScreen(vm, settings, onMore = { nav.navigate("session") { popUpTo("home") } }, onClose = home, onPlans = { nav.navigate("plans") { popUpTo("home") } })
                            }
                            composable(
                                "answer/{plan}/{section}/{quiz}/{answer}",
                                arguments = listOf(
                                    navArgument("plan") { type = NavType.StringType },
                                    navArgument("section") { type = NavType.StringType },
                                    navArgument("quiz") { type = NavType.IntType },
                                    navArgument("answer") { type = NavType.IntType },
                                ),
                            ) { entry ->
                                val a = entry.arguments!!
                                val vm: AnswerViewModel = viewModel(factory = viewModelFactory {
                                    initializer { AnswerViewModel(c, a.getString("plan")!!, a.getString("section")!!, a.getInt("quiz"), a.getInt("answer")) }
                                })
                                AnswerScreen(
                                    vm, settings,
                                    onRead = { nav.navigate("session") { popUpTo("home") } },
                                    onVerse = { nav.navigate("verse") { popUpTo("home") } },
                                    onClose = home,
                                )
                            }
                            composable("plans") {
                                val vm: PlansViewModel = viewModel(factory = viewModelFactory { initializer { PlansViewModel(c) } })
                                PlansScreen(vm, onChosen = { id -> scope.launch { vm.choose(id); home() } }, onBible = { nav.navigate("bible") }, onBack = { nav.popBackStack() })
                            }
                            composable("bible") {
                                val vm: BibleViewModel = viewModel(factory = viewModelFactory { initializer { BibleViewModel(c) } })
                                BooksScreen(vm, onBook = { nav.navigate("bible/$it") }, onBack = { nav.popBackStack() })
                            }
                            composable("bible/{book}", arguments = listOf(navArgument("book") { type = NavType.IntType })) { e ->
                                val vm: BibleViewModel = viewModel(factory = viewModelFactory { initializer { BibleViewModel(c) } })
                                val book = e.arguments!!.getInt("book")
                                ChaptersScreen(vm, book, onChapter = { nav.navigate("bible/$book/$it") }, onBack = { nav.popBackStack() })
                            }
                            composable(
                                "bible/{book}/{chapter}",
                                arguments = listOf(navArgument("book") { type = NavType.IntType }, navArgument("chapter") { type = NavType.IntType }),
                            ) { e ->
                                val vm: BibleViewModel = viewModel(factory = viewModelFactory { initializer { BibleViewModel(c) } })
                                val book = e.arguments!!.getInt("book")
                                ChapterScreen(
                                    vm, settings, book, e.arguments!!.getInt("chapter"),
                                    onChapter = { ch -> nav.navigate("bible/$book/$ch") { popUpTo("bible/$book") } },
                                    onBack = { nav.popBackStack() },
                                )
                            }
                            composable("album") {
                                val vm: AlbumViewModel = viewModel(factory = viewModelFactory { initializer { AlbumViewModel(c) } })
                                AlbumScreen(vm, onBack = { nav.popBackStack() })
                            }
                            composable("settings") {
                                SettingsScreen(
                                    settings,
                                    onChange = { f -> scope.launch { c.settings.update(f) } },
                                    onReminders = { nav.navigate("reminders") },
                                    onBack = { nav.popBackStack() },
                                )
                            }
                            composable("reminders") {
                                ReminderSetupScreen(
                                    settings,
                                    onSave = { f -> scope.launch { c.settings.update(f); c.rescheduleReminders() } },
                                    onBack = { nav.popBackStack() },
                                )
                            }
                        }
                    }
                }
            }
        }
    }

    override fun onNewIntent(intent: Intent) {
        super.onNewIntent(intent)
        routeFor(intent)?.let { pendingRoute.value = it }
    }

    override fun onResume() {
        super.onResume()
        // something may have been read via another path – plan the next reminder accordingly
        (application as MannaApp).container.rescheduleReminders()
    }

    private fun routeFor(intent: Intent?): String? = when (intent?.getStringExtra(Reminders.EXTRA_TARGET)) {
        "session" -> "session"
        "verse" -> "verse"
        "review" -> {
            Reminders.cancelNotification(this)
            "answer/${intent.getStringExtra(Reminders.EXTRA_PLAN)}/${intent.getStringExtra(Reminders.EXTRA_SECTION)}/" +
                "${intent.getIntExtra(Reminders.EXTRA_QUIZ, 0)}/${intent.getIntExtra(Reminders.EXTRA_ANSWER, -1)}"
        }
        else -> null
    }.also { if (it != null) Reminders.cancelNotification(this) }
}

/** „Nicht stören“ for as long as the reading screen is visible (if the user enabled it). */
@androidx.compose.runtime.Composable
private fun DndWhileReading(c: AppContainer) {
    val context = LocalContext.current
    DisposableEffect(Unit) {
        c.scope.launch { Dnd.begin(context.applicationContext, c) }
        onDispose { c.scope.launch { Dnd.end(context.applicationContext, c) } }
    }
}
