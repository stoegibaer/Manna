package dev.tobi.manna.data.backup

import android.content.Context
import android.net.Uri
import androidx.room.withTransaction
import dev.tobi.manna.data.progress.CardUnlock
import dev.tobi.manna.data.progress.FavoriteVerse
import dev.tobi.manna.data.progress.GardenTree
import dev.tobi.manna.data.progress.JournalEntry
import dev.tobi.manna.data.progress.MannaDb
import dev.tobi.manna.data.progress.QuizResult
import dev.tobi.manna.data.progress.ReadingDay
import dev.tobi.manna.data.progress.SectionDone
import dev.tobi.manna.data.settings.Settings
import dev.tobi.manna.data.settings.SettingsRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json
import java.time.LocalDate

/** Contents of a backup file (manna-sicherung-<date>.json). Bump [version] on incompatible changes. */
@Serializable
data class BackupFile(
    val format: String = FORMAT,
    val version: Int = 1,
    val appVersion: String = "",
    val exportedAt: Long = 0,
    val sections: List<SectionDone> = emptyList(),
    val quiz: List<QuizResult> = emptyList(),
    val cards: List<CardUnlock> = emptyList(),
    val days: List<ReadingDay> = emptyList(),
    val favorites: List<FavoriteVerse> = emptyList(),
    val journal: List<JournalEntry> = emptyList(),
    val garden: List<GardenTree> = emptyList(),
    val settings: Settings? = null,
)

private const val FORMAT = "manna-backup"

/** What an import added, for the confirmation message. */
data class ImportResult(val sections: Int, val cards: Int, val favorites: Int, val journal: Int, val settings: Boolean = false) {
    fun message(): String {
        val parts = listOf(
            sections to ("neuer Abschnitt" to "neue Abschnitte"), cards to ("Karte" to "Karten"),
            favorites to ("Vers" to "Verse"), journal to ("Tagebucheintrag" to "Tagebucheinträge"),
        ).filter { it.first > 0 }.map { (n, w) -> "$n ${if (n == 1) w.first else w.second}" }
        val what = if (parts.isEmpty()) "Sicherung eingelesen – es war schon alles auf dem Gerät." else "Sicherung eingelesen: ${parts.joinToString(", ")}."
        return what + if (settings) " Einstellungen übernommen." else ""
    }
}

class BackupException(message: String) : Exception(message)

/**
 * Export and import of all user data. Import **merges**: nothing already on the device is lost;
 * for entries present on both sides the more recent one wins. Settings are taken from the file.
 */
class Backup(private val context: Context, private val db: MannaDb, private val settings: SettingsRepository) {
    private val json = Json { ignoreUnknownKeys = true; encodeDefaults = true; prettyPrint = true }

    fun suggestedFileName() = "manna-sicherung-${LocalDate.now()}.json"

    suspend fun export(uri: Uri) = withContext(Dispatchers.IO) {
        val dao = db.progress()
        val current = settings.current()
        val file = db.withTransaction {
            BackupFile(
                appVersion = appVersion(),
                exportedAt = System.currentTimeMillis(),
                sections = dao.exportSections(),
                quiz = dao.exportQuiz(),
                cards = dao.exportCards(),
                days = dao.exportDays(),
                favorites = dao.exportFavorites(),
                journal = dao.exportJournal(),
                garden = dao.exportGarden(),
                settings = current,
            )
        }
        // "wt" truncates an existing file; some providers only support "w"
        val out = runCatching { context.contentResolver.openOutputStream(uri, "wt") }.getOrNull()
            ?: context.contentResolver.openOutputStream(uri, "w") ?: throw BackupException("Die Datei konnte nicht geschrieben werden.")
        out.bufferedWriter(Charsets.UTF_8).use { it.write(json.encodeToString(BackupFile.serializer(), file)) }
    }

    suspend fun import(uri: Uri): ImportResult = withContext(Dispatchers.IO) {
        val text = runCatching {
            context.contentResolver.openInputStream(uri)?.bufferedReader(Charsets.UTF_8)?.use { it.readText() }
        }.getOrNull() ?: throw BackupException("Die Datei konnte nicht gelesen werden.")
        val file = runCatching { json.decodeFromString(BackupFile.serializer(), text) }.getOrNull()
        if (file == null || file.format != FORMAT) throw BackupException("Diese Datei ist keine Manna-Sicherung.")
        if (file.version > 1) throw BackupException("Diese Sicherung stammt aus einer neueren Version von Manna. Bitte aktualisiere die App zuerst.")
        val result = merge(file)
        file.settings?.let { s -> settings.update { cur -> s.copy(energyDate = cur.energyDate, energy = cur.energy) } }
        result.copy(settings = file.settings != null)
    }

    private suspend fun merge(f: BackupFile): ImportResult {
        val dao = db.progress()
        return db.withTransaction {
            val sections = f.sections.count { dao.insertSection(it) != -1L }
            val cards = f.cards.count { dao.insertCard(it) != -1L }
            // trees already planted on the device stay; positions still free are taken from the file
            f.garden.forEach { dao.insertTree(it) }

            val quiz = dao.exportQuiz().associateBy { Triple(it.planId, it.sectionId, it.quizIndex) }
            f.quiz.forEach { q ->
                val old = quiz[Triple(q.planId, q.sectionId, q.quizIndex)]
                if (old == null || q.answeredAt > old.answeredAt) dao.upsertQuiz(q)
            }

            val days = dao.exportDays().associateBy { it.date }
            f.days.forEach { d ->
                val old = days[d.date]
                dao.upsertDay(
                    if (old == null) d
                    else ReadingDay(
                        d.date, maxOf(old.verses, d.verses), maxOf(old.sections, d.sections),
                        listOf(old.firstMinute, d.firstMinute).filter { it >= 0 }.minOrNull() ?: -1,
                    )
                )
            }

            var favorites = 0
            f.favorites.forEach { v ->
                val old = dao.favorite(v.book, v.chapter, v.verse)
                if (old == null) favorites++
                if (old == null || v.savedAt > old.savedAt) dao.upsertFavorite(v)
            }

            var journal = 0
            f.journal.forEach { j ->
                val old = dao.journal(j.planId, j.sectionId)
                if (old == null) journal++
                if (old == null || j.savedAt > old.savedAt) dao.upsertJournal(j)
            }
            ImportResult(sections, cards, favorites, journal)
        }
    }

    private fun appVersion() = runCatching { context.packageManager.getPackageInfo(context.packageName, 0).versionName }.getOrNull().orEmpty()
}
