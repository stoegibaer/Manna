package dev.tobi.manna

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.getValue
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Modifier
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.lifecycle.viewmodel.initializer
import androidx.lifecycle.viewmodel.viewModelFactory
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import dev.tobi.manna.data.settings.Settings
import dev.tobi.manna.ui.components.LocalFeedback
import dev.tobi.manna.ui.components.rememberFeedback
import dev.tobi.manna.ui.album.AlbumScreen
import dev.tobi.manna.ui.album.AlbumViewModel
import dev.tobi.manna.ui.home.HomeScreen
import dev.tobi.manna.ui.plans.PlansScreen
import dev.tobi.manna.ui.plans.PlansViewModel
import dev.tobi.manna.ui.home.HomeViewModel
import dev.tobi.manna.ui.session.SessionScreen
import dev.tobi.manna.ui.session.SessionViewModel
import dev.tobi.manna.ui.settings.SettingsScreen
import dev.tobi.manna.ui.theme.MannaTheme
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        val c = (application as MannaApp).container
        // Debug-only: `adb shell am start -n dev.tobi.manna/.MainActivity --ei debugTree 40` previews the tree at 40 sections.
        val debuggable = (applicationInfo.flags and android.content.pm.ApplicationInfo.FLAG_DEBUGGABLE) != 0
        val debugTree = if (debuggable) intent.getIntExtra("debugTree", -1) else -1
        setContent {
            val settings by c.settings.settings.collectAsStateWithLifecycle(initialValue = Settings())
            val scope = rememberCoroutineScope()
            MannaTheme(settings.theme) {
                CompositionLocalProvider(LocalFeedback provides rememberFeedback(settings)) {
                    Surface(Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
                        val nav = rememberNavController()
                        NavHost(nav, startDestination = "home") {
                            composable("home") {
                                val vm: HomeViewModel = viewModel(factory = viewModelFactory { initializer { HomeViewModel(c) } })
                                HomeScreen(
                                    vm, settings, debugTree = debugTree,
                                    onStart = { nav.navigate("session") },
                                    onSettings = { nav.navigate("settings") },
                                    onPlans = { nav.navigate("plans") },
                                    onAlbum = { nav.navigate("album") },
                                )
                            }
                            composable("session") {
                                val vm: SessionViewModel = viewModel(factory = viewModelFactory { initializer { SessionViewModel(c) } })
                                SessionScreen(
                                    vm, settings,
                                    onClose = { nav.popBackStack("home", inclusive = false) },
                                    onChoosePlan = { nav.navigate("plans") { popUpTo("home") } },
                                )
                            }
                            composable("plans") {
                                val vm: PlansViewModel = viewModel(factory = viewModelFactory { initializer { PlansViewModel(c) } })
                                PlansScreen(vm, onChosen = { id -> scope.launch { vm.choose(id); nav.popBackStack("home", inclusive = false) } }, onBack = { nav.popBackStack() })
                            }
                            composable("album") {
                                val vm: AlbumViewModel = viewModel(factory = viewModelFactory { initializer { AlbumViewModel(c) } })
                                AlbumScreen(vm, onBack = { nav.popBackStack() })
                            }
                            composable("settings") {
                                SettingsScreen(settings, onChange = { f -> scope.launch { c.settings.update(f) } }, onBack = { nav.popBackStack() })
                            }
                        }
                    }
                }
            }
        }
    }
}
