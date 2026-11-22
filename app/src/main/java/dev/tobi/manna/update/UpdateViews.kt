package dev.tobi.manna.update

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp

/** True if the state is worth a card on the home screen (an update is there or on its way). */
fun UpdateState.showOnHome() = this is UpdateState.Available || this is UpdateState.NeedsPermission ||
    this is UpdateState.Downloading || this is UpdateState.Installing || (this is UpdateState.Failed && release != null)

/**
 * Card for an available update, in the style of the home hints. [onLater] hides it (home screen only).
 * [showNotes] shows what is new (settings); on the home screen it stays short.
 */
@Composable
fun UpdateCard(state: UpdateState, updater: Updater, onLater: (() -> Unit)? = null, showNotes: Boolean = false, modifier: Modifier = Modifier) {
    val context = LocalContext.current
    val fg = MaterialTheme.colorScheme.onSecondaryContainer
    Surface(color = MaterialTheme.colorScheme.secondaryContainer, shape = RoundedCornerShape(20.dp), modifier = modifier.fillMaxWidth()) {
        Column(Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            val release = when (state) {
                is UpdateState.Available -> state.release
                is UpdateState.NeedsPermission -> state.release
                is UpdateState.Downloading -> state.release
                is UpdateState.Installing -> state.release
                is UpdateState.Failed -> state.release
                else -> null
            } ?: return@Column
            Text("Neue Version ${release.version} ist da", style = MaterialTheme.typography.titleMedium, color = fg)
            val text = when (state) {
                is UpdateState.NeedsPermission ->
                    "Erlaube Manna einmal, Apps zu installieren: Schalter „Dieser Quelle vertrauen“ (oder ähnlich) antippen, dann zurück."
                is UpdateState.Downloading -> "Wird geladen … ${(state.progress * 100).toInt()} %"
                is UpdateState.Installing ->
                    "Bitte bestätige mit „Aktualisieren“. Fragt Play Protect nach einem Scan und es geht nicht weiter: dort „Nicht installieren“ wählen und hier neu starten."
                is UpdateState.Failed -> state.message
                is UpdateState.Available -> if (state.ready) "Schon geladen – ein Tippen installiert es. Dein Fortschritt bleibt erhalten."
                    else "Ein Tippen genügt. Dein Fortschritt und deine Einstellungen bleiben erhalten."
                else -> ""
            }
            Text(text, style = MaterialTheme.typography.bodyMedium, color = fg)
            if (state is UpdateState.Downloading) {
                LinearProgressIndicator(progress = { state.progress }, modifier = Modifier.fillMaxWidth().padding(vertical = 6.dp))
            }
            if (showNotes && release.notes.isNotBlank() && state is UpdateState.Available) {
                Text(
                    release.notes, style = MaterialTheme.typography.bodySmall, color = fg.copy(alpha = 0.85f),
                    maxLines = 12, overflow = TextOverflow.Ellipsis, modifier = Modifier.padding(top = 6.dp),
                )
            }
            val (label, action) = when (state) {
                is UpdateState.NeedsPermission -> "Erlauben" to { context.startActivity(updater.permissionIntent()) }
                is UpdateState.Available -> (if (state.ready) "Installieren" else "Aktualisieren") to { updater.install(release) }
                is UpdateState.Installing -> "Neu starten" to { updater.install(release) }
                is UpdateState.Failed -> "Noch mal" to { updater.install(release) }
                else -> null to {}
            }
            if (label != null || onLater != null) {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.End) {
                    val idle = state !is UpdateState.Downloading && state !is UpdateState.Installing
                    if (onLater != null && idle) TextButton(onClick = onLater) { Text("Später", color = fg.copy(alpha = 0.75f)) }
                    if (label != null) TextButton(onClick = action) { Text(label, color = fg, fontWeight = FontWeight.Bold) }
                }
            }
        }
    }
}
