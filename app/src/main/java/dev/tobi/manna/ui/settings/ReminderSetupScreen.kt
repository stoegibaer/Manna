package dev.tobi.manna.ui.settings

import kotlin.math.roundToInt
import android.Manifest
import android.content.pm.PackageManager
import android.os.Build
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.rounded.ArrowBack
import androidx.compose.material.icons.outlined.Schedule
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Slider
import androidx.compose.material3.Surface
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TimePicker
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.rememberTimePickerState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.core.content.ContextCompat
import dev.tobi.manna.data.settings.Settings
import dev.tobi.manna.reminder.Dnd
import java.time.LocalDate

fun formatMinute(m: Int) = "%d:%02d".format(m / 60, m % 60)

private val ANCHORS = listOf(
    "dem Aufstehen" to 7 * 60,
    "dem ersten Kaffee" to 7 * 60 + 30,
    "dem Frühstück" to 8 * 60,
    "der Mittagspause" to 12 * 60 + 30,
    "dem Heimkommen" to 17 * 60 + 30,
    "dem Abendessen" to 19 * 60,
    "dem Zähneputzen am Abend" to 21 * 60 + 30,
)

private val PLAN_B = listOf("vor dem Schlafengehen", "direkt nach dem Abendessen", "bevor ich das Handy weglege")

/**
 * „Nach dem ___ lese ich einen Vers.“ – the if-then plan, the time of the first reminder,
 * a plan B with its time (the last reminder of the day) and the weekly goal. Everything optional and changeable later.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReminderSetupScreen(settings: Settings, onSave: ((Settings) -> Settings) -> Unit, onBack: () -> Unit) {
    val context = LocalContext.current
    var on by rememberSaveable { mutableStateOf(settings.remindersOn || !settings.reminderSetupSeen) }
    var anchor by rememberSaveable { mutableStateOf(settings.anchorText.ifBlank { "dem ersten Kaffee" }) }
    var anchorMinute by rememberSaveable { mutableIntStateOf(settings.anchorMinute) }
    var planB by rememberSaveable { mutableStateOf(settings.planB) }
    var quiet by rememberSaveable { mutableIntStateOf(settings.quietMinute) }
    var goal by rememberSaveable { mutableIntStateOf(settings.weeklyGoal) }
    var dnd by rememberSaveable { mutableStateOf(settings.dndWhileReading) }
    var pickTime by remember { mutableStateOf<String?>(null) } // "anchor" | "quiet"

    val save: () -> Unit = {
        onSave {
            it.copy(
                remindersOn = on, reminderSetupSeen = true, anchorText = anchor.trim(), anchorMinute = anchorMinute,
                planB = planB.trim(), quietMinute = quiet, weeklyGoal = goal, dndWhileReading = dnd,
            )
        }
        onBack()
    }
    val permission = rememberLauncherForActivityResult(ActivityResultContracts.RequestPermission()) { save() }
    val needsPermission = Build.VERSION.SDK_INT >= 33 &&
        ContextCompat.checkSelfPermission(context, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Erinnerungen") },
                navigationIcon = { IconButton(onClick = onBack) { Icon(Icons.AutoMirrored.Rounded.ArrowBack, "Zurück") } },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.background),
            )
        },
        containerColor = MaterialTheme.colorScheme.background,
    ) { pad ->
        Column(
            Modifier.fillMaxSize().padding(pad).verticalScroll(rememberScrollState()).padding(horizontal = 24.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Text(
                "Ein Vers am Tag reicht. Verknüpf das Lesen mit etwas, das du sowieso jeden Tag tust – dann vergisst man es seltener.",
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )

            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                Text("Erinnerungen", style = MaterialTheme.typography.titleMedium, modifier = Modifier.weight(1f))
                Switch(checked = on, onCheckedChange = { on = it })
            }

            Section("Nach …")
            FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                ANCHORS.forEach { (label, minute) ->
                    FilterChip(
                        selected = anchor == label,
                        onClick = { anchor = label; anchorMinute = minute },
                        label = { Text(label) },
                    )
                }
            }
            OutlinedTextField(
                value = anchor, onValueChange = { anchor = it }, singleLine = true,
                label = { Text("oder eigener Anker") }, modifier = Modifier.fillMaxWidth(),
            )
            TimeRow("Ungefähr um", anchorMinute) { pickTime = "anchor" }

            Section("Plan B – wenn ich es verpasse, dann …")
            FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                PLAN_B.forEach { label ->
                    FilterChip(selected = planB == label, onClick = { planB = if (planB == label) "" else label }, label = { Text(label) })
                }
            }
            OutlinedTextField(value = planB, onValueChange = { planB = it }, singleLine = true, label = { Text("oder eigener Plan B") }, modifier = Modifier.fillMaxWidth())
            TimeRow("Plan B um", quiet) { pickTime = "quiet" }
            Text("Zu dieser Zeit kommt die letzte Erinnerung des Tages – danach ist Ruhe.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)

            // the if-then sentence – said out loud it sticks better
            Surface(color = MaterialTheme.colorScheme.primaryContainer, shape = RoundedCornerShape(16.dp), modifier = Modifier.fillMaxWidth().padding(top = 4.dp)) {
                Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                    Text("Nach ${anchor.ifBlank { "…" }} lese ich einen Vers.", fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onPrimaryContainer)
                    if (planB.isNotBlank()) Text("Wenn ich es verpasse, dann $planB.", color = MaterialTheme.colorScheme.onPrimaryContainer)
                    Text(
                        if (on) "Ab ${formatMinute(anchorMinute)} Uhr erinnert dich Manna stündlich, bis du gelesen hast. Um ${formatMinute(quiet)} Uhr kommt dein Plan B, danach ist Ruhe."
                        else "Ohne Erinnerungen – nur dein Plan.",
                        style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onPrimaryContainer,
                    )
                }
            }

            Section("Wochenziel")
            Text(if (goal == 7) "Jeden Tag" else "$goal von 7 Tagen", style = MaterialTheme.typography.titleMedium)
            Slider(value = goal.toFloat(), onValueChange = { goal = it.roundToInt() }, valueRange = 1f..7f, steps = 5)
            Text("Verpasste Tage zählen nicht gegen dich – jede Woche fängt neu an.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)

            Section("Beim Lesen")
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth()) {
                Column(Modifier.weight(1f).padding(end = 12.dp)) {
                    Text("Nicht stören", style = MaterialTheme.typography.titleMedium)
                    Text("Benachrichtigungen stumm, solange du liest. Danach wieder wie vorher.", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                Switch(checked = dnd, onCheckedChange = { v ->
                    dnd = v
                    if (v && !Dnd.hasAccess(context)) context.startActivity(Dnd.accessSettingsIntent())
                })
            }
            if (dnd && !Dnd.hasAccess(context)) {
                Text("Bitte erlaube Manna in den Systemeinstellungen den Zugriff auf „Nicht stören“.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.error)
            }

            if (settings.remindersOn && settings.pausedDate != LocalDate.now().toString()) {
                HorizontalDivider(Modifier.padding(vertical = 8.dp))
                OutlinedButton(onClick = { onSave { it.copy(pausedDate = LocalDate.now().toString()) }; onBack() }, modifier = Modifier.fillMaxWidth()) {
                    Text("Heute bewusst aussetzen")
                }
                Text("Für heute keine Erinnerungen mehr – ohne schlechtes Gewissen. Morgen geht’s normal weiter.", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            }

            Spacer(Modifier.height(8.dp))
            Button(
                onClick = { if (on && needsPermission) permission.launch(Manifest.permission.POST_NOTIFICATIONS) else save() },
                modifier = Modifier.fillMaxWidth().height(56.dp),
            ) { Text("Speichern", style = MaterialTheme.typography.titleMedium) }
            Spacer(Modifier.height(24.dp))
        }
    }

    pickTime?.let { which ->
        val initial = if (which == "anchor") anchorMinute else quiet
        val state = rememberTimePickerState(initial / 60, initial % 60, is24Hour = true)
        AlertDialog(
            onDismissRequest = { pickTime = null },
            confirmButton = {
                TextButton(onClick = {
                    val m = state.hour * 60 + state.minute
                    if (which == "anchor") anchorMinute = m else quiet = m
                    pickTime = null
                }) { Text("OK") }
            },
            dismissButton = { TextButton(onClick = { pickTime = null }) { Text("Abbrechen") } },
            text = { TimePicker(state = state) },
        )
    }
}

@Composable
private fun Section(title: String) {
    Text(title, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary, modifier = Modifier.padding(top = 12.dp))
}

@Composable
private fun TimeRow(label: String, minute: Int, onClick: () -> Unit) {
    Surface(onClick = onClick, shape = RoundedCornerShape(14.dp), color = MaterialTheme.colorScheme.surfaceContainer, modifier = Modifier.fillMaxWidth()) {
        Row(Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
            Icon(Icons.Outlined.Schedule, null, tint = MaterialTheme.colorScheme.primary)
            Text(label, modifier = Modifier.weight(1f).padding(start = 12.dp))
            Text("${formatMinute(minute)} Uhr", style = MaterialTheme.typography.titleMedium)
        }
    }
}
