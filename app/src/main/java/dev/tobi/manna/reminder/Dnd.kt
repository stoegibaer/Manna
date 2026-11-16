package dev.tobi.manna.reminder

import android.app.NotificationManager
import android.content.Context
import android.content.Intent
import android.provider.Settings as AndroidSettings
import dev.tobi.manna.AppContainer

/**
 * Optional „Nicht stören“ while reading. Only switches it on if the user had it off,
 * and remembers that, so it is restored even if the app was killed mid-session.
 */
object Dnd {
    fun hasAccess(context: Context) = context.getSystemService(NotificationManager::class.java).isNotificationPolicyAccessGranted

    fun accessSettingsIntent() = Intent(AndroidSettings.ACTION_NOTIFICATION_POLICY_ACCESS_SETTINGS).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)

    suspend fun begin(context: Context, c: AppContainer) {
        if (!c.settings.current().dndWhileReading || !hasAccess(context)) return
        val nm = context.getSystemService(NotificationManager::class.java)
        val current = nm.currentInterruptionFilter
        if (current != NotificationManager.INTERRUPTION_FILTER_ALL) return // user already uses DND – leave it alone
        c.settings.setDndRestore(current)
        nm.setInterruptionFilter(NotificationManager.INTERRUPTION_FILTER_PRIORITY)
    }

    suspend fun end(context: Context, c: AppContainer) {
        val restore = c.settings.dndRestore() ?: return
        if (hasAccess(context)) context.getSystemService(NotificationManager::class.java).setInterruptionFilter(restore)
        c.settings.setDndRestore(null)
    }
}
