package dev.tobi.manna.data.progress

import android.content.Context
import androidx.room.Dao
import androidx.room.Database
import androidx.room.Entity
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Room
import androidx.room.RoomDatabase
import androidx.room.migration.Migration
import androidx.sqlite.db.SupportSQLiteDatabase
import kotlinx.coroutines.flow.Flow
import java.time.LocalDate
import java.time.LocalTime

@Entity(primaryKeys = ["planId", "sectionId"])
data class SectionDone(val planId: String, val sectionId: String, val completedAt: Long)

/**
 * One answered quiz question, also used for spaced repetition (Leitner boxes).
 * [box] 0..4 selects the next interval, [dueAt] is when it may come back as „Erinnerst du dich?“.
 */
@Entity(primaryKeys = ["planId", "sectionId", "quizIndex"])
data class QuizResult(
    val planId: String,
    val sectionId: String,
    val quizIndex: Int,
    val firstTry: Boolean,
    val answeredAt: Long,
    val box: Int = 0,
    val dueAt: Long = 0,
)

@Entity(primaryKeys = ["planId", "cardId"])
data class CardUnlock(val planId: String, val cardId: String, val unlockedAt: Long)

/**
 * Per-day reading log (date = ISO yyyy-MM-dd). Basis for daily minimum and weekly goal.
 * [firstMinute] = minute of the day of the first reading (for the reminder-time suggestion), -1 unknown.
 */
@Entity(primaryKeys = ["date"])
data class ReadingDay(val date: String, val verses: Int, val sections: Int, val firstMinute: Int = -1)

/** A saved verse. [source] = "favorite" (long-press) or "memory" (learned in the memory-verse game). */
@Entity(primaryKeys = ["book", "chapter", "verse"])
data class FavoriteVerse(val book: Int, val chapter: Int, val verse: Int, val savedAt: Long, val source: String = "favorite")

/** One-tap reflection after a section („Was nimmst du mit?“). [tags] comma separated chip ids. */
@Entity(primaryKeys = ["planId", "sectionId"])
data class JournalEntry(val planId: String, val sectionId: String, val sectionTitle: String, val tags: String, val note: String, val savedAt: Long)

@Dao
interface ProgressDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertFavorite(f: FavoriteVerse)

    @Query("DELETE FROM FavoriteVerse WHERE book = :book AND chapter = :chapter AND verse = :verse")
    suspend fun deleteFavorite(book: Int, chapter: Int, verse: Int)

    @Query("SELECT * FROM FavoriteVerse ORDER BY savedAt DESC")
    fun favorites(): Flow<List<FavoriteVerse>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertJournal(j: JournalEntry)

    @Query("SELECT * FROM JournalEntry WHERE planId = :planId AND sectionId = :sectionId")
    suspend fun journal(planId: String, sectionId: String): JournalEntry?

    @Query("SELECT * FROM JournalEntry ORDER BY savedAt DESC")
    fun journalEntries(): Flow<List<JournalEntry>>

    @Query("SELECT * FROM SectionDone WHERE planId = :planId")
    fun sectionsDone(planId: String): Flow<List<SectionDone>>

    @Query("SELECT * FROM SectionDone")
    fun allSectionsDone(): Flow<List<SectionDone>>

    @Query("SELECT * FROM SectionDone ORDER BY completedAt DESC LIMIT 1")
    suspend fun lastSection(): SectionDone?

    @Query("SELECT COUNT(*) FROM SectionDone")
    fun totalSections(): Flow<Int>

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insertSection(s: SectionDone): Long

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertQuiz(r: QuizResult)

    @Query("SELECT * FROM QuizResult WHERE planId = :planId AND sectionId = :sectionId AND quizIndex = :index")
    suspend fun quiz(planId: String, sectionId: String, index: Int): QuizResult?

    @Query("SELECT * FROM QuizResult WHERE dueAt <= :now ORDER BY dueAt LIMIT :limit")
    suspend fun dueReviews(now: Long, limit: Int): List<QuizResult>

    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insertCard(c: CardUnlock): Long

    /** Card ids that were renamed in a plan update: keep the user's unlocks. */
    @Query("UPDATE OR IGNORE CardUnlock SET cardId = :to WHERE planId = :planId AND cardId = :from")
    suspend fun renameCard(planId: String, from: String, to: String)

    @Query("SELECT * FROM CardUnlock ORDER BY unlockedAt")
    fun cards(): Flow<List<CardUnlock>>

    @Query("SELECT * FROM ReadingDay WHERE date = :date")
    suspend fun day(date: String): ReadingDay?

    @Query("SELECT * FROM ReadingDay WHERE date = :date")
    fun dayFlow(date: String): Flow<ReadingDay?>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertDay(d: ReadingDay)

    @Query("SELECT * FROM ReadingDay WHERE date >= :from ORDER BY date")
    fun daysSince(from: String): Flow<List<ReadingDay>>

    @Query("SELECT * FROM ReadingDay WHERE date >= :from ORDER BY date")
    suspend fun daysSinceNow(from: String): List<ReadingDay>

    @Query("SELECT MAX(date) FROM ReadingDay WHERE verses > 0 OR sections > 0")
    fun lastReadDate(): Flow<String?>
}

private val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE QuizResult ADD COLUMN box INTEGER NOT NULL DEFAULT 0")
        // existing answers come back for review from the day after they were answered
        db.execSQL("ALTER TABLE QuizResult ADD COLUMN dueAt INTEGER NOT NULL DEFAULT 0")
        db.execSQL("UPDATE QuizResult SET dueAt = answeredAt + 86400000")
        db.execSQL("ALTER TABLE ReadingDay ADD COLUMN firstMinute INTEGER NOT NULL DEFAULT -1")
    }
}

private val MIGRATION_2_3 = object : Migration(2, 3) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("CREATE TABLE IF NOT EXISTS `FavoriteVerse` (`book` INTEGER NOT NULL, `chapter` INTEGER NOT NULL, `verse` INTEGER NOT NULL, `savedAt` INTEGER NOT NULL, `source` TEXT NOT NULL, PRIMARY KEY(`book`, `chapter`, `verse`))")
        db.execSQL("CREATE TABLE IF NOT EXISTS `JournalEntry` (`planId` TEXT NOT NULL, `sectionId` TEXT NOT NULL, `sectionTitle` TEXT NOT NULL, `tags` TEXT NOT NULL, `note` TEXT NOT NULL, `savedAt` INTEGER NOT NULL, PRIMARY KEY(`planId`, `sectionId`))")
    }
}

@Database(
    entities = [SectionDone::class, QuizResult::class, CardUnlock::class, ReadingDay::class, FavoriteVerse::class, JournalEntry::class],
    version = 3,
)
abstract class MannaDb : RoomDatabase() {
    abstract fun progress(): ProgressDao

    companion object {
        fun create(context: Context) = Room.databaseBuilder(context, MannaDb::class.java, "manna.db")
            .addMigrations(MIGRATION_1_2, MIGRATION_2_3)
            .build()
    }
}

/** Leitner intervals in days per box. */
private val INTERVAL_DAYS = longArrayOf(1, 3, 7, 21, 60)
private const val DAY_MS = 86_400_000L

class ProgressRepository(private val dao: ProgressDao) {
    fun sectionsDone(planId: String) = dao.sectionsDone(planId)
    val totalSections: Flow<Int> = dao.totalSections()
    val allSectionsDone: Flow<List<SectionDone>> = dao.allSectionsDone()
    val cards = dao.cards()
    val lastReadDate: Flow<String?> = dao.lastReadDate()
    fun today(): Flow<ReadingDay?> = dao.dayFlow(LocalDate.now().toString())
    fun daysSince(from: LocalDate) = dao.daysSince(from.toString())
    suspend fun daysSinceNow(from: LocalDate) = dao.daysSinceNow(from.toString())
    suspend fun lastSection() = dao.lastSection()

    /** @return true if the section was newly completed (not a re-read). */
    suspend fun completeSection(planId: String, sectionId: String): Boolean =
        dao.insertSection(SectionDone(planId, sectionId, System.currentTimeMillis())) != -1L

    /** Answer in a reading session: new questions come back for review tomorrow; re-reads keep the review progress. */
    suspend fun recordQuiz(planId: String, sectionId: String, index: Int, firstTry: Boolean) {
        val now = System.currentTimeMillis()
        val old = dao.quiz(planId, sectionId, index)
        dao.upsertQuiz(old?.copy(firstTry = firstTry, answeredAt = now) ?: QuizResult(planId, sectionId, index, firstTry, now, 0, now + DAY_MS))
    }

    /** A review („Erinnerst du dich?“): right on first try moves to the next box, otherwise back to box 0. */
    suspend fun recordReview(planId: String, sectionId: String, index: Int, correct: Boolean) {
        val now = System.currentTimeMillis()
        val old = dao.quiz(planId, sectionId, index) ?: QuizResult(planId, sectionId, index, correct, now)
        val box = if (correct) (old.box + 1).coerceAtMost(INTERVAL_DAYS.lastIndex) else 0
        dao.upsertQuiz(old.copy(box = box, answeredAt = now, dueAt = now + INTERVAL_DAYS[box] * DAY_MS))
    }

    /** Due questions; [until] overrides „now“ (debug: Long.MAX_VALUE = any answered question). */
    suspend fun dueReviews(until: Long? = null, limit: Int = 20) = dao.dueReviews(until ?: System.currentTimeMillis(), limit)

    /** @return ids of cards that were newly unlocked. */
    suspend fun unlockCards(planId: String, cardIds: List<String>): List<String> {
        val now = System.currentTimeMillis()
        return cardIds.filter { dao.insertCard(CardUnlock(planId, it, now)) != -1L }
    }

    /** Small data migrations after content updates. Idempotent. */
    suspend fun migrate() {
        dao.renameCard("habakuk", "jehova", "gottesname")
    }

    suspend fun logReading(verses: Int, sections: Int) {
        val today = LocalDate.now().toString()
        val d = dao.day(today) ?: ReadingDay(today, 0, 0)
        val minute = if (d.firstMinute < 0 && verses + sections > 0) LocalTime.now().let { it.hour * 60 + it.minute } else d.firstMinute
        dao.upsertDay(d.copy(verses = d.verses + verses, sections = d.sections + sections, firstMinute = minute))
    }

    val favorites = dao.favorites()
    suspend fun setFavorite(book: Int, chapter: Int, verse: Int, on: Boolean, source: String = "favorite") =
        if (on) dao.upsertFavorite(FavoriteVerse(book, chapter, verse, System.currentTimeMillis(), source)) else dao.deleteFavorite(book, chapter, verse)

    val journal = dao.journalEntries()
    suspend fun journalFor(planId: String, sectionId: String) = dao.journal(planId, sectionId)
    suspend fun saveJournal(planId: String, sectionId: String, title: String, tags: Set<String>, note: String) =
        dao.upsertJournal(JournalEntry(planId, sectionId, title, tags.joinToString(","), note.trim(), System.currentTimeMillis()))

    suspend fun readToday(): Boolean = dao.day(LocalDate.now().toString())?.let { it.verses > 0 || it.sections > 0 } == true
}
