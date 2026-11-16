package dev.tobi.manna.ui.settings

import kotlin.math.roundToInt
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowBack
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SegmentedButton
import androidx.compose.material3.SegmentedButtonDefaults
import androidx.compose.material3.SingleChoiceSegmentedButtonRow
import androidx.compose.material3.Slider
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import dev.tobi.manna.data.settings.Settings
import dev.tobi.manna.data.settings.ThemeMode
import dev.tobi.manna.ui.theme.bibleTextStyle

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(settings: Settings, onChange: ((Settings) -> Settings) -> Unit, onReminders: () -> Unit, onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Einstellungen") },
                navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Rounded.ArrowBack, "Zurück") } },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.background),
            )
        },
        containerColor = MaterialTheme.colorScheme.background,
    ) { pad ->
        Column(
            Modifier.fillMaxSize().padding(pad).verticalScroll(rememberScrollState()).padding(horizontal = 24.dp),
            verticalArrangement = Arrangement.spacedBy(4.dp),
        ) {
            Group("Gewohnheit")
            androidx.compose.material3.Surface(
                onClick = onReminders,
                shape = androidx.compose.foundation.shape.RoundedCornerShape(14.dp),
                color = MaterialTheme.colorScheme.surfaceContainer,
                modifier = Modifier.fillMaxWidth(),
            ) {
                Column(Modifier.padding(16.dp)) {
                    Text("Erinnerungen & Wochenziel", style = MaterialTheme.typography.titleMedium)
                    Text(
                        if (settings.remindersOn) "An – ab ${formatMinute(settings.anchorMinute)} Uhr, Ziel ${settings.weeklyGoal} Tage pro Woche"
                        else "Aus – Ziel ${settings.weeklyGoal} Tage pro Woche",
                        style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            }

            Group("Lesen")
            Toggle("Fokusmodus", "Immer nur ein Vers ist hell – tippen zum Weiterlesen.", settings.focusMode) { v -> onChange { it.copy(focusMode = v) } }
            Text("Textgröße", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(top = 12.dp))
            Slider(value = settings.textScale, onValueChange = { v -> onChange { it.copy(textScale = v) } }, valueRange = 0.8f..1.6f, steps = 7)
            Text("Der Gerechte aber wird durch seinen Glauben leben.", style = bibleTextStyle(settings.textScale))

            Text("Vorlese-Tempo", style = MaterialTheme.typography.titleMedium, modifier = Modifier.padding(top = 12.dp))
            Slider(value = settings.ttsRate, onValueChange = { v -> onChange { it.copy(ttsRate = (v * 10).roundToInt() / 10f) } }, valueRange = 0.7f..1.4f, steps = 6)
            Text(
                when {
                    settings.ttsRate < 0.95f -> "Etwas langsamer"
                    settings.ttsRate > 1.05f -> "Etwas schneller"
                    else -> "Normal"
                },
                style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant,
            )

            Group("Rückmeldung")
            Toggle("Ruhiger Modus", "Keine Animationen, kein Konfetti, keine Töne.", settings.calm) { v -> onChange { it.copy(calm = v) } }
            Toggle("Vibration", null, settings.haptics) { v -> onChange { it.copy(haptics = v) } }
            Toggle("Töne", null, settings.sound, enabled = !settings.calm) { v -> onChange { it.copy(sound = v) } }
            Toggle("Konfetti", null, settings.confetti, enabled = !settings.calm) { v -> onChange { it.copy(confetti = v) } }

            Group("Darstellung")
            SingleChoiceSegmentedButtonRow(Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
                val modes = listOf(ThemeMode.SYSTEM to "System", ThemeMode.LIGHT to "Hell", ThemeMode.DARK to "Dunkel")
                modes.forEachIndexed { i, (mode, label) ->
                    SegmentedButton(
                        selected = settings.theme == mode,
                        onClick = { onChange { it.copy(theme = mode) } },
                        shape = SegmentedButtonDefaults.itemShape(i, modes.size),
                    ) { Text(label) }
                }
            }

            HorizontalDivider(Modifier.padding(vertical = 16.dp))
            Text(
                "Bibeltext: Elberfelder Übersetzung, Edition bibelkommentare.de. © 2019 Verbreitung des christlichen Glaubens e.V., lizenziert unter CC BY-NC-ND 4.0. Karte: Natural Earth (gemeinfrei).",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(bottom = 32.dp),
            )
        }
    }
}

@Composable
private fun Group(title: String) {
    Text(title, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(top = 20.dp, bottom = 4.dp))
}

@Composable
private fun Toggle(title: String, subtitle: String?, checked: Boolean, enabled: Boolean = true, onChange: (Boolean) -> Unit) {
    Row(Modifier.fillMaxWidth().padding(vertical = 8.dp), verticalAlignment = Alignment.CenterVertically) {
        Column(Modifier.weight(1f).padding(end = 12.dp)) {
            Text(title, style = MaterialTheme.typography.titleMedium, color = if (enabled) MaterialTheme.colorScheme.onSurface else MaterialTheme.colorScheme.onSurfaceVariant)
            subtitle?.let { Text(it, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant) }
        }
        Switch(checked = checked, onCheckedChange = onChange, enabled = enabled)
    }
}
