package dev.tobi.manna.reminder

import android.Manifest
import android.app.AlarmManager
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Build
import androidx.core.app.NotificationCompat
import dev.tobi.manna.ui.session.refLabel
import androidx.core.app.NotificationManagerCompat
import androidx.core.content.ContextCompat
import dev.tobi.manna.AppContainer
import dev.tobi.manna.MainActivity
import dev.tobi.manna.MannaApp
import dev.tobi.manna.R
import dev.tobi.manna.data.plan.Quiz
import dev.tobi.manna.data.plan.resolve
import dev.tobi.manna.data.settings.Settings
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.ZoneId

/**
 * Daily minimum = 1 verse. From the anchor time on, one reminder per hour until something was read,
 * the user paused today, or the quiet time starts.
 * The first reminder of the day is a „Erinnerst du dich?“ question with answer buttons,
 * later ones show the curiosity question of the next section.
 */
object Reminders {
    const val CHANNEL = "reminders"
    private const val NOTIFICATION_ID = 1
    private const val REQ_ALARM = 100

    // intent extras understood by MainActivity
    const val EXTRA_TARGET = "target"           // "session" | "verse" | "review"
    const val EXTRA_PLAN = "plan"
    const val EXTRA_SECTION = "section"
    const val EXTRA_QUIZ = "quiz"
    const val EXTRA_ANSWER = "answer"           // option index (choice/whosaid) or 1/0 (truefalse)

    fun minuteOfDay(t: LocalDateTime) = t.hour * 60 + t.minute

    /** Next reminder time, or null if reminders are off. Pure function – easy to reason about. */
    fun nextTrigger(s: Settings, now: LocalDateTime, readToday: Boolean): LocalDateTime? {
        if (!s.remindersOn) return null
        val today = now.toLocalDate()
        val anchor = s.anchorMinute
        val quiet = if (s.quietMinute > anchor) s.quietMinute else 24 * 60 - 1
        fun at(day: LocalDate, minute: Int) = day.atStartOfDay().plusMinutes(minute.toLong())
        val tomorrow = at(today.plusDays(1), anchor)
        if (readToday || s.pausedDate == today.toString()) return tomorrow
        val m = minuteOfDay(now)
        if (m < anchor) return at(today, anchor)
        val nextSlot = anchor + ((m - anchor) / 60 + 1) * 60
        return if (nextSlot < quiet) at(today, nextSlot) else tomorrow
    }

    fun ensureChannel(context: Context) {
        val nm = context.getSystemService(NotificationManager::class.java)
        if (nm.getNotificationChannel(CHANNEL) == null) {
            nm.createNotificationChannel(
                NotificationChannel(CHANNEL, "Leseerinnerungen", NotificationManager.IMPORTANCE_DEFAULT).apply {
                    description = "Erinnert dich an deinen Vers für heute"
                }
            )
        }
    }

    private fun alarmIntent(context: Context) = PendingIntent.getBroadcast(
        context, REQ_ALARM, Intent(context, ReminderReceiver::class.java).setAction(ReminderReceiver.ACTION_FIRE),
        PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
    )

    /** (Re)plans the next alarm. Call after settings change, after reading, at app start and boot. */
    suspend fun reschedule(context: Context, c: AppContainer) {
        val s = c.settings.current()
        val am = context.getSystemService(AlarmManager::class.java)
        val pi = alarmIntent(context)
        val readToday = c.progress.readToday()
        if (readToday || s.pausedDate == LocalDate.now().toString()) cancelNotification(context)
        val next = nextTrigger(s, LocalDateTime.now(), readToday)
        if (next == null) {
            am.cancel(pi)
            cancelNotification(context)
            return
        }
        val millis = next.atZone(ZoneId.systemDefault()).toInstant().toEpochMilli()
        // a 10-minute window: precise enough for hourly reminders, needs no exact-alarm permission
        am.setWindow(AlarmManager.RTC_WAKEUP, millis, 10 * 60_000L, pi)
    }

    fun cancelNotification(context: Context) = NotificationManagerCompat.from(context).cancel(NOTIFICATION_ID)

    private fun openApp(context: Context, req: Int, extras: Intent.() -> Unit): PendingIntent {
        val i = Intent(context, MainActivity::class.java).apply {
            flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_SINGLE_TOP
            extras()
        }
        return PendingIntent.getActivity(context, req, i, PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE)
    }

    /** Builds and shows the reminder. [number] = how many reminders today including this one. */
    /** Button labels longer than this get cut off by Android. */
    const val MAX_BUTTON_CHARS = 18
    /** Answer value meaning: not answered yet – show the question with all options in the app. */
    const val ASK = -1

    suspend fun show(context: Context, c: AppContainer, number: Int, isLast: Boolean, anyReview: Boolean = false, forced: ReviewPick? = null) {
        if (Build.VERSION.SDK_INT >= 33 &&
            ContextCompat.checkSelfPermission(context, Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED
        ) return
        ensureChannel(context)
        val s = c.settings.current()
        val tapOpen = openApp(context, 1) { putExtra(EXTRA_TARGET, "session") }
        val builder = NotificationCompat.Builder(context, CHANNEL)
            .setSmallIcon(R.drawable.ic_stat_seed)
            .setContentIntent(tapOpen)
            .setAutoCancel(true)
            .setCategory(NotificationCompat.CATEGORY_REMINDER)
            .setOnlyAlertOnce(true)

        val review = forced ?: if (number == 1) pickReview(c, anyReview) else null
        if (review != null) {
            val (planId, sectionId, index, quiz) = review
            // The question was written to be asked right after reading – in a notification it needs its context:
            // passage and section title go into the title, so "hier" or "V. 5" make sense.
            val section = c.plans.plan(planId).sections.firstOrNull { it.id == sectionId }
            val books = c.text.info().books.associateBy { it.nr }
            val where = section?.let { refLabel(it.refs) { n -> books[n]?.name ?: "" } + " · " + it.title }.orEmpty()
            val question = if (quiz.type == "whosaid") "Wer hat das gesagt? „${quiz.quote}“" else quiz.q.orEmpty()
            // Only answers that fit completely on a button; otherwise one "Antworten" button that opens the question in the app.
            val buttons: List<Pair<String, Int>>? = if (quiz.type == "truefalse") {
                listOf("Stimmt" to 1, "Stimmt nicht" to 0)
            } else {
                val wrong = quiz.options.indices.filter { it != quiz.answerIndex }.shuffled().take(2)
                val pick = (wrong + quiz.answerIndex).shuffled()
                if (pick.all { quiz.options[it].length <= MAX_BUTTON_CHARS }) pick.map { quiz.options[it] to it } else null
            }
            builder.setContentTitle(where.ifBlank { "Erinnerst du dich?" })
                .setSubText("Erinnerst du dich?")
                .setContentText(question)
                .setStyle(NotificationCompat.BigTextStyle().bigText(question).setBigContentTitle(where.ifBlank { null }))
            fun answerIntent(code: Int, value: Int) = openApp(context, code) {
                putExtra(EXTRA_TARGET, "review"); putExtra(EXTRA_PLAN, planId); putExtra(EXTRA_SECTION, sectionId)
                putExtra(EXTRA_QUIZ, index); putExtra(EXTRA_ANSWER, value)
            }
            if (buttons != null) buttons.forEachIndexed { i, (label, value) -> builder.addAction(0, label, answerIntent(10 + i, value)) }
            else builder.addAction(0, "Antworten", answerIntent(13, ASK))
        } else {
            val idx = c.plans.index()
            val planId = idx.resolve(s.activePlan)
            val plan = c.plans.plan(planId)
            val done = c.progress.allSectionsDone.first()
                .filter { it.planId == planId }.map { it.sectionId }.toSet()
            val nextIdx = plan.sections.indexOfFirst { it.id !in done }
            val next = plan.sections.getOrNull(nextIdx)
            val teaser = plan.sections.getOrNull(nextIdx - 1)?.teaser
            val title = next?.title ?: plan.title
            val body = buildString {
                append(teaser ?: "Ein Vers reicht für heute.")
                if (isLast && s.planB.isNotBlank()) append("\nDein Plan B: ${s.planB}")
            }
            builder.setContentTitle(title)
                .setContentText(body)
                .setStyle(NotificationCompat.BigTextStyle().bigText(body))
                .addAction(0, "1 Vers lesen", openApp(context, 20) { putExtra(EXTRA_TARGET, "verse") })
                .addAction(0, "Weiterlesen", openApp(context, 21) { putExtra(EXTRA_TARGET, "session") })
                .addAction(0, "Heute aussetzen", PendingIntent.getBroadcast(
                    context, 22, Intent(context, ReminderReceiver::class.java).setAction(ReminderReceiver.ACTION_PAUSE),
                    PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE,
                ))
        }
        NotificationManagerCompat.from(context).notify(NOTIFICATION_ID, builder.build())
    }

    data class ReviewPick(val planId: String, val sectionId: String, val index: Int, val quiz: Quiz)

    /** A due question that works with buttons (choice, true/false, who said it). */
    suspend fun pickReview(c: AppContainer, any: Boolean = false): ReviewPick? {
        val available = c.plans.index().plans.filter { it.available }.map { it.id }.toSet()
        for (r in c.progress.dueReviews(if (any) Long.MAX_VALUE else null)) {
            if (r.planId !in available) continue
            val section = c.plans.plan(r.planId).sections.firstOrNull { it.id == r.sectionId } ?: continue
            val q = section.quiz.getOrNull(r.quizIndex) ?: continue
            if (q.type in setOf("choice", "truefalse", "whosaid")) return ReviewPick(r.planId, r.sectionId, r.quizIndex, q)
        }
        return null
    }
}

/** Alarm fired / „Heute aussetzen“ / boot. */
class ReminderReceiver : BroadcastReceiver() {
    companion object {
        const val ACTION_FIRE = "dev.tobi.manna.REMINDER"
        const val ACTION_PAUSE = "dev.tobi.manna.PAUSE_TODAY"
    }

    override fun onReceive(context: Context, intent: Intent) {
        val c = (context.applicationContext as MannaApp).container
        val pending = goAsync()
        CoroutineScope(Dispatchers.IO).launch {
            try {
                when (intent.action) {
                    ACTION_FIRE -> {
                        val s = c.settings.current()
                        val now = LocalDateTime.now()
                        val today = now.toLocalDate().toString()
                        if (s.remindersOn && s.pausedDate != today && !c.progress.readToday()) {
                            val n = c.settings.nextReminderNumber(today)
                            val following = Reminders.nextTrigger(s, now.plusMinutes(1), false)
                            val isLast = following == null || following.toLocalDate() != now.toLocalDate()
                            Reminders.show(context, c, n, isLast)
                        }
                    }
                    ACTION_PAUSE -> {
                        c.settings.update { it.copy(pausedDate = LocalDate.now().toString()) }
                        Reminders.cancelNotification(context)
                    }
                }
                Reminders.reschedule(context, c)
            } finally {
                pending.finish()
            }
        }
    }
}

class BootReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action != Intent.ACTION_BOOT_COMPLETED && intent.action != Intent.ACTION_MY_PACKAGE_REPLACED) return
        val c = (context.applicationContext as MannaApp).container
        val pending = goAsync()
        CoroutineScope(Dispatchers.IO).launch {
            try { Reminders.reschedule(context, c) } finally { pending.finish() }
        }
    }
}
